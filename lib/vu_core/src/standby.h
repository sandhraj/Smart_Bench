// Standby rainbow and colour helper. Pure logic, no Arduino.
#pragma once
#include <stdint.h>
#include "vu_config.h"

namespace vu {

// h, s, v all 0..255. h = 0 is red.
Rgb hsv_to_rgb(uint8_t h, uint8_t s, uint8_t v);

// Writes kNumLeds pixels of a slow rainbow along the chain at time t_ms.
void render_standby(float t_ms, Rgb* out);

}  // namespace vu
