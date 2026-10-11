// Display style interface. A style turns audio levels and time into 112 pixel colours.
// Pure logic, no Arduino, so every style is host-testable.
#pragma once
#include "led_map.h"
#include "vu_config.h"

namespace vu {

struct AudioFrame {
  float level[2];  // LEFT, RIGHT: already scaled to 0..1 (see level_from_amplitude)
};

class Style {
 public:
  virtual ~Style() {}
  virtual void reset() = 0;
  virtual void update(const AudioFrame& f, float dt_ms) = 0;
  // Writes kNumLeds pixels. Pixels the style does not use are black.
  virtual void render(Orientation o, Rgb* out) const = 0;
};

}  // namespace vu
