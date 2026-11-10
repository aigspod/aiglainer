# Episode 28 art: prompt

For `aigspod.github.io/images/ep028.png` (the feed already points there). Match the felt-robot series in
`images/thumbs/ep024.jpg`-`ep027.jpg`: the same small needle-felted robot, the same night-time, lamp-lit, handmade look.

## Prompt

A square illustration, 1:1, at least 1400 x 1400 px. A small needle-felted wool robot, cream and oatmeal felt with
visible fibres, a round head with dark felt ear discs like headphones, stubby striped arms and a brass rivet or two,
sits at an old wooden desk at night, seen from slightly behind and to one side, so we see the back of its head and
what it is looking at. A brass desk lamp casts a warm amber pool of light; behind, a window full of stars over dark
hills, deep blue and near-black. Shallow depth of field, soft film grain, cozy and quiet, like a stop-motion set.

On the desk in front of the robot: a small handmade spring-and-weight toy, a coiled brass spring hanging from a little
wooden frame with a felted weight at the bottom, caught mid-bounce. A thin glowing amber thread rises from the weight
and traces a smooth closed loop in the air above the desk, slightly lopsided like a limit cycle, softly glowing like
fairy lights. Along the thread, just before it joins the loop, five tiny glowing beads sit in a row, evenly spaced,
the last one brightest. The robot reaches one felt hand toward the loop, curious. A spool of brass wire and a
pair of tweezers lie nearby; a felt mug sits at the edge of the light.

Lettering at the top centre, in thin, widely tracked white capitals in a clean sans-serif: "THE AIGS POD", and
beneath it, smaller and also widely tracked: "EP 28". No other text anywhere.

## Avoid

Any other words, numbers, equations or labels; logos; charts or anything copied from the paper's figures; photo
realism; harsh or cool lighting; a cluttered desk; the robot facing the camera.

## Checks before committing the image

- 1400 x 1400 px PNG at `images/ep028.png` (the site's pre-commit hook fails anything smaller).
- Make the web thumbnail with `sh tools/make_thumbs.sh`, which writes `images/thumbs/ep028.jpg` (the hook does it
  too when enabled).
- The lettering reads "THE AIGS POD" and "EP 28" exactly; image generators often misspell it, so fix or regenerate.
