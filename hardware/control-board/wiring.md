# Control perfboard wiring list

Single-sided dot perfboard, 97.8 x 59.8 mm (same outline as the power board), 38 x 23 holes at 2.54 mm (hole count assumed from the outline). Holes are named column letter + row number, from the top-left as seen from the component side.

Routing: short solder busses on the underside (max 5 holes) and straight insulated jumper wires along a row or column.

45 jumper wires (48 hops), 47 bus groups (115 bridges).

## Connectors

**J1** 5V logic in (from MP1584), 5.08 mm screw terminal: 1 5V_LOGIC @ A5, 2 GND @ A3

**J2** 5V LED rail in (from XL4015), 5.08 mm screw terminal: 1 5V_LED @ C23, 2 GND @ A23

**J3** Relay board IN1..IN4, JST-XH 6-pin: 1 GND @ A22, 2 IN4 @ A21, 3 IN3 @ A20, 4 IN2 @ A19, 5 IN1 @ A18, 6 VCC @ A17

**J4** LED strip data, 5.08 mm screw terminal: 1 DATA @ H23, 2 GND @ J23

**J5** Speaker-leg audio sense, JST-XH 3-pin: 1 L_SPK @ Y2, 2 R_SPK @ X2, 3 GND @ W2

**J6** Panel buttons, JST-XH 5-pin: 1 BTN1 @ N1, 2 BTN2 @ O1, 3 BTN3 @ P1, 4 BTN4 @ Q1, 5 GND @ R1

**J7** Amp blue-LED sense, JST-XH 2-pin: 1 SENSE @ S3, 2 GND @ R3

**J8** Key-press outputs to amp pads, JST-XH 6-pin: 1 K1C @ Y18, 2 K1E @ Y19, 3 K2C @ Y20, 4 K2E @ Y21, 5 K3C @ Y22, 6 K3E @ Y23


## Jumper wires

| Wire | Net | From | To | Holes | Also at | Note |
|---|---|---|---|---|---|---|
| W1 | 3V3 | D12 (free hole) | AC12 (free hole) | 25 | W12 (free hole) |  |
| W2 | 3V3 | E15 (free hole) | I15 (free hole) | 4 | - |  |
| W3 | 3V3 | W12 (free hole) | W17 (U3.VCC-IN) | 5 | - | run on solder side (passes over 1 part cells) |
| W4 | 3V3 | AC4 (R5.2) | AC12 (free hole) | 8 | - |  |
| W5 | 5V_LED | B14 (C4.+) | B22 (free hole) | 8 | - | run on solder side (passes over 4 part cells) |
| W6 | 5V_LED | C22 (free hole) | H22 (C3.1) | 5 | - |  |
| W7 | 5V_LOGIC | C5 (C1.+) | E5 (D2.A) | 2 | - |  |
| W8 | BTN1 | N1 (J6.BTN1) | N6 (U1.IO27) | 5 | - |  |
| W9 | BTN2 | O1 (J6.BTN2) | O6 (U1.IO26) | 5 | - |  |
| W10 | BTN3 | P1 (J6.BTN3) | P6 (U1.IO25) | 5 | - |  |
| W11 | BTN4 | Q1 (J6.BTN4) | Q6 (U1.IO33) | 5 | - | run on solder side (passes over 2 part cells) |
| W12 | D16 | G14 (free hole) | G18 (U2.1A) | 4 | - |  |
| W13 | D16 | G14 (free hole) | N14 (free hole) | 7 | - |  |
| W14 | DATA_BUF | F18 (U2.1Y) | I18 (R1.1) | 3 | - | run on solder side (passes over 2 part cells) |
| W15 | IN1 | A18 (J3.IN1) | C18 (U2.2Y) | 2 | - | run on solder side (passes over 1 part cells) |
| W16 | INT1 | P14 (free hole) | P17 (U3.INT1) | 3 | - | run on solder side (passes over 1 part cells) |
| W17 | INT1 | P14 (free hole) | W14 (free hole) | 7 | - |  |
| W18 | KEY1 | K13 (free hole) | K19 (R11.1) | 6 | - | run on solder side (passes over 1 part cells) |
| W19 | KEY1 | K13 (free hole) | Q13 (free hole) | 6 | - |  |
| W20 | KEY1_A | N19 (R11.2) | AE19 (free hole) | 17 | - | run on solder side (passes over 5 part cells) |
| W21 | KEY1_C | Y18 (J8.K1C) | AD18 (free hole) | 5 | - | run on solder side (passes over 4 part cells) |
| W22 | KEY2 | M15 (free hole) | M17 (free hole) | 2 | - | run on solder side (passes over 1 part cells) |
| W23 | KEY2 | M15 (free hole) | R15 (free hole) | 5 | - |  |
| W24 | KEY2_A | K17 (free hole) | AA17 (U4.A2) | 16 | - | run on solder side (passes over 9 part cells) |
| W25 | KEY2_C | Y20 (J8.K2C) | AA20 (U4.C2) | 2 | - | run on solder side (passes over 1 part cells) |
| W26 | KEY3 | N17 (free hole) | N21 (R13.1) | 4 | - |  |
| W27 | KEY3_C | N22 (U5.C) | Y22 (J8.K3C) | 11 | - |  |
| W28 | KEY3_E | N23 (U5.E) | Y23 (J8.K3E) | 11 | - |  |
| W29 | MUTE | C17 (free hole) | C21 (U2.3A) | 4 | - | run on solder side (passes over 3 part cells) |
| W30 | MUTE | E16 (free hole) | M16 (U1.IO4) | 8 | - | run on solder side (passes over 4 part cells) |
| W31 | SCL | T15 (free hole) | T17 (U3.SCL) | 2 | - | run on solder side (passes over 1 part cells) |
| W32 | VU_L | V4 (C7.1) | Z4 (R5.1) | 4 | - |  |
| W33 | VU_L | Z3 (R7.1) | AE3 (R3.2) | 5 | - | run on solder side (passes over 2 part cells) |
| W34 | VU_R | U7 (free hole) | AF7 (free hole) | 11 | - |  |
| W35 | VU_R | AF2 (R6.1) | AF7 (free hole) | 5 | - |  |
| W36 | GND | A23 (J2.GND) | J23 (J4.GND) | 9 | - | run on solder side (passes over 4 part cells) |
| W37 | GND | B17 (free hole) | H17 (free hole) | 6 | E17 (free hole) |  |
| W38 | GND | C4 (C1.-) | C15 (free hole) | 11 | - |  |
| W39 | GND | C4 (C1.-) | R4 (R8.2) | 15 | - |  |
| W40 | GND | F21 (U2.4A) | J21 (free hole) | 4 | - | run on solder side (passes over 2 part cells) |
| W41 | GND | J6 (U1.GND) | J22 (C3.2) | 16 | J16 (U1.GND) | run on solder side (passes over 1 part cells) |
| W42 | GND | R1 (J6.GND) | U1 (C8.2) | 3 | - |  |
| W43 | GND | U1 (C8.2) | U17 (U3.GND) | 16 | - | run on solder side (passes over 4 part cells) |
| W44 | GND | W3 (R7.2) | W5 (R10.2) | 2 | - |  |
| W45 | GND | Z5 (free hole) | Z17 (U4.K2) | 12 | - |  |

## Solder busses (underside)

| Bus | Net | Holes |
|---|---|---|
| B1 | 3V3 | D12 > D13 > D14 (R2.2) > D15 > E15 |
| B2 | 3V3 | I15 > I16 (U1.3V3) |
| B3 | 3V3 | AC2 (R6.2) > AC3 > AC4 (R5.2) |
| B4 | 5V_LED | A14 > A15 > A16 > A17 (J3.VCC) > B14 (C4.+) |
| B5 | 5V_LED | B22 > C22 > C23 (J2.5V_LED) |
| B6 | 5V_LED | G21 (U2.4OE) > H21 (U2.VCC) > H22 (C3.1) |
| B7 | 5V_LOGIC | A5 (J1.5V_LOGIC) > A6 > B5 > B6 (C2.1) > C5 (C1.+) |
| B8 | D16 | N14 > N15 > N16 (U1.IO16) |
| B9 | GND | A3 (J1.GND) > A4 > B4 (C2.2) > C4 (C1.-) |
| B10 | GND | A22 (J3.GND) > A23 (J2.GND) |
| B11 | GND | B15 (C4.-) > B16 > B17 > B18 (U2.GND) > C15 |
| B12 | GND | D20 > D21 (U2.3OE) > E20 > F20 > F21 (U2.4A) |
| B13 | GND | E17 > E18 (U2.2OE) |
| B14 | GND | H17 > H18 (U2.1OE) > I17 > J16 (U1.GND) > J17 |
| B15 | GND | J21 > J22 (C3.2) > J23 (J4.GND) > K23 (U5.K) |
| B16 | GND | R1 (J6.GND) > R2 > R3 (J7.GND) > R4 (R8.2) |
| B17 | GND | U1 (C8.2) > U2 > V2 (C7.2) > W2 (J5.GND) > W3 (R7.2) |
| B18 | GND | W5 (R10.2) > X5 > Y5 > Z5 |
| B19 | GND | Z16 > Z17 (U4.K2) > AA16 > AB16 > AB17 (U4.K1) |
| B20 | IN2 | A19 (J3.IN2) > B19 > B20 > B21 (U2.3Y) |
| B21 | INT1 | W14 > W15 > W16 (U1.IO23) |
| B22 | KEY1 | Q13 > Q14 > Q15 > Q16 (U1.IO18) |
| B23 | KEY1_A | AC17 (U4.A1) > AD17 > AE17 > AE18 > AE19 |
| B24 | KEY1_C | AC18 > AC19 > AC20 (U4.C1) > AD18 |
| B25 | KEY1_E | Y19 (J8.K1E) > Z19 > AA19 > AB19 > AB20 (U4.E1) |
| B26 | KEY2 | M17 > M18 > N18 (R12.1) |
| B27 | KEY2 | R15 > R16 (U1.IO19) |
| B28 | KEY2_A | K17 > K18 (R12.2) |
| B29 | KEY2_E | Y21 (J8.K2E) > Z20 (U4.E2) > Z21 |
| B30 | KEY3 | N17 > O16 (U1.IO17) > O17 |
| B31 | KEY3_A | K21 (R13.2) > K22 (U5.A) |
| B32 | LED_DATA | H23 (J4.DATA) > I21 (R1.2) > I22 > I23 |
| B33 | L_SPK | Y2 (J5.L_SPK) > Z2 (C5.1) |
| B34 | MUTE | C17 > D16 > D17 (R2.1) > D18 (U2.2A) > E16 |
| B35 | R_SPK | X1 (C6.1) > X2 (J5.R_SPK) |
| B36 | SCL | T15 > U15 > V15 > V16 (U1.IO22) |
| B37 | SDA | S16 (U1.IO21) > S17 (U3.SDA) |
| B38 | SENSE | S5 (D1.K) > T5 (R10.1) > T6 (U1.IO34) |
| B39 | SENSE_D | P2 (R9.2) > P3 > P4 > P5 (D1.A) |
| B40 | SENSE_RAW | S2 (R9.1) > S3 (J7.SENSE) |
| B41 | VIN | I5 (D2.K) > I6 (U1.VIN) |
| B42 | VU_L | V4 (C7.1) > V5 > V6 (U1.IO36) |
| B43 | VU_L | Z3 (R7.1) > Z4 (R5.1) |
| B44 | VU_L_C | AB2 (C5.2) > AB3 (R3.1) |
| B45 | VU_R | U3 (C8.1) > U4 (R8.1) > U5 > U6 (U1.IO39) > U7 |
| B46 | VU_R | AF1 (R4.2) > AF2 (R6.1) |
| B47 | VU_R_C | Z1 (C6.2) > AA1 > AB1 > AC1 (R4.1) |

## Parts

| Ref | Part | Pins |
|---|---|---|
| C1 | 100uF 16V | + C5, - C4 |
| C2 | 100nF | 1 B6, 2 B4 |
| C3 | 100nF | 1 H22, 2 J22 |
| C4 | 100uF 16V | + B14, - B15 |
| C5 | 100nF | 1 Z2, 2 AB2 |
| C6 | 100nF | 1 X1, 2 Z1 |
| C7 | 1nF | 1 V4, 2 V2 |
| C8 | 1nF | 1 U3, 2 U1 |
| D1 | 1N4148 | A P5, K S5 |
| D2 | 1N5819 | A E5, K I5 |
| R1 | 330R | 1 I18, 2 I21 |
| R2 | 10k | 1 D17, 2 D14 |
| R3 | 100k | 1 AB3, 2 AE3 |
| R4 | 100k | 1 AC1, 2 AF1 |
| R5 | 22k | 1 Z4, 2 AC4 |
| R6 | 22k | 1 AF2, 2 AC2 |
| R7 | 22k | 1 Z3, 2 W3 |
| R8 | 22k | 1 U4, 2 R4 |
| R9 | 10k | 1 S2, 2 P2 |
| R10 | 100k | 1 T5, 2 W5 |
| R11 | 1k | 1 K19, 2 N19 |
| R12 | 1k | 1 N18, 2 K18 |
| R13 | 1k | 1 N21, 2 K21 |
| U1 | ESP32 DevKit 30-pin on 2x15 sockets | VIN I6, GND J6, IO27 N6, IO26 O6, IO25 P6, IO33 Q6, IO34 T6, IO39 U6, IO36 V6, 3V3 I16, GND J16, IO4 M16, IO16 N16, IO17 O16, IO18 Q16, IO19 R16, IO21 S16, IO22 V16, IO23 W16 |
| U2 | SN74AHCT125N DIP-14 in socket | 1OE H18, 1A G18, 1Y F18, 2OE E18, 2A D18, 2Y C18, GND B18, 3Y B21, 3A C21, 3OE D21, 4A F21, 4OE G21, VCC H21 |
| U3 | GY-45 MMA8452Q accelerometer, 1x8 header | VCC-IN W17, GND U17, SCL T17, SDA S17, INT1 P17 |
| U4 | PC827 dual optocoupler in DIP-8 socket | A1 AC17, K1 AB17, A2 AA17, K2 Z17, E2 Z20, C2 AA20, E1 AB20, C1 AC20 |
| U5 | PC817 optocoupler in DIP-4 socket | A K22, K K23, E N23, C N22 |
