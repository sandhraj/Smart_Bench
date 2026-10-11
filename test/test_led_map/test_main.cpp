#include <unity.h>
#include "led_map.h"

using namespace vu;

void setUp() {}
void tearDown() {}

static void expect_bar(Orientation o, Channel c, int first, int last) {
  TEST_ASSERT_EQUAL_INT(first, bar_index(o, c, 0));
  TEST_ASSERT_EQUAL_INT(last, bar_index(o, c, kBarLeds - 1));
}

void test_o1_left_seg10_forward() { expect_bar(O1, LEFT, 67, 86); }    // R-010
void test_o1_right_seg5_reversed() { expect_bar(O1, RIGHT, 50, 31); }  // R-010
void test_o2_left_seg5_forward() { expect_bar(O2, LEFT, 31, 50); }     // R-011
void test_o2_right_seg10_reversed() { expect_bar(O2, RIGHT, 86, 67); } // R-011

void test_bars_stay_in_chain_and_do_not_overlap() {
  for (int o = 0; o < 2; ++o) {
    bool seen[kNumLeds] = {false};
    for (int c = 0; c < 2; ++c) {
      for (int k = 0; k < kBarLeds; ++k) {
        int i = bar_index(static_cast<Orientation>(o), static_cast<Channel>(c), k);
        TEST_ASSERT_TRUE(i >= 0 && i < kNumLeds);
        TEST_ASSERT_FALSE(seen[i]);
        seen[i] = true;
      }
    }
  }
}

void test_out_of_range_k() {
  TEST_ASSERT_EQUAL_INT(-1, bar_index(O1, LEFT, -1));
  TEST_ASSERT_EQUAL_INT(-1, bar_index(O1, LEFT, kBarLeds));
}

void test_lit_count_ends() {  // R-012
  TEST_ASSERT_EQUAL_INT(0, lit_count(0.0f));
  TEST_ASSERT_EQUAL_INT(20, lit_count(1.0f));
  TEST_ASSERT_EQUAL_INT(0, lit_count(-0.5f));
  TEST_ASSERT_EQUAL_INT(20, lit_count(3.0f));
}

void test_lit_count_rounds_to_nearest() {
  TEST_ASSERT_EQUAL_INT(10, lit_count(0.5f));
  TEST_ASSERT_EQUAL_INT(1, lit_count(0.03f));  // 0.6 LED rounds to 1
  TEST_ASSERT_EQUAL_INT(0, lit_count(0.02f));  // 0.4 LED rounds to 0
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_o1_left_seg10_forward);
  RUN_TEST(test_o1_right_seg5_reversed);
  RUN_TEST(test_o2_left_seg5_forward);
  RUN_TEST(test_o2_right_seg10_reversed);
  RUN_TEST(test_bars_stay_in_chain_and_do_not_overlap);
  RUN_TEST(test_out_of_range_k);
  RUN_TEST(test_lit_count_ends);
  RUN_TEST(test_lit_count_rounds_to_nearest);
  return UNITY_END();
}
