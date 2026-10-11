// Display controller: pattern list, selection, automatic standby. Pure logic.
#pragma once
#include "standby.h"
#include "style.h"
#include "style_gravity.h"
#include "style_peak_bar.h"
#include "style_vu_bar.h"
#include "style_zone_bar.h"

namespace vu {

constexpr int kPatternCount = 5;
constexpr int kPatternStandby = 4;  // forced standby; automatic standby overlays any pattern

class DisplayController {
 public:
  DisplayController();
  static const char* name(int index);
  void select(int index);
  void next();
  int selected() const { return selected_; }
  void update(const AudioFrame& f, float dt_ms);
  void render(Orientation o, Rgb* out) const;
  bool standby_active() const;

 private:
  StyleVuBar vu_;
  StylePeakBar peak_;
  StyleZoneBar zone_;
  StyleGravityDot gravity_;
  Style* styles_[kPatternCount];  // [kPatternStandby] is null
  int selected_;
  float silence_ms_;
  float t_ms_;
};

}  // namespace vu
