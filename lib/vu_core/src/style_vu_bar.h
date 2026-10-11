// Style 1: classic VU bar, one bar per channel, slow needle-like ballistics.
#pragma once
#include "ballistics.h"
#include "style.h"

namespace vu {

class StyleVuBar : public Style {
 public:
  StyleVuBar();
  void reset() override;
  void update(const AudioFrame& f, float dt_ms) override;
  void render(Orientation o, Rgb* out) const override;
  float shown(Channel c) const { return s_[c].value(); }

 private:
  Smoother s_[2];
};

}  // namespace vu
