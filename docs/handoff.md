# VU Speaker handoff (13 Oct 2026)

Working state of the Bluetooth VU-meter speaker build. Requirements live in `docs/SPEC.md`; this file is the bench-side picture and what to do next. Build is staged: 1 Power, 2 Audio, 3 Tweeter, 4 VU meter. Nothing goes into the box until every stage passes.

## What changed since 10 Oct
1. The XH-M548 amp arrived and was bench-listened with a tweeter: works, sounds good. It replaces the earlier dead amp board.
2. Two tweeters, one per channel, on passive crossovers off the amp's speaker outputs. The tweeter amp, L+R mix and trimmer are dropped.
3. A 0.15 mH coil in series with each woofer.
4. Voice-prompt mute designed: relay module, SN74AHCT125N, ESP32 GPIO23, driven from the amp's blue Bluetooth LED.

## Power (stage 1)
- 19.5 V 2.31 A (45 W) adapter. Chain: 5.5x2.1 jack, rocker switch, 5 A fuse (3 A preferred), SR560 (band toward the rail), rail.
- Across the rail: P6KE27A, 1000 uF 50 V, 10 uF electrolytic (25 V or more), 100 nF. Star ground at the 1000 uF negative leg.
- MP1584 gives 5 V logic (ESP32). XL4015 gives the 5 V LED rail with 1000 uF 25 V on its output, and also feeds the AHCT125 and relay module. Both set to 5.00 to 5.05 V.
- Load-test results (MP1584 at 0.5 and 1 A, XL4015 at 2 A) are not recorded yet.

## Amp: XH-M548
- TPA3116D2 under a heatsink, JieLi Bluetooth chip.
- DC jack marked 12-24 V with no polarity mark; SS54 on the input, band toward the board, so centre pin should be positive. Still to verify by continuity from the centre pin to the unbanded end.
- Three keys (play/reset, previous/minus, next/plus). R12, R13 and R14 differ, so it may be a resistor-ladder key line. Measure pad voltages before designing ESP32 key presses.
- A 78M05 feeds the Bluetooth chip and runs warm at 19 V.
- Voice prompts and LED timing are recorded in SPEC.md under Mute.

## Mute (designed, relay module bench-checked)
- 4-channel relay module, Songle SRD-05VDC-SL-C, no optocouplers. At power-on with inputs floating the relays stay off. Input pulled to GND switches the relay on.
- IN1 breaks the left speaker line, IN2 the right. Tweeters sit after the relays. IN3 and IN4 spare.
- Drive table and logic are in SPEC.md under Mute drive. GPIO23 LOW = sound on.
- Firmware rule: start muted, unmute after the LED has been solid for 2.5 s, re-mute on any off-blink.
- LED sense: blue LED through 10 k and 1N4148 to an ESP32 input. Sense point on the amp not yet located.

## Crossovers (decided by bench listening)
Circuit and test table are in SPEC.md under Audio path. Final: 10 ohm 5 W plus 2.2 uF film (63 V or more) per tweeter; 0.15 mH air-core coil per woofer. Ready-made crossover boards were rejected (8 ohm designs, no tweeter attenuation, more space).

## Next bench session: XL4015 + LED strip test
Goal: prove the XL4015 holds 5 V at the 2 A firmware cap, check heat, confirm the data path.

Wiring:
- ESP32 GPIO16, AHCT125 buffer 1 (pin 1 OE to GND, pin 2 in, pin 3 out), 330 ohm, strip DIN. AHCT VCC from the XL4015, 100 nF across pins 14 and 7.
- Unused buffers: tie OE to 5 V and inputs to GND if the mute is not wired yet.
- Strip 5 V and GND from the XL4015, 1000 uF 25 V at the strip input, 20 AWG feed. All grounds joined.
- ESP32 on USB; do not also feed its 5 V pin from the MP1584.
- WS2812B, 50 LEDs/m; a shorter piece is fine. Meter in series on the 5 V feed (10 A socket).

Test firmware: the `esp32dev` bring-up sketch (commands in SPEC.md), power cap on by default, `c` toggles.

Pass criteria are H-004 and H-005 in SPEC.md, plus: steps 2, 5 and f recorded at the cap, 5 min full white with XL4015 warm but touchable and SR560 warm only. Never run uncapped full white on long lengths (112 LEDs can draw over 6 A).

| Step | Brightness | I (A) | XL4015 out (V) | Strip end (V) | Rail (V) | Temp / notes |
|---|---|---|---|---|---|---|

## Still to do
- XH-M548: polarity check, 5.5x2.1 lead from the rail, key short/hold behaviour, heat after 5 min, key-pad voltages, locate the LED sense point.
- Decide the VU audio feed (SPEC.md open decision 3).
- Mount position and rating of the second tweeter.
- MP1584 load tests; XL4015 + LED test above.
- Stage 4: accelerometer, button 4 orientation teach, VU firmware, 112-LED mirror-box chain.
- Buy: second tweeter (match the first), two 0.15 mH coils, two 2.2 uF film capacitors, plus general wire, heat-shrink, fuse, buttons.
