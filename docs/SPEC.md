# Bluetooth VU Meter Speaker

Status: draft 1, written from the owner's handover notes. Items under "Open decisions" are not requirements until decided.

## Purpose

A stereo Bluetooth speaker in a wooden box. A mirror box on top has addressable LEDs along its 12 inside edges. An ESP32 shows a level meter (bar mode) or a spectrum (FFT mode) from the audio, and uses an accelerometer to reorient the display when the box stands on its end. Personal-use DIY build.

Bluetooth reception and amplification are done by an off-the-shelf amp board. The ESP32 does not handle Bluetooth audio.

## Hardware

| Part | Model | Role |
|---|---|---|
| MCU | ESP32 dev board, classic ESP32, no PSRAM | Meter, LEDs, orientation, buttons |
| Amp + Bluetooth | XH-M548 (TPA3116D2, Bluetooth 4.0) | A2DP sink, speaker drive |
| Tweeter amp | PAM8403 module | Drives the centre tweeter from the L+R mix |
| LED strip | WS2812B, 50 LEDs/m, 112 LEDs used | Mirror-box edges |
| Level shifter | SN74AHCT125N | 3.3 V to 5 V LED data |
| Accelerometer | GY-45 (MMA845x), I2C 0x1C or 0x1D | Orientation |
| Buttons | 4 panel momentary, normally open | Controls |
| Supply | 19.5 V, 2.31 A adapter | Main rail |
| Logic buck | MP1584, 5.00 to 5.05 V | ESP32 + PAM8403 |
| LED buck | XL4015, 5.00 to 5.05 V | LED rail |

### ESP32 pin map

| GPIO | Signal | State |
|---|---|---|
| 36 (ADC1) | L audio tap | decided |
| 39 (ADC1) | R audio tap | decided |
| 21 | I2C SDA | decided |
| 22 | I2C SCL | decided |
| 27 | Accelerometer INT1 (optional) | decided |
| 16 | LED data to AHCT125 pin 2 | decided |
| 32, 33, 25, 26 | Buttons 1 to 4, INPUT_PULLUP | proposed |
| 18, 19, 23 | Amp key outputs via optocouplers | proposed |

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
| R-022 | The selectable pattern list, in order, is: VU bar, peak bar, zone bar, gravity dot, standby. Spectrum styles join in a later batch. [owner] | Pattern table test | host | todo |

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
| R-046 | Gravity dot: rises instantly to a higher input, then falls with constant acceleration so that full scale takes 1.2 s from rest. [owner] | Time-stepped test | host | todo |
| R-047 | Zone bar: LEDs 0-13 of a bar are green, 14-17 yellow, 18-19 red. [owner, indices derived] | Colour test per index | host | green@a2612cb |
| R-048 | Standby: after 5 s with input below the noise floor, the display shows a slow rainbow; any input above the floor returns to the selected style. [owner] | Time-stepped state test | host | todo |
| R-049 | The display updates at 60 frames per second. [owner] | Frame counter over 10 s on serial | target | todo |

### Power and LED current

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| R-030 | With the LED cap enabled, measured strip current at full white does not exceed 2.2 A. [owner, tolerance derived] | Meter in series on LED feed | hand | todo |
| R-031 | The LED cap is enabled at boot and a status command reports cap state. [owner] | Serial status output | target | todo |

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

## Hand checks (power chain)

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| H-001 | With no load, each buck reads 5.00 to 5.05 V. [owner] | Meter | hand | todo |
| H-002 | At 0.5 A on each buck, output is 4.95 V or more and the main rail is 18.9 V or more. [owner] | Meter and 10 ohm loads | hand | todo |
| H-003 | At 1 A for 5 min, each buck stays at 4.90 V or more and is touchable for 5 s. [owner] | Meter, touch | hand | todo |
| H-004 | At the 2 A LED cap, XL4015 output is 4.85 V or more, strip far end is 4.6 V or more, main rail is 18.5 V or more, and the adapter does not cut out. [owner] | Meter during `f` step | hand | todo |
| H-005 | Output ripple is under 0.05 V AC under load. [owner] | Meter on ACV 20 | hand | todo |
| H-006 | With supply polarity reversed the rail reads 0 V and nothing is damaged. [owner] | Meter | hand | todo |

## Open decisions

Ordered by how much they block.

1. **LED cap method.** The existing bring-up sketch applies a hand-written cap because the library limiter "did not hold" on an earlier build, and notes real current of 1.8 to 2.2 times the modelled value. R-030 is therefore stated as a measured current, not a library setting.
2. **Amp board key type.** Separate keys, resistor ladder or volume potentiometer. Decides the volume and track control path (optocouplers, digital potentiometer, or parallel buttons). Needs the amp board in hand.
3. **Audio tap location** on the amp board and its mute pin. Needs the amp board.
4. **Auto-scale method.** Ballistics are decided (R-041 to R-046). The gain-follow and noise-gate algorithm is still to be specified.
5. **Spectrum.** FFT size, window, 32 band edges, and layout across LEDs.
6. **Noise floor value** for standby (R-048); the behaviour itself is decided.
7. **Fault behaviour.** Bluetooth disconnect, LED strip failure, accelerometer missing or wrong ID.
8. **Orientation teach.** How O1 and O2 are chosen, and confirmation feedback.
9. **"Stable" definition** for the gravity vector (threshold on change per second).
10. **Mute behaviour.** Release delay at power-on, 2 s re-mute on connect, sense pin.
11. **Libraries.** FastLED version, FFT library, accelerometer access (plain I2C registers likely).
12. **Back-edge segments** (1 and 12) mirroring the bars.
13. **Persistence of the selected pattern.**
14. **Diagnostics** (current and temperature sensors), proposed only.
15. **Bluetooth device name.**
