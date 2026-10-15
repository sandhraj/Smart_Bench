"""Control board (board B) placement and netlist.

Placement follows the marked-up mock (PXL_20261014_203840603~2.jpg) on the landscape
97.8 x 59.8 mm outline, pin assignments follow image.png / docs/SPEC.md:

  top header row (row 6):    caps and diode top-left, panel button leads top-middle,
                             amp inputs top-right, VU taps under the module
  bottom header row (row 16): level shifter bottom-left, optocouplers bottom-centre,
                             GY-45 under the right-hand header pins
"""
from perf import Part, Design, H, colname, COLS, ROWS


def cells(c0, c1, r0, r1):
    return [(c, r) for c in range(c0, c1 + 1) for r in range(r0, r1 + 1)]


def build():
    d = Design()

    # ---------------- ESP32 DevKit 30-pin, USB at the left -------------------------
    top = ['VIN', 'GND', 'D13', 'D12', 'D14', 'D27', 'D26', 'D25', 'D33', 'D32', 'D35', 'D34', 'VN', 'VP', 'EN']
    bot = ['3V3', 'GND', 'D15', 'D2', 'D4', 'D16', 'D17', 'D5', 'D18', 'D19', 'D21', 'RX0', 'TX0', 'D22', 'D23']
    tnet = {'VIN': 'VIN', 'GND': 'GND', 'D27': 'BTN1', 'D26': 'BTN2', 'D25': 'BTN3', 'D33': 'BTN4',
            'D34': 'SENSE', 'VN': 'VU_R', 'VP': 'VU_L'}
    bnet = {'3V3': '3V3', 'GND': 'GND', 'D4': 'MUTE', 'D16': 'LED_IN', 'D17': 'KEY3', 'D18': 'KEY1',
            'D19': 'KEY2', 'D21': 'SDA', 'D22': 'SCL', 'D23': 'INT1'}
    X0 = 12  # column of pin 1 (L)
    pins = []
    for i, n in enumerate(top):
        pins.append((f'T.{n}', (X0 + i, 6), tnet.get(n)))
    for i, n in enumerate(bot):
        pins.append((f'B.{n}', (X0 + i, 16), bnet.get(n)))
    pin_cells = {h for _, h, _ in pins}
    esp_area = [c for c in cells(8, 28, 6, 16) if c not in pin_cells]
    d.add(Part('U1', 'esp32', 'ESP32 DevKit 30-pin on 2x15 sockets', pins, esp_area=esp_area,
               draw={'x0': 8, 'x1': 28, 'y0': 5.4, 'y1': 16.6}))

    # ---------------- top-left: logic power in, diode, caps -------------------------
    d.add(Part('CN1', 'screw', '5.08 mm screw terminal 2P, 5 V logic in',
               [('1', 'B3', '5V_LOGIC'), ('2', 'B5', 'GND')], body=cells(1, 3, 2, 6)))
    d.add(Part('C1', 'elec', '100uF 16V', [('+', 'G2', '5V_LOGIC'), ('-', 'H2', 'GND')]))
    d.add(Part('C2', 'cap', '100nF', [('1', 'G4', '5V_LOGIC'), ('2', 'H4', 'GND')]))
    d.add(Part('D2', 'diode', '1N5819', [('A', 'H5', '5V_LOGIC'), ('K', 'L5', 'VIN')],
               body=['I5', 'J5', 'K5']))

    # ---------------- top-middle: panel button leads --------------------------------
    d.add(Part('CN6', 'jst', 'JST-XH 5P, panel buttons',
               [('GND', 'P2', 'GND'), ('B1', 'Q2', 'BTN1'), ('B2', 'R2', 'BTN2'),
                ('B3', 'S2', 'BTN3'), ('B4', 'T2', 'BTN4')], body=cells(15, 20, 1, 3)))

    # ---------------- top-right: amp inputs ----------------------------------------
    d.add(Part('CN5', 'jst', 'JST-XH 4P, amp: BT LED sense, L, R, GND',
               [('SENSE', 'AC2', 'SENSE_RAW'), ('L', 'AD2', 'L_SPK'), ('R', 'AE2', 'R_SPK'),
                ('GND', 'AF2', 'GND')], body=cells(29, 32, 1, 3)))

    # BT LED sense stack above D34
    d.add(Part('R9', 'res_v', '10k', [('1', 'W2', 'SENSE_RAW'), ('2', 'W3', 'SENSE_D')]))
    d.add(Part('D1', 'diode_v', '1N4148', [('A', 'W4', 'SENSE_D'), ('K', 'W5', 'SENSE')]))
    d.add(Part('R10', 'res_v', '100k', [('1', 'V5', 'SENSE'), ('2', 'V4', 'GND')]))

    # VU tap, L channel (node under VP)
    d.add(Part('R3', 'res_v', '100k', [('2', 'Y7', 'VU_L'), ('1', 'Y8', 'VU_L_C')]))
    d.add(Part('R5', 'res_v', '22k', [('1', 'Z7', 'VU_L'), ('2', 'Z8', '3V3')]))
    d.add(Part('R7', 'res_v', '22k', [('1', 'AA7', 'VU_L'), ('2', 'AA8', 'GND')]))
    d.add(Part('C7', 'cap_v', '1nF', [('1', 'AB7', 'VU_L'), ('2', 'AB8', 'GND')]))
    d.add(Part('C5', 'cap_v', '100nF', [('2', 'Y9', 'VU_L_C'), ('1', 'Y10', 'L_SPK')]))
    # VU tap, R channel (node under VN)
    d.add(Part('R4', 'res_v', '100k', [('2', 'X7', 'VU_R'), ('1', 'X8', 'VU_R_C')]))
    d.add(Part('R6', 'res_v', '22k', [('1', 'W7', 'VU_R'), ('2', 'W8', '3V3')]))
    d.add(Part('R8', 'res_v', '22k', [('1', 'V7', 'VU_R'), ('2', 'V8', 'GND')]))
    d.add(Part('C8', 'cap_v', '1nF', [('1', 'U7', 'VU_R'), ('2', 'U8', 'GND')]))
    d.add(Part('C6', 'cap_v', '100nF', [('2', 'X11', 'VU_R_C'), ('1', 'X12', 'R_SPK')]))

    # ---------------- left edge connectors (top to bottom) ---------------------------
    d.add(Part('CN4', 'screw', '5.08 mm screw terminal 2P, LED strip data',
               [('1', 'B8', 'LED_OUT'), ('2', 'B10', 'GND')], body=cells(1, 3, 7, 11)))
    d.add(Part('CN2', 'screw', '5.08 mm screw terminal 2P, 5 V LED rail in',
               [('1', 'B13', '5V_LED'), ('2', 'B15', 'GND')], body=cells(1, 3, 12, 16)))
    d.add(Part('CN3', 'jst', 'JST-XH 4P, relay module: 5 V, GND, IN1, IN2',
               [('1', 'B18', '5V_LED'), ('2', 'B19', 'GND'), ('3', 'B20', 'IN1'), ('4', 'B21', 'IN2')],
               body=cells(1, 3, 17, 22)))
    d.add(Part('R1', 'res', '330R', [('1', 'H8', 'LED_BUF'), ('2', 'E8', 'LED_OUT')],
               body=['F8', 'G8']))

    # ---------------- bottom-left: level shifter -----------------------------------
    u2 = {1: 'GND', 2: 'LED_IN', 3: 'LED_BUF', 4: 'GND', 5: 'MUTE', 6: 'IN1', 7: 'GND',
          8: 'IN2', 9: 'MUTE', 10: 'GND', 11: None, 12: 'GND', 13: '5V_LED', 14: '5V_LED'}
    p = []
    c0 = 8
    for k in range(1, 8):
        p.append((str(k), (c0 + k - 1, 19), u2[k]))
    for k in range(14, 7, -1):
        p.append((str(k), (c0 + 14 - k, 22), u2[k]))
    d.add(Part('U2', 'dip', 'SN74AHCT125N DIP-14 in socket', p, body=cells(c0, c0 + 6, 20, 21),
               draw={'c0': c0, 'n': 7, 'r0': 19, 'r1': 22}))
    d.add(Part('C3', 'cap_v', '100nF', [('1', 'I23', '5V_LED'), ('2', 'J23', 'GND')]))
    d.add(Part('R2', 'res_v', '10k', [('1', 'P15', 'MUTE'), ('2', 'P14', '3V3')]))

    # ---------------- bottom-centre: optocouplers ----------------------------------
    q = 17
    u4 = [('1', (q, 19), 'KEY3_A'), ('2', (q + 1, 19), 'GND'), ('3', (q + 2, 19), 'KEY1_A'),
          ('4', (q + 3, 19), 'GND'),
          ('5', (q + 3, 22), 'KEY1_E'), ('6', (q + 2, 22), 'KEY1_C'), ('7', (q + 1, 22), 'KEY3_E'),
          ('8', (q, 22), 'KEY3_C')]
    d.add(Part('U4', 'dip', 'PC827 dual optocoupler in DIP-8 socket', u4, body=cells(q, q + 3, 20, 21),
               draw={'c0': q, 'n': 4, 'r0': 19, 'r1': 22}))
    c5 = 22
    u5 = [('1', (c5, 19), 'KEY2_A'), ('2', (c5 + 1, 19), 'GND'),
          ('3', (c5 + 1, 22), 'KEY2_E'), ('4', (c5, 22), 'KEY2_C')]
    d.add(Part('U5', 'dip', 'PC817 optocoupler in DIP-4 socket', u5, body=cells(c5, c5 + 1, 20, 21),
               draw={'c0': c5, 'n': 2, 'r0': 19, 'r1': 22}))
    d.add(Part('R11', 'res_v', '1k', [('1', 'T17', 'KEY1'), ('2', 'T18', 'KEY1_A')]))
    d.add(Part('R12', 'res_v', '1k', [('1', 'U17', 'KEY2'), ('2', 'U18', 'KEY2_A')]))
    d.add(Part('R13', 'res_v', '1k', [('1', 'R17', 'KEY3'), ('2', 'R18', 'KEY3_A')]))
    d.add(Part('CN7', 'header', '1x6 2.54 mm header, key outputs to amp pads',
               [('K3C', 'Q23', 'KEY3_C'), ('K3E', 'R23', 'KEY3_E'), ('K1C', 'S23', 'KEY1_C'),
                ('K1E', 'T23', 'KEY1_E'), ('K2C', 'U23', 'KEY2_C'), ('K2E', 'V23', 'KEY2_E')]))

    # ---------------- GY-45 under the right-hand header pins ------------------------
    gy = [('INT1', 'Y17', 'INT1'), ('INT2', 'Z17', None), ('SA0', 'AA17', None), ('SDA', 'AB17', 'SDA'),
          ('SCL', 'AC17', 'SCL'), ('GND', 'AD17', 'GND'), ('3V3out', 'AE17', None),
          ('VCC-IN', 'AF17', '3V3')]
    gy_pins = {H(h) for _, h, _ in gy}
    gy_area = [c for c in cells(25, 33, 17, 22) if c not in gy_pins]
    d.add(Part('U3', 'gy45', 'GY-45 MMA8452Q accelerometer on 1x8 header', gy, gy_area=gy_area,
               draw={'x0': 24.3, 'x1': 33.7, 'y0': 16.3, 'y1': 22.4}))
    return d


if __name__ == '__main__':
    d = build()
    for e in d.check_placement():
        print('PLACEMENT:', e)
    print(len(d.parts), 'parts')
