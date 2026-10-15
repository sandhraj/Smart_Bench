"""PNG preview of the placement and wiring (component side / solder side)."""
import colorsys
import zlib
from PIL import Image, ImageDraw, ImageFont
from perf import xy, line, COLS, ROWS, BOARD_W, BOARD_H, MOUNT, colname

S = 14  # px per mm


def net_color(net):
    if net == 'GND':
        return (30, 30, 30)
    if net in ('3V3',):
        return (230, 120, 0)
    if net in ('5V_LED', '5V_LOGIC', 'VIN'):
        return (210, 30, 30)
    h = (zlib.crc32(net.encode()) % 360) / 360.0
    r, g, b = colorsys.hsv_to_rgb(h, 0.85, 0.75)
    return (int(r * 255), int(g * 255), int(b * 255))


def P(h, mirror=False):
    x, y = xy(h)
    if mirror:
        x = BOARD_W - x
    return (x * S + 20, y * S + 20)


def render(d, wires, side='top', path='out.png'):
    mirror = side == 'bottom'
    W, Hh = int(BOARD_W * S + 40), int(BOARD_H * S + 40)
    im = Image.new('RGB', (W, Hh), (245, 245, 240))
    g = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
        fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
    except Exception:
        f = fb = ImageFont.load_default()
    g.rectangle([20, 20, 20 + BOARD_W * S, 20 + BOARD_H * S], fill=(201, 179, 122), outline=(90, 70, 30), width=2)
    for c in range(1, COLS + 1):
        for r in range(1, ROWS + 1):
            x, y = P((c, r), mirror)
            g.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(80, 65, 30))
    for c in range(1, COLS + 1, 1):
        x, y = P((c, 1), mirror)
        if c % 2 == 1:
            g.text((x - 6, 4), colname(c), fill=(0, 0, 0), font=f)
    for r in range(1, ROWS + 1):
        x, y = P((1, r), mirror)
        g.text((1 if not mirror else W - 18, y - 6), str(r), fill=(0, 0, 0), font=f)
    for (mx, my) in MOUNT:
        x = (BOARD_W - mx if mirror else mx) * S + 20
        y = my * S + 20
        g.ellipse([x - 1.5 * S, y - 1.5 * S, x + 1.5 * S, y + 1.5 * S], fill=(255, 255, 255), outline=(0, 0, 0))

    if side == 'top':
        # module shadows
        for p in d.parts:
            if p.kind == 'esp32':
                dr = p.draw
                a = P((dr['x0'], dr['y0'] + 0.0), False)
                x0 = X(dr['x0']); x1 = X(dr['x1']); y0 = Y(dr['y0']); y1 = Y(dr['y1'])
                g.rectangle([x0 - 0.5 * S, y0, x1 + 0.5 * S, y1], outline=(20, 110, 90), width=2)
                g.text((x0 + 4 * S, y0 + 5.5 * S), 'ESP32 DevKit (USB left) - low parts and wires pass under', fill=(20, 110, 90), font=f)
            if p.kind == 'gy45':
                dr = p.draw
                x0 = X(dr['x0']); x1 = X(dr['x1']); y0 = Y(dr['y0']); y1 = Y(dr['y1'])
                g.rectangle([x0, y0, x1, y1], outline=(30, 80, 200), width=2)
                g.text((x0 + 6, y1 - 16), 'GY-45 (above header)', fill=(30, 80, 200), font=f)
        for p in d.parts:
            body(g, p, f, fb)
        for net, a, b in wires.tops:
            g.line([P(a), P(b)], fill=net_color(net), width=3)
            for h in (a, b):
                x, y = P(h)
                g.ellipse([x - 4, y - 4, x + 4, y + 4], outline=net_color(net), width=2)
    else:
        for net, a, b in wires.bridges:
            g.line([P(a, True), P(b, True)], fill=net_color(net), width=7)
        for net, a, b in wires.jumps:
            g.line([P(a, True), P(b, True)], fill=net_color(net), width=2)
            for h in (a, b):
                x, y = P(h, True)
                g.ellipse([x - 4, y - 4, x + 4, y + 4], outline=net_color(net), width=2)
        for p in d.parts:
            for n, h, net in p.pins:
                x, y = P(h, True)
                g.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(232, 226, 200) if net else (160, 150, 110),
                          outline=(0, 0, 0))
            xs = [P(h, True) for _, h, _ in p.pins]
            g.text((min(x for x, _ in xs), min(y for _, y in xs) - 14), p.ref, fill=(0, 0, 0), font=f)
    im.save(path)


def X(c):
    return xy((c, 1))[0] * S + 20


def Y(r):
    return xy((1, r))[1] * S + 20


COLORS = {'res': (232, 207, 154), 'res_v': (232, 207, 154), 'cap': (240, 164, 58), 'cap_v': (240, 164, 58),
          'elec': (43, 58, 103), 'diode': (60, 60, 60), 'diode_v': (60, 60, 60), 'dip': (50, 50, 50),
          'jst': (235, 235, 215), 'screw': (60, 140, 90), 'header': (30, 30, 30)}


def body(g, p, f, fb):
    if p.kind in ('esp32', 'gy45'):
        for n, h, net in p.pins:
            x, y = P(h)
            g.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(25, 25, 25))
            if net:
                g.ellipse([x - 3, y - 3, x + 3, y + 3], fill=net_color(net))
        return
    col = COLORS.get(p.kind, (180, 180, 180))
    pts = [P(h) for _, h, _ in p.pins]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    if p.kind in ('jst', 'screw', 'dip'):
        bc = list(p.body | {h for _, h, _ in p.pins})
        bx = [P(h)[0] for h in bc]
        by = [P(h)[1] for h in bc]
        m = 0.9 * S
        g.rectangle([min(bx) - m, min(by) - m, max(bx) + m, max(by) + m], fill=col, outline=(0, 0, 0), width=2)
    else:
        pad = 7
        if len(pts) == 2 and (abs(pts[0][0] - pts[1][0]) > 1 or abs(pts[0][1] - pts[1][1]) > 1):
            g.line([pts[0], pts[1]], fill=col if p.kind not in ('diode', 'diode_v') else (60, 60, 60), width=11)
            if p.kind in ('diode', 'diode_v'):
                # cathode band at K
                k = [h for n, h, _ in p.pins if n == 'K'][0]
                kx, ky = P(k)
                g.ellipse([kx - 5, ky - 5, kx + 5, ky + 5], fill=(220, 220, 220))
        for q in pts:
            pass
    for n, h, net in p.pins:
        x, y = P(h)
        g.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(232, 226, 200) if net else (170, 160, 120), outline=(0, 0, 0))
        if net:
            g.ellipse([x - 2, y - 2, x + 2, y + 2], fill=net_color(net))
    cx, cy = min(xs), min(ys)
    g.text((cx - 6, cy - 16), p.ref, fill=(0, 0, 0), font=fb)
