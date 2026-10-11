#include "ballistics.h"
#include <math.h>

namespace vu {

static const float kLn100 = 4.605170186f;

Smoother::Smoother(float rise_ms99, float fall_ms99)
    : tau_rise_ms_(rise_ms99 / kLn100), tau_fall_ms_(fall_ms99 / kLn100), value_(0.0f) {}

float Smoother::step(float target, float dt_ms) {
  const float tau = (target > value_) ? tau_rise_ms_ : tau_fall_ms_;
  if (tau <= 0.0f) {
    value_ = target;
  } else {
    const float a = 1.0f - expf(-dt_ms / tau);
    value_ += (target - value_) * a;
  }
  return value_;
}

}  // namespace vu
