// Style 3: zone bar. VU-bar ballistics, coloured green / yellow / red by position.
#pragma once
#include "ballistics.h"
#include "style.h"

namespace vu {

// Colour of the k-th LED of a bar (0..kBarLeds-1).
Rgb zone_color(int k);

class StyleZoneBar : public Style {
 public:
  StyleZoneBar();
  void reset() override;
  void update(const AudioFrame& f, float dt_ms) override;
  void render(Orientation o, Rgb* out) const override;
  float shown(Channel c) const { return s_[c].value(); }

 private:
  Smoother s_[2];
};

}  // namespace vu
