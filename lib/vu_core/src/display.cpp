#include "display.h"
#include "button.h"

namespace vu {

DisplayController::DisplayController() : selected_(0), silence_ms_(0.0f), t_ms_(0.0f) {
  styles_[0] = &vu_;
  styles_[1] = &peak_;
  styles_[2] = &zone_;
  styles_[3] = &gravity_;
  styles_[kPatternStandby] = nullptr;
}

const char* DisplayController::name(int index) {
  static const char* const names[kPatternCount] = {"VU bar", "Peak bar", "Zone bar",
                                                    "Gravity dot", "Standby"};
  if (index < 0 || index >= kPatternCount) return "?";
  return names[index];
}

void DisplayController::select(int index) {
  if (index < 0 || index >= kPatternCount) return;
  selected_ = index;
  if (styles_[index]) styles_[index]->reset();
}

void DisplayController::next() { select(next_pattern(selected_, kPatternCount)); }

void DisplayController::update(const AudioFrame& f, float dt_ms) {
  t_ms_ += dt_ms;
  const float loud = f.level[LEFT] > f.level[RIGHT] ? f.level[LEFT] : f.level[RIGHT];
  if (loud > kNoiseFloor) {
    silence_ms_ = 0.0f;
  } else {
    silence_ms_ += dt_ms;
  }
  if (styles_[selected_]) styles_[selected_]->update(f, dt_ms);
}

bool DisplayController::standby_active() const {
  return selected_ == kPatternStandby || silence_ms_ > kStandbyAfterMs;
}

void DisplayController::render(Orientation o, Rgb* out) const {
  if (standby_active() || !styles_[selected_]) {
    render_standby(t_ms_, out);
  } else {
    styles_[selected_]->render(o, out);
  }
}

}  // namespace vu
