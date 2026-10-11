// Orientation classification and 1 s hysteresis. Pure logic, no Arduino.
// Input vectors are already smoothed; smoothing is not part of this module.
#pragma once
#include <stdint.h>

namespace vu {

struct Vec3 {
  float x, y, z;
};

constexpr float kMaxMatchDeg = 25.0f;
constexpr uint32_t kHoldMs = 1000;
constexpr int kMaxStored = 2;

// Angle between two vectors in degrees. A zero-length vector returns 180.
float angle_deg(const Vec3& a, const Vec3& b);

// Index of the nearest stored vector within max_deg, or -1 if none is within range.
int classify(const Vec3& v, const Vec3* stored, int n, float max_deg = kMaxMatchDeg);

class OrientationTracker {
 public:
  OrientationTracker();
  void set_stored(int index, const Vec3& v);   // index 0..kMaxStored-1
  int stored_count() const { return count_; }
  // Feed a smoothed vector at time now_ms. Returns the active orientation index, or -1 if
  // none has been established yet (callers show a default layout).
  int update(const Vec3& v, uint32_t now_ms);
  int active() const { return active_; }

 private:
  Vec3 stored_[kMaxStored];
  int count_;
  int active_;
  int candidate_;
  uint32_t candidate_since_;
};

}  // namespace vu
