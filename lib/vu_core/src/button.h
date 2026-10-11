// Button press classification. Pure logic, no Arduino.
#pragma once
#include <stdint.h>

namespace vu {

constexpr uint32_t kTapMaxMs = 400;      // under this is a tap, at or over is a hold
constexpr uint32_t kTeachMinMs = 3000;   // button 4: at or over this starts orientation teach

enum class Press { Tap, Hold };
enum class Button4Action { NextPattern, Teach };

Press classify_press(uint32_t held_ms);
Button4Action classify_button4(uint32_t held_ms);

// Next pattern index, wrapping. count <= 0 returns 0.
int next_pattern(int current, int count);

}  // namespace vu
