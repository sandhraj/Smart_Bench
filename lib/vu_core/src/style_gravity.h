// Style 4: gravity dot with a fading tail. Rises instantly, falls with constant acceleration.
#pragma once
#include "style.h"

namespace vu {

class StyleGravityDot : public Style {
 public:
  StyleGravityDot();
  void reset() override;
  void update(const AudioFrame& f, float dt_ms) override;
  void render(Orientation o, Rgb* out) const override;
  float pos(Channel c) const { return ch_[c].pos; }
  float tail(Channel c, int k) const { return ch_[c].trail[k]; }

 private:
  struct Chan {
    float pos;
    float vel;  // level units per second, downward
    float trail[kBarLeds];
  };
  Chan ch_[2];
};

}  // namespace vu
