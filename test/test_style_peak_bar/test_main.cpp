#include <unity.h>
#include "style_peak_bar.h"

using namespace vu;

void setUp() {}
void tearDown() {}

static void feed(StylePeakBar& s, float l, float r, float total_ms, float dt_ms = 10.0f) {
  AudioFrame f = {{l, r}};
  const int n = static_cast<int>(total_ms / dt_ms + 0.5f);
  for (int i = 0; i < n; ++i) s.update(f, dt_ms);
}

void test_attack_is_instant() {  // R-043
  StylePeakBar s;
  feed(s, 0.2f, 0.2f, 10.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.2f, s.shown(LEFT));
  AudioFrame f = {{0.9f, 0.4f}};
  s.update(f, 16.0f);  // one frame
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.9f, s.shown(LEFT));
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.4f, s.shown(RIGHT));
}

void test_fall_is_linear_full_scale_in_1s() {  // R-044
  StylePeakBar s;
  feed(s, 1.0f, 1.0f, 10.0f);
  feed(s, 0.0f, 0.0f, 500.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.011f, 0.5f, s.shown(LEFT));
  feed(s, 0.0f, 0.0f, 500.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.011f, 0.0f, s.shown(LEFT));
}

void test_bar_does_not_fall_below_input() {  // R-044
  StylePeakBar s;
  feed(s, 1.0f, 1.0f, 10.0f);
  feed(s, 0.3f, 0.3f, 2000.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.3f, s.shown(LEFT));
}

void test_peak_holds_600ms_then_falls() {  // R-045
  StylePeakBar s;
  feed(s, 1.0f, 1.0f, 10.0f);
  feed(s, 0.0f, 0.0f, 590.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 1.0f, s.peak(LEFT));
  feed(s, 0.0f, 0.0f, 110.0f);  // 700 ms after the peak
  TEST_ASSERT_FLOAT_WITHIN(0.02f, 0.9f, s.peak(LEFT));
}

void test_new_high_resets_hold() {  // R-045
  StylePeakBar s;
  feed(s, 0.8f, 0.8f, 10.0f);
  feed(s, 0.0f, 0.0f, 500.0f);
  feed(s, 0.9f, 0.9f, 10.0f);     // new high
  feed(s, 0.0f, 0.0f, 590.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.9f, s.peak(LEFT));
}

void test_render_shows_hold_led_above_bar() {  // R-045
  StylePeakBar s;
  feed(s, 1.0f, 1.0f, 10.0f);
  feed(s, 0.0f, 0.0f, 500.0f);   // bar about 0.5, peak still 1.0
  Rgb px[kNumLeds];
  s.render(O1, px);
  const Rgb top = px[bar_index(O1, LEFT, 19)];
  TEST_ASSERT_EQUAL_UINT8(kPeakHoldColor.r, top.r);
  TEST_ASSERT_EQUAL_UINT8(kPeakHoldColor.b, top.b);
  const Rgb below = px[bar_index(O1, LEFT, 18)];
  TEST_ASSERT_EQUAL_UINT8(0, below.r | below.g | below.b);
  const Rgb mid = px[bar_index(O1, LEFT, 5)];
  TEST_ASSERT_EQUAL_UINT8(kVuBarColor.g, mid.g);
}

void test_silence_renders_black() {
  StylePeakBar s;
  Rgb px[kNumLeds];
  s.render(O2, px);
  int lit = 0;
  for (int i = 0; i < kNumLeds; ++i) lit += (px[i].r | px[i].g | px[i].b) != 0;
  TEST_ASSERT_EQUAL_INT(0, lit);
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_attack_is_instant);
  RUN_TEST(test_fall_is_linear_full_scale_in_1s);
  RUN_TEST(test_bar_does_not_fall_below_input);
  RUN_TEST(test_peak_holds_600ms_then_falls);
  RUN_TEST(test_new_high_resets_hold);
  RUN_TEST(test_render_shows_hold_led_above_bar);
  RUN_TEST(test_silence_renders_black);
  return UNITY_END();
}
