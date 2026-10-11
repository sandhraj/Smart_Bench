#include "orientation.h"
#include <math.h>

namespace vu {

float angle_deg(const Vec3& a, const Vec3& b) {
  const float na = sqrtf(a.x * a.x + a.y * a.y + a.z * a.z);
  const float nb = sqrtf(b.x * b.x + b.y * b.y + b.z * b.z);
  if (na == 0.0f || nb == 0.0f) return 180.0f;
  float c = (a.x * b.x + a.y * b.y + a.z * b.z) / (na * nb);
  if (c > 1.0f) c = 1.0f;
  if (c < -1.0f) c = -1.0f;
  return acosf(c) * 57.29577951f;
}

int classify(const Vec3& v, const Vec3* stored, int n, float max_deg) {
  int best = -1;
  float best_deg = max_deg;
  for (int i = 0; i < n; ++i) {
    const float d = angle_deg(v, stored[i]);
    if (d <= best_deg) {
      best_deg = d;
      best = i;
    }
  }
  return best;
}

OrientationTracker::OrientationTracker()
    : stored_{{0, 0, 0}, {0, 0, 0}}, count_(0), active_(-1), candidate_(-1), candidate_since_(0) {}

void OrientationTracker::set_stored(int index, const Vec3& v) {
  if (index < 0 || index >= kMaxStored) return;
  stored_[index] = v;
  if (index + 1 > count_) count_ = index + 1;
}

int OrientationTracker::update(const Vec3& v, uint32_t now_ms) {
  const int c = classify(v, stored_, count_);
  if (c < 0 || c == active_) {
    candidate_ = -1;           // no match, or already showing it: nothing pending
  } else if (c != candidate_) {
    candidate_ = c;            // new candidate, start the hold timer
    candidate_since_ = now_ms;
  } else if (now_ms - candidate_since_ >= kHoldMs) {
    active_ = c;
    candidate_ = -1;
  }
  return active_;
}

}  // namespace vu
