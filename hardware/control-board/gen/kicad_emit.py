"""Write a KiCad 9 perfboard footprint (97.8 x 59.8 mm, 38 x 23 holes) and a board file with the
placement, solder bridges (B.Cu tracks) and jumpers (User.1 top, User.2 under-board)."""
import os
import sys
import uuid
from perf import Router, xy, COLS, ROWS, BOARD_W, BOARD_H, MOUNT, colname, hname, line
from design import build
from manual import apply

OUT = sys.argv[1] if len(sys.argv) > 1 else '../kicad'
os.makedirs(os.path.join(OUT, 'Perfboard.pretty'), exist_ok=True)
OX, OY = 30.0, 30.0
FPNAME = 'Perfboard_97.8x59.8_38x23_P2.54mm'

d = build()
r = Router(d)
assert not apply(r)
w = r.wires
lead = d.lead_owner()
nets = sorted({n for n in lead.values() if not n.startswith('NC:')})
nid = {n: i for i, n in enumerate(nets, 1)}


def u():
    return str(uuid.uuid4())


def f(x):
    return f'{x:.3f}'


def near_mount(x, y):
    return any((x - mx) ** 2 + (y - my) ** 2 < 2.6 ** 2 for mx, my in MOUNT)


def pad_lines(with_nets):
    out = []
    for c in range(1, COLS + 1):
        for rr in range(1, ROWS + 1):
            x, y = xy((c, rr))
            if near_mount(x, y):
                continue          # hole sits under the mounting-hole clearance, not usable
            name = f'{colname(c)}{rr}'
            net = ''
            if with_nets:
                n = r.own.get((c, rr))
                if n and not n.startswith('NC:'):
                    net = f' (net {nid[n]} "{n}")'
            out.append(f'    (pad "{name}" thru_hole circle (at {f(x)} {f(y)}) (size 1.7 1.7) (drill 1.0) '
                       f'(layers "*.Cu"){net} (uuid "{u()}"))')
    for i, (mx, my) in enumerate(MOUNT, 1):
        out.append(f'    (pad "MH{i}" np_thru_hole circle (at {f(mx)} {f(my)}) (size 3.0 3.0) (drill 3.0) '
                   f'(layers "*.Cu") (uuid "{u()}"))')
    return out


def outline(layer, ox=0.0, oy=0.0):
    pts = [(0, 0), (BOARD_W, 0), (BOARD_W, BOARD_H), (0, BOARD_H)]
    out = []
    for (a, b), (c, dd) in zip(pts, pts[1:] + pts[:1]):
        out.append(f'(fp_line (start {f(a + ox)} {f(b + oy)}) (end {f(c + ox)} {f(dd + oy)}) '
                   f'(stroke (width 0.1) (type solid)) (layer "{layer}") (uuid "{u()}"))')
    return out


# ---- footprint library entry (no nets) -------------------------------------------------
fp = [f'(footprint "{FPNAME}" (version 20241229) (generator "control-board-gen") (layer "F.Cu")',
      '  (descr "Single-sided dot perfboard 97.8 x 59.8 mm, 38 x 23 holes at 2.54 mm, 3 mm mounting holes at '
      '75 x 54.7 mm centres. Pad names are column letters + row number from the top-left.")',
      '  (tags "perfboard protoboard 2.54mm")',
      '  (attr through_hole exclude_from_pos_files exclude_from_bom)',
      f'  (property "Reference" "PB1" (at 48.9 -3 0) (layer "F.SilkS") (uuid "{u()}") '
      f'(effects (font (size 1.2 1.2) (thickness 0.15))))',
      f'  (property "Value" "{FPNAME}" (at 48.9 63 0) (layer "F.Fab") (uuid "{u()}") '
      f'(effects (font (size 1.2 1.2) (thickness 0.15))))']
fp += ['  ' + s for s in outline('F.SilkS')]
fp += ['  ' + s for s in outline('F.CrtYd')]
fp += pad_lines(False)
fp.append(')')
open(os.path.join(OUT, 'Perfboard.pretty', FPNAME + '.kicad_mod'), 'w').write('\n'.join(fp) + '\n')

# ---- board -----------------------------------------------------------------------------
b = []
b.append('(kicad_pcb (version 20241229) (generator "control-board-gen") (generator_version "9.0")')
b.append('  (general (thickness 1.6) (legacy_teardrops no))')
b.append('  (paper "A4")')
b.append('''  (layers
    (0 "F.Cu" signal) (2 "B.Cu" signal)
    (9 "F.Adhes" user "F.Adhesive") (11 "B.Adhes" user "B.Adhesive")
    (13 "F.Paste" user) (15 "B.Paste" user)
    (5 "F.SilkS" user "F.Silkscreen") (7 "B.SilkS" user "B.Silkscreen")
    (1 "F.Mask" user) (3 "B.Mask" user)
    (17 "Dwgs.User" user "User.Drawings") (19 "Cmts.User" user "User.Comments")
    (21 "Eco1.User" user "User.Eco1") (23 "Eco2.User" user "User.Eco2")
    (25 "Edge.Cuts" user) (27 "Margin" user)
    (31 "F.CrtYd" user "F.Courtyard") (29 "B.CrtYd" user "B.Courtyard")
    (35 "F.Fab" user "F.Fabrication") (33 "B.Fab" user "B.Fabrication")
    (39 "User.1" user "Top jumpers") (41 "User.2" user "Under-board jumps")
    (43 "User.3" user "Parts")
  )''')
b.append('  (setup (pad_to_mask_clearance 0) (pcbplotparams (layerselection 0x00010fc_ffffffff)))')
b.append('  (net 0 "")')
for n in nets:
    b.append(f'  (net {nid[n]} "{n}")')
# edge cuts
pts = [(0, 0), (BOARD_W, 0), (BOARD_W, BOARD_H), (0, BOARD_H)]
for (a, bb), (c, dd) in zip(pts, pts[1:] + pts[:1]):
    b.append(f'  (gr_line (start {f(a + OX)} {f(bb + OY)}) (end {f(c + OX)} {f(dd + OY)}) '
             f'(stroke (width 0.1) (type solid)) (layer "Edge.Cuts") (uuid "{u()}"))')
# perfboard footprint with nets
b.append(f'  (footprint "{FPNAME}" (layer "F.Cu") (uuid "{u()}") (at {OX} {OY})')
b.append(f'    (property "Reference" "PB1" (at 48.9 -3 0) (layer "F.SilkS") (uuid "{u()}") '
         f'(effects (font (size 1.2 1.2) (thickness 0.15))))')
b.append(f'    (property "Value" "{FPNAME}" (at 48.9 63 0) (layer "F.Fab") (uuid "{u()}") '
         f'(effects (font (size 1.2 1.2) (thickness 0.15))))')
b.append('    (attr through_hole exclude_from_pos_files exclude_from_bom)')
b += ['  ' + s for s in pad_lines(True)]
b.append('  )')


def P(h):
    x, y = xy(h)
    return x + OX, y + OY


# solder bridges as B.Cu tracks
for net, a, bb in w.bridges:
    (x1, y1), (x2, y2) = P(a), P(bb)
    b.append(f'  (segment (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) (width 1.0) (layer "B.Cu") '
             f'(net {nid[net]}) (uuid "{u()}"))')
# jumpers as drawings
for i, (net, a, bb) in enumerate(w.tops, 1):
    (x1, y1), (x2, y2) = P(a), P(bb)
    b.append(f'  (gr_line (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) (stroke (width 0.4) (type solid)) '
             f'(layer "User.1") (uuid "{u()}"))')
    b.append(f'  (gr_text "T{i} {net}" (at {f((x1 + x2) / 2)} {f((y1 + y2) / 2 - 0.9)} 0) (layer "User.1") '
             f'(uuid "{u()}") (effects (font (size 0.8 0.8) (thickness 0.12))))')
for i, (net, a, bb) in enumerate(w.jumps, 1):
    (x1, y1), (x2, y2) = P(a), P(bb)
    b.append(f'  (gr_line (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) (stroke (width 0.3) (type dash)) '
             f'(layer "User.2") (uuid "{u()}"))')
    b.append(f'  (gr_text "S{i} {net}" (at {f((x1 + x2) / 2)} {f((y1 + y2) / 2 + 0.9)} 0) (layer "User.2") '
             f'(uuid "{u()}") (effects (font (size 0.8 0.8) (thickness 0.12))))')
# parts: outline around leads / body, with reference
for p in d.parts:
    cs = [h for _, h, _ in p.pins] + list(p.body)
    xs = [P(h)[0] for h in cs]
    ys = [P(h)[1] for h in cs]
    x0, x1, y0, y1 = min(xs) - 1.4, max(xs) + 1.4, min(ys) - 1.4, max(ys) + 1.4
    if p.kind == 'esp32':
        x0, x1 = P((p.draw['x0'], 1))[0] - 1.2, P((p.draw['x1'], 1))[0]
        y0, y1 = P((1, p.draw['y0']))[1], P((1, p.draw['y1']))[1]
    if p.kind == 'gy45':
        x0, x1 = P((p.draw['x0'], 1))[0], P((p.draw['x1'], 1))[0]
        y0, y1 = P((1, p.draw['y0']))[1], P((1, p.draw['y1']))[1]
    b.append(f'  (gr_rect (start {f(x0)} {f(y0)}) (end {f(x1)} {f(y1)}) (stroke (width 0.2) (type solid)) '
             f'(fill no) (layer "User.3") (uuid "{u()}"))')
    b.append(f'  (gr_text "{p.ref}" (at {f((x0 + x1) / 2)} {f(y0 - 0.8)} 0) (layer "User.3") (uuid "{u()}") '
             f'(effects (font (size 1.2 1.2) (thickness 0.18))))')
b.append(')')
path = os.path.join(OUT, 'control-board.kicad_pcb')
open(path, 'w').write('\n'.join(b) + '\n')
print('wrote', path, len(nets), 'nets,', len(w.bridges), 'bridges,', len(w.tops), 'top,', len(w.jumps), 'jumps')
