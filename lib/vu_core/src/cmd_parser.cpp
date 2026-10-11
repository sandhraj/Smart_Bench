#include "cmd_parser.h"

namespace vu {

Parsed parse_key(char c) {
  if (c >= '0' && c <= '9') {
    return {Cmd::White, true, static_cast<uint8_t>((c - '0') * 10)};
  }
  switch (c) {
    case 'f': return {Cmd::White, true, 100};
    case 'w': return {Cmd::White, false, 0};
    case 'r': return {Cmd::Red, false, 0};
    case 'g': return {Cmd::Green, false, 0};
    case 'b': return {Cmd::Blue, false, 0};
    case 'x': return {Cmd::Rainbow, false, 0};
    case 'p': return {Cmd::Walk, false, 0};
    case 'o': return {Cmd::Off, false, 0};
    case 'c': return {Cmd::ToggleCap, false, 0};
    case 's': return {Cmd::Status, false, 0};
    default:  return {Cmd::None, false, 0};
  }
}

}  // namespace vu
