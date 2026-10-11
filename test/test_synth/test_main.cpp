#include <unity.h>
#include "synth_audio.h"

using namespace vu;

void setUp() {}
void tearDown() {}

void test_levels_stay_in_range_and_move() {  // R-051
  SynthAudio s;
  float lo = 1.0f, hi = 0.0f;
  for (int i = 0; i < 2000; ++i) {
    const AudioFrame f = s.next(10.0f);
    for (int c = 0; c < 2; ++c) {
      TEST_ASSERT_TRUE(f.level[c] >= 0.0f && f.level[c] <= 1.0f);
      if (f.level[c] < lo) lo = f.level[c];
      if (f.level[c] > hi) hi = f.level[c];
    }
  }
  TEST_ASSERT_TRUE(hi - lo > 0.3f);
}

void test_has_beats() {  // R-051: level jumps at the kick
  SynthAudio s;
  float before = 0.0f, at_kick = 0.0f;
  for (int i = 0; i < 49; ++i) before = s.next(10.0f).level[LEFT];   // 490 ms
  at_kick = s.next(10.0f).level[LEFT];                               // 500 ms: kick
  TEST_ASSERT_TRUE(at_kick > before + 0.1f);
}

void test_disabled_is_silent() {  // R-051
  SynthAudio s;
  s.set_enabled(false);
  const AudioFrame f = s.next(10.0f);
  TEST_ASSERT_EQUAL_FLOAT(0.0f, f.level[LEFT]);
  TEST_ASSERT_EQUAL_FLOAT(0.0f, f.level[RIGHT]);
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_levels_stay_in_range_and_move);
  RUN_TEST(test_has_beats);
  RUN_TEST(test_disabled_is_silent);
  return UNITY_END();
}
