// All tunable display numbers in one place. Change here, not in the logic.
// Values come from docs/SPEC.md (R-040..R-049).
#pragma once
#include <stdint.h>

namespace vu {

constexpr float kFrameHz = 60.0f;
constexpr float kDbRange = 40.0f;          // amplitude 1.0 = 0 dB, floor at -kDbRange

constexpr float kVuRiseMs99 = 300.0f;      // time to reach 99 % of a step
constexpr float kVuFallMs99 = 300.0f;      // time to fall to 1 %

constexpr float kPeakFallFullScaleMs = 1000.0f;
constexpr float kPeakHoldMs = 600.0f;
constexpr float kGravityFullScaleMs = 1200.0f;  // fall from 1.0 to 0 starting at rest

struct Rgb {
  uint8_t r, g, b;
};

constexpr Rgb kBlack = {0, 0, 0};
constexpr Rgb kVuBarColor = {0, 160, 255};  // colour mapping is still a design choice; tune by eye

}  // namespace vu
