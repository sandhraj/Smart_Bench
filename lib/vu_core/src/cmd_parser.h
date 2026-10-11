// Serial command parser for the LED bring-up sketch. Pure logic, no Arduino.
#pragma once
#include <stdint.h>

namespace vu {

enum class Cmd : uint8_t {
  None,       // unknown character, ignore
  White,      // solid white; brightness_pct valid only if has_brightness
  Red,
  Green,
  Blue,
  Rainbow,
  Walk,
  Off,
  ToggleCap,
  Status,
};

struct Parsed {
  Cmd cmd;
  bool has_brightness;
  uint8_t brightness_pct;  // 0..100
};

Parsed parse_key(char c);

}  // namespace vu
