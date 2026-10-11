// Synthetic stereo audio levels for demos and tests. Pure logic, no Arduino.
#pragma once
#include "style.h"

namespace vu {

class SynthAudio {
 public:
  SynthAudio();
  void set_enabled(bool on) { enabled_ = on; }
  bool enabled() const { return enabled_; }
  AudioFrame next(float dt_ms);

 private:
  bool enabled_;
  float t_ms_;
  float kick_ms_;
};

}  // namespace vu
