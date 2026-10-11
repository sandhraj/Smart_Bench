#include <unity.h>
#include "style_vu_bar.h"

using namespace vu;

void setUp() {}
void tearDown() {}

static bool is_lit(const Rgb& p) { return p.r || p.g || p.b; }

static int count_lit(const Rgb* px) {
  int n = 0;
  for (int i = 0; i < kNumLeds; ++i) n += is_lit(px[i]);
  return n;
}

// Drive the style at a constant input until it has settled (2 s).
static void settle(StyleVuBar& s, float l, float r) {
  AudioFrame f = {{l, r}};
  for (int i = 0; i < 200; ++i) s.update(f, 10.0f);
}

void test_silence_lights_nothing() {  // R-042
  StyleVuBar s;
  Rgb px[kNumLeds];
  s.render(O1, px);
  TEST_ASSERT_EQUAL_INT(0, count_lit(px));
}

void test_half_level_lights_10_per_bar() {  // R-042
  StyleVuBar s;
  settle(s, 0.5f, 0.5f);
  Rgb px[kNumLeds];
  s.render(O1, px);
  TEST_ASSERT_EQUAL_INT(20, count_lit(px));
  for (int k = 0; k < 10; ++k) {
    TEST_ASSERT_TRUE(is_lit(px[bar_index(O1, LEFT, k)]));
    TEST_ASSERT_TRUE(is_lit(px[bar_index(O1, RIGHT, k)]));
  }
  for (int k = 10; k < kBarLeds; ++k) {
    TEST_ASSERT_FALSE(is_lit(px[bar_index(O1, LEFT, k)]));
    TEST_ASSERT_FALSE(is_lit(px[bar_index(O1, RIGHT, k)]));
  }
}

void test_full_level_lights_both_bars_only() {  // R-042
  StyleVuBar s;
  settle(s, 1.0f, 1.0f);
  Rgb px[kNumLeds];
  s.render(O2, px);
  TEST_ASSERT_EQUAL_INT(40, count_lit(px));
}

void test_channels_are_independent() {  // R-042
  StyleVuBar s;
  settle(s, 1.0f, 0.0f);
  Rgb px[kNumLeds];
  s.render(O1, px);
  TEST_ASSERT_EQUAL_INT(20, count_lit(px));
  TEST_ASSERT_TRUE(is_lit(px[bar_index(O1, LEFT, 0)]));
  TEST_ASSERT_FALSE(is_lit(px[bar_index(O1, RIGHT, 0)]));
}

void test_orientation_moves_the_bars() {  // R-010, R-011 through the style
  StyleVuBar s;
  settle(s, 1.0f, 0.0f);
  Rgb a[kNumLeds], b[kNumLeds];
  s.render(O1, a);
  s.render(O2, b);
  TEST_ASSERT_TRUE(is_lit(a[67]));   // O1 left starts at index 67
  TEST_ASSERT_TRUE(is_lit(b[31]));   // O2 left starts at index 31
  TEST_ASSERT_FALSE(is_lit(a[31]));
  TEST_ASSERT_FALSE(is_lit(b[67]));
}

void test_rises_gradually() {  // R-041 via the style
  StyleVuBar s;
  AudioFrame f = {{1.0f, 1.0f}};
  s.update(f, 16.0f);
  TEST_ASSERT_TRUE(s.shown(LEFT) > 0.0f);
  TEST_ASSERT_TRUE(s.shown(LEFT) < 0.5f);
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_silence_lights_nothing);
  RUN_TEST(test_half_level_lights_10_per_bar);
  RUN_TEST(test_full_level_lights_both_bars_only);
  RUN_TEST(test_channels_are_independent);
  RUN_TEST(test_orientation_moves_the_bars);
  RUN_TEST(test_rises_gradually);
  return UNITY_END();
}
