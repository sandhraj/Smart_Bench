"""Route the control board and print a summary + ASCII map."""
import sys
from perf import Router, check, bridge_chains, hname, colname, COLS, ROWS, line
from design import build

ORDER_LAST = ['GND']


def route_all(d, order=None):
    r = Router(d)
    nets = d.pins_by_net()

    def span(n):
        hs = [h for _, _, h in nets[n]]
        return (max(h[0] for h in hs) - min(h[0] for h in hs)) + (max(h[1] for h in hs) - min(h[1] for h in hs))

    if order is None:
        order = sorted([n for n in nets if n not in ORDER_LAST], key=span) + ORDER_LAST
    fails = {}
    for n in order:
        if len(nets[n]) < 2:
            continue
        f = r.route_net(n, nets[n])
        if f:
            fails[n] = f
    return r, fails


def ascii_map(d, r):
    grid = {}
    for p in d.parts:
        for n, h, net in p.pins:
            grid[h] = p.ref[0].lower() if net else 'x'
    for net, a, b in r.wires.bridges:
        for h in (a, b):
            grid.setdefault(h, '=')
    for net, a, b in r.wires.tops:
        for c in [a, b] + (line(a, b) or []):
            grid.setdefault(c, '-' if a[1] == b[1] else '|')
        grid[a] = grid[b] = 'T'
    for net, a, b in r.wires.jumps:
        grid[a] = grid[b] = 'J'
    out = ['    ' + ''.join(colname(c)[-1] for c in range(1, COLS + 1))]
    for rr in range(1, ROWS + 1):
        out.append(f'{rr:3d} ' + ''.join(grid.get((c, rr), '.') for c in range(1, COLS + 1)))
    return '\n'.join(out)


def cost(r, fails):
    w = r.wires
    return 1000 * len(fails) + len(w.bridges) + 4 * len(w.tops) + 9 * len(w.jumps)


def search(d, tries=24, seed=1):
    import random
    nets = d.pins_by_net()
    names = [n for n in nets if n not in ORDER_LAST and len(nets[n]) > 1]
    rng = random.Random(seed)
    best = None
    for t in range(tries):
        order = list(names)
        if t:
            rng.shuffle(order)
        else:
            order.sort(key=lambda n: len(nets[n]))
        order += ORDER_LAST
        r, fails = route_all(d, order)
        c = cost(r, fails)
        print('try', t, 'cost', c, 'fails', list(fails), flush=True)
        if best is None or c < best[0]:
            best = (c, r, fails, order)
    return best


if __name__ == '__main__':
    d = build()
    tries = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if tries > 1:
        _, r, fails, order = search(d, tries)
        print('ORDER', order)
    else:
        r, fails = route_all(d)
    print('route failures:', fails)
    probs = check(d, r.wires)
    print('check problems:', probs)
    w = r.wires
    print(f'bridges {len(w.bridges)}  top jumpers {len(w.tops)}  solder-side jumps {len(w.jumps)}')
    long_chains = [c for c in bridge_chains(w) if c[1] > 5]
    print('chains >5:', long_chains)
    for net, a, b in w.tops:
        print('TOP ', net, hname(a), hname(b), abs(a[0] - b[0]) + abs(a[1] - b[1]))
    for net, a, b in w.jumps:
        print('JUMP', net, hname(a), hname(b))
    print(ascii_map(d, r))
