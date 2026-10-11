#include <unity.h>
#include "style_zone_bar.h"

using namespace vu;

void setUp() {}
void tearDown() {}

static bool same(const Rgb& a, const Rgb& b) { return a.r == b.r && a.g == b.g && a.b == b.b; }

static void settle(StyleZoneBar& s, float l, float r) {
  AudioFrame f = {{l, r}};
  for (int i = 0; i < 200; ++i) s.update(f, 10.0f);
}

void test_zone_colour_by_position() {  // R-047
  for (int k = 0; k <= 13; ++k) TEST_ASSERT_TRUE(same(zone_color(k), kZoneGreen));
  for (int k = 14; k <= 17; ++k) TEST_ASSERT_TRUE(same(zone_color(k), kZoneYellow));
  for (int k = 18; k <= 19; ++k) TEST_ASSERT_TRUE(same(zone_color(k), kZoneRed));
}

void test_full_bar_is_green_yellow_red() {  // R-047
  StyleZoneBar s;
  settle(s, 1.0f, 1.0f);
  Rgb px[kNumLeds];
  s.render(O1, px);
  TEST_ASSERT_TRUE(same(px[bar_index(O1, LEFT, 0)], kZoneGreen));
  TEST_ASSERT_TRUE(same(px[bar_index(O1, LEFT, 13)], kZoneGreen));
  TEST_ASSERT_TRUE(same(px[bar_index(O1, LEFT, 14)], kZoneYellow));
  TEST_ASSERT_TRUE(same(px[bar_index(O1, LEFT, 17)], kZoneYellow));
  TEST_ASSERT_TRUE(same(px[bar_index(O1, LEFT, 18)], kZoneRed));
  TEST_ASSERT_TRUE(same(px[bar_index(O1, LEFT, 19)], kZoneRed));
}

void test_colours_follow_bar_position_on_reversed_bar() {  // R-047 with R-010
  StyleZoneBar s;
  settle(s, 1.0f, 1.0f);
  Rgb px[kNumLeds];
  s.render(O1, px);
  // O1 right bar is wired reversed: k=19 is index 31, k=0 is index 50.
  TEST_ASSERT_TRUE(same(px[31], kZoneRed));
  TEST_ASSERT_TRUE(same(px[50], kZoneGreen));
}

void test_low_level_is_green_only() {  // R-047
  StyleZoneBar s;
  settle(s, 0.5f, 0.0f);
  Rgb px[kNumLeds];
  s.render(O2, px);
  int green = 0, other = 0;
  for (int i = 0; i < kNumLeds; ++i) {
    if (same(px[i], kBlack)) continue;
    if (same(px[i], kZoneGreen)) ++green; else ++other;
  }
  TEST_ASSERT_EQUAL_INT(10, green);
  TEST_ASSERT_EQUAL_INT(0, other);
}

void test_80_percent_reaches_yellow() {  // R-047
  StyleZoneBar s;
  settle(s, 0.8f, 0.0f);
  Rgb px[kNumLeds];
  s.render(O1, px);
  TEST_ASSERT_TRUE(same(px[bar_index(O1, LEFT, 15)], kZoneYellow));  // 16 lit: k 0..15
  TEST_ASSERT_TRUE(same(px[bar_index(O1, LEFT, 16)], kBlack));
}

void test_uses_vu_ballistics() {  // R-041 shared
  StyleZoneBar s;
  AudioFrame f = {{1.0f, 1.0f}};
  s.update(f, 16.0f);
  TEST_ASSERT_TRUE(s.shown(LEFT) > 0.0f && s.shown(LEFT) < 0.5f);
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_zone_colour_by_position);
  RUN_TEST(test_full_bar_is_green_yellow_red);
  RUN_TEST(test_colours_follow_bar_position_on_reversed_bar);
  RUN_TEST(test_low_level_is_green_only);
  RUN_TEST(test_80_percent_reaches_yellow);
  RUN_TEST(test_uses_vu_ballistics);
  return UNITY_END();
}
