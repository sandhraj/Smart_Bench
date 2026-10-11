#include "level.h"
#include "vu_config.h"
#include <math.h>

namespace vu {

float level_from_amplitude(float amplitude) {
  if (!(amplitude > 0.0f)) return 0.0f;  // also handles NaN
  const float db = 20.0f * log10f(amplitude);
  float n = (db + kDbRange) / kDbRange;
  if (n < 0.0f) n = 0.0f;
  if (n > 1.0f) n = 1.0f;
  return n;
}

}  // namespace vu
