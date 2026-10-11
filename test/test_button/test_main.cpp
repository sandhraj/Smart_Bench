#include <unity.h>
#include "button.h"

using namespace vu;

void setUp() {}
void tearDown() {}

void test_tap_below_400ms() {  // R-020
  TEST_ASSERT_TRUE(classify_press(0) == Press::Tap);
  TEST_ASSERT_TRUE(classify_press(399) == Press::Tap);
}
void test_hold_at_and_above_400ms() {  // R-020
  TEST_ASSERT_TRUE(classify_press(400) == Press::Hold);
  TEST_ASSERT_TRUE(classify_press(5000) == Press::Hold);
}
void test_button4_short_cycles_pattern() {  // R-021
  TEST_ASSERT_TRUE(classify_button4(100) == Button4Action::NextPattern);
  TEST_ASSERT_TRUE(classify_button4(2999) == Button4Action::NextPattern);
}
void test_button4_long_teaches() {  // R-005
  TEST_ASSERT_TRUE(classify_button4(3000) == Button4Action::Teach);
}
void test_pattern_wraps() {  // R-021, R-022 (bar, spectrum)
  TEST_ASSERT_EQUAL_INT(1, next_pattern(0, 2));
  TEST_ASSERT_EQUAL_INT(0, next_pattern(1, 2));
  TEST_ASSERT_EQUAL_INT(0, next_pattern(5, 0));
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_tap_below_400ms);
  RUN_TEST(test_hold_at_and_above_400ms);
  RUN_TEST(test_button4_short_cycles_pattern);
  RUN_TEST(test_button4_long_teaches);
  RUN_TEST(test_pattern_wraps);
  return UNITY_END();
}
