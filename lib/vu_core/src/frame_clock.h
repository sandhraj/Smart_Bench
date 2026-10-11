// Frame pacing. Pure logic, microsecond timestamps.
#pragma once
#include <stdint.h>

namespace vu {

class FrameClock {
 public:
  explicit FrameClock(float hz);
  // True when a frame is due at now_us. Keeps the cadence; resyncs after a long stall.
  bool due(uint32_t now_us);

 private:
  uint32_t period_us_;
  uint32_t next_us_;
  bool started_;
};

}  // namespace vu
