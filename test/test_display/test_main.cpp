#include <unity.h>
#include <string.h>
#include "display.h"

using namespace vu;

void setUp() {}
void tearDown() {}

static bool lit(const Rgb& p) { return p.r || p.g || p.b; }

static void feed(DisplayController& d, float l, float r, float total_ms, float dt_ms = 10.0f) {
  AudioFrame f = {{l, r}};
  const int n = static_cast<int>(total_ms / dt_ms + 0.5f);
  for (int i = 0; i < n; ++i) d.update(f, dt_ms);
}

void test_pattern_list_in_order() {  // R-022
  TEST_ASSERT_EQUAL_INT(5, kPatternCount);
  TEST_ASSERT_EQUAL_STRING("VU bar", DisplayController::name(0));
  TEST_ASSERT_EQUAL_STRING("Peak bar", DisplayController::name(1));
  TEST_ASSERT_EQUAL_STRING("Zone bar", DisplayController::name(2));
  TEST_ASSERT_EQUAL_STRING("Gravity dot", DisplayController::name(3));
  TEST_ASSERT_EQUAL_STRING("Standby", DisplayController::name(4));
}

void test_next_cycles_and_wraps() {  // R-021, R-022
  DisplayController d;
  TEST_ASSERT_EQUAL_INT(0, d.selected());
  for (int i = 1; i < kPatternCount; ++i) {
    d.next();
    TEST_ASSERT_EQUAL_INT(i, d.selected());
  }
  d.next();
  TEST_ASSERT_EQUAL_INT(0, d.selected());
}

void test_no_standby_before_5s_of_silence() {  // R-048
  DisplayController d;
  feed(d, 0.0f, 0.0f, 4900.0f);
  TEST_ASSERT_FALSE(d.standby_active());
}

void test_standby_after_5s_of_silence() {  // R-048
  DisplayController d;
  feed(d, 0.0f, 0.0f, 5100.0f);
  TEST_ASSERT_TRUE(d.standby_active());
  Rgb px[kNumLeds];
  d.render(O1, px);
  int n = 0;
  for (int i = 0; i < kNumLeds; ++i) n += lit(px[i]);
  TEST_ASSERT_TRUE(n > 100);  // rainbow covers the chain
}

void test_audio_returns_from_standby_immediately() {  // R-048
  DisplayController d;
  feed(d, 0.0f, 0.0f, 6000.0f);
  TEST_ASSERT_TRUE(d.standby_active());
  feed(d, 0.5f, 0.5f, 10.0f);
  TEST_ASSERT_FALSE(d.standby_active());
}

void test_below_floor_counts_as_silence() {  // R-048
  DisplayController d;
  feed(d, kNoiseFloor * 0.5f, kNoiseFloor * 0.5f, 5100.0f);
  TEST_ASSERT_TRUE(d.standby_active());
}

void test_forced_standby_pattern() {  // R-022
  DisplayController d;
  d.select(kPatternStandby);
  feed(d, 0.9f, 0.9f, 100.0f);
  TEST_ASSERT_TRUE(d.standby_active());
}

void test_selected_style_renders_when_loud() {  // R-022
  DisplayController d;
  feed(d, 1.0f, 1.0f, 2000.0f);
  Rgb px[kNumLeds];
  d.render(O1, px);
  int n = 0;
  for (int i = 0; i < kNumLeds; ++i) n += lit(px[i]);
  TEST_ASSERT_EQUAL_INT(40, n);  // VU bar, both bars full
}

void test_standby_rainbow_starts_red_and_is_dim() {  // R-048
  Rgb px[kNumLeds];
  render_standby(0.0f, px);
  TEST_ASSERT_EQUAL_UINT8(kStandbyValue, px[0].r);
  TEST_ASSERT_EQUAL_UINT8(0, px[0].b);
}

void test_hsv_primaries() {
  const Rgb red = hsv_to_rgb(0, 255, 255);
  TEST_ASSERT_EQUAL_UINT8(255, red.r);
  TEST_ASSERT_EQUAL_UINT8(0, red.g);
  TEST_ASSERT_EQUAL_UINT8(0, red.b);
  const Rgb white = hsv_to_rgb(0, 0, 200);
  TEST_ASSERT_EQUAL_UINT8(200, white.r);
  TEST_ASSERT_EQUAL_UINT8(200, white.g);
  TEST_ASSERT_EQUAL_UINT8(200, white.b);
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_pattern_list_in_order);
  RUN_TEST(test_next_cycles_and_wraps);
  RUN_TEST(test_no_standby_before_5s_of_silence);
  RUN_TEST(test_standby_after_5s_of_silence);
  RUN_TEST(test_audio_returns_from_standby_immediately);
  RUN_TEST(test_below_floor_counts_as_silence);
  RUN_TEST(test_forced_standby_pattern);
  RUN_TEST(test_selected_style_renders_when_loud);
  RUN_TEST(test_standby_rainbow_starts_red_and_is_dim);
  RUN_TEST(test_hsv_primaries);
  return UNITY_END();
}
