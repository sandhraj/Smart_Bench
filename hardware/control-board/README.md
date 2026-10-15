# Control perfboard (board B)

Single-sided dot perfboard, same outline as the power board: 97.8 x 59.8 mm, landscape, 38 x 23 holes at 2.54 mm, mounting holes 3 mm at 75 x 54.7 mm centres (hole count assumed from the outline; check against the real board before soldering). Placement follows the marked-up mock (`Pics/PXL_20261014_203840603~2.jpg`), pin assignments follow `Pics/image.png` and `docs/SPEC.md`.

## Files

| File | What it is |
|---|---|
| `wiring.md` | Connector pinouts, every top jumper, under-board jump and solder bridge, hole by hole, plus parts and nets |
| `BOM.csv` | Parts list |
| `top.png`, `bottom.png` | Component side and solder side (solder side is mirrored, as you see it when the board is flipped) |
| `top.svg`, `bottom.svg`, `perfboard-viewer.html` | Same as vector, with a net highlighter |
| `wiring.json` | The routed design as data |
| `kicad/Perfboard.pretty/` | KiCad footprint of this perfboard: 38 x 23 pads, 3 mm mounting holes, names are column letter + row |
| `kicad/control-board.kicad_pcb` | The footprint with the placement, solder bridges as tracks and jumpers on `User.1` (top) and `User.2` (under) |
| `gen/` | Python that builds all of the above from the placement (`design.py`) and the route list (`manual.py`) |

## Layout

- ESP32 DevKit on two 2 x 15 sockets in the middle, USB at the left. Low parts (flat resistors, the pull-up, the VU tap parts) sit under the module, as do many jumpers.
- Above the top header row: logic power in, 100 uF, 100 nF and the VIN Schottky at the left; panel button leads in the middle; amp tap and the Bluetooth LED sense stack at the right.
- Below the bottom header row: level shifter at the left, optocouplers in the middle with the key output header under them, GY-45 on its header under the right-hand pins (D21 to D23).
- Left edge, top to bottom: 5 V logic in, strip data, 5 V LED in, relay module.

## Wire types

Solder bridge (adjacent holes, at most 5 in a chain), top jumper (insulated, component side, straight, both ends in free holes), under-board jump (insulated, solder side, at most 6 holes). The checker in `gen/` confirms no two nets touch and every net is in one piece; KiCad DRC on `kicad/control-board.kicad_pcb` reports 0 violations (52 unconnected items are the jumper connections, which KiCad does not model).

## Rebuild

```
cd hardware/control-board/gen
python3 run.py            # placement + route check, ASCII map
python3 emit.py ..        # wiring.md, BOM.csv, wiring.json, svg, png, viewer
python3 kicad_emit.py ../kicad
kicad-cli pcb drc ../kicad/control-board.kicad_pcb
```

## Things to check before soldering

1. Hole count and mounting-hole positions on the real board (the power-board dimensions were taken from the spec).
2. GY-45 header order, assumed INT1, INT2, SA0, SDA, SCL, GND, 3.3 V, VCC-IN from the left with the module body below. The module's own 3.3 V pin is not connected.
3. CN7 is a plain 1x6 pin header; a JST-XH housing there would sit on the DIP-8 socket.
4. Amp key-pad voltages (which pad is the ground side) before wiring CN7, per the spec.
