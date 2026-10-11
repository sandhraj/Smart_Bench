// Amplitude to display level. Pure logic, no Arduino.
#pragma once

namespace vu {

// amplitude: linear, 1.0 = full scale. Returns 0..1, linear in dB over kDbRange.
float level_from_amplitude(float amplitude);

}  // namespace vu
