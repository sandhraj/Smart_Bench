#include <unity.h>
#include "cmd_parser.h"

using namespace vu;

void setUp() {}
void tearDown() {}

void test_digits_are_white_at_tens_of_percent() {  // B-002
  for (char c = '0'; c <= '9'; ++c) {
    Parsed p = parse_key(c);
    TEST_ASSERT_TRUE(p.cmd == Cmd::White);
    TEST_ASSERT_TRUE(p.has_brightness);
    TEST_ASSERT_EQUAL_UINT8((c - '0') * 10, p.brightness_pct);
  }
}
void test_f_is_full_white() {
  Parsed p = parse_key('f');
  TEST_ASSERT_TRUE(p.cmd == Cmd::White);
  TEST_ASSERT_EQUAL_UINT8(100, p.brightness_pct);
}
void test_w_is_white_without_brightness_change() {
  Parsed p = parse_key('w');
  TEST_ASSERT_TRUE(p.cmd == Cmd::White);
  TEST_ASSERT_FALSE(p.has_brightness);
}
void test_colour_and_mode_keys() {
  TEST_ASSERT_TRUE(parse_key('r').cmd == Cmd::Red);
  TEST_ASSERT_TRUE(parse_key('g').cmd == Cmd::Green);
  TEST_ASSERT_TRUE(parse_key('b').cmd == Cmd::Blue);
  TEST_ASSERT_TRUE(parse_key('x').cmd == Cmd::Rainbow);
  TEST_ASSERT_TRUE(parse_key('p').cmd == Cmd::Walk);
  TEST_ASSERT_TRUE(parse_key('o').cmd == Cmd::Off);
  TEST_ASSERT_TRUE(parse_key('c').cmd == Cmd::ToggleCap);
  TEST_ASSERT_TRUE(parse_key('s').cmd == Cmd::Status);
}
void test_unknown_ignored() {  // B-003
  const char junk[] = {'z', ' ', '\n', '\r', 'F', '#', 0};
  for (char c : junk) TEST_ASSERT_TRUE(parse_key(c).cmd == Cmd::None);
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_digits_are_white_at_tens_of_percent);
  RUN_TEST(test_f_is_full_white);
  RUN_TEST(test_w_is_white_without_brightness_change);
  RUN_TEST(test_colour_and_mode_keys);
  RUN_TEST(test_unknown_ignored);
  return UNITY_END();
}
