#include "synth_audio.h"
#include <math.h>

namespace vu {

static float clamp01(float v) { return v < 0.0f ? 0.0f : (v > 1.0f ? 1.0f : v); }

SynthAudio::SynthAudio() : enabled_(true), t_ms_(0.0f), kick_ms_(0.0f) {}

AudioFrame SynthAudio::next(float dt_ms) {
  t_ms_ += dt_ms;
  kick_ms_ += dt_ms;
  if (kick_ms_ >= 500.0f) kick_ms_ -= 500.0f;  // 120 bpm
  if (!enabled_) return {{0.0f, 0.0f}};
  const float two_pi = 6.2831853f;
  const float kick = expf(-kick_ms_ / 120.0f);
  const float base_l = 0.35f + 0.15f * sinf(two_pi * t_ms_ / 4000.0f);
  const float base_r = 0.30f + 0.15f * sinf(two_pi * t_ms_ / 3000.0f + 1.0f);
  return {{clamp01(base_l + 0.5f * kick), clamp01(base_r + 0.45f * kick)}};
}

}  // namespace vu
