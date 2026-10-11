#include "led_map.h"

namespace vu {

int bar_index(Orientation o, Channel c, int k) {
  if (k < 0 || k >= kBarLeds) return -1;
  // O1: L on seg10 filling I->L (wire order); R on seg5 filling E->H (reverse wire order).
  // O2: L on seg5 filling H->E (wire order);  R on seg10 filling L->I (reverse wire order).
  const bool seg10 = (o == O1) ? (c == LEFT) : (c == RIGHT);
  const bool forward = (c == LEFT);  // left bars follow wire order in both orientations
  if (seg10) {
    return forward ? 67 + k : 86 - k;
  }
  return forward ? 31 + k : 50 - k;
}

int lit_count(float level) {
  if (!(level > 0.0f)) return 0;  // also handles NaN
  if (level >= 1.0f) return kBarLeds;
  return static_cast<int>(level * kBarLeds + 0.5f);
}

}  // namespace vu
