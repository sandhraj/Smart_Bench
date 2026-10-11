// Level ballistics. Pure logic, no Arduino. dt is in milliseconds.
#pragma once

namespace vu {

// Exponential smoothing with separate rise and fall times, each given as the
// time to cover 99 % of a step.
class Smoother {
 public:
  Smoother(float rise_ms99, float fall_ms99);
  float step(float target, float dt_ms);
  float value() const { return value_; }
  void reset(float v = 0.0f) { value_ = v; }

 private:
  float tau_rise_ms_;
  float tau_fall_ms_;
  float value_;
};

}  // namespace vu
