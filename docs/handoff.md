# VU Speaker handoff (15 Oct 2026)

Working state of the Bluetooth VU-meter speaker build. Requirements live in `docs/SPEC.md`; this file is the bench-side picture and what to do next. Build is staged: 1 Power, 2 Audio, 3 Tweeter, 4 VU meter. Nothing goes into the box until every stage passes.

## What changed since 13 Oct
1. Pin map re-partitioned by header edge and agreed: mute on GPIO4 (was 23), accelerometer INT1 on GPIO23 (was 27), buttons on 27, 26, 25, 33 (was 32, 33, 25, 26), amp keys on 18, 19, 17, Bluetooth LED sense on 34. No Wi-Fi; the ESP32 radio stays off. SPEC.md is the source of truth for pins.
2. A 1N5819 Schottky now sits on ESP32 VIN, so the 5 V logic wire can stay connected while the ESP32 is on USB.
3. Control board moves to a perfboard with the same outline as the power board (97.8 x 59.8 mm, mounting holes 3 mm at 75 x 54.7 mm centres) so screw terminals and JST-XH connectors fit on the edges.
4. VU audio feed decided: tap the speaker outputs (see below).
5. Tweeter crossover is now 10 ohm 5 W plus 1.1 uF film, tweeter polarity reversed, no woofer coil.
6. Amp key presses will go through PC827 and PC817 optocouplers.
7. GY-45 confirmed as an MMA8452Q.

## Power (stage 1)
- 19.5 V 2.31 A (45 W) adapter. Chain: 5.5x2.1 jack, rocker switch, 5 A fuse (3 A preferred), SR560 (band toward the rail), rail.
- Across the rail: P6KE27A, 1000 uF 50 V, 10 uF electrolytic (25 V or more), 100 nF. Star ground at the 1000 uF negative leg.
- MP1584 gives 5 V logic (ESP32). XL4015 gives the 5 V LED rail with 1000 uF 25 V on its output, and also feeds the AHCT125 and relay module. Both set to 5.00 to 5.05 V.
- Load-test results (MP1584 at 0.5 and 1 A, XL4015 at 2 A) are not recorded yet.

## Amp: XH-M548
- TPA3116D2 under a heatsink, JieLi Bluetooth chip.
- DC jack marked 12-24 V with no polarity mark; SS54 on the input, band toward the board, so centre pin should be positive. Still to verify by continuity from the centre pin to the unbanded end.
- Three keys (play/pause, previous/minus, next/plus). R12, R13 and R14 differ, so it may be a resistor-ladder key line. Measure pad voltages before wiring the optocouplers.
- A 78M05 feeds the Bluetooth chip and runs warm at 19 V.
- Voice prompts and LED timing are recorded in SPEC.md under Mute.

## Mute (designed, relay module bench-checked)
- 4-channel relay module, Songle SRD-05VDC-SL-C, no optocouplers. At power-on with inputs floating the relays stay off. Input pulled to GND switches the relay on.
- IN1 breaks the left speaker line, IN2 the right. Tweeters sit after the relays. IN3 and IN4 spare.
- Drive table and logic are in SPEC.md under Mute drive. GPIO4 LOW = sound on, HIGH or floating = muted, 10 k pull-up to 3.3 V.
- Firmware rule: start muted, unmute after the LED has been solid for 2.5 s, re-mute on any off-blink.
- LED sense: blue LED through 10 k and 1N4148 to GPIO34 (input only). Sense point on the amp not yet located.

## Crossovers (decided by bench listening)
Circuit and test table are in SPEC.md under Audio path. Final: 10 ohm 5 W plus 1.1 uF film (two 2.2 uF 400 V film in series) per tweeter, tweeter polarity reversed; woofers full range. If the woofer top end is harsh in the box, try 0.07 to 0.1 mH. Ready-made crossover boards were rejected (8 ohm designs, no tweeter attenuation).

## VU audio tap (decided)
Per channel from the amp side of the relay: 100 nF, 100 k, node to GPIO36 (L) or GPIO39 (R); node biased by 22 k to 3.3 V and 22 k to GND; 1 nF to GND. Bias 1.65 V, high-cut about 16 kHz. Details in SPEC.md under VU audio tap. Bench check: the pin sits about 1.65 V at idle. Never tie the tap ground to a speaker leg (outputs are bridge-tied).

## Amp key presses
PC827 (dual) and PC817 (single) in sockets: GPIO, 1 k, LED anode; cathode to GND; collector and emitter across each button's pads. Channel table in SPEC.md under Key presses into the amp. Measure the pad voltages first.

## Accelerometer: GY-45 (MMA8452Q)
VCC-IN to 3V3 (not 5 V: the board's I2C pull-ups may follow VCC-IN), GND, SDA to GPIO21, SCL to GPIO22, INT1 to GPIO23 (optional). Leave SA0, INT2 and the on-board 3.3 V pin unconnected. Address 0x1D or 0x1C; WHO_AM_I (0x0D) reads 0x2A. Library: SparkFun MMA8452Q.

## Infinity mirror box: assembly plan
- Glass 4 mm: bottom 432 x 127, back 432 x 69. Acrylic 3 mm: front 432 x 69, top 432 x 127, ends 120 x 69 (two). Ends sit inside between front and back; the top rests on all walls.
- Dry-fit first. Apply the film wet, one side only, on the inside of the front, top and ends (adhesive side to the acrylic, hard coat into the box); let it dry 2 to 3 days before closing.
- Bottom and back glass with neutral-cure silicone; drill a 4 to 5 mm wire exit low in the left end acrylic (glass cannot be drilled). Ends silicone to the glass; front acrylic solvent cement to the ends (no superglue, it fogs), silicone to the glass base.
- LED strips in the inside corners facing in; connector on the top-ring lead so the top comes off. Test before closing, blow out the dust, fix the top with thin clear VHB.
- Outside only: 25 mm silver tape over all 12 edges to hide strip backs and glue lines.

## Next bench session: XL4015 + LED strip test
Goal: prove the XL4015 holds 5 V at the 2 A firmware cap, check heat, confirm the data path.

Wiring:
- ESP32 GPIO16, AHCT125 buffer 1 (pin 1 OE to GND, pin 2 in, pin 3 out), 330 ohm, strip DIN. AHCT VCC from the XL4015, 100 nF across pins 14 and 7.
- Unused buffers: tie OE to 5 V and inputs to GND if the mute is not wired yet.
- Strip 5 V and GND from the XL4015, 1000 uF 25 V at the strip input, 20 AWG feed. All grounds joined.
- ESP32 on USB; do not also feed its 5 V pin from the MP1584 unless the VIN diode is fitted.
- WS2812B, 50 LEDs/m; a shorter piece is fine. Meter in series on the 5 V feed (10 A socket).

Test firmware: the `esp32dev` bring-up sketch (commands in SPEC.md), power cap on by default, `c` toggles.

Pass criteria are H-004 and H-005 in SPEC.md, plus: steps 2, 5 and f recorded at the cap, 5 min full white with XL4015 warm but touchable and SR560 warm only. Never run uncapped full white on long lengths (112 LEDs can draw over 6 A).

| Step | Brightness | I (A) | XL4015 out (V) | Strip end (V) | Rail (V) | Temp / notes |
|---|---|---|---|---|---|---|

## Still to do
- XH-M548: polarity check, 5.5x2.1 lead from the rail, key short/hold behaviour, heat after 5 min, key-pad voltages, locate the LED sense point.
- Build the VU tap and check the pin sits about 1.65 V at idle.
- Mount position and rating of the second tweeter.
- MP1584 load tests; XL4015 + LED test above.
- Build the control perfboard (layout files in the control-board folder), then stage 4: accelerometer, button 4 orientation teach, VU firmware, 112-LED mirror-box chain.
- Buy: second tweeter (match the first), 2 x 1 nF ceramic, PC827 and PC817 with sockets, JST-XH and screw terminals, plus general wire, heat-shrink and fuse.
