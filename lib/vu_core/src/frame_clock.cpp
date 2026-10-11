#include "frame_clock.h"

namespace vu {

FrameClock::FrameClock(float hz)
    : period_us_(static_cast<uint32_t>(1000000.0f / hz + 0.5f)), next_us_(0), started_(false) {}

bool FrameClock::due(uint32_t now_us) {
  if (!started_) {
    started_ = true;
    next_us_ = now_us + period_us_;
    return true;
  }
  if (static_cast<int32_t>(now_us - next_us_) < 0) return false;
  next_us_ += period_us_;
  // Stalled for several frames: resync instead of bursting.
  if (static_cast<int32_t>(now_us - next_us_) > static_cast<int32_t>(4 * period_us_)) {
    next_us_ = now_us + period_us_;
  }
  return true;
}

}  // namespace vu
