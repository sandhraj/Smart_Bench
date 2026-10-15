"""Hand-planned routes for the control board.

Each entry is (net, op) with op one of
  'B h1 h2 ...'  solder-bridged chain of orthogonally adjacent holes (solder side)
  'T a b'        insulated jumper on the component side, straight
  'J a b'        short insulated jump on the solder side, straight, <= 6 holes apart
"""
from perf import H, hname, line, BRIDGE_MAX, JUMP_MAX

ROUTES = [
    # ---- logic power in, VIN diode, caps (top-left) ------------------------------
    ('5V_LOGIC', 'J B3 G3'),
    ('5V_LOGIC', 'B G2 G3 G4 G5 H5'),
    ('VIN', 'B L5 L6'),
    ('GND', 'B B5 B4'),
    ('GND', 'J B4 H4'),
    ('GND', 'J H2 H4'),
    ('GND', 'B H4 I4'),
    ('GND', 'T I4 M4'),
    ('GND', 'B M4 M5 M6'),
    # panel button leads (CN6)
    ('GND', 'B P2 P3 P4'),
    ('GND', 'J P4 M4'),
    ('BTN1', 'J Q2 Q6'), ('BTN2', 'J R2 R6'), ('BTN3', 'J S2 S6'), ('BTN4', 'J T2 T6'),
    # ---- BT LED sense stack above D34 ---------------------------------------------
    ('SENSE_RAW', 'B AC2 AB2'), ('SENSE_RAW', 'T AB2 X2'), ('SENSE_RAW', 'B X2 W2'),
    ('SENSE_D', 'B W3 W4'),
    ('SENSE', 'B W5 W6'), ('SENSE', 'B V5 W5'),
    ('GND', 'J V4 P4'),
    # ---- VU taps (under the module) -----------------------------------------------
    ('VU_L', 'B Y6 Y7 Z7 AA7 AB7'),
    ('VU_R', 'B X6 X7 W7 V7 U7'),
    ('VU_L_C', 'B Y8 Y9'),
    ('VU_R_C', 'J X8 X11'),
    ('L_SPK', 'B AD2 AD3 AD4'), ('L_SPK', 'T AD4 AD10'), ('L_SPK', 'B AD10 AC10'),
    ('L_SPK', 'T AC10 Z10'), ('L_SPK', 'B Z10 Y10'),
    ('R_SPK', 'B AE2 AE3 AE4'), ('R_SPK', 'T AE4 AE12'), ('R_SPK', 'B AE12 AD12'),
    ('R_SPK', 'T AD12 Y12'), ('R_SPK', 'B Y12 X12'),
    # GND for the taps and CN5 ground
    ('GND', 'B M16 M15'), ('GND', 'T M15 M10'), ('GND', 'B M10 N10'), ('GND', 'T N10 V10'),
    ('GND', 'B V10 V9 V8'), ('GND', 'B U8 V8'), ('GND', 'J V9 AA9'), ('GND', 'B AA9 AA8'),
    ('GND', 'B AA8 AB8'),
    ('GND', 'B AF2 AF3 AF4'), ('GND', 'T AF4 AF7'), ('GND', 'B AF7 AF8'), ('GND', 'J AF8 AB8'),
    # ---- 3V3 -------------------------------------------------------------------
    ('3V3', 'B L16 L15 L14'), ('3V3', 'T L14 O14'), ('3V3', 'B O14 P14'), ('3V3', 'B P14 Q14'),
    ('3V3', 'T Q14 W14'), ('3V3', 'B W14 W13'), ('3V3', 'T W13 W9'), ('3V3', 'B W9 W8'),
    ('3V3', 'J W8 Z8'),
    ('3V3', 'B W14 X14'), ('3V3', 'T X14 AF14'), ('3V3', 'B AF14 AF15 AF16 AF17'),
    # ---- mute, LED data -----------------------------------------------------------
    ('MUTE', 'B P15 P16 P17 P18'), ('MUTE', 'T P18 L18'), ('MUTE', 'B L18 L19'),
    ('MUTE', 'J L19 L21'), ('MUTE', 'B L21 M21 M22'),
    ('LED_IN', 'B Q16 Q17'), ('LED_IN', 'T Q17 I17'), ('LED_IN', 'B I17 I18 I19'),
    ('LED_BUF', 'B J19 J18'), ('LED_BUF', 'T J18 J9'), ('LED_BUF', 'B J9 J8 I8 H8'),
    ('LED_OUT', 'B E8 D8 C8 B8'),
    # ---- relay and 5 V LED, left side --------------------------------------------
    ('IN1', 'B M19 M20'), ('IN1', 'J M20 H20'), ('IN1', 'B H20 G20'), ('IN1', 'T G20 D20'),
    ('IN1', 'B D20 C20 B20'),
    ('IN2', 'B N22 N21'), ('IN2', 'J N21 I21'), ('IN2', 'B I21 H21 G21'), ('IN2', 'T G21 D21'),
    ('IN2', 'B D21 C21 B21'),
    ('5V_LED', 'J B13 B18'),
    ('5V_LED', 'B B18 C18 D18 E18 F18'), ('5V_LED', 'T F18 F22'),
    ('5V_LED', 'B F22 G22 H22 I22 I23'),
    # ---- GND, bottom cluster -------------------------------------------------------
    ('GND', 'B B5 C5'), ('GND', 'J C5 C10'), ('GND', 'B C10 B10'),
    ('GND', 'J C10 C15'), ('GND', 'B C15 B15'), ('GND', 'J C15 C19'), ('GND', 'B C19 B19'),
    ('GND', 'J B19 H19'), ('GND', 'J H19 K19'), ('GND', 'J K19 N19'),
    ('GND', 'J M16 M18'), ('GND', 'B M18 N18 N19'),
    ('GND', 'B K19 K20 K21 J21 J22'),
    ('GND', 'J J23 L23'), ('GND', 'B L23 L22'), ('GND', 'J J22 L22'),
    ('GND', 'J N19 R19'), ('GND', 'J R19 T19'), ('GND', 'J T19 W19'),
    ('GND', 'B W19 X19 X18'), ('GND', 'J X18 AD18'), ('GND', 'B AD18 AD17'),
    # ---- keys -------------------------------------------------------------------
    ('KEY3', 'B R16 R17'), ('KEY3_A', 'B R18 Q18 Q19'),
    ('KEY1', 'B T16 T17'), ('KEY1_A', 'B T18 S18 S19'),
    ('KEY2', 'B U16 U17'), ('KEY2_A', 'B U18 V18 V19'),
    ('KEY3_C', 'B Q22 Q23'), ('KEY3_E', 'B R22 R23'),
    ('KEY1_C', 'B S22 S23'), ('KEY1_E', 'B T22 T23'),
    ('KEY2_C', 'B V22 U22 U23'), ('KEY2_E', 'B W22 W23 V23'),
    # ---- GY-45 ---------------------------------------------------------------------
    ('SDA', 'B V16 V17'), ('SDA', 'J V17 AB17'),
    ('SCL', 'B Y16 Y15'), ('SCL', 'T Y15 AC15'), ('SCL', 'B AC15 AC16 AC17'),
    ('INT1', 'J Z16 Z18'), ('INT1', 'B Z18 Y18 Y17'),
]


def apply(router, routes=ROUTES):
    """Commit routes into the router with ownership checks. Returns list of errors."""
    errs = []
    for net, op in routes:
        t = op.split()
        kind, hs = t[0], [H(x) for x in t[1:]]
        if kind == 'B':
            for a, b in zip(hs, hs[1:]):
                if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
                    errs.append(f'{net}: {op}: {hname(a)}-{hname(b)} not adjacent')
            for h in hs:
                o = router.own.get(h)
                if h in router.keep:
                    errs.append(f'{net}: {op}: {hname(h)} in mounting-hole clearance')
                if o not in (None, net):
                    errs.append(f'{net}: {op}: {hname(h)} owned by {o}')
            for a, b in zip(hs, hs[1:]):
                router.commit(net, 'bridge', a, b)
        elif kind == 'T':
            a, b = hs
            cells = line(a, b)
            if cells is None:
                errs.append(f'{net}: {op}: not straight')
                continue
            for h in (a, b):
                if h in router.lead:
                    errs.append(f'{net}: {op}: end {hname(h)} is a component lead hole')
                if h in router.hard:
                    errs.append(f'{net}: {op}: end {hname(h)} under {router.hard[h]}')
                if h in router.gy:
                    errs.append(f'{net}: {op}: end {hname(h)} under the GY-45')
                if h in router.keep:
                    errs.append(f'{net}: {op}: end {hname(h)} in mounting-hole clearance')
                if router.own.get(h) not in (None, net):
                    errs.append(f'{net}: {op}: end {hname(h)} owned by {router.own.get(h)}')
                if h in router.top_cells:
                    errs.append(f'{net}: {op}: end {hname(h)} already under another top wire')
            for c in cells:
                if c in router.block_pass:
                    errs.append(f'{net}: {op}: passes over a lead at {hname(c)}')
                if c in router.hard and c not in router.esp:
                    errs.append(f'{net}: {op}: passes over {router.hard[c]} body at {hname(c)}')
                if c in router.keep:
                    errs.append(f'{net}: {op}: passes over mounting hole clearance at {hname(c)}')
                if router.top_cells.get(c) == ('H' if a[1] == b[1] else 'V'):
                    errs.append(f'{net}: {op}: runs along another top wire at {hname(c)}')
            router.commit(net, 'top', a, b)
        elif kind == 'J':
            a, b = hs
            if line(a, b) is None:
                errs.append(f'{net}: {op}: not straight')
                continue
            n = abs(a[0] - b[0]) + abs(a[1] - b[1])
            if n > JUMP_MAX:
                errs.append(f'{net}: {op}: jump {n} holes > {JUMP_MAX}')
            for h in (a, b):
                if router.own.get(h) not in (None, net):
                    errs.append(f'{net}: {op}: end {hname(h)} owned by {router.own.get(h)}')
                if h in router.keep:
                    errs.append(f'{net}: {op}: end {hname(h)} in mounting-hole clearance')
            ori = 'H' if a[1] == b[1] else 'V'
            for c in line(a, b):
                if router.jump_cells.get(c) == ori:
                    errs.append(f'{net}: {op}: runs along another jump at {hname(c)}')
            router.commit(net, 'jump', a, b)
        else:
            errs.append(f'{net}: unknown op {op}')
    return errs
