# Control perfboard

Board B of the VU speaker. Single-sided dot perfboard with the same outline as the power board: 97.8 x 59.8 mm, mounting holes 3 mm at 75 x 54.7 mm centres, 38 x 23 holes at 2.54 mm (hole count assumed from the outline; check against the real board before soldering).

- `wiring.md`: connector pinouts, every jumper wire and solder bus, hole by hole.
- `BOM.csv`: parts list.
- `perfboard-viewer.html`: open in a browser for layer, net and view toggles.
- `top.svg`, `bottom.svg`: component side and solder side.
- `wiring.json`: the routed design the other files are generated from.

Pin assignments and circuits are defined in `docs/SPEC.md` (ESP32 pin map, Mute drive, VU audio tap, Key presses into the amp). The layout follows the marked-up placement: panel leads and amp inputs along the top, 5 V input with the VIN Schottky top left, level shifter and relay and strip terminals bottom left, optocouplers bottom centre, GY-45 under the right-hand header pins.
