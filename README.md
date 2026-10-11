# Smart_Bench

AI closed-loop firmware development on ESP32. The agent writes firmware, CI builds it,
a Raspberry Pi testbench flashes and tests it, and the agent fixes failures until the
tests pass. Built on the method from
[Embedded-AI-Harness](https://github.com/SensorsIot/Embedded-AI-Harness) (MIT),
trimmed down to what a hobby project needs.

## Skills (`.claude/skills/`)

| Skill | Purpose |
|---|---|
| `grill-me` | Interview to settle what to build |
| `spec` | Write and amend `docs/SPEC.md`: requirements, each with how it is proven |
| `loop` | Test first, code, CI build, flash, test, fix, repeat |
| `setup-action` | GitHub Actions build for ESP-IDF firmware |
| `esp-idf-handling`, `esp-pio-handling` | Build, flash and monitor reference (ESP-IDF or PlatformIO) |
| `testbench-install`, `testbench-logging` | Set up the Pi bench; read serial and UDP logs |

The full upstream skill set (define, harness, commission, build, wifi, mqtt, ble, debug, sdr,
siggen) is kept unchanged in `vendor/embedded-ai-harness-full/` for when a broader harness is needed.

## Stages

| Stage | Needs | Result |
|---|---|---|
| 1 · Spec + CI | GitHub only | `docs/SPEC.md`, host tests, firmware builds in CI, loop runs at level A |
| 2 · Testbench | Raspberry Pi + one ESP32 board on USB | Loop flashes and tests on real hardware (level B) |
| 3 · Grow | sensors, LED strips, second board | Wi-Fi/MQTT fault tests, simulators, regression on every push |

## Hardware on hand

ESP32 camera boards, temperature/humidity sensors, LED strips, starter kit, one Raspberry Pi.
Product: decided with `/grill-me`.

## Licence

Project code: to be decided. Vendored upstream material is MIT, see
`vendor/embedded-ai-harness-full/docs/LICENSE`.
