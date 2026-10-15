# Bluetooth VU Meter Speaker

Status: draft 2, amp board received and bench-listened, two-tweeter crossover and relay mute added. Items under "Open decisions" are not requirements until decided.

## Purpose

A stereo Bluetooth speaker in a wooden box. A mirror box on top has addressable LEDs along its 12 inside edges. An ESP32 shows a level meter (bar mode) or a spectrum (FFT mode) from the audio, and uses an accelerometer to reorient the display when the box stands on its end. Personal-use DIY build.

Bluetooth reception and amplification are done by an off-the-shelf amp board. The ESP32 does not handle Bluetooth audio.

## Hardware

| Part | Model | Role |
|---|---|---|
| MCU | ESP32 dev board, classic ESP32, no PSRAM | Meter, LEDs, orientation, buttons |
| Amp + Bluetooth | XH-M548 (TPA3116D2, Bluetooth 4.0) | A2DP sink, speaker drive |
| Tweeters | 2, one per channel | Passive crossover off the amp's speaker outputs (see Audio path) |
| Mute relay | 4-channel 5 V relay module, active-low inputs, no optocouplers | Breaks each speaker line (2 of 4 used) |
| LED strip | WS2812B, 50 LEDs/m, 112 LEDs used | Mirror-box edges |
| Level shifter | SN74AHCT125N | 3.3 V to 5 V LED data (buffer 1), mute relay drive (buffers 2 and 3) |
| Accelerometer | GY-45 (MMA845x), I2C 0x1C or 0x1D | Orientation |
| Buttons | 4 panel momentary, normally open | Controls |
| Supply | 19.5 V, 2.31 A adapter | Main rail |
| Logic buck | MP1584, 5.00 to 5.05 V | ESP32 |
| LED buck | XL4015, 5.00 to 5.05 V | LED rail, AHCT125, relay module |

### ESP32 pin map

| GPIO | Signal | State |
|---|---|---|
| 36 (ADC1) | L audio tap | decided |
| 39 (ADC1) | R audio tap | decided |
| 21 | I2C SDA | decided |
| 22 | I2C SCL | decided |
| 23 | Accelerometer INT1 (optional), next to the GY-45 | decided |
| 16 | LED data to AHCT125 pin 2 | decided |
| 27, 26, 25, 33 | Buttons 1 to 4, INPUT_PULLUP, contiguous on one header row | decided |
| 4 | Mute (AHCT125 buffers 2 and 3, 10 k pull-up to 3.3 V): LOW = sound on, HIGH or floating = muted | decided |
| 18, 19, 17 | Amp key outputs 1 to 3 via optocouplers | proposed |
| 34 (input only) | Amp Bluetooth LED sense (LED, 10 k, 1N4148 to input); sense point on the amp still open | proposed |

Pins kept free: EN, TX0 and RX0 (USB serial), GPIO 5, 2, 12 and 15 (strapping), GPIO 6 to 11 (flash), GPIO 32 and 35 (spare, left as a gap between the buttons and the audio taps), GPIO 13 and 14.

The ESP32 radio is not used: no Wi-Fi, and Bluetooth stays with the amp board. Firmware leaves the radio off.

Header-row partition (devkit with USB at the left, so the top row reads VIN, GND, 13, 12, 14, 27, 26, 25, 33, 32, 35, 34, VN, VP, EN and the bottom row reads 3V3, GND, 15, 2, 4, 16, 17, 5, 18, 19, 21, RX0, TX0, 22, 23). Top row: power in at the left, buttons in the middle, audio and LED sense at the right. Bottom row: mute and LED data at the left (next to the AHCT125), amp keys in the middle (next to the optocouplers), I2C and INT at the right (next to the GY-45).

### LED chain (112 LEDs, one data line)

Index ranges in wiring order, zero-based. Corners: bottom E F G H, top I J K L.

| Seg | Edge | LEDs | Index range |
|---|---|---|---|
| 1 | F to G | 20 | 0 to 19 |
| 2 | G to K (spur) | 3 | 20 to 22 |
| 3 | G to H | 5 | 23 to 27 |
| 4 | H to L (spur) | 3 | 28 to 30 |
| 5 | H to E | 20 | 31 to 50 |
| 6 | E to I (spur) | 3 | 51 to 53 |
| 7 | E to F | 5 | 54 to 58 |
| 8 | F to J | 3 | 59 to 61 |
| 9 | J to I | 5 | 62 to 66 |
| 10 | I to L | 20 | 67 to 86 |
| 11 | L to K | 5 | 87 to 91 |
| 12 | K to J | 20 | 92 to 111 |

Index ranges are derived from the segment lengths and are the single source of truth for host tests.

### Audio path

Per channel, from the amp's speaker output, through the mute relay:

```
Amp L+ --+------------------------------- Woofer +
         +-- 1.1 uF film -- 10 ohm 5 W -- Tweeter - (tweeter polarity reversed)
Amp L- --+-- Woofer - ------------------- Tweeter +
```

- Both tweeters sit after the relay, so they mute with their channel. Each relay switches one wire per channel on COM and NO.
- Tweeter branch: 10 ohm 5 W plus 1.1 uF film (two 2.2 uF 400 V film capacitors in series, on hand) gives about -10 dB, crossing at about 10 kHz, with the amp load staying near 4 ohm. Chosen by bench listening: 5 ohm was too loud, 10 ohm plus 2.35 uF was shrill on "s" sounds, 20 ohm only dropped the crossover to about 2.8 kHz. Reversing the tweeter polarity helped. Polarised capacitors are not used.
- Woofers run full range with no coil. A 4 kHz roll-off would leave a hole between 4 and 9 kHz. If the woofer top end is harsh in the box, try about 0.07 to 0.1 mH.
- The earlier tweeter amp, L+R mix and trimmer are dropped. Nothing is tapped from the amp board for a tweeter feed.

### VU audio tap

Decided: tap the speaker outputs on the amp side of the relay, no soldering on the amp board. One per channel:

```
Amp L+ terminal -- 100 nF -- 100 k --+-- GPIO36 (L) / GPIO39 (R)
                     3.3 V -- 22 k --+
                       GND -- 22 k --+
                       GND -- 1 nF --+
```

- Bias is 1.65 V from a separate 22 k / 22 k pair per channel; the node is not shared between channels.
- Each output leg sits at about 9.5 V DC and carries half the speaker signal, so about 1/10 at the pin gives roughly 0.95 V peak at full volume, inside the ADC range. Firmware auto-scales.
- High-cut about 16 kHz (100 k in parallel with 11 k, with 1 nF), low-cut about 14 Hz.
- The 100 nF capacitor sees about 8 V DC plus up to 9.5 V of audio: ceramic, 25 V or more.
- The ESP32 ground shares the star ground with the amp. Never tie the tap's ground to a speaker leg (the outputs are bridge-tied).
- To confirm on the bench: the pin sits about 1.65 V DC at idle.

### Key presses into the amp

PC827 (dual) and PC817 (single) optocouplers in sockets, no power pin. Per channel: GPIO to 1 k to the LED anode, cathode to GND; collector to the button's higher-voltage pad and emitter to the lower pad, in parallel with the on-board button.

| Channel | Optocoupler pins (A, K, C, E) | Button |
|---|---|---|
| 1 (GPIO18) | PC827 3, 4, 6, 5 | Play/pause |
| 2 (GPIO19) | PC817 1, 2, 4, 3 | Volume-/previous |
| 3 (GPIO17) | PC827 1, 2, 8, 7 | Volume+/next |

The device-to-channel mapping follows the header order on the control board (GPIO17, 18 and 19 sit side by side, so the dual part takes 17 and 18 and the single part takes 19); the GPIO to button function is unchanged.

A tap gives a short pulse for next and previous; a hold gives timed volume steps, capped below maximum volume (where the amp beeps and skips a track). Measure the amp's key-pad voltages, powered, before wiring to identify the ground side of each button.

### Mute drive

| Buffer | OE | Input | Output | To |
|---|---|---|---|---|
| 1 | pin 1 to GND | pin 2 | pin 3 | LED data |
| 2 | pin 4 to GND | pin 5 | pin 6 | relay IN1 (left) |
| 3 | pin 10 to GND | pin 9 | pin 8 | relay IN2 (right) |
| 4 | pin 13 to 5 V | pin 12 to GND | none | unused |

Inputs 5 and 9 join to GPIO4 with a 10 k pull-up to 3.3 V so the relays stay off while the ESP32 boots. Relay module VCC from the LED buck, common ground. Relay IN pulled low switches the relay on (active-low, bench-checked: no clicks at power-on with inputs floating).

## Boards

No custom PCB. One existing perf board and one new perf board carry the discrete parts; everything else is an off-the-shelf module. A custom board for B is only worth it after the open decisions on audio feed, amp keys and LED sense are closed, or if a second unit is wanted.

| Board | Contents | Build |
|---|---|---|
| A Power | DC jack, rocker switch, fuse, SR560, TVS, bulk and bypass caps, MP1584, XL4015, star ground. Outputs: 19.5 V, 5 V logic, 5 V LED | Existing perf board, unchanged |
| B Control | ESP32 devkit on a socket, 1N5819 Schottky on VIN with bulk and bypass caps ahead of it, AHCT125 with 100 nF, 330 ohm data resistor next to the strip terminal, mute pull-up, Bluetooth LED sense, VU tap parts for L and R, PC827 and PC817 key optocouplers with 1 k series resistors, connectors | New perf board, same outline as A: 97.8 x 59.8 mm, mounting holes 3 mm at 75 x 54.7 mm centres. Landscape, ESP32 USB end at the left. Edge connectors: 5.08 mm screw terminals for the two 5 V inputs and strip data (left edge), JST-XH for the relay module (left), panel buttons (top) and amp tap (top right), a 1x6 header for the key outputs (bottom). Layout, wiring list, BOM and the KiCad perfboard footprint and placement in `hardware/control-board/` |
| C Amp | XH-M548 | Off the shelf |
| D Relay | 4-channel module, 2 channels used | Off the shelf, mounted beside the amp speaker terminals |
| E Accelerometer | GY-45 | Off the shelf, fixed rigidly to the box on a short lead |
| LED strip | WS2812B, 112 LEDs | Powered directly from A, not through B |

Placement reasons: D switches speaker wires so it sits by the amp outputs, not by the 19 V rail. B holds every open circuit decision, which perf lets change freely. A stays separate so stages 1 to 3 run without B.

### Interconnects

Keyed connectors (JST-XH or screw terminals) between boards so each stage can be unplugged. Heavy wire is 20 AWG or thicker.

| From | To | Signals | Notes |
|---|---|---|---|
| A | C | 19.5 V, GND | 5.5x2.1 plug lead from the fused rail |
| A | B | 5 V logic, GND | To ESP32 VIN through a 1N5819 Schottky (D2, band toward VIN), with 100 uF and 100 nF across the logic input ahead of the diode (C1, C2). The diode blocks back-feed, so the wire can stay connected while the ESP32 is on USB |
| A | B | 5 V LED, GND | AHCT125 supply and pass-through to D |
| A | LED strip | 5 V LED, GND | Heavy wire, 1000 uF at the strip input. Never through B |
| B | LED strip | Data | Via AHCT125 buffer 1 and 330 ohm at the strip end |
| B | D | 5 V, GND, IN1, IN2 | Four wires |
| C | B | Audio L, audio R, ground | Per the VU audio feed decision |
| C | B | Bluetooth LED sense | Via 10 k and 1N4148 |
| B | C | Key lines | Optocoupler collector and emitter per channel (six wires), after pad voltages are measured |
| C | D | Speaker L, speaker R | Through the relay contacts to crossovers and drivers |
| B | E | 3.3 V to VCC-IN, GND, SDA, SCL, INT1 (GPIO23) | Short (under 30 cm), shielded from LED data if possible. SA0, INT2 and the board's 3.3 V pin stay unconnected. Address 0x1D or 0x1C, WHO_AM_I 0x2A |
| Panel | B | Buttons 1 to 4, GND | INPUT_PULLUP |

### Layout rules

1. One star ground at the 1000 uF negative leg on A. LED return current (up to 2 A) runs from the XL4015 straight to the strip and never through B. B returns a thin signal-ground wire to the star.
2. Keep the XL4015 and the amp heatsink away from the ESP32 and the sense parts.
3. Keep audio conditioning on B away from the 5 V LED feed and the LED data wire.
4. AHCT125 sits next to the ESP32. The 330 ohm sits at the strip end of the data wire.
5. Relay coil supply and the LED strip share the LED rail; the relay contacts carry only speaker signals.
6. Pin assignments follow the placement (see Header-row partition under the ESP32 pin map): each signal uses the header pin nearest its part, so no wire crosses the module. The audio bias network sits at VP and VN, the AHCT125 near GPIO4 and 16, the optocouplers near 17 to 19, the GY-45 near 21 to 23.

## Requirements

Tiers: **host** runs on a PC in CI, **target** needs a flashed board, **bench** needs board plus instruments, **hand** is a manual measurement.
Provenance: [owner] stated by the owner, [derived] computed from owner statements.

### Display and orientation

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| R-001 | Orientations are O1 (landscape) and O2 (portrait). Each has one stored gravity vector. [owner] | Classifier unit test with two stored vectors | host | green@62cb8a0 |
| R-002 | A smoothed gravity vector within 25 degrees of a stored vector classifies as the nearest such orientation. [owner, nearest derived] | Test vectors at 0, 24, 26 degrees from each stored vector | host | green@62cb8a0 |
| R-003 | A vector more than 25 degrees from every stored vector leaves the active layout unchanged. [owner] | Test vector at 90 degrees from both | host | green@62cb8a0 |
| R-004 | The layout switches only after the new classification has held for 1.0 s, and not before. [owner] | Time-stepped test: held 0.9 s gives no switch, 1.0 s gives switch | host | green@62cb8a0 |
| R-005 | A button 4 press of 3 s or longer stores the current smoothed gravity vector to non-volatile storage. [owner] | Button simulator plus storage fake | host | todo |
| R-006 | Stored orientation vectors survive a reboot. [owner] | Teach, reset, read back and compare | target | todo |
| R-007 | On boot the accelerometer WHO_AM_I register (0x0D) is read and accepted only if 0x1A, 0x2A or 0x3A. [owner] | Serial output shows the value read | target | todo |

### LED mapping

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| R-010 | In O1, the L bar fills segment 10 from index 67 upward and the R bar fills segment 5 from index 50 downward. [owner, derived] | Mapper test: level n lights exactly the expected indices | host | green@62cb8a0 |
| R-011 | In O2, the L bar fills segment 5 from index 31 upward and the R bar fills segment 10 from index 86 downward. [owner, derived] | Same | host | green@62cb8a0 |
| R-012 | A bar of level 0.0 lights no LED and 1.0 lights all 20 LEDs of its segment. [derived] | Mapper test at 0.0 and 1.0 | host | green@62cb8a0 |
| R-013 | The strip is initialised with 112 LEDs, GRB order, data on GPIO16. [owner] | Startup sweep shows R, G, B across all 112 | target | todo |

### Controls

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| R-020 | A press released in under 400 ms is a tap; a press held 400 ms or longer is a hold. [owner] | Button classifier test at 399 ms and 400 ms | host | green@62cb8a0 |
| R-021 | A button 4 press shorter than 3 s advances to the next display pattern and wraps after the last. [owner] | Pattern-cycle test | host | green@62cb8a0 |
| R-022 | The selectable pattern list, in order, is: VU bar, peak bar, zone bar, gravity dot, standby. Spectrum styles join in a later batch. [owner] | Pattern table test | host | green@15d1196 |

### Display styles (first batch)

All numbers live in one configuration header so they can be retuned by eye. Tests check behaviour against those constants.

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| R-040 | Level scale: amplitude 1.0 maps to 1.0 and amplitude 0.01 (-40 dB) maps to 0.0, linear in dB between, clamped to 0..1. [owner] | Scale test at 1.0, 0.1, 0.01, 0.0 | host | green@63a6b58 |
| R-041 | VU bar: the displayed level reaches 99 % of a step input in 300 ms (rise) and falls to 1 % in 300 ms. [owner] | Time-stepped smoother test | host | green@63a6b58 |
| R-042 | VU bar lights, for each channel, exactly lit_count(level) LEDs of that channel's bar in the active orientation and no others. [derived] | Render test at 0, 0.5, 1.0 | host | green@63a6b58 |
| R-043 | Peak bar: displayed level jumps to a higher input on the next frame. [owner] | Frame-stepped test | host | green@f1b71db |
| R-044 | Peak bar: with zero input the displayed level falls from full scale to zero in 1.0 s, linearly. [owner] | Time-stepped test | host | green@f1b71db |
| R-045 | Peak bar: a peak-hold LED stays at the highest recent level for 600 ms, then falls with the bar. [owner] | Time-stepped test | host | green@f1b71db |
| R-046 | Gravity dot: rises instantly to a higher input, then falls with constant acceleration so that full scale takes 1.2 s from rest. [owner] | Time-stepped test | host | green@15d1196 |
| R-047 | Zone bar: LEDs 0-13 of a bar are green, 14-17 yellow, 18-19 red. [owner, indices derived] | Colour test per index | host | green@a2612cb |
| R-048 | Standby: after 5 s with input below the noise floor, the display shows a slow rainbow; any input above the floor returns to the selected style. [owner] | Time-stepped state test | host | green@15d1196 |
| R-050 | Gravity dot leaves a fading tail: LEDs the dot has passed fade with a 120 ms time constant, and the dot itself is at full brightness. [owner, constant derived] | Trail decay test | host | green@15d1196 |
| R-051 | A synthetic stereo audio source (120 bpm kick, slow swells) can drive every style with levels in 0..1, so styles can be judged without the amp board. [derived] | Range and beat test; demo build | host | green@15d1196 |
| R-049 | The display updates at 60 frames per second. [owner] | Frame counter over 10 s on serial | target | todo |

### Power and LED current

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| R-030 | With the LED cap enabled, measured strip current at full white does not exceed 2.2 A. [owner, tolerance derived] | Meter in series on LED feed | hand | todo |
| R-031 | The LED cap is enabled at boot and a status command reports cap state. [owner] | Serial status output | target | todo |

### Mute

The amp board plays Chinese voice prompts that cannot be disabled, so the speaker lines are muted around them. Prompt timings measured from video at 10 fps, plus or minus 0.1 s: power-on prompt at +1.6 s (0.5 s long) after a thump at +0.2 s; connect prompt about 1.4 s long, starting 0.3 to 0.7 s after the last off-blink; disconnect prompt about 0.5 s long, starting about 0.2 s before blinking resumes. Bluetooth LED: pairing is mostly on with a 0.2 s off-blink every 0.8 s, connected is solid.

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| M-001 | On boot, and while the ESP32 is resetting, the speakers are muted (GPIO4 high or floating). [owner] | Scope or meter on relay inputs through a reset | bench | todo |
| M-002 | Sound is enabled (GPIO4 low) only after the Bluetooth LED has been solid for 2.5 s. [owner] | Time-stepped state test on a fake LED input | host | todo |
| M-003 | Any off-blink of the Bluetooth LED mutes immediately. [owner] | Same | host | todo |
| M-004 | The power-on thump and prompt and the connect prompt are inaudible on the speakers. [owner] | Listen on three power-ups and three connects | hand | todo |

## Bring-up sketch (LED load test)

A separate small firmware, serial 115200, single-character commands. It exists to prove the LED supply and data path before the main firmware.

| Key | Action |
|---|---|
| 0 to 9 | White at 0 to 90 % |
| f | White at 100 % |
| r, g, b | Solid red, green, blue |
| w | White |
| x | Rainbow chase |
| p | Walk one lit pixel along the strip, print its index |
| o | All off |
| c | Toggle power cap, warn when off |
| s | Print status |

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| B-001 | On boot, the strip shows red, green, blue, then off. [owner] | Visual or camera check | hand | todo |
| B-002 | Each command above produces the described state and a status line. [owner] | Serial command parser test | host | green@62cb8a0 |
| B-003 | Unknown characters are ignored. [derived] | Parser test | host | green@62cb8a0 |

## Hand checks (power chain and boards)

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| H-001 | With no load, each buck reads 5.00 to 5.05 V. [owner] | Meter | hand | todo |
| H-002 | At 0.5 A on each buck, output is 4.95 V or more and the main rail is 18.9 V or more. [owner] | Meter and 10 ohm loads | hand | todo |
| H-003 | At 1 A for 5 min, each buck stays at 4.90 V or more and is touchable for 5 s. [owner] | Meter, touch | hand | todo |
| H-004 | At the 2 A LED cap, XL4015 output is 4.85 V or more, strip far end is 4.6 V or more, main rail is 18.5 V or more, and the adapter does not cut out. [owner] | Meter during `f` step | hand | todo |
| H-005 | Output ripple is under 0.05 V AC under load. [owner] | Meter on ACV 20 | hand | todo |
| H-006 | With supply polarity reversed the rail reads 0 V and nothing is damaged. [owner] | Meter | hand | todo |
| H-007 | Each of the five patterns looks acceptable on the finished mirror box using the demo build, and colours, tail length and peak-hold look right. [owner] | Visual check, notes recorded in the spec | hand | todo |

## Open decisions

Ordered by how much they block.

1. **LED cap method.** The existing bring-up sketch applies a hand-written cap because the library limiter "did not hold" on an earlier build, and notes real current of 1.8 to 2.2 times the modelled value. R-030 is therefore stated as a measured current, not a library setting.
2. **Amp board key type.** The board is in hand. The three keys may be a resistor ladder (three different resistor values). Pad voltages are to be measured before the optocouplers are wired (circuit is decided, see Key presses into the amp).
3. **VU audio feed** is decided: speaker-output tap, see VU audio tap. Open: verify the bias and level at the pin on the bench.
4. **Auto-scale method.** Ballistics are decided (R-041 to R-046). The gain-follow and noise-gate algorithm is still to be specified.
5. **Spectrum.** FFT size, window, 32 band edges, and layout across LEDs.
6. **Noise floor value** for standby (R-048). Placeholder 0.05 normalised level (about -38 dB) until measured with real audio.
7. **Fault behaviour.** Bluetooth disconnect, LED strip failure, accelerometer missing or wrong ID.
8. **Orientation teach.** How O1 and O2 are chosen, and confirmation feedback.
9. **"Stable" definition** for the gravity vector (threshold on change per second).
10. **Mute behaviour.** Rule is set (M-002, M-003). Open: the sense point on the amp board (the ESP32 pin is GPIO34), and the disconnect prompt, which the LED rule cannot catch (an idle mute could).
11. **Libraries.** FastLED version, FFT library, accelerometer access (plain I2C registers likely).
12. **Back-edge segments** (1 and 12) mirroring the bars.
13. **Persistence of the selected pattern.**
14. **Diagnostics** (current and temperature sensors), proposed only.
15. **Bluetooth device name.**
16. **Second tweeter mounting.** The box is pre-cut for one centre tweeter. Stack both in the centre bay, or one per woofer chamber (only if the tweeter backs are sealed). Tweeter power rating also to be confirmed.
17. **Amp supply polarity.** Centre pin of the amp's DC jack is expected to be positive; continuity to the input diode to be confirmed before powering from the rail.
| H-008 | Board A alone: with B, C and D unplugged, 19.5 V rail, 5 V logic and 5 V LED read within H-001 limits. [derived] | Meter | hand | todo |
| H-009 | Ground continuity: B ground to the star point and strip ground to the XL4015 negative are under 0.5 ohm, and no LED return current flows in B's ground wire at full white. [derived] | Meter, current clamp or series meter | hand | todo |
| H-010 | Board B with the ESP32 on USB and the 5 V logic wire connected: D2 (1N5819) is reverse biased, the MP1584 output reads unchanged, and no current flows back into A. [owner] | Meter on the logic rail with USB plugged, then with the rail powered | hand | todo |
| H-011 | Board D: with GPIO4 floating or high both relays are off; with it low both are on and the contacts pass speaker signal. [owner] | Listen, meter on contacts | hand | todo |
| H-012 | Each interconnect in the table is continuity-checked end to end and its connector cannot be plugged in reversed. [derived] | Meter, visual | hand | todo |
