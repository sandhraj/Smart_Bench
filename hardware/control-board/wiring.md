# Control perfboard wiring list

Single-sided dot perfboard, 97.8 x 59.8 mm (same outline as the power board), landscape, 38 x 23 holes at 2.54 mm (hole count assumed from the outline; check against the real board). Holes are named column letter + row number, from the top-left as seen from the component side. Mounting holes 3 mm at 75 x 54.7 mm centres; no holes are used within 3 mm of them.

Three kinds of wire, nothing else:

- **Solder bridge**: neighbouring holes joined on the underside (chains of at most 5 holes).
- **Top jumper**: insulated wire on the component side, straight along a row or column, both ends in free holes (never in a component lead hole). Many run under the ESP32 module.
- **Under-board jump**: short insulated wire on the solder side, straight, at most 6 holes between ends, soldered to the pads. May cross pads of other nets.

20 top jumpers, 32 under-board jumps, 123 bridged hole pairs in 70 chains. Checked: no short between nets, every net in one piece.

## Connectors

| Ref | Type | Pins (hole) | Goes to |
|---|---|---|---|
| CN1 | 5.08 mm screw terminal 2P, 5 V logic in | 1 B3, 2 B5 | Board A, MP1584 5 V logic output (1) and ground (2) |
| CN2 | 5.08 mm screw terminal 2P, 5 V LED rail in | 1 B13, 2 B15 | Board A, XL4015 5 V LED rail (1) and ground (2); no LED current flows through B |
| CN3 | JST-XH 4P, relay module: 5 V, GND, IN1, IN2 | 1 B18, 2 B19, 3 B20, 4 B21 | Relay module: VCC, GND, IN1, IN2 (four wires) |
| CN4 | 5.08 mm screw terminal 2P, LED strip data | 1 B8, 2 B10 | LED strip data (1, after the 330 ohm) and a signal ground (2) |
| CN5 | JST-XH 4P, amp: BT LED sense, L, R, GND | SENSE AC2, L AD2, R AE2, GND AF2 | Amp XH-M548: Bluetooth LED sense (1), L speaker leg (2), R speaker leg (3), ground (4) |
| CN6 | JST-XH 5P, panel buttons | GND P2, B1 Q2, B2 R2, B3 S2, B4 T2 | Panel buttons 1 to 4 and common ground |
| CN7 | 1x6 2.54 mm header, key outputs to amp pads | K3C Q23, K3E R23, K1C S23, K1E T23, K2C U23, K2E V23 | Amp key pads: collector and emitter of optocoupler channels 3, 1 and 2 (six wires) |

Pin to net:

- **CN1**: 1 B3 = 5V_LOGIC, 2 B5 = GND
- **CN2**: 1 B13 = 5V_LED, 2 B15 = GND
- **CN3**: 1 B18 = 5V_LED, 2 B19 = GND, 3 B20 = IN1, 4 B21 = IN2
- **CN4**: 1 B8 = LED_OUT, 2 B10 = GND
- **CN5**: SENSE AC2 = SENSE_RAW, L AD2 = L_SPK, R AE2 = R_SPK, GND AF2 = GND
- **CN6**: GND P2 = GND, B1 Q2 = BTN1, B2 R2 = BTN2, B3 S2 = BTN3, B4 T2 = BTN4
- **CN7**: K3C Q23 = KEY3_C, K3E R23 = KEY3_E, K1C S23 = KEY1_C, K1E T23 = KEY1_E, K2C U23 = KEY2_C, K2E V23 = KEY2_E

## Top jumpers (component side, insulated)

| Wire | Net | From | To | Holes |
|---|---|---|---|---|
| T1 | GND | I4 | M4 | 4 |
| T2 | SENSE_RAW | AB2 | X2 | 4 |
| T3 | L_SPK | AD4 | AD10 | 6 |
| T4 | L_SPK | AC10 | Z10 | 3 |
| T5 | R_SPK | AE4 | AE12 | 8 |
| T6 | R_SPK | AD12 | Y12 | 5 |
| T7 | GND | M15 | M10 | 5 |
| T8 | GND | N10 | V10 | 8 |
| T9 | GND | AF4 | AF7 | 3 |
| T10 | 3V3 | L14 | O14 | 3 |
| T11 | 3V3 | Q14 | W14 | 6 |
| T12 | 3V3 | W13 | W9 | 4 |
| T13 | 3V3 | X14 | AF14 | 8 |
| T14 | MUTE | P18 | L18 | 4 |
| T15 | LED_IN | Q17 | I17 | 8 |
| T16 | LED_BUF | J18 | J9 | 9 |
| T17 | IN1 | G20 | D20 | 3 |
| T18 | IN2 | G21 | D21 | 3 |
| T19 | 5V_LED | F18 | F22 | 4 |
| T20 | SCL | Y15 | AC15 | 4 |

## Under-board jumps (solder side, insulated)

| Wire | Net | From | To | Holes | Ends |
|---|---|---|---|---|---|
| S1 | 5V_LOGIC | B3 | G3 | 5 | CN1.1 / free hole |
| S2 | GND | B4 | H4 | 6 | free hole / C2.2 |
| S3 | GND | H2 | H4 | 2 | C1.- / C2.2 |
| S4 | GND | P4 | M4 | 3 | free hole / free hole |
| S5 | BTN1 | Q2 | Q6 | 4 | CN6.B1 / U1.T.D27 |
| S6 | BTN2 | R2 | R6 | 4 | CN6.B2 / U1.T.D26 |
| S7 | BTN3 | S2 | S6 | 4 | CN6.B3 / U1.T.D25 |
| S8 | BTN4 | T2 | T6 | 4 | CN6.B4 / U1.T.D33 |
| S9 | GND | V4 | P4 | 6 | R10.2 / free hole |
| S10 | VU_R_C | X8 | X11 | 3 | R4.1 / C6.2 |
| S11 | GND | V9 | AA9 | 5 | free hole / free hole |
| S12 | GND | AF8 | AB8 | 4 | free hole / C7.2 |
| S13 | 3V3 | W8 | Z8 | 3 | R6.2 / R5.2 |
| S14 | MUTE | L19 | L21 | 2 | U2.5 / free hole |
| S15 | IN1 | M20 | H20 | 5 | free hole / free hole |
| S16 | IN2 | N21 | I21 | 5 | free hole / free hole |
| S17 | 5V_LED | B13 | B18 | 5 | CN2.1 / CN3.1 |
| S18 | GND | C5 | C10 | 5 | free hole / free hole |
| S19 | GND | C10 | C15 | 5 | free hole / free hole |
| S20 | GND | C15 | C19 | 4 | free hole / free hole |
| S21 | GND | B19 | H19 | 6 | CN3.2 / U2.1 |
| S22 | GND | H19 | K19 | 3 | U2.1 / U2.4 |
| S23 | GND | K19 | N19 | 3 | U2.4 / U2.7 |
| S24 | GND | M16 | M18 | 2 | U1.B.GND / free hole |
| S25 | GND | J23 | L23 | 2 | C3.2 / free hole |
| S26 | GND | J22 | L22 | 2 | U2.12 / U2.10 |
| S27 | GND | N19 | R19 | 4 | U2.7 / U4.2 |
| S28 | GND | R19 | T19 | 2 | U4.2 / U4.4 |
| S29 | GND | T19 | W19 | 3 | U4.4 / U5.2 |
| S30 | GND | X18 | AD18 | 6 | free hole / free hole |
| S31 | SDA | V17 | AB17 | 6 | free hole / U3.SDA |
| S32 | INT1 | Z16 | Z18 | 2 | U1.B.D23 / free hole |

## Solder bridges (underside)

| Bridge | Net | Holes |
|---|---|---|
| B1 | 3V3 | AF14 > AF15 > AF16 > AF17 (U3.VCC-IN) |
| B2 | 3V3 | L16 (U1.B.3V3) > L15 > L14 |
| B3 | 3V3 | O14 > P14 (R2.2) > Q14 |
| B4 | 3V3 | W13 > W14 > X14 |
| B5 | 3V3 | W9 > W8 (R6.2) |
| B6 | 5V_LED | B18 (CN3.1) > C18 > D18 > E18 > F18 |
| B7 | 5V_LED | F22 > G22 > H22 (U2.14) > I22 (U2.13) > I23 (C3.1) |
| B8 | 5V_LOGIC | G2 (C1.+) > G3 > G4 (C2.1) > G5 > H5 (D2.A) |
| B9 | GND | AA9 > AA8 (R7.2) > AB8 (C7.2) |
| B10 | GND | AD18 > AD17 (U3.GND) |
| B11 | GND | AF2 (CN5.GND) > AF3 > AF4 |
| B12 | GND | AF7 > AF8 |
| B13 | GND | C10 > B10 (CN4.2) |
| B14 | GND | C15 > B15 (CN2.2) |
| B15 | GND | C19 > B19 (CN3.2) |
| B16 | GND | B4 > B5 (CN1.2) > C5 |
| B17 | GND | H4 (C2.2) > I4 |
| B18 | GND | K19 (U2.4) > K20 > K21 > J21 > J22 (U2.12) |
| B19 | GND | L23 > L22 (U2.10) |
| B20 | GND | M10 > N10 |
| B21 | GND | M16 (U1.B.GND) > M15 |
| B22 | GND | M18 > N18 > N19 (U2.7) |
| B23 | GND | M4 > M5 > M6 (U1.T.GND) |
| B24 | GND | P2 (CN6.GND) > P3 > P4 |
| B25 | GND | V10 > V9 > V8 (R8.2) > U8 (C8.2) |
| B26 | GND | W19 (U5.2) > X19 > X18 |
| B27 | IN1 | D20 > C20 > B20 (CN3.3) |
| B28 | IN1 | H20 > G20 |
| B29 | IN1 | M19 (U2.6) > M20 |
| B30 | IN2 | D21 > C21 > B21 (CN3.4) |
| B31 | IN2 | I21 > H21 > G21 |
| B32 | IN2 | N22 (U2.8) > N21 |
| B33 | INT1 | Z18 > Y18 > Y17 (U3.INT1) |
| B34 | KEY1 | T16 (U1.B.D18) > T17 (R11.1) |
| B35 | KEY1_A | T18 (R11.2) > S18 > S19 (U4.3) |
| B36 | KEY1_C | S22 (U4.6) > S23 (CN7.K1C) |
| B37 | KEY1_E | T22 (U4.5) > T23 (CN7.K1E) |
| B38 | KEY2 | U16 (U1.B.D19) > U17 (R12.1) |
| B39 | KEY2_A | U18 (R12.2) > V18 > V19 (U5.1) |
| B40 | KEY2_C | V22 (U5.4) > U22 > U23 (CN7.K2C) |
| B41 | KEY2_E | W22 (U5.3) > W23 > V23 (CN7.K2E) |
| B42 | KEY3 | R16 (U1.B.D17) > R17 (R13.1) |
| B43 | KEY3_A | R18 (R13.2) > Q18 > Q19 (U4.1) |
| B44 | KEY3_C | Q22 (U4.8) > Q23 (CN7.K3C) |
| B45 | KEY3_E | R22 (U4.7) > R23 (CN7.K3E) |
| B46 | LED_BUF | J9 > J8 > I8 > H8 (R1.1) |
| B47 | LED_BUF | J19 (U2.3) > J18 |
| B48 | LED_IN | I17 > I18 > I19 (U2.2) |
| B49 | LED_IN | Q16 (U1.B.D16) > Q17 |
| B50 | LED_OUT | E8 (R1.2) > D8 > C8 > B8 (CN4.1) |
| B51 | L_SPK | AD10 > AC10 |
| B52 | L_SPK | AD2 (CN5.L) > AD3 > AD4 |
| B53 | L_SPK | Z10 > Y10 (C5.1) |
| B54 | MUTE | L18 > L19 (U2.5) |
| B55 | MUTE | L21 > M21 > M22 (U2.9) |
| B56 | MUTE | P15 (R2.1) > P16 (U1.B.D4) > P17 > P18 |
| B57 | R_SPK | AE12 > AD12 |
| B58 | R_SPK | AE2 (CN5.R) > AE3 > AE4 |
| B59 | R_SPK | Y12 > X12 (C6.1) |
| B60 | SCL | AC15 > AC16 > AC17 (U3.SCL) |
| B61 | SCL | Y16 (U1.B.D22) > Y15 |
| B62 | SDA | V16 (U1.B.D21) > V17 |
| B63 | SENSE | W6 (U1.T.D34) > W5 (D1.K) > V5 (R10.1) |
| B64 | SENSE_D | W3 (R9.2) > W4 (D1.A) |
| B65 | SENSE_RAW | AC2 (CN5.SENSE) > AB2 |
| B66 | SENSE_RAW | X2 > W2 (R9.1) |
| B67 | VIN | L5 (D2.K) > L6 (U1.T.VIN) |
| B68 | VU_L | Y6 (U1.T.VP) > Y7 (R3.2) > Z7 (R5.1) > AA7 (R7.1) > AB7 (C7.1) |
| B69 | VU_L_C | Y8 (R3.1) > Y9 (C5.2) |
| B70 | VU_R | X6 (U1.T.VN) > X7 (R4.2) > W7 (R6.1) > V7 (R8.1) > U7 (C8.1) |

## Parts

| Ref | Part | Pins (hole) |
|---|---|---|
| U1 | ESP32 DevKit 30-pin on 2x15 sockets | T.VIN L6, T.GND M6, T.D13 N6, T.D12 O6, T.D14 P6, T.D27 Q6, T.D26 R6, T.D25 S6, T.D33 T6, T.D32 U6, T.D35 V6, T.D34 W6, T.VN X6, T.VP Y6, T.EN Z6, B.3V3 L16, B.GND M16, B.D15 N16, B.D2 O16, B.D4 P16, B.D16 Q16, B.D17 R16, B.D5 S16, B.D18 T16, B.D19 U16, B.D21 V16, B.RX0 W16, B.TX0 X16, B.D22 Y16, B.D23 Z16 |
| C1 | 100uF 16V | + G2, - H2 |
| C2 | 100nF | 1 G4, 2 H4 |
| D2 | 1N5819 | A H5, K L5 |
| R9 | 10k | 1 W2, 2 W3 |
| D1 | 1N4148 | A W4, K W5 |
| R10 | 100k | 1 V5, 2 V4 |
| R3 | 100k | 2 Y7, 1 Y8 |
| R5 | 22k | 1 Z7, 2 Z8 |
| R7 | 22k | 1 AA7, 2 AA8 |
| C7 | 1nF | 1 AB7, 2 AB8 |
| C5 | 100nF | 2 Y9, 1 Y10 |
| R4 | 100k | 2 X7, 1 X8 |
| R6 | 22k | 1 W7, 2 W8 |
| R8 | 22k | 1 V7, 2 V8 |
| C8 | 1nF | 1 U7, 2 U8 |
| C6 | 100nF | 2 X11, 1 X12 |
| R1 | 330R | 1 H8, 2 E8 |
| U2 | SN74AHCT125N DIP-14 in socket | 1 H19, 2 I19, 3 J19, 4 K19, 5 L19, 6 M19, 7 N19, 14 H22, 13 I22, 12 J22, 11 K22, 10 L22, 9 M22, 8 N22 |
| C3 | 100nF | 1 I23, 2 J23 |
| R2 | 10k | 1 P15, 2 P14 |
| U4 | PC827 dual optocoupler in DIP-8 socket | 1 Q19, 2 R19, 3 S19, 4 T19, 5 T22, 6 S22, 7 R22, 8 Q22 |
| U5 | PC817 optocoupler in DIP-4 socket | 1 V19, 2 W19, 3 W22, 4 V22 |
| R11 | 1k | 1 T17, 2 T18 |
| R12 | 1k | 1 U17, 2 U18 |
| R13 | 1k | 1 R17, 2 R18 |
| U3 | GY-45 MMA8452Q accelerometer on 1x8 header | INT1 Y17, INT2 Z17, SA0 AA17, SDA AB17, SCL AC17, GND AD17, 3V3out AE17, VCC-IN AF17 |

## Nets

- **3V3**: U1.B.3V3 (L16), R5.2 (Z8), R6.2 (W8), R2.2 (P14), U3.VCC-IN (AF17)
- **5V_LED**: CN2.1 (B13), CN3.1 (B18), U2.14 (H22), U2.13 (I22), C3.1 (I23)
- **5V_LOGIC**: CN1.1 (B3), C1.+ (G2), C2.1 (G4), D2.A (H5)
- **BTN1**: U1.T.D27 (Q6), CN6.B1 (Q2)
- **BTN2**: U1.T.D26 (R6), CN6.B2 (R2)
- **BTN3**: U1.T.D25 (S6), CN6.B3 (S2)
- **BTN4**: U1.T.D33 (T6), CN6.B4 (T2)
- **GND**: U1.T.GND (M6), U1.B.GND (M16), CN1.2 (B5), C1.- (H2), C2.2 (H4), CN6.GND (P2), CN5.GND (AF2), R10.2 (V4), R7.2 (AA8), C7.2 (AB8), R8.2 (V8), C8.2 (U8), CN4.2 (B10), CN2.2 (B15), CN3.2 (B19), U2.1 (H19), U2.4 (K19), U2.7 (N19), U2.12 (J22), U2.10 (L22), C3.2 (J23), U4.2 (R19), U4.4 (T19), U5.2 (W19), U3.GND (AD17)
- **IN1**: CN3.3 (B20), U2.6 (M19)
- **IN2**: CN3.4 (B21), U2.8 (N22)
- **INT1**: U1.B.D23 (Z16), U3.INT1 (Y17)
- **KEY1**: U1.B.D18 (T16), R11.1 (T17)
- **KEY1_A**: U4.3 (S19), R11.2 (T18)
- **KEY1_C**: U4.6 (S22), CN7.K1C (S23)
- **KEY1_E**: U4.5 (T22), CN7.K1E (T23)
- **KEY2**: U1.B.D19 (U16), R12.1 (U17)
- **KEY2_A**: U5.1 (V19), R12.2 (U18)
- **KEY2_C**: U5.4 (V22), CN7.K2C (U23)
- **KEY2_E**: U5.3 (W22), CN7.K2E (V23)
- **KEY3**: U1.B.D17 (R16), R13.1 (R17)
- **KEY3_A**: U4.1 (Q19), R13.2 (R18)
- **KEY3_C**: U4.8 (Q22), CN7.K3C (Q23)
- **KEY3_E**: U4.7 (R22), CN7.K3E (R23)
- **LED_BUF**: R1.1 (H8), U2.3 (J19)
- **LED_IN**: U1.B.D16 (Q16), U2.2 (I19)
- **LED_OUT**: CN4.1 (B8), R1.2 (E8)
- **L_SPK**: CN5.L (AD2), C5.1 (Y10)
- **MUTE**: U1.B.D4 (P16), U2.5 (L19), U2.9 (M22), R2.1 (P15)
- **R_SPK**: CN5.R (AE2), C6.1 (X12)
- **SCL**: U1.B.D22 (Y16), U3.SCL (AC17)
- **SDA**: U1.B.D21 (V16), U3.SDA (AB17)
- **SENSE**: U1.T.D34 (W6), D1.K (W5), R10.1 (V5)
- **SENSE_D**: R9.2 (W3), D1.A (W4)
- **SENSE_RAW**: CN5.SENSE (AC2), R9.1 (W2)
- **VIN**: U1.T.VIN (L6), D2.K (L5)
- **VU_L**: U1.T.VP (Y6), R3.2 (Y7), R5.1 (Z7), R7.1 (AA7), C7.1 (AB7)
- **VU_L_C**: R3.1 (Y8), C5.2 (Y9)
- **VU_R**: U1.T.VN (X6), R4.2 (X7), R6.1 (W7), R8.1 (V7), C8.1 (U7)
- **VU_R_C**: R4.1 (X8), C6.2 (X11)

ESP32 pins left unconnected: D13, D12, D14, D32, D35, EN, D15, D2, D5, RX0, TX0 (USB serial and strapping pins are not used).
