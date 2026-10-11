#include "button.h"

namespace vu {

Press classify_press(uint32_t held_ms) {
  return held_ms < kTapMaxMs ? Press::Tap : Press::Hold;
}

Button4Action classify_button4(uint32_t held_ms) {
  return held_ms < kTeachMinMs ? Button4Action::NextPattern : Button4Action::Teach;
}

int next_pattern(int current, int count) {
  if (count <= 0) return 0;
  return (current + 1) % count;
}

}  // namespace vu
