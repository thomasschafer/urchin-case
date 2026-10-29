# Handoff: fold-flat tenting case for the Urchin keyboard

This is a handoff from a brainstorming session to whoever picks up the design next. It covers what Tom wants, what we decided and why, the current concept with its numbers, and what is still open. Read it in full before starting. Then open `viewer/index.html` in a browser and play with it, because most of the reasoning is easier to see than to read.

Status: concept agreed in principle, no CAD yet. The next step is to get answers to the open questions below from Tom, then build a parametric CAD model.

## The keyboard

- Urchin: a 34-key wireless split by duckyb, ZMK on a nice!nano v2 (https://github.com/duckyb/urchin). We worked from commit `02b1ab1315f3560f637eeaa8f375541f4fa621b9` (MIT licence).
- Tom's unit is the pre-soldered one from beekeeb (https://shop.beekeeb.com/products/soldered-urchin-wireless-split-keyboard), bought without a case.
- Kailh Choc v1 switches in hotswap sockets, MBK keycaps, a nice!view display on each half. Which Choc v1 switch is not yet known.
- Nothing protrudes from the PCB underside except the hotswap sockets (Tom confirmed). There is no switch plate at the moment.

## What Tom wants, and why

- Fold flat: non-negotiable. He carries it to the office and back three days a week.
- Fixed tent of about 75°. He thinks it is 75°, not the 70° he first said, and will measure the exact angle before anything is ordered. A fixed angle is fine; no adjustment is needed.
- Going from flat to tented and back has to be quick and tool-free.
- Nothing that relies on friction to hold the angle. His current setup is a tenting puck on a Z-fold camera mount, and the hinge works loose so he has to retighten it with an allen key.
- Very stable. This came up as a direct concern: the Z-fold has a base almost as long as the keyboard, and when typing gently he doesn't even need anything between the halves. That is the benchmark.
- The PCB enclosed. This is his main complaint about the current setup; the puck and mount rule out off-the-shelf cases.
- Clean, integrated, good-looking.
- The pinky edge goes down and should sit very low. Currently the bottom of the board is a millimetre or two off the desk, his hands rest on the desk at the sides, and his little fingers end up on the outside of each half. 11 mm from desk to the lowest key was too high; the current concept gets about 6.8 mm. Ask whether that is acceptable (see open questions).
- The halves stay separate, never joined. He keeps a laptop case lying between them, which stops them sliding towards each other.
- He has no 3D printer and doesn't want one, so parts are ordered online. He is in south-west London. No fixed budget, but cheaper is better. He is happy to wait for shipping from China, and can assemble with simple tools.

## Decisions so far

Each of these was discussed with Tom. Revisit any of them if new information warrants it, but say so rather than quietly changing direction.

1. A fixed triangle plus a hard stop holds the angle. Hinges swing freely on steel pins and never carry the angle through friction, so nothing loosens.
2. A plain kickstand was rejected on stability. At 75° a keypress pushes each half almost sideways, about 15° below horizontal, from up to 100 mm high, so the failure mode is tipping inward over the innermost support. A kickstand's foot is only about 50 mm in from the pivot and adds little mass. The estimate was that it tips at about 55 gf on the worst key (62 gf with a steel kickstand), less than a firm keystroke. It only seemed fine because the laptop case was propping it.
3. A base plate with a strut was adopted. This was Tom's suggestion. The base moves the tipping edge out to about 110 mm and carries weight. A 3 mm steel plate the size of the case weighs roughly 200 g.
4. Base on top of the case was superseded, because the hinge sitting on top of 3 mm of steel plus feet put the lowest key at about 11 mm.
5. The current concept is the sunk base, described below. It brings the lowest key down to about 6.8 mm and the folded thickness to about 17 mm, with similar stability.
6. Nothing may protrude between the case and the base when folded. An earlier raised slot lip on the base would have blocked the fold (Tom spotted it). Use recesses and through-cuts only.

## Current concept: sunk base

In the viewer this is the default concept ("Sunk base"). The numbers are the viewer's defaults.

- Case: a printed tray screwed to the PCB's M2 mounting points. Its top surface doubles as an integrated switch plate, which encloses the PCB and adds stiffness the hotswap-only build lacks. The nice!nano and nice!view get a cover with a screen window.
- Steel base plate: about 3 mm, laser-cut to the case footprint inset by about 2.6 mm. It sits flush inside a recess in the case bottom, with the case forming a thin rim around it.
- Main hinge: along the straight pinky-side edge of the PCB (about 50 mm long), set in about 2.6 mm from the case's outer face, with the case's outer bottom corner bevelled at the tent angle so the case can roll over it. The pin sits at about the plate's mid-thickness so the knuckles don't hang below the plate.
- Strut: the piece laser-cut out of a window in the base plate, so it costs no extra steel. In the viewer it is 40 mm wide and 54 mm long, hinged on the plate 50 mm in from the main hinge. Folded, it lies flush in its window. Raised, it swings about 145° up out of the window and its tip clicks into a groove in the underside of the case, about 31 mm in from the main hinge. It sits about 35° to the base. A magnet in the strut tip holds it.
- Feet: silicone bumpers under the plate. The case's own lowest point is about 2.5 mm off the desk when tented.
- Results at 75°: about 271 g per half. It tips inward at about 330 gf on the worst key and slides at about 290 gf, both without the laptop case. The lowest keycap edge is about 6.8 mm above the desk, the top of the half is about 106 mm high, it folds to about 16.8 mm thick, and the folded footprint is about 116 × 96 mm.

Two side benefits: magnets in the case can hold it shut against the steel plate for carrying, and the steel plate means no separate weights are needed.

## Board facts from the KiCad file

`tools/extract_pcb.py` produces `data/urchin-right-half.json` from the Urchin `main.kicad_pcb`. Things that matter for the design:

- The KiCad file contains both halves joined by mouse bites at x ≈ 128 mm. The part with x < 128 is the right-hand half seen from above. Its inner (thumb) side is at low x and its outer (pinky) side is the straight edge at x = 127.13. The left half is a mirror image.
- Coordinates are KiCad's: millimetres, with x to the right and y downwards (towards the user). The right half spans about 109.5 mm (x 17.6 to 127.1) by 89.6 mm (y 16.2 to 105.8).
- The pinky-side edge is straight from y ≈ 35 to 85, which makes it a natural hinge line.
- The nice!nano and nice!view sit on the top side at the inner edge, next to the thumb keys (nano centre about x 27.0, y 57.9), with USB-C at the back end (low y). When tented that edge is at the top, so USB stays accessible.
- The power switch (`smt-slider-switch`) is on the underside (B.Cu) at about x 27.1, y 41.6, near the back edge by the MCU. The case must leave it reachable. Check which way it actuates and whether the plate or rim covers it.
- The reset button (`SW_RESET`) is on the top at about x 21.2, y 84.4.
- Battery connector pads are at about x 19.2 and 34.8, y 41.3. Battery size and placement in Tom's unit are unknown; ask him. The README mentions 301230 cells, and the jadefalkner case fits a 40 × 20 × 4 mm cell.
- There are mounting holes of two footprint types (`M2_hole_3.5mm` and `M2_hole_4.2mm`) at eight distinct positions on the right half; see the JSON. Check which ones the existing cases use.
- The PCB has a footprint for a tenting puck (`Tenting_Puck2_no_pads`, centre about x 73.8, y 51.6); that's what Tom uses now.
- Useful references in the Urchin repo: `main.step` (3D board model), `plate-case/` (KiCad switch plate and base plate), and `3d-prints/` (community cases with STEP files, e.g. carrefino and iamDrakkir), handy for clearances. The jadefalkner tenting bottom documents its floor and pocket dimensions. The official Coral case is on MakerWorld; check its licence before borrowing anything.

## Assumptions in the viewer to verify

The viewer is a concept tool, not CAD. Every dimension except the board outline, key positions, holes and nano position is a guess:

- Wall plus clearance around the PCB: 3.0 mm. Bevel inset and rim: 2.6 mm.
- Case floor stack: a 4.0 mm recess, a 1.2 mm skin, 2.2 mm socket clearance, then the PCB (1.6 mm assumed) at 7.4 to 9.0 mm.
- Integrated plate top 2.2 mm above the PCB top. MBK keycap bottom 2.0 mm above the plate top, keycap 2.6 mm thick. Check against Choc v1 and MBK datasheets.
- Masses: electronics, switches and keycaps 60 g. Printed case 30 g. Nylon 1.0 g/cm³, steel 7.85 g/cm³.
- Stability model: rigid body at full tent, weight at the combined centre of mass. Each keycap top gets a force along the inward key normal, and we take the worst key's moment about the innermost support edge. "Slides" assumes friction 0.8. The laptop case is ignored in both. Treat the outputs as a comparison between designs, not predictions.

## Open questions for Tom

Ask these before committing to dimensions:

1. A photo of the current setup from the front at desk level, showing one half tented, the laptop case and the gap. Plus the laptop case's height and the distance from each half to it. The strut, base footprint and spacing all depend on this.
2. The weight of one half with its puck and Z-fold mount, and the Z-fold base's dimensions. Running the same stability estimate on the current setup calibrates the target, since Tom knows how it feels.
3. The exact tent angle. He will measure it, e.g. with a phone level app on the keycaps.
4. Whether about 6.8 mm to the lowest key is acceptable. Thinning the pinky-side wall gets about 1 mm back; about 5 to 6 mm is roughly the floor with an enclosed case and a hinge.
5. Which Choc v1 switches he has, for typing force.
6. Battery size and where it sits.
7. Colours and material preferences, and whether the steel should be stainless, zinc-plated or powder-coated (mild steel rusts and laser-cut edges are sharp).

## Problems to solve in CAD

- The strut groove sits under the ring-finger column, where the hotswap sockets leave only about 1 to 1.5 mm of floor. Keep it shallow. A small steel striker plate plus the tip magnet may do more of the holding than the groove does.
- The main hinge knuckles need matching notches in the case rim and the plate edge, and should run the full straight edge. Decide how to attach the knuckles to the steel: printed or metal hinge blocks screwed to the plate, or a cut-down stainless piano hinge.
- The strut hinge also needs a steel-to-hinge method, such as small hinge blocks or an off-the-shelf stainless hinge. Keep it inside the plate thickness, or recess it into the case, so the fold stays flush.
- The plate, window and strut need clearances, so the strut drops into its window without binding and the plate drops into the case recess.
- The power switch and USB must be reachable both tented and folded.
- Magnets: sizes (6×2 or 6×3 mm N52 discs were suggested), positions and polarity, for the strut tip, the strut stowed position and holding the case shut.
- Feet: positions under the plate, and whether the bevel needs a silicone strip.
- Left and right halves are mirror images. Make sure magnets and asymmetric hardware are mirrored correctly.

## Manufacturing and cost

- Printed parts: JLC3DP. MJF nylon (PA12) is tough and doesn't creep under constant load. SLA resin is cheaper and looks good but is brittle at screw bosses and pins. A cheap prototype round first (resin or PLA) is worth it to check fit and the exact angle before final parts.
- Steel plate and strut: laser cutting, e.g. JLC's sheet-metal service or a UK laser cutter. Laser cutting only does through-cuts, so the design must use through-features only (holes, slots, windows). Countersinks and threads would be extra operations.
- Hardware: steel dowel pins for hinges (about 3 mm), M2 screws and heat-set inserts, magnets, silicone bumpers. All cheap from Amazon or first4magnets in the UK.
- Price guesses from the session (not quotes): printed parts plus plates probably a few tens of pounds per round. Get real quotes early.

## The viewer

`viewer/index.html` is a self-contained three.js page. It loads three.js from a CDN, so it needs internet. Open it directly in a browser; no server is needed.

- Concepts: Sunk base (default), Base on top, Kickstand only. Sliders cover tent angle, strut position and length, plate thickness, and laptop case size and gap. It also has X-ray, labels, preset views, follows the system light/dark setting, and shows a live numbers panel with warnings.
- URL hash shortcuts for screenshots: `#view=iso|front|top|back|under|end&t=0..1&mode=nest|base|kick&xray=1&steel=1`.
- `renders/` holds screenshots made like this (macOS, headless Chrome):

  ```sh
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
    --use-angle=swiftshader --enable-unsafe-swiftshader --window-size=1500,1000 \
    --virtual-time-budget=8000 --screenshot=out.png "file://$PWD/viewer/index.html#view=end&t=0.5"
  ```

- The board data is embedded in the page as `const DATA = ...`. If you regenerate `data/urchin-right-half.json`, paste its `outline`, `keys`, `holes` and `nano` fields back in.

## Suggested next steps

1. Get answers to the open questions.
2. Build a parametric model. CadQuery suits an agent well (Python, STEP and STL export, easy to script and check). Drive it from `data/urchin-right-half.json` or the KiCad file, and check against the Urchin `main.step`.
3. Model the folded and tented states as assemblies, and check for interference in both.
4. Redo the stability estimate with real part masses from the CAD.
5. Prepare a prototype order: printed parts plus plates. Tom places all orders himself.
