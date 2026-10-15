"""Generate wiring.md, BOM.csv, wiring.json, top/bottom SVG, viewer and PNG previews
from design.py + manual.py. Run from this directory:  python3 emit.py <out_dir>"""
import csv
import json
import os
import sys
from perf import (Router, check, bridge_chains, hname, line, xy, COLS, ROWS, BOARD_W, BOARD_H,
                  MOUNT, colname, PITCH)
from design import build
from manual import apply, ROUTES
from render import render, net_color

OUT = sys.argv[1] if len(sys.argv) > 1 else '..'

d = build()
assert not d.check_placement()
r = Router(d)
errs = apply(r)
assert not errs, errs
probs = check(d, r.wires)
assert not probs, probs
w = r.wires

# ------------------------------------------------------------------ netlist helpers
pins_by_net = d.pins_by_net()
part_by_ref = {p.ref: p for p in d.parts}


def hx(h):
    return hname(h)


def hole_note(h):
    for p in d.parts:
        for n, hh, net in p.pins:
            if hh == h:
                return f'{p.ref}.{n}'
    return 'free hole'


# ------------------------------------------------------------------ wiring.md
CONN = ['CN1', 'CN2', 'CN3', 'CN4', 'CN5', 'CN6', 'CN7']
L = []
L.append('# Control perfboard wiring list\n')
L.append('Single-sided dot perfboard, 97.8 x 59.8 mm (same outline as the power board), landscape, '
         '38 x 23 holes at 2.54 mm (hole count assumed from the outline; check against the real board). '
         'Holes are named column letter + row number, from the top-left as seen from the component side. '
         'Mounting holes 3 mm at 75 x 54.7 mm centres; no holes are used within 3 mm of them.\n')
L.append('Three kinds of wire, nothing else:\n')
L.append('- **Solder bridge**: neighbouring holes joined on the underside (chains of at most 5 holes).')
L.append('- **Top jumper**: insulated wire on the component side, straight along a row or column, '
         'both ends in free holes (never in a component lead hole). Many run under the ESP32 module.')
L.append('- **Under-board jump**: short insulated wire on the solder side, straight, at most 6 holes '
         'between ends, soldered to the pads. May cross pads of other nets.\n')
L.append(f'{len(w.tops)} top jumpers, {len(w.jumps)} under-board jumps, {len(w.bridges)} bridged hole pairs '
         f'in {len(bridge_chains(w))} chains. Checked: no short between nets, every net in one piece.\n')

L.append('## Connectors\n')
L.append('| Ref | Type | Pins (hole) | Goes to |')
L.append('|---|---|---|---|')
goes = {
    'CN1': 'Board A, MP1584 5 V logic output (1) and ground (2)',
    'CN2': 'Board A, XL4015 5 V LED rail (1) and ground (2); no LED current flows through B',
    'CN3': 'Relay module: VCC, GND, IN1, IN2 (four wires)',
    'CN4': 'LED strip data (1, after the 330 ohm) and a signal ground (2)',
    'CN5': 'Amp XH-M548: Bluetooth LED sense (1), L speaker leg (2), R speaker leg (3), ground (4)',
    'CN6': 'Panel buttons 1 to 4 and common ground',
    'CN7': 'Amp key pads: collector and emitter of optocoupler channels 3, 1 and 2 (six wires)',
}
for ref in CONN:
    p = part_by_ref[ref]
    pins = ', '.join(f'{n} {p_h}' for n, p_h in [(n, hx(h)) for n, h, _ in p.pins])
    pn = '; '.join(f'{n}={net}' for n, _, net in p.pins)
    L.append(f'| {ref} | {p.value} | {pins} | {goes[ref]} |')
L.append('')
L.append('Pin to net:\n')
for ref in CONN:
    p = part_by_ref[ref]
    L.append(f'- **{ref}**: ' + ', '.join(f'{n} {hx(h)} = {net}' for n, h, net in p.pins))
L.append('')

L.append('## Top jumpers (component side, insulated)\n')
L.append('| Wire | Net | From | To | Holes |')
L.append('|---|---|---|---|---|')
tw = {}
for i, (net, a, b) in enumerate(w.tops, 1):
    tw[(a, b)] = f'T{i}'
    L.append(f'| T{i} | {net} | {hx(a)} | {hx(b)} | {abs(a[0] - b[0]) + abs(a[1] - b[1])} |')
L.append('')
L.append('## Under-board jumps (solder side, insulated)\n')
L.append('| Wire | Net | From | To | Holes | Ends |')
L.append('|---|---|---|---|---|---|')
for i, (net, a, b) in enumerate(w.jumps, 1):
    L.append(f'| S{i} | {net} | {hx(a)} | {hx(b)} | {abs(a[0] - b[0]) + abs(a[1] - b[1])} | '
             f'{hole_note(a)} / {hole_note(b)} |')
L.append('')
L.append('## Solder bridges (underside)\n')
L.append('| Bridge | Net | Holes |')
L.append('|---|---|---|')
chains = sorted(bridge_chains(w), key=lambda c: (c[0], c[2][0]))
# order the holes of each chain along the path for readability
order = {}
for net, a, b in w.bridges:
    order.setdefault(net, []).append((a, b))


def walk(net, comp):
    comp = set(comp)
    adj = {}
    for a, b in order[net]:
        if hname(a) in comp and hname(b) in comp:
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
    start = [h for h in adj if len(adj[h]) == 1] or list(adj)
    seen, seq = set(), []
    stack = [start[0]]
    while stack:
        h = stack.pop()
        if h in seen:
            continue
        seen.add(h)
        seq.append(h)
        stack.extend(x for x in adj[h] if x not in seen)
    return seq


for i, (net, n, holes) in enumerate(chains, 1):
    seq = walk(net, holes)
    L.append(f'| B{i} | {net} | ' + ' > '.join(
        hx(h) + (f' ({hole_note(h)})' if hole_note(h) != 'free hole' else '') for h in seq) + ' |')
L.append('')

L.append('## Parts\n')
L.append('| Ref | Part | Pins (hole) |')
L.append('|---|---|---|')
for p in d.parts:
    if p.ref in CONN:
        continue
    pins = ', '.join(f'{n} {hx(h)}' for n, h, _ in p.pins)
    L.append(f'| {p.ref} | {p.value} | {pins} |')
L.append('')
L.append('## Nets\n')
for net in sorted(pins_by_net):
    L.append(f'- **{net}**: ' + ', '.join(f'{ref}.{n} ({hx(h)})' for ref, n, h in pins_by_net[net]))
L.append('')
L.append('ESP32 pins left unconnected: D13, D12, D14, D32, D35, EN, D15, D2, D5, RX0, TX0 '
         '(USB serial and strapping pins are not used).\n')
open(os.path.join(OUT, 'wiring.md'), 'w').write('\n'.join(L))

# ------------------------------------------------------------------ BOM.csv
bom = {}
for p in d.parts:
    if p.ref == 'U1':
        key = ('ESP32 DevKit 30-pin', '1', 'U1', 'on 2 x 15 pin female headers (sockets)')
    else:
        key = None
rows = []


def add(part, val, refs, note=''):
    rows.append([part, val, len(refs), ' '.join(refs), note])


add('Resistor 1/4 W', '330R', ['R1'], 'LED data series, near the strip terminal')
add('Resistor 1/4 W', '1k', ['R11', 'R12', 'R13'], 'optocoupler LED series')
add('Resistor 1/4 W', '10k', ['R2', 'R9'], 'mute pull-up to 3V3; BT LED sense series')
add('Resistor 1/4 W', '22k', ['R5', 'R6', 'R7', 'R8'], 'VU tap bias, two per channel')
add('Resistor 1/4 W', '100k', ['R3', 'R4', 'R10'], 'VU tap series; sense pulldown')
add('Capacitor ceramic 50 V', '100nF', ['C2', 'C3', 'C5', 'C6'],
    '2.54 mm lead pitch; C5, C6 see 25 V or more')
add('Capacitor ceramic', '1nF', ['C7', 'C8'], 'VU tap high cut')
add('Capacitor electrolytic 16 V', '100uF', ['C1'], 'ahead of D2 on the 5 V logic input')
add('Diode 1N5819', '1N5819', ['D2'], 'Schottky, band toward VIN')
add('Diode 1N4148', '1N4148', ['D1'], 'BT LED sense')
add('IC SN74AHCT125N', 'DIP-14', ['U2'], 'with DIP-14 socket')
add('Optocoupler PC827', 'DIP-8', ['U4'], 'with DIP-8 socket')
add('Optocoupler PC817', 'DIP-4', ['U5'], 'with DIP-4 socket')
add('ESP32 DevKit 30-pin', '1', ['U1'], '2 x 15 pin 2.54 mm female headers, rows 25.4 mm apart')
add('GY-45 MMA8452Q', '1', ['U3'], '1 x 8 pin 2.54 mm header, GY-45 on top of it')
add('Screw terminal 5.08 mm 2P', '', ['CN1', 'CN2', 'CN4'], 'power in x2, strip data')
add('JST-XH header 4P', '', ['CN3', 'CN5'], 'relay module; amp tap (top entry)')
add('JST-XH header 5P', '', ['CN6'], 'panel buttons (top entry)')
add('Pin header 1x6 2.54 mm', '', ['CN7'], 'amp key outputs; a JST-XH housing would sit on the DIP-8 socket')
add('Insulated hookup wire 28-30 AWG', '', ['T1..T%d' % len(w.tops), 'S1..S%d' % len(w.jumps)],
    f'{len(w.tops)} top jumpers, {len(w.jumps)} under-board jumps; short offcuts')
add('Perfboard 97.8 x 59.8 mm', '38 x 23 holes', ['B'], 'same outline as the power board')
with open(os.path.join(OUT, 'BOM.csv'), 'w', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['Part', 'Value', 'Qty', 'Refs', 'Note'])
    wr.writerows(rows)

# ------------------------------------------------------------------ wiring.json
js = {
    'board': {'w_mm': BOARD_W, 'h_mm': BOARD_H, 'cols': COLS, 'rows': ROWS, 'pitch_mm': PITCH},
    'parts': [{'ref': p.ref, 'value': p.value, 'kind': p.kind,
               'pins': [{'name': n, 'hole': hx(h), 'net': net} for n, h, net in p.pins]} for p in d.parts],
    'top_jumpers': [{'id': f'T{i}', 'net': n, 'from': hx(a), 'to': hx(b)} for i, (n, a, b) in enumerate(w.tops, 1)],
    'underboard_jumps': [{'id': f'S{i}', 'net': n, 'from': hx(a), 'to': hx(b)} for i, (n, a, b) in enumerate(w.jumps, 1)],
    'bridges': [{'net': n, 'a': hx(a), 'b': hx(b)} for n, a, b in w.bridges],
    'nets': {n: [f'{ref}.{pn}' for ref, pn, _ in v] for n, v in sorted(pins_by_net.items())},
}
json.dump(js, open(os.path.join(OUT, 'wiring.json'), 'w'), indent=1)


# ------------------------------------------------------------------ SVG
def sx(h, mirror):
    x, y = xy(h)
    return (BOARD_W - x if mirror else x), y


def svg_side(side):
    m = side == 'bottom'
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -5 {BOARD_W + 10:.1f} {BOARD_H + 10:.1f}" '
             f'class="board" font-family="ui-monospace,monospace">')
    o.append(f'<rect x="0" y="0" width="{BOARD_W}" height="{BOARD_H}" rx="1.2" fill="#c9b37a" '
             f'stroke="#7a6a3a" stroke-width=".3"/>')
    for c in range(1, COLS + 1):
        for rr in range(1, ROWS + 1):
            x, y = sx((c, rr), m)
            o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r=".38" fill="#4d4120"/>')
    for c in range(1, COLS + 1):
        x, y = sx((c, 1), m)
        if c % 2 == 1:
            o.append(f'<text x="{x:.2f}" y="-1.2" font-size="1.3" text-anchor="middle">{colname(c)}</text>')
    for rr in range(1, ROWS + 1):
        x, y = sx((1, rr), m)
        xx = -2.2 if not m else BOARD_W + 2.2
        o.append(f'<text x="{xx}" y="{y + .45:.2f}" font-size="1.3" text-anchor="middle">{rr}</text>')
    for (mx, my) in MOUNT:
        x = BOARD_W - mx if m else mx
        o.append(f'<circle cx="{x:.2f}" cy="{my:.2f}" r="1.5" fill="#fff" stroke="#222" stroke-width=".3"/>')
    if side == 'top':
        for p in d.parts:
            if p.kind == 'esp32':
                x0 = xy((p.draw['x0'], 1))[0]; x1 = xy((p.draw['x1'], 1))[0]
                y0 = xy((1, p.draw['y0']))[1]; y1 = xy((1, p.draw['y1']))[1]
                o.append(f'<rect x="{x0 - 1.2:.2f}" y="{y0:.2f}" width="{x1 - x0 + 2.4:.2f}" height="{y1 - y0:.2f}" '
                         f'rx="1" fill="none" stroke="#1b6b5a" stroke-width=".35" stroke-dasharray="1.2 .8"/>')
                o.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{(y0 + y1) / 2:.1f}" font-size="1.9" '
                         f'text-anchor="middle" fill="#1b6b5a">ESP32 DevKit 30-pin, USB left (parts and wires pass under)</text>')
            if p.kind == 'gy45':
                x0 = xy((p.draw['x0'], 1))[0]; x1 = xy((p.draw['x1'], 1))[0]
                y0 = xy((1, p.draw['y0']))[1]; y1 = xy((1, p.draw['y1']))[1]
                o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" rx=".8" '
                         f'fill="none" stroke="#1d4ed8" stroke-width=".35" stroke-dasharray="1.2 .8"/>')
                o.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{y1 - 1.5:.1f}" font-size="1.7" text-anchor="middle" '
                         f'fill="#1d4ed8">GY-45 plugged on its header</text>')
        pal = {'res': '#e8cf9a', 'res_v': '#e8cf9a', 'cap': '#f0a43a', 'cap_v': '#f0a43a', 'elec': '#2b3a67',
               'diode': '#2b2b2b', 'diode_v': '#2b2b2b', 'dip': '#3a3a3a', 'jst': '#ecebd6', 'screw': '#3c8c5a',
               'header': '#222'}
        for p in d.parts:
            if p.kind in ('esp32', 'gy45'):
                for n, h, net in p.pins:
                    x, y = sx(h, False)
                    o.append(f'<rect x="{x - 1:.2f}" y="{y - 1:.2f}" width="2" height="2" fill="#222" '
                             f'data-net="{net or ""}"/>')
                continue
            col = pal.get(p.kind, '#bbb')
            pts = [sx(h, False) for _, h, _ in p.pins]
            if p.kind in ('jst', 'screw', 'dip', 'header'):
                cs = list(p.body | {h for _, h, _ in p.pins})
                xs = [sx(h, False)[0] for h in cs]; ys = [sx(h, False)[1] for h in cs]
                m_ = 1.2 if p.kind != 'header' else .9
                o.append(f'<rect x="{min(xs) - m_:.2f}" y="{min(ys) - m_:.2f}" width="{max(xs) - min(xs) + 2 * m_:.2f}" '
                         f'height="{max(ys) - min(ys) + 2 * m_:.2f}" rx=".6" fill="{col}" fill-opacity=".85" '
                         f'stroke="#222" stroke-width=".3"/>')
                if p.kind == 'dip':
                    x, y = pts[0]
                    o.append(f'<circle cx="{x + 0.0:.2f}" cy="{y + 1.6:.2f}" r=".7" fill="#fff"/>')
            elif len(pts) == 2:
                (x1_, y1_), (x2_, y2_) = pts
                o.append(f'<line x1="{x1_:.2f}" y1="{y1_:.2f}" x2="{x2_:.2f}" y2="{y2_:.2f}" stroke="{col}" '
                         f'stroke-width="2.3" stroke-linecap="round"/>')
                if p.kind in ('diode', 'diode_v'):
                    kx, ky = sx(p.pin('K'), False)
                    o.append(f'<circle cx="{kx:.2f}" cy="{ky:.2f}" r=".95" fill="#ddd"/>')
            for n, h, net in p.pins:
                x, y = sx(h, False)
                o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1" fill="#e8e2c8" stroke="#222" stroke-width=".2" '
                         f'data-net="{net or ""}"/>')
            xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
            o.append(f'<text x="{min(xs):.2f}" y="{min(ys) - 1.4:.2f}" font-size="1.7" font-weight="600">{p.ref}</text>')
            o.append(f'<text x="{min(xs):.2f}" y="{max(ys) + 3.0:.2f}" font-size="1.3" fill="#333">{p.value.split(",")[0][:22]}</text>')
        for i, (net, a, b) in enumerate(w.tops, 1):
            (x1_, y1_), (x2_, y2_) = sx(a, False), sx(b, False)
            c = '#%02x%02x%02x' % net_color(net)
            o.append(f'<g data-net="{net}"><line x1="{x1_:.2f}" y1="{y1_:.2f}" x2="{x2_:.2f}" y2="{y2_:.2f}" '
                     f'stroke="{c}" stroke-width=".7" stroke-linecap="round"/>'
                     f'<circle cx="{x1_:.2f}" cy="{y1_:.2f}" r="1.1" fill="none" stroke="{c}" stroke-width=".35"/>'
                     f'<circle cx="{x2_:.2f}" cy="{y2_:.2f}" r="1.1" fill="none" stroke="{c}" stroke-width=".35"/>'
                     f'<text x="{(x1_ + x2_) / 2:.2f}" y="{(y1_ + y2_) / 2 - .8:.2f}" font-size="1.3" fill="#111" '
                     f'paint-order="stroke" stroke="#c9b37a" stroke-width=".4">T{i}</text></g>')
    else:
        for net, a, b in w.bridges:
            (x1_, y1_), (x2_, y2_) = sx(a, True), sx(b, True)
            c = '#%02x%02x%02x' % net_color(net)
            o.append(f'<line data-net="{net}" x1="{x1_:.2f}" y1="{y1_:.2f}" x2="{x2_:.2f}" y2="{y2_:.2f}" '
                     f'stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>')
        for i, (net, a, b) in enumerate(w.jumps, 1):
            (x1_, y1_), (x2_, y2_) = sx(a, True), sx(b, True)
            c = '#%02x%02x%02x' % net_color(net)
            o.append(f'<g data-net="{net}"><line x1="{x1_:.2f}" y1="{y1_:.2f}" x2="{x2_:.2f}" y2="{y2_:.2f}" '
                     f'stroke="{c}" stroke-width=".6" stroke-dasharray="1.2 .6" stroke-linecap="round"/>'
                     f'<circle cx="{x1_:.2f}" cy="{y1_:.2f}" r="1.1" fill="none" stroke="{c}" stroke-width=".35"/>'
                     f'<circle cx="{x2_:.2f}" cy="{y2_:.2f}" r="1.1" fill="none" stroke="{c}" stroke-width=".35"/>'
                     f'<text x="{(x1_ + x2_) / 2:.2f}" y="{(y1_ + y2_) / 2 - .8:.2f}" font-size="1.3" fill="#111" '
                     f'paint-order="stroke" stroke="#c9b37a" stroke-width=".4">S{i}</text></g>')
        for p in d.parts:
            for n, h, net in p.pins:
                x, y = sx(h, True)
                o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r=".95" fill="{"#e8e2c8" if net else "#a89a68"}" '
                         f'stroke="#222" stroke-width=".2" data-net="{net or ""}"/>')
            xs = [sx(h, True)[0] for _, h, _ in p.pins]; ys = [sx(h, True)[1] for _, h, _ in p.pins]
            o.append(f'<text x="{min(xs):.2f}" y="{min(ys) - 1.4:.2f}" font-size="1.5">{p.ref}</text>')
    o.append('</svg>')
    return '\n'.join(o)


top_svg, bot_svg = svg_side('top'), svg_side('bottom')
open(os.path.join(OUT, 'top.svg'), 'w').write(top_svg)
open(os.path.join(OUT, 'bottom.svg'), 'w').write(bot_svg)
render(d, w, 'top', os.path.join(OUT, 'top.png'))
render(d, w, 'bottom', os.path.join(OUT, 'bottom.png'))

nets_js = json.dumps([{'net': n, 'color': '#%02x%02x%02x' % net_color(n), 'pins': [f'{a}.{b}' for a, b, _ in v]}
                      for n, v in sorted(pins_by_net.items())])
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Control perfboard</title>
<style>
:root{{--bg:#fff;--fg:#1d1d1d;--mut:#666;--line:#d8d8d8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16181c;--fg:#e8e8e8;--mut:#9aa;--line:#333}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 ui-sans-serif,system-ui,sans-serif}}
main{{display:grid;grid-template-columns:230px 1fr;gap:16px;padding:16px}}
@media(max-width:900px){{main{{grid-template-columns:1fr}}}}
h1{{font-size:16px;margin:0 0 6px}} h3{{font-size:12px;margin:12px 0 4px;color:var(--mut)}}
.net{{display:flex;gap:6px;align-items:center;font:12px ui-monospace,monospace;cursor:pointer;padding:1px 0}}
.sw{{width:16px;height:4px;border-radius:2px;flex:none}}
.views{{display:grid;gap:16px}} .views.both{{grid-template-columns:1fr 1fr}}
@media(max-width:1300px){{.views.both{{grid-template-columns:1fr}}}}
svg{{width:100%;height:auto;border:1px solid var(--line);border-radius:8px}}
[data-net].dim{{opacity:.12}} .btn{{padding:4px 10px;border:1px solid var(--line);background:none;color:var(--fg);
border-radius:6px;cursor:pointer}} .btn[aria-pressed=true]{{background:var(--fg);color:var(--bg)}}
</style></head><body><main>
<aside><h1>Control perfboard</h1>
<div>97.8 x 59.8 mm, 38 x 23 holes, landscape.<br>{len(w.tops)} top jumpers, {len(w.jumps)} under-board jumps.</div>
<h3>VIEW</h3><div><button class="btn" data-v="top" aria-pressed="true">Component side</button>
<button class="btn" data-v="bottom" aria-pressed="false">Solder side</button>
<button class="btn" data-v="both" aria-pressed="false">Both</button></div>
<h3>NETS (click: show only this net; hover: highlight)</h3><div id="nets"></div>
<p><button class="btn" id="all">Show all</button></p></aside>
<section class="views" id="views"><div id="vtop">{top_svg}</div><div id="vbot" hidden>{bot_svg}</div></section>
</main><script>
const NETS={nets_js};
const nw=document.getElementById('nets');
function setOnly(n){{document.querySelectorAll('svg [data-net]').forEach(e=>{{
 const v=e.getAttribute('data-net');e.classList.toggle('dim',n!==null&&v!==n&&v!=='')}})}}
NETS.forEach(n=>{{const d=document.createElement('div');d.className='net';
 d.innerHTML=`<span class="sw" style="background:${{n.color}}"></span>${{n.net}}`;
 d.title=n.pins.join(', ');d.onmouseenter=()=>setOnly(n.net);d.onmouseleave=()=>setOnly(null);
 d.onclick=()=>{{window.sticky=window.sticky===n.net?null:n.net;setOnly(window.sticky)}};nw.append(d)}});
document.getElementById('all').onclick=()=>{{window.sticky=null;setOnly(null)}};
document.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>{{
 document.querySelectorAll('[data-v]').forEach(x=>x.setAttribute('aria-pressed',x===b));
 const v=b.dataset.v;document.getElementById('vtop').hidden=v==='bottom';
 document.getElementById('vbot').hidden=v==='top';
 document.getElementById('views').classList.toggle('both',v==='both')}});
</script></body></html>'''
open(os.path.join(OUT, 'perfboard-viewer.html'), 'w').write(html)
print('ok', len(w.tops), len(w.jumps), len(w.bridges))
