"""Perfboard model, router and checker for the VU speaker control board (board B).

Board: 97.8 x 59.8 mm, landscape, 38 columns (A..AL) x 23 rows (1..23) at 2.54 mm.
Hole (col, row) is 1-based. Names are column letters + row number, from the top-left
as seen from the component side.

Wire kinds
  bridge   solder bridge between two orthogonally adjacent holes, solder side
  top      insulated jumper on the component side, straight along a row or column
  jump     short insulated jump on the solder side, straight, up to JUMP_MAX holes apart
"""
import heapq
import itertools
import re

COLS, ROWS = 38, 23
PITCH = 2.54
X0, Y0 = 1.91, 1.96            # centre of hole A1 from the board corner, mm
BOARD_W, BOARD_H = 97.8, 59.8
MOUNT = [(11.40, 2.55), (86.40, 2.55), (11.40, 57.25), (86.40, 57.25)]  # 3 mm holes
BRIDGE_MAX = 5                 # holes in one solder-bridged chain
JUMP_MAX = 6                   # holes between ends of a solder-side jump


def colname(c):
    s = ''
    while c:
        c, r = divmod(c - 1, 26)
        s = chr(65 + r) + s
    return s


def hname(h):
    return f'{colname(h[0])}{h[1]}'


def H(s):
    m = re.fullmatch(r'([A-Z]+)(\d+)', s)
    c = 0
    for ch in m.group(1):
        c = c * 26 + ord(ch) - 64
    return (c, int(m.group(2)))


def xy(h):
    return (X0 + PITCH * (h[0] - 1), Y0 + PITCH * (h[1] - 1))


def line(a, b):
    """Holes strictly between a and b along a row or column, or None if not straight."""
    if a[0] == b[0]:
        s = 1 if b[1] > a[1] else -1
        return [(a[0], r) for r in range(a[1] + s, b[1], s)]
    if a[1] == b[1]:
        s = 1 if b[0] > a[0] else -1
        return [(c, a[1]) for c in range(a[0] + s, b[0], s)]
    return None


def mount_keepout():
    """Holes too close to the 3 mm mounting holes (screw head ~ 5.5 mm)."""
    out = set()
    for (mx, my) in MOUNT:
        for c in range(1, COLS + 1):
            for r in range(1, ROWS + 1):
                x, y = xy((c, r))
                if (x - mx) ** 2 + (y - my) ** 2 < 3.0 ** 2:
                    out.add((c, r))
    return out


class Part:
    def __init__(self, ref, kind, value, pins, body=(), esp_area=(), gy_area=(), note='', draw=None):
        self.ref, self.kind, self.value = ref, kind, value
        self.pins = [(n, H(h) if isinstance(h, str) else h, net) for n, h, net in pins]
        self.body = {H(h) if isinstance(h, str) else h for h in body}
        self.esp_area = set(esp_area)
        self.gy_area = set(gy_area)
        self.note = note
        self.draw = draw or {}

    def pin(self, name):
        for n, h, net in self.pins:
            if n == name:
                return h
        raise KeyError(f'{self.ref}.{name}')


class Design:
    def __init__(self):
        self.parts = []
        self.keepout = mount_keepout()

    def add(self, p):
        self.parts.append(p)
        return p

    # ---- derived maps -------------------------------------------------------
    def lead_owner(self):
        own = {}
        for p in self.parts:
            for n, h, net in p.pins:
                key = net if net is not None else f'NC:{p.ref}.{n}'
                if h in own and own[h] != key:
                    raise ValueError(f'hole {hname(h)} used by {own[h]} and {key} ({p.ref}.{n})')
                own[h] = key
        return own

    def pins_by_net(self):
        d = {}
        for p in self.parts:
            for n, h, net in p.pins:
                if net is not None:
                    d.setdefault(net, []).append((p.ref, n, h))
        return d

    def body_cells(self):
        hard, esp, gy = {}, set(), set()
        for p in self.parts:
            for c in p.body:
                hard[c] = p.ref
            esp |= p.esp_area
            gy |= p.gy_area
        return hard, esp, gy

    def check_placement(self):
        errs = []
        cells = {}
        for p in self.parts:
            occ = {h for _, h, _ in p.pins} | p.body
            for c in occ:
                if not (1 <= c[0] <= COLS and 1 <= c[1] <= ROWS):
                    errs.append(f'{p.ref} off board at {c}')
                    continue
                if c in cells and cells[c] != p.ref:
                    # a low part may sit in the ESP/GY shadow, only pins collide
                    errs.append(f'{p.ref} overlaps {cells[c]} at {hname(c)}')
                cells[c] = p.ref
            for _, h, _ in p.pins:
                if h in self.keepout:
                    errs.append(f'{p.ref} pin {hname(h)} within mounting-hole clearance')
        return errs


class Wires:
    """Result of routing: bridges (pairs), tops, jumps, all tagged with a net."""

    def __init__(self):
        self.bridges = []   # (net, a, b)
        self.tops = []      # (net, a, b)
        self.jumps = []     # (net, a, b)

    def edges(self):
        for net, a, b in self.bridges + self.tops + self.jumps:
            yield net, a, b


class Router:
    def __init__(self, design, w_bridge=1.0, w_top=(3.0, 0.25), w_jump=(7.0, 0.6),
                 w_cross=1.5, w_adj=0.3):
        self.d = design
        self.own = dict(design.lead_owner())          # hole -> net (leads and routed holes)
        self.lead = set(self.own)
        self.hard, self.esp, self.gy = design.body_cells()
        self.keep = design.keepout
        self.wires = Wires()
        self.comp = {}            # (net, hole) -> set of holes in its bridge chain
        self.top_cells = {}       # cell -> 'H'/'V'
        self.jump_cells = {}
        self.jump_ends = set()
        self.w_bridge, self.w_top, self.w_jump = w_bridge, w_top, w_jump
        self.w_cross, self.w_adj = w_cross, w_adj
        # sockets of the ESP and GY header: cells wires cannot pass over
        self.block_pass = set(self.lead)

    # ---- hole classification ------------------------------------------------
    def inb(self, h):
        return 1 <= h[0] <= COLS and 1 <= h[1] <= ROWS

    def free_for(self, h, net):
        o = self.own.get(h)
        return o is None or o == net

    def can_bridge_into(self, h, net):
        return self.inb(h) and h not in self.keep and self.free_for(h, net)

    def top_end_ok(self, h, net):
        if not self.inb(h) or h in self.keep or h in self.lead or h in self.gy:
            return False
        if h in self.hard:
            return False
        if self.own.get(h) not in (None, net):
            return False
        return h not in self.top_cells

    def top_pass_ok(self, cells):
        for c in cells:
            if c in self.block_pass:
                return False
            if c in self.hard and c not in self.esp:
                return False
            if c in self.keep:
                return False
        return True

    # ---- search -------------------------------------------------------------
    def neighbors(self, h, net, run):
        c, r = h
        # bridges
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c + dc, r + dr)
            if self.can_bridge_into(n, net):
                nrun = run + len(self.comp.get((net, n), (n,)))
                if nrun > BRIDGE_MAX:
                    continue
                adj = sum(1 for ddc, ddr in ((1, 0), (-1, 0), (0, 1), (0, -1))
                          if self.own.get((n[0] + ddc, n[1] + ddr)) not in (None, net))
                yield n, nrun, self.w_bridge + self.w_adj * adj, ('bridge', h, n)
        # top jumpers: from h straight to a free hole
        if self.top_end_ok(h, net) or h in self.tree_hint:
            if self.top_end_ok(h, net):
                for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    cells = []
                    n = (c + dc, r + dr)
                    steps = 1
                    while self.inb(n) and steps <= 40:
                        if steps >= 2 and self.top_end_ok(n, net) and self.top_pass_ok(cells):
                            ok, cross = self.top_free(h, n, 'H' if dr == 0 else 'V')
                            if ok:
                                cost = self.w_top[0] + self.w_top[1] * steps + self.w_cross * cross
                                yield n, 1, cost, ('top', h, n)
                        cells.append(n)
                        if n in self.block_pass or (n in self.hard and n not in self.esp):
                            break
                        n = (n[0] + dc, n[1] + dr)
                        steps += 1
        # solder-side jumps: any hole of this net or free hole, <= JUMP_MAX apart
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c + dc, r + dr)
            steps = 1
            while self.inb(n) and steps <= JUMP_MAX:
                if steps >= 2 and n not in self.keep and self.free_for(n, net):
                    ok = self.jump_free(h, n, 'H' if dr == 0 else 'V')
                    if ok:
                        yield n, 1, self.w_jump[0] + self.w_jump[1] * steps, ('jump', h, n)
                n = (n[0] + dc, n[1] + dr)
                steps += 1

    def top_free(self, a, b, ori):
        cross = 0
        cells = line(a, b) or []
        for c in [a, b] + cells:
            o = self.top_cells.get(c)
            if o is None:
                continue
            if o == ori or c in (a, b):
                return False, 0
            cross += 1
        return True, cross

    def jump_free(self, a, b, ori):
        for c in (line(a, b) or []):
            if self.jump_cells.get(c) == ori:
                return False
        return True

    tree_hint = frozenset()

    def route_net(self, net, pins, preferred=None):
        """Connect all pin holes of net into one tree. Returns list of failures."""
        holes = [h for _, _, h in pins]
        tree = {holes[0]}
        remaining = set(holes[1:]) - tree
        fails = []
        while remaining:
            path = self.dijkstra(net, tree, remaining)
            if path is None:
                fails.append(sorted(hname(h) for h in remaining))
                break
            end, edges = path
            for kind, a, b in edges:
                self.commit(net, kind, a, b)
                tree |= {a, b}
            remaining -= tree
        return fails

    def dijkstra(self, net, sources, targets):
        pq = []
        best = {}
        prev = {}
        cnt = itertools.count()
        for s in sources:
            r0 = len(self.comp.get((net, s), (s,)))
            best[(s, r0)] = 0.0
            heapq.heappush(pq, (0.0, next(cnt), s, r0))
        self.tree_hint = frozenset(sources)
        while pq:
            d, _, h, run = heapq.heappop(pq)
            if best.get((h, run), 1e18) < d:
                continue
            if h in targets:
                edges = []
                st = (h, run)
                while st in prev:
                    pst, e = prev[st]
                    edges.append(e)
                    st = pst
                return h, edges[::-1]
            for n, nrun, cost, e in self.neighbors(h, net, run):
                nd = d + cost
                key = (n, nrun)
                if nd < best.get(key, 1e18):
                    best[key] = nd
                    prev[key] = ((h, run), e)
                    heapq.heappush(pq, (nd, next(cnt), n, nrun))
        return None

    def commit(self, net, kind, a, b):
        if kind == 'bridge':
            self.wires.bridges.append((net, a, b))
            for h in (a, b):
                self.own.setdefault(h, net)
            ca = self.comp.get((net, a), {a})
            cb = self.comp.get((net, b), {b})
            m = ca | cb
            for h in m:
                self.comp[(net, h)] = m
        elif kind == 'top':
            self.wires.tops.append((net, a, b))
            ori = 'H' if a[1] == b[1] else 'V'
            for c in [a, b] + (line(a, b) or []):
                self.top_cells[c] = ori
            for h in (a, b):
                self.own.setdefault(h, net)
        else:
            self.wires.jumps.append((net, a, b))
            ori = 'H' if a[1] == b[1] else 'V'
            for c in line(a, b) or []:
                self.jump_cells[c] = ori
            self.jump_ends.update((a, b))
            for h in (a, b):
                self.own.setdefault(h, net)


# ---- checker ------------------------------------------------------------------
def check(design, wires):
    """Union-find over holes using the wire list. Returns list of problems."""
    parent = {}

    def f(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def u(a, b):
        ra, rb = f(a), f(b)
        if ra != rb:
            parent[ra] = rb

    for _, a, b in wires.edges():
        u(a, b)
    # parts that tie two holes of the same net are handled by net name below
    problems = []
    comp_nets = {}
    lead = design.lead_owner()
    for h, net in lead.items():
        comp_nets.setdefault(f(h), set()).add(net)
    for root, nets in comp_nets.items():
        real = {n for n in nets}
        if len(real) > 1:
            problems.append(f'SHORT: {sorted(real)}')
    # every net fully connected
    by_net = {}
    for h, net in lead.items():
        by_net.setdefault(net, set()).add(f(h))
    for net, roots in by_net.items():
        if net.startswith('NC:'):
            continue
        if len(roots) > 1:
            problems.append(f'OPEN: {net} in {len(roots)} pieces')
    # route holes must belong to the net they are tagged with
    return problems


def bridge_chains(wires):
    """Sizes of solder-bridged chains per net."""
    adj = {}
    for net, a, b in wires.bridges:
        adj.setdefault((net, a), set()).add((net, b))
        adj.setdefault((net, b), set()).add((net, a))
    seen, out = set(), []
    for k in adj:
        if k in seen:
            continue
        stack, comp = [k], []
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            comp.append(x)
            stack.extend(adj[x])
        out.append((k[0], len(comp), sorted(hname(h) for _, h in comp)))
    return out
