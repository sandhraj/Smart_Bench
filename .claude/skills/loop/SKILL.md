---
name: loop
description: >
  Drive the closed development loop: pick the next requirement from
  docs/SPEC.md, write its test, write the code, build in CI, flash and test on
  the bench when one exists, fix failures, repeat until green. Use when the
  user says build, continue, run the loop, what's next, where are we, or after
  the spec changes. Replaces upstream /build and /commission.
---

# Loop: spec to silicon

Inputs: `docs/SPEC.md`. State lives in its Status column and in git. Say where the project stands before doing anything else: counts of todo, red, green, and the next requirement.

## Capability levels

Detect which one applies and say so. Never pretend a higher level.

| Level | Available | The loop can |
|-------|-----------|--------------|
| A | repo + GitHub Actions | write code and tests, run host tests and the firmware build in CI |
| B | A + bench Pi with a board in a slot | also flash the CI artifact and run target and bench tests |

Level B check: `curl -s $TESTBENCH_URL/api/devices` answers and a slot shows the expected board. `TESTBENCH_URL` and the bench IP are recorded in `docs/BENCH.md`. Use the `esp-idf-handling` and `testbench-logging` skills for the API calls.

## One iteration

1. **Pick** the lowest-tier `todo` or `red` requirement.
2. **Test first.** Write the test for its "Verified by" and watch it fail. Host tests in `tests/host/`, target and bench tests in `tests/bench/`.
3. **Code.** Smallest change that satisfies this one requirement. Touch nothing the spec does not cover.
4. **Push** to a branch or main. Watch CI: `gh run watch`. Host tests and the build both must pass.
5. **Level B only:** `gh run download` the artifact, flash it with `POST /api/flash`, run the tests that need hardware. Start every run with `POST /api/bench/reset`. Flash only the CI artifact, never a local binary.
6. **Read the evidence.** Serial output and `GET /api/udplog` for what the device did, CI log for what the build did.
7. **Green:** set Status to `green@<commit>`. **Red:** fix the code and go to 3.

## Commissioning (once per board or peripheral, Level B)

Prove the setup before blaming the code. Record results in `docs/BENCH.md`.

1. Board appears in a slot and reports the expected chip.
2. A minimal known-good image flashes and prints its boot marker.
3. Each wired peripheral answers a trivial read (sensor value, LED lights, camera frame).
4. Reset works from the bench without anyone touching the board.

If a later test fails and one of these would also fail, fix the setup, not the firmware.

## Rules

- No code without a requirement. If the work is not in SPEC.md, run `/spec` first.
- Never weaken, skip or delete a test to make it pass. If the test is wrong, amend the spec and say so.
- After 5 failed iterations on one requirement, stop and report what was tried and what the evidence shows.
- If the spec is ambiguous or a number is missing, ask. Do not guess thresholds.
- Never run destructive actions on the bench (erase, eFuse) without explicit approval.
- Report plainly: what is green, what is red, what is blocked by missing hardware.
