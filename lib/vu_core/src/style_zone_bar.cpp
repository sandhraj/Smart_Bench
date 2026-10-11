#include "style_zone_bar.h"

namespace vu {

Rgb zone_color(int k) {
  if (k >= kZoneRedFrom) return kZoneRed;
  if (k >= kZoneYellowFrom) return kZoneYellow;
  return kZoneGreen;
}

StyleZoneBar::StyleZoneBar()
    : s_{Smoother(kVuRiseMs99, kVuFallMs99), Smoother(kVuRiseMs99, kVuFallMs99)} {}

void StyleZoneBar::reset() {
  s_[LEFT].reset();
  s_[RIGHT].reset();
}

void StyleZoneBar::update(const AudioFrame& f, float dt_ms) {
  s_[LEFT].step(f.level[LEFT], dt_ms);
  s_[RIGHT].step(f.level[RIGHT], dt_ms);
}

void StyleZoneBar::render(Orientation o, Rgb* out) const {
  for (int i = 0; i < kNumLeds; ++i) out[i] = kBlack;
  for (int c = 0; c < 2; ++c) {
    const int n = lit_count(s_[c].value());
    for (int k = 0; k < n; ++k) {
      out[bar_index(o, static_cast<Channel>(c), k)] = zone_color(k);
    }
  }
}

}  // namespace vu
