// Style demo: drives every display style from a synthetic audio source so the styles can
// be judged on the real strip before the amp board and audio taps exist.
// Serial 115200: n=next style, o=toggle orientation, a=toggle audio, s=status.
#include <Arduino.h>
#include <FastLED.h>
#include <display.h>
#include <frame_clock.h>
#include <synth_audio.h>

#ifndef NUM_LEDS
#define NUM_LEDS 112
#endif
#ifndef LED_PIN
#define LED_PIN 16
#endif
#ifndef CAP_MA
#define CAP_MA 1000
#endif
static_assert(NUM_LEDS == vu::kNumLeds, "chain length must match the LED map");

static CRGB leds[NUM_LEDS];
static vu::Rgb px[vu::kNumLeds];
static vu::DisplayController display;
static vu::SynthAudio synth;
static vu::FrameClock clock60(vu::kFrameHz);
static vu::Orientation orient = vu::O1;
static uint32_t lastUs = 0;
static uint32_t framesThisSecond = 0, fps = 0, lastFpsMs = 0;

static void status() {
  Serial.printf("style=%s%s orientation=O%d audio=%s fps=%lu cap=%u mA(model) leds=%d pin=%d\n",
                vu::DisplayController::name(display.selected()),
                display.standby_active() ? " [standby]" : "", orient == vu::O1 ? 1 : 2,
                synth.enabled() ? "on" : "off", (unsigned long)fps, (unsigned)CAP_MA, NUM_LEDS,
                LED_PIN);
}

void setup() {
  Serial.begin(115200);
  delay(300);
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(255);
  Serial.println("\nStyle demo. n=next style, o=orientation, a=audio on/off, s=status");
  status();
  lastUs = micros();
}

void loop() {
  while (Serial.available()) {
    switch (Serial.read()) {
      case 'n': display.next(); status(); break;
      case 'o': orient = (orient == vu::O1) ? vu::O2 : vu::O1; status(); break;
      case 'a': synth.set_enabled(!synth.enabled()); status(); break;
      case 's': status(); break;
      default: break;
    }
  }
  const uint32_t now = micros();
  if (!clock60.due(now)) return;
  const float dt_ms = (now - lastUs) / 1000.0f;
  lastUs = now;

  display.update(synth.next(dt_ms), dt_ms);
  display.render(orient, px);
  for (int i = 0; i < NUM_LEDS; ++i) leds[i] = CRGB(px[i].r, px[i].g, px[i].b);
  // Hand-applied power cap, same approach as the bring-up sketch (FastLED's limiter did not hold).
  FastLED.setBrightness(calculate_max_brightness_for_power_mW(leds, NUM_LEDS, 255, 5UL * CAP_MA));
  FastLED.show();

  ++framesThisSecond;
  if (millis() - lastFpsMs >= 1000) {
    fps = framesThisSecond;
    framesThisSecond = 0;
    lastFpsMs = millis();
  }
}
