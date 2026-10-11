#include <unity.h>
#include "ballistics.h"

using namespace vu;

void setUp() {}
void tearDown() {}

static float run(Smoother& s, float target, float total_ms, float dt_ms) {
  const int n = static_cast<int>(total_ms / dt_ms + 0.5f);
  for (int i = 0; i < n; ++i) s.step(target, dt_ms);
  return s.value();
}

void test_rise_reaches_99_percent_in_300ms() {  // R-041
  Smoother s(300.0f, 300.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.002f, 0.99f, run(s, 1.0f, 300.0f, 10.0f));
}

void test_rise_is_not_instant() {  // R-041
  Smoother s(300.0f, 300.0f);
  TEST_ASSERT_TRUE(run(s, 1.0f, 50.0f, 10.0f) < 0.6f);
}

void test_fall_reaches_1_percent_in_300ms() {  // R-041
  Smoother s(300.0f, 300.0f);
  s.reset(1.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.002f, 0.01f, run(s, 0.0f, 300.0f, 10.0f));
}

void test_rise_and_fall_times_are_independent() {
  Smoother s(100.0f, 1000.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.002f, 0.99f, run(s, 1.0f, 100.0f, 5.0f));
  TEST_ASSERT_TRUE(run(s, 0.0f, 100.0f, 5.0f) > 0.6f);  // falling is slow
}

void test_frame_step_size_does_not_change_result() {
  Smoother a(300.0f, 300.0f), b(300.0f, 300.0f);
  TEST_ASSERT_FLOAT_WITHIN(0.002f, run(a, 1.0f, 300.0f, 5.0f), run(b, 1.0f, 300.0f, 20.0f));
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_rise_reaches_99_percent_in_300ms);
  RUN_TEST(test_rise_is_not_instant);
  RUN_TEST(test_fall_reaches_1_percent_in_300ms);
  RUN_TEST(test_rise_and_fall_times_are_independent);
  RUN_TEST(test_frame_step_size_does_not_change_result);
  return UNITY_END();
}
