---
name: spec
description: >
  Write or amend docs/SPEC.md, the single source of truth for what this device
  must do and how each behaviour is proven. Use whenever the user describes a
  device or feature, asks what it should do, wants to add or change behaviour,
  or before any firmware is written. Replaces upstream /define and /harness.
---

# Spec: what "done" means

One file, `docs/SPEC.md`. No firmware is written for behaviour that has no row in it.

## Process

1. No SPEC.md yet: run `/grill-me` on the rough idea first, one question at a time, each with a recommended answer. Then write the file from the decisions.
2. SPEC.md exists: amend the spec first, then hand over to `/loop`. A change is never code first.
3. Commit the spec change on its own, before the code that implements it.

## File layout

```
# <Project>
## Purpose        2-3 sentences
## Hardware       board, sensors, pins, power. Pin numbers are decisions: state them here.
## Interfaces     MQTT topics, HTTP routes, serial output markers, config keys
## Requirements   table below
## Out of scope   things deliberately not done
```

Requirements table:

| ID | Requirement | Verified by | Tier | Status |
|----|-------------|-------------|------|--------|
| R-001 | On boot the device prints `BOOT_OK <version>` on serial within 3 s | serial monitor matches pattern | target | todo |

- **ID**: `R-nnn`, never reused.
- **Requirement**: one obligation. Stimulus, observable response, number (deadline or tolerance). Say what happens on failure.
- **Verified by**: the observation a test makes. If you cannot write this, the requirement is not finished.
- **Tier**: `host` (logic on a PC, no board), `target` (flashed board, serial only), `bench` (board plus Pi: Wi-Fi, MQTT, GPIO), `field` (manual, real environment).
- **Status**: `todo`, `red`, or `green@<short-commit>`. Only `/loop` changes it.

## Quality rules

- Atomic: if it contains "and", split it.
- Falsifiable: no "appropriate", "graceful", "robust", "reasonable", "fast", "user-friendly". Replace with a number or an observable.
- Prefer the cheapest tier that can prove it. Pure logic (parsing, scaling, thresholds, debounce) must be `host`.
- Include negative cases: bad input, sensor missing, Wi-Fi gone, broker down.
- Do not invent thresholds. If a number is missing, ask the user.
