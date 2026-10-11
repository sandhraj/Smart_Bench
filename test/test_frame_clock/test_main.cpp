#include <unity.h>
#include "frame_clock.h"

using namespace vu;

void setUp() {}
void tearDown() {}

void test_60_fps_over_10_seconds() {  // R-049 (clock logic; rate on target is measured separately)
  FrameClock c(60.0f);
  int frames = 0;
  for (uint32_t t = 0; t < 10000000u; t += 1000u) frames += c.due(t) ? 1 : 0;
  TEST_ASSERT_INT_WITHIN(2, 600, frames);
}

void test_does_not_burst_after_stall() {
  FrameClock c(60.0f);
  c.due(0);
  TEST_ASSERT_TRUE(c.due(1000000u));   // 1 s stall: one frame, then resync
  int extra = 0;
  for (uint32_t t = 1001000u; t < 1010000u; t += 1000u) extra += c.due(t) ? 1 : 0;
  TEST_ASSERT_TRUE(extra <= 1);        // about 9 ms later: at most one frame, no burst
}

void test_handles_timer_wraparound() {
  FrameClock c(60.0f);
  const uint32_t start = 0xFFFFF000u;
  int frames = 0;
  for (uint32_t i = 0; i < 1000000u; i += 1000u) frames += c.due(start + i) ? 1 : 0;
  TEST_ASSERT_INT_WITHIN(2, 60, frames);
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_60_fps_over_10_seconds);
  RUN_TEST(test_does_not_burst_after_stall);
  RUN_TEST(test_handles_timer_wraparound);
  return UNITY_END();
}
