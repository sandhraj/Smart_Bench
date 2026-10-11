#include "style_peak_bar.h"

namespace vu {

StylePeakBar::StylePeakBar() { reset(); }

void StylePeakBar::reset() {
  for (int c = 0; c < 2; ++c) ch_[c] = {0.0f, 0.0f, 0.0f};
}

void StylePeakBar::update(const AudioFrame& f, float dt_ms) {
  const float fall = dt_ms / kPeakFallFullScaleMs;  // linear, in level units per frame
  for (int c = 0; c < 2; ++c) {
    Chan& s = ch_[c];
    const float in = f.level[c];
    // Bar: instant attack, linear fall.
    if (in >= s.bar) {
      s.bar = in;
    } else {
      s.bar -= fall;
      if (s.bar < in) s.bar = in;
    }
    // Peak hold: a new high resets the timer; after the hold time it falls with the bar.
    if (s.bar >= s.peak) {
      s.peak = s.bar;
      s.since_peak_ms = 0.0f;
    } else {
      s.since_peak_ms += dt_ms;
      if (s.since_peak_ms > kPeakHoldMs) {
        s.peak -= fall;
        if (s.peak < s.bar) s.peak = s.bar;
      }
    }
  }
}

void StylePeakBar::render(Orientation o, Rgb* out) const {
  for (int i = 0; i < kNumLeds; ++i) out[i] = kBlack;
  for (int c = 0; c < 2; ++c) {
    const Channel ch = static_cast<Channel>(c);
    const int n = lit_count(ch_[c].bar);
    for (int k = 0; k < n; ++k) out[bar_index(o, ch, k)] = kVuBarColor;
    const int p = lit_count(ch_[c].peak);
    if (p > 0) out[bar_index(o, ch, p - 1)] = kPeakHoldColor;
  }
}

}  // namespace vu
