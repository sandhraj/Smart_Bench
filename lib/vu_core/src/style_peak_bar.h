// Style 2: peak bar. Instant attack, linear fall, one peak-hold LED per bar.
#pragma once
#include "style.h"

namespace vu {

class StylePeakBar : public Style {
 public:
  StylePeakBar();
  void reset() override;
  void update(const AudioFrame& f, float dt_ms) override;
  void render(Orientation o, Rgb* out) const override;
  float shown(Channel c) const { return ch_[c].bar; }
  float peak(Channel c) const { return ch_[c].peak; }

 private:
  struct Chan {
    float bar;
    float peak;
    float since_peak_ms;
  };
  Chan ch_[2];
};

}  // namespace vu
