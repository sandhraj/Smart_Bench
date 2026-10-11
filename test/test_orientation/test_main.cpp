#include <unity.h>
#include <math.h>
#include "orientation.h"

using namespace vu;

static const Vec3 kO1 = {0, 0, 1};  // gravity along z
static const Vec3 kO2 = {1, 0, 0};  // gravity along x

// Vector at `deg` degrees from kO1, tilted toward the y axis (away from kO2).
static Vec3 off_o1(float deg) {
  const float r = deg * 3.14159265f / 180.0f;
  return {0, sinf(r), cosf(r)};
}

void setUp() {}
void tearDown() {}

void test_angle_basic() {
  TEST_ASSERT_FLOAT_WITHIN(0.01f, 0.0f, angle_deg(kO1, kO1));
  TEST_ASSERT_FLOAT_WITHIN(0.01f, 90.0f, angle_deg(kO1, kO2));
  TEST_ASSERT_FLOAT_WITHIN(0.01f, 180.0f, angle_deg({0, 0, 0}, kO1));
}

void test_classify_within_and_beyond_25_degrees() {  // R-002, R-003
  const Vec3 stored[2] = {kO1, kO2};
  TEST_ASSERT_EQUAL_INT(0, classify(off_o1(0), stored, 2));
  TEST_ASSERT_EQUAL_INT(0, classify(off_o1(24), stored, 2));
  TEST_ASSERT_EQUAL_INT(-1, classify(off_o1(26), stored, 2));
  TEST_ASSERT_EQUAL_INT(-1, classify({0, 1, 0}, stored, 2));  // 90 deg from both
}

void test_classify_picks_nearest() {
  const Vec3 stored[2] = {kO1, kO2};
  const Vec3 v = {0.9f, 0, 0.3f};  // closer to kO2
  TEST_ASSERT_EQUAL_INT(1, classify(v, stored, 2));
}

void test_switch_only_after_1s() {  // R-004
  OrientationTracker t;
  t.set_stored(0, kO1);
  t.set_stored(1, kO2);
  TEST_ASSERT_EQUAL_INT(-1, t.update(kO1, 0));      // candidate starts at t=0
  TEST_ASSERT_EQUAL_INT(-1, t.update(kO1, 999));    // 0.999 s: not yet
  TEST_ASSERT_EQUAL_INT(0, t.update(kO1, 1000));    // 1.000 s: switched
  TEST_ASSERT_EQUAL_INT(0, t.update(kO2, 2000));    // new candidate, timer restarts
  TEST_ASSERT_EQUAL_INT(0, t.update(kO2, 2900));    // 0.9 s: no switch
  TEST_ASSERT_EQUAL_INT(1, t.update(kO2, 3000));    // 1.0 s: switch
}

void test_interrupted_candidate_restarts_timer() {  // R-004
  OrientationTracker t;
  t.set_stored(0, kO1);
  t.set_stored(1, kO2);
  t.update(kO1, 0);
  t.update(kO1, 1000);                  // active = 0
  t.update(kO2, 2000);                  // candidate 1
  t.update(kO1, 2500);                  // flick back to active: candidate cleared
  t.update(kO2, 2600);                  // candidate 1 again, timer from 2600
  TEST_ASSERT_EQUAL_INT(0, t.update(kO2, 3500));  // only 0.9 s
  TEST_ASSERT_EQUAL_INT(1, t.update(kO2, 3600));
}

void test_unmatched_keeps_layout() {  // R-003
  OrientationTracker t;
  t.set_stored(0, kO1);
  t.set_stored(1, kO2);
  t.update(kO1, 0);
  t.update(kO1, 1000);                                  // active = 0
  TEST_ASSERT_EQUAL_INT(0, t.update({0, 1, 0}, 5000));  // far from both
  TEST_ASSERT_EQUAL_INT(0, t.update({0, 1, 0}, 9000));
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_angle_basic);
  RUN_TEST(test_classify_within_and_beyond_25_degrees);
  RUN_TEST(test_classify_picks_nearest);
  RUN_TEST(test_switch_only_after_1s);
  RUN_TEST(test_interrupted_candidate_restarts_timer);
  RUN_TEST(test_unmatched_keeps_layout);
  return UNITY_END();
}
