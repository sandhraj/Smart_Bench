#include "style_gravity.h"
#include <math.h>

namespace vu {

StyleGravityDot::StyleGravityDot() { reset(); }

void StyleGravityDot::reset() {
  for (int c = 0; c < 2; ++c) {
    ch_[c].pos = 0.0f;
    ch_[c].vel = 0.0f;
    for (int k = 0; k < kBarLeds; ++k) ch_[c].trail[k] = 0.0f;
  }
}

void StyleGravityDot::update(const AudioFrame& f, float dt_ms) {
  const float dt = dt_ms / 1000.0f;
  const float T = kGravityFullScaleMs / 1000.0f;
  const float g = 2.0f / (T * T);  // full scale in T seconds from rest
  const float decay = expf(-dt_ms / kGravityTailTauMs);
  for (int c = 0; c < 2; ++c) {
    Chan& s = ch_[c];
    const float in = f.level[c];
    if (in >= s.pos) {
      s.pos = in;
      s.vel = 0.0f;
    } else {
      s.vel += g * dt;
      s.pos -= s.vel * dt;
      if (s.pos <= in) {
        s.pos = in;
        s.vel = 0.0f;
      }
    }
    for (int k = 0; k < kBarLeds; ++k) s.trail[k] *= decay;
    const int n = lit_count(s.pos);
    if (n > 0) s.trail[n - 1] = 1.0f;
  }
}

static Rgb scaled(const Rgb& c, float f) {
  return {static_cast<uint8_t>(c.r * f + 0.5f), static_cast<uint8_t>(c.g * f + 0.5f),
          static_cast<uint8_t>(c.b * f + 0.5f)};
}

void StyleGravityDot::render(Orientation o, Rgb* out) const {
  for (int i = 0; i < kNumLeds; ++i) out[i] = kBlack;
  for (int c = 0; c < 2; ++c) {
    for (int k = 0; k < kBarLeds; ++k) {
      const float b = ch_[c].trail[k];
      if (b > 0.02f) out[bar_index(o, static_cast<Channel>(c), k)] = scaled(kGravityDotColor, b);
    }
  }
}

}  // namespace vu
