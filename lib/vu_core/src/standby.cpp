#include "standby.h"
#include "led_map.h"
#include <math.h>

namespace vu {

Rgb hsv_to_rgb(uint8_t h, uint8_t s, uint8_t v) {
  const int region = h / 43;
  const int rem = (h - region * 43) * 6;
  const int p = (v * (255 - s)) / 255;
  const int q = (v * (255 - (s * rem) / 255)) / 255;
  const int t = (v * (255 - (s * (255 - rem)) / 255)) / 255;
  switch (region) {
    case 0:  return {v, static_cast<uint8_t>(t), static_cast<uint8_t>(p)};
    case 1:  return {static_cast<uint8_t>(q), v, static_cast<uint8_t>(p)};
    case 2:  return {static_cast<uint8_t>(p), v, static_cast<uint8_t>(t)};
    case 3:  return {static_cast<uint8_t>(p), static_cast<uint8_t>(q), v};
    case 4:  return {static_cast<uint8_t>(t), static_cast<uint8_t>(p), v};
    default: return {v, static_cast<uint8_t>(p), static_cast<uint8_t>(q)};
  }
}

void render_standby(float t_ms, Rgb* out) {
  const float cycle = fmodf(t_ms / kStandbyPeriodMs, 1.0f);
  const int phase = static_cast<int>(cycle * 256.0f) & 255;
  for (int i = 0; i < kNumLeds; ++i) {
    const int hue = (i * 256 / kNumLeds + phase) & 255;
    out[i] = hsv_to_rgb(static_cast<uint8_t>(hue), 255, kStandbyValue);
  }
}

}  // namespace vu
