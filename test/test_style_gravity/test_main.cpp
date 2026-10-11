#include <unity.h>
#include "style_gravity.h"

using namespace vu;

void setUp() {}
void tearDown() {}

static void feed(StyleGravityDot& s, float l, float r, float total_ms, float dt_ms = 10.0f) {
  AudioFrame f = {{l, r}};
  const int n = static_cast<int>(total_ms / dt_ms + 0.5f);
  for (int i = 0; i < n; ++i) s.update(f, dt_ms);
}

static bool lit(const Rgb& p) { return p.r || p.g || p.b; }

void test_rises_instantly() {  // R-046
  StyleGravityDot s;
  AudioFrame f = {{0.8f, 0.3f}};
  s.update(f, 16.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.8f, s.pos(LEFT));
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.3f, s.pos(RIGHT));
}

void test_full_scale_fall_takes_1_2_seconds() {  // R-046
  StyleGravityDot s;
  feed(s, 1.0f, 1.0f, 10.0f);
  int steps = 0;
  AudioFrame f = {{0.0f, 0.0f}};
  while (s.pos(LEFT) > 0.0f && steps < 1000) {
    s.update(f, 10.0f);
    ++steps;
  }
  const float seconds = steps * 0.010f;
  TEST_ASSERT_FLOAT_WITHIN(0.05f, 1.2f, seconds);
}

void test_fall_accelerates() {  // R-046: constant acceleration, not linear
  StyleGravityDot s;
  feed(s, 1.0f, 1.0f, 10.0f);
  feed(s, 0.0f, 0.0f, 600.0f);
  // After half the time, a constant-acceleration fall has covered a quarter of the distance.
  TEST_ASSERT_FLOAT_WITHIN(0.04f, 0.75f, s.pos(LEFT));
}

void test_stops_at_input() {  // R-046
  StyleGravityDot s;
  feed(s, 1.0f, 1.0f, 10.0f);
  feed(s, 0.4f, 0.4f, 3000.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.4f, s.pos(LEFT));
}

void test_tail_fades_behind_dot() {  // R-050
  StyleGravityDot s;
  feed(s, 1.0f, 1.0f, 10.0f);
  feed(s, 0.0f, 0.0f, 300.0f);  // falling: positions above the dot were visited recently
  const int dot = lit_count(s.pos(LEFT)) - 1;
  TEST_ASSERT_TRUE(dot >= 0 && dot < kBarLeds - 3);
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 1.0f, s.tail(LEFT, dot));
  // Just above the dot the tail is dim but present, and fades with distance.
  const float near_t = s.tail(LEFT, dot + 1);
  const float far_t = s.tail(LEFT, dot + 3);
  TEST_ASSERT_TRUE(near_t > 0.0f && near_t < 1.0f);
  TEST_ASSERT_TRUE(far_t < near_t);
}

void test_tail_time_constant() {  // R-050: one time constant leaves about 37 %
  StyleGravityDot s;
  feed(s, 1.0f, 1.0f, 10.0f);  // dot at LED 19, tail[19] = 1
  AudioFrame f = {{0.0f, 0.0f}};
  int guard = 0;
  while (lit_count(s.pos(LEFT)) - 1 >= 19 && guard++ < 1000) s.update(f, 10.0f);  // dot leaves 19
  feed(s, 0.0f, 0.0f, 120.0f);  // one time constant later
  TEST_ASSERT_FLOAT_WITHIN(0.06f, 0.37f, s.tail(LEFT, 19));
}

void test_render_dot_full_brightness_and_tail_dimmer() {  // R-050
  StyleGravityDot s;
  feed(s, 1.0f, 1.0f, 10.0f);
  feed(s, 0.0f, 0.0f, 200.0f);
  Rgb px[kNumLeds];
  s.render(O1, px);
  const int dot = lit_count(s.pos(LEFT)) - 1;
  const Rgb d = px[bar_index(O1, LEFT, dot)];
  TEST_ASSERT_EQUAL_UINT8(kGravityDotColor.r, d.r);
  const Rgb t = px[bar_index(O1, LEFT, dot + 1)];
  TEST_ASSERT_TRUE(lit(t));
  TEST_ASSERT_TRUE(t.r < d.r);
}

void test_silence_renders_black() {
  StyleGravityDot s;
  Rgb px[kNumLeds];
  s.render(O1, px);
  for (int i = 0; i < kNumLeds; ++i) TEST_ASSERT_FALSE(lit(px[i]));
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_rises_instantly);
  RUN_TEST(test_full_scale_fall_takes_1_2_seconds);
  RUN_TEST(test_fall_accelerates);
  RUN_TEST(test_stops_at_input);
  RUN_TEST(test_tail_fades_behind_dot);
  RUN_TEST(test_tail_time_constant);
  RUN_TEST(test_render_dot_full_brightness_and_tail_dimmer);
  RUN_TEST(test_silence_renders_black);
  return UNITY_END();
}
