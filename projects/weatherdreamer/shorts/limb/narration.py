"""Short: limb. Facts: §3.3, §3.6, §4.4, Figs. 9, S7 of arXiv:2611.18393v1, via projects/weatherdreamer/AGENTS.md."""
VOICE = 'michael'
SPEED = 1.0

SCENES = [
    dict(scene='LimbSlant', headline='Satellites see colder at the *edge*', hold=0.5, beats=[
        (0.3, 'A satellite looking straight down sees deep into the air. Looking at a slant, its view crosses more atmosphere, and sees higher, colder layers.'),
        (8.0, 'So images go cold toward the edges, with seams where one satellite hands off to the next.'),
    ]),
    dict(scene='LimbFix', headline='Satellites see colder at the *edge*', hold=2.4, beats=[
        (0.3, "This weather model is told each view's angle, and can redraw any view as if looking straight down."),
        (6.0, 'That removes eighty-three to ninety-six percent of the edge cooling, from about six degrees in a clear window channel to twenty-two in an ozone channel.'),
        (14.0, 'The stripes vanish. It learned this because the same spot is often seen from two angles at once. What else could disagreement teach a model?'),
    ]),
]
