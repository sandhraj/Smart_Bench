#include <unity.h>
#include "level.h"

using namespace vu;

void setUp() {}
void tearDown() {}

void test_full_scale_is_one() { TEST_ASSERT_FLOAT_WITHIN(0.001f, 1.0f, level_from_amplitude(1.0f)); }      // R-040
void test_minus_20_db_is_half() { TEST_ASSERT_FLOAT_WITHIN(0.001f, 0.5f, level_from_amplitude(0.1f)); }   // R-040
void test_minus_40_db_is_zero() { TEST_ASSERT_FLOAT_WITHIN(0.001f, 0.0f, level_from_amplitude(0.01f)); }  // R-040
void test_clamped() {                                                                                    // R-040
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.0f, level_from_amplitude(0.0f));
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.0f, level_from_amplitude(-1.0f));
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 0.0f, level_from_amplitude(0.0001f));
  TEST_ASSERT_FLOAT_WITHIN(0.0001f, 1.0f, level_from_amplitude(4.0f));
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_full_scale_is_one);
  RUN_TEST(test_minus_20_db_is_half);
  RUN_TEST(test_minus_40_db_is_zero);
  RUN_TEST(test_clamped);
  return UNITY_END();
}
