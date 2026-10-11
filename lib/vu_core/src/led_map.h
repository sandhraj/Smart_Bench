// LED index mapping for the 112-LED mirror-box chain. Pure logic, no Arduino.
// Wiring order, zero-based: seg5 = 31..50 (H->E), seg10 = 67..86 (I->L). See docs/SPEC.md.
#pragma once

namespace vu {

constexpr int kNumLeds = 112;
constexpr int kBarLeds = 20;

enum Orientation { O1 = 0, O2 = 1 };
enum Channel { LEFT = 0, RIGHT = 1 };

// LED index of the k-th LED (0 = bar start, 19 = bar end) of a channel's bar.
// Returns -1 if k is outside 0..kBarLeds-1.
int bar_index(Orientation o, Channel c, int k);

// Number of LEDs lit for a level; level is clamped to 0.0..1.0 and rounded to nearest.
int lit_count(float level);

}  // namespace vu
