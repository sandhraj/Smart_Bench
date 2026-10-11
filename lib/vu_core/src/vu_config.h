// All tunable display numbers in one place. Change here, not in the logic.
// Values come from docs/SPEC.md (R-040..R-049).
#pragma once
#include <stdint.h>

namespace vu {

struct Rgb {
  uint8_t r, g, b;
};

constexpr Rgb kBlack = {0, 0, 0};

constexpr float kFrameHz = 60.0f;
constexpr float kDbRange = 40.0f;          // amplitude 1.0 = 0 dB, floor at -kDbRange

constexpr float kVuRiseMs99 = 300.0f;      // time to reach 99 % of a step
constexpr float kVuFallMs99 = 300.0f;      // time to fall to 1 %

constexpr float kPeakFallFullScaleMs = 1000.0f;
constexpr float kPeakHoldMs = 600.0f;
constexpr float kGravityFullScaleMs = 1200.0f;  // fall from 1.0 to 0 starting at rest
constexpr float kGravityTailTauMs = 120.0f;     // tail fade time constant
constexpr Rgb kGravityDotColor = {255, 255, 255};

// Standby (no audio). The noise floor is a tunable default, see SPEC open decisions.
constexpr float kNoiseFloor = 0.05f;            // normalised level, about -38 dB
constexpr float kStandbyAfterMs = 5000.0f;
constexpr float kStandbyPeriodMs = 20000.0f;    // one full rainbow cycle
constexpr uint8_t kStandbyValue = 64;           // dim, to save current

constexpr Rgb kVuBarColor = {0, 160, 255};  // colour mapping is still a design choice; tune by eye
constexpr Rgb kPeakHoldColor = {255, 255, 255};

// Zone bar: LED position k within a bar (0 = start, 19 = end).
constexpr int kZoneYellowFrom = 14;   // 70 % of 20
constexpr int kZoneRedFrom = 18;      // 90 % of 20
constexpr Rgb kZoneGreen = {0, 200, 0};
constexpr Rgb kZoneYellow = {255, 170, 0};
constexpr Rgb kZoneRed = {255, 0, 0};

}  // namespace vu
