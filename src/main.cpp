// LED bring-up sketch: proves the LED supply and data path before the main firmware.
// Serial 115200, single-character commands, see docs/SPEC.md "Bring-up sketch".
#include <Arduino.h>
#include <FastLED.h>
#include <cmd_parser.h>

#ifndef NUM_LEDS
#define NUM_LEDS 112
#endif
#ifndef LED_PIN
#define LED_PIN 16
#endif
// Cap in FastLED's model mA at 5 V. Real strip current was measured at about 1.8x (white)
// to 2.2x (rainbow) of this on an earlier build, so 1000 is roughly 1.8-2.2 A real.
// R-030 / H-004 require the measured value; re-measure before raising.
#ifndef CAP_MA
#define CAP_MA 1000
#endif
static const uint32_t CAP_MV = 5;

enum Mode { M_OFF, M_WHITE, M_RED, M_GREEN, M_BLUE, M_RAINBOW, M_WALK };

static CRGB leds[NUM_LEDS];
static Mode mode = M_OFF;
static uint8_t bri = 0;  // requested master brightness 0-255
static bool capOn = true;
static uint8_t hue = 0;
static int walkPos = 0;

// FastLED's built-in limiter did not hold on an earlier build, so the cap is applied by hand.
static void render() {
  switch (mode) {
    case M_OFF:     fill_solid(leds, NUM_LEDS, CRGB::Black); break;
    case M_WHITE:   fill_solid(leds, NUM_LEDS, CRGB::White); break;
    case M_RED:     fill_solid(leds, NUM_LEDS, CRGB::Red); break;
    case M_GREEN:   fill_solid(leds, NUM_LEDS, CRGB::Green); break;
    case M_BLUE:    fill_solid(leds, NUM_LEDS, CRGB::Blue); break;
    case M_RAINBOW: fill_rainbow(leds, NUM_LEDS, hue, 255 / NUM_LEDS + 1); break;
    case M_WALK:    fill_solid(leds, NUM_LEDS, CRGB::Black); leds[walkPos] = CRGB::White; break;
  }
  uint8_t eff = bri;
  if (capOn) eff = calculate_max_brightness_for_power_mW(leds, NUM_LEDS, bri, CAP_MV * CAP_MA);
  FastLED.setBrightness(eff);
  FastLED.show();
}

static void printStatus() {
  const char* names[] = {"off", "white", "red", "green", "blue", "rainbow", "walk"};
  uint8_t eff = FastLED.getBrightness();
  uint32_t estMA = calculate_unscaled_power_mW(leds, NUM_LEDS) * eff / 255 / CAP_MV;
  Serial.printf("mode=%s req=%u%% (%u/255) cap=%s(%u mA) effective=%u/255 est=%lu mA leds=%d pin=%d\n",
                names[mode], (unsigned)(bri * 100 / 255), bri, capOn ? "ON" : "OFF",
                (unsigned)CAP_MA, eff, (unsigned long)estMA, NUM_LEDS, LED_PIN);
}

void setup() {
  Serial.begin(115200);
  delay(300);
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  const CRGB seq[] = {CRGB::Red, CRGB::Green, CRGB::Blue, CRGB::Black};
  FastLED.setBrightness(20);
  for (CRGB c : seq) { fill_solid(leds, NUM_LEDS, c); FastLED.show(); delay(400); }
  render();
  Serial.println("\nLED test ready. 0-9=white 0-90%, f=100%, r/g/b, w=white, x=rainbow, "
                 "o=off, p=walk one pixel, c=toggle cap, s=status");
  printStatus();
}

void loop() {
  while (Serial.available()) {
    const vu::Parsed p = vu::parse_key((char)Serial.read());
    switch (p.cmd) {
      case vu::Cmd::None: continue;
      case vu::Cmd::White:
        mode = M_WHITE;
        if (p.has_brightness) bri = (uint8_t)(p.brightness_pct * 255 / 100);
        break;
      case vu::Cmd::Red:     mode = M_RED; break;
      case vu::Cmd::Green:   mode = M_GREEN; break;
      case vu::Cmd::Blue:    mode = M_BLUE; break;
      case vu::Cmd::Rainbow: mode = M_RAINBOW; if (bri == 0) bri = 76; break;
      case vu::Cmd::Walk:    mode = M_WALK; walkPos = 0; if (bri == 0) bri = 76; break;
      case vu::Cmd::Off:     mode = M_OFF; break;
      case vu::Cmd::ToggleCap:
        capOn = !capOn;
        if (capOn) Serial.printf("Power cap ON (5V / %u mA model)\n", (unsigned)CAP_MA);
        else Serial.println("WARNING: power cap OFF - do not run full white on long strips!");
        break;
      case vu::Cmd::Status: printStatus(); continue;
    }
    render();
    printStatus();
  }
  if (mode == M_RAINBOW) { hue += 2; render(); delay(20); }
  if (mode == M_WALK) {
    render();
    if (walkPos % 10 == 0) Serial.printf("pixel %d\n", walkPos);
    delay(250);
    walkPos = (walkPos + 1) % NUM_LEDS;
  }
}
