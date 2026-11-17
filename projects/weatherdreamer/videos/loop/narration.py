"""The Forecaster With No Answer Key: what Bella says over each scene. Beats are (visual_time, text), pointed at the
moment the visual appears in the scene's authored timeline (scenes1.py, scenes2.py). Facts: arXiv:2611.18393v1
(section, figure or table noted per scene); numbers and caveats in projects/weatherdreamer/AGENTS.md.
Story: the forecast's starting picture ("now") as the thing nobody can see; the old hand-built loop; an apprentice
that learns the loop with no answer key; it works near the ground; the turn (higher up), its two causes; reading the
scoreboard fairly; the payoff (an hourly picture of now on one GPU) and the honest limit (no continuous cycling yet)."""

VOICE = 'bella-nicole'
SPEED = 1.0
LANG = 'a'
SAY = {
    'Kalman': 'Kahlman',
}

SCENES = [
    # §1: every forecast starts from an analysis; sparse, indirect observations; DA is the expensive step
    dict(scene='ColdOpen', smax=1.4, hold=0.5, beats=[
        (0.8, "Every weather forecast starts from a picture of the atmosphere right now."),
        (5.0, "But nobody can see right now. Stations dot the land. Balloons rise twice a day. Satellites sweep past in narrow stripes."),
        (13.5, "Turning those scattered clues into one picture is the slow, expensive step that every forecast waits for."),
        (20.5, "So here is the question. Can a machine learn to see the present, with no answer key?"),
    ]),
    dict(scene='Title', hold=0.9, vend=8.0, beats=[
        (0.7, "This paper, by Kate Duffy and her colleagues at Zeus AI, builds a world model that learns from the observations alone."),
    ]),
    # §2.1, Table 1: ~11,000 ISD stations; ~650 soundings at 00 and 12 UTC; satellites measure radiances (§1)
    dict(scene='Clues', hold=0.5, vend=26.5, beats=[
        (0.6, "Start with the clues. About eleven thousand surface stations report every hour, but only on land, and only near the ground."),
        (8.5, "About six hundred and fifty weather balloons climb through the whole atmosphere, twice a day."),
        (14.5, "And satellites see nearly everything, but they don't measure temperature or wind. They measure light, glowing from a deep column of air."),
        (23.5, "Sparse, irregular, indirect."),
    ]),
    # §1: DA, analysis, 6-hourly and hours late, hand-built operators; MLWP starts from analyses
    dict(scene='Analysis', hold=0.5, vend=27.0, beats=[
        (0.6, "Turning clues into a full state of the atmosphere is called data assimilation. Its output is the analysis."),
        (7.5, "Global centres run it every six hours, with hand-built models for every instrument, and the result arrives hours late."),
        (15.0, "Machine learning forecasters now rival the physics models. But most of them start from that physics-built analysis."),
        (23.0, "They learned to forecast. They never learned to see."),
    ]),
    # §3.1, Eq. 1-3 (Kalman 1960); scalar gain as an illustration
    dict(scene='Kalman', hold=0.5, beats=[
        (0.6, "Assimilation is a loop: predict, then correct."),
        (4.0, "Run the last analysis forward to get a background, the forecast of now."),
        (9.5, "Compare it with new observations, and move toward them by a gain."),
        (15.0, "Say the forecast reads twenty degrees and a thermometer twenty-two. If the thermometer is the more reliable of the two, move most of the way."),
        (24.0, "Rudolf Kalman wrote this down in 1960. Operational systems still set every error by hand."),
    ]),
    # §3.1-3.6, Eq. 4-7: memory h (512), latent z (64), prior = background, posterior = analysis, decoders = H
    dict(scene='Dreamer', hold=0.5, beats=[
        (0.6, "This model learns every piece of that loop instead."),
        (4.5, "Each cell of a fifty kilometre grid carries a wide memory, five hundred and twelve numbers, and a narrow latent state, sixty-four numbers."),
        (12.5, "Each hour, the memory steps forward and guesses the latent state. That's the background."),
        (18.5, "Then new observations arrive, and an attention step, reading them through the memory, corrects it. That's the analysis."),
        (26.0, "Decoders translate the latent state into what any instrument would see, anywhere. Nobody writes down the gain."),
    ]),
    # §1, §2, Fig. 1: no reanalysis; 18 observing systems; 2020-2023
    dict(scene='NoKey', hold=0.5, beats=[
        (0.6, "And there is no answer key. It trains on four years of raw observations from eighteen observing systems."),
        (7.5, "No reanalysis, the physics-built record that most AI weather models learn from, and whose biases they inherit."),
        (14.5, "From one shared latent state, it can paint stations, balloons and satellite channels across the whole globe."),
        (21.5, "Earlier models also skipped reanalysis, but built each forecast in one pass, with no running memory. Keeping the loop is what's new."),
    ]),
    # §3.7, Eq. 15-18: reconstruction with masking (weights 1/2/3), prior matching, CRPS rollout
    dict(scene='Lessons', hold=0.5, beats=[
        (0.6, "Three lessons train it. One: rebuild what the instruments saw, including whole instruments hidden on purpose."),
        (8.5, "Two: make the guess before each hour match the picture after it. The only way is to anticipate the observations."),
        (16.5, "Three: run alone for hours, as an ensemble, scored on how well its spread of futures matches what happened."),
    ]),
    # §4.1, Fig. 4: 534 held-out stations; wind CRPS 1.09 / 1.31 / 1.15; T2m best 8 h; spread-skill
    dict(scene='Surface', hold=0.5, beats=[
        (0.6, "Does it work? At five hundred and thirty-four stations it never sees, forecasts run twelve hours ahead."),
        (7.5, "For wind, it beats both the American and the European ensembles at every hour."),
        (13.0, "For temperature, it beats the American one throughout, and the European one for eight hours, before the European ensemble pulls ahead."),
        (21.0, "And its spread of possible outcomes matches its real errors far better than either, though all three are still overconfident."),
    ]),
    # §4.2: precipitation (best to +6 h, two-thirds, smooth); cloud top vs EarthCARE (r, RMSE, FAR)
    dict(scene='Unseen', hold=0.5, beats=[
        (0.6, "Rain, sunlight and cloud tops are never fed in. It reads them out of the latent state."),
        (6.5, "For rain, it's the best ensemble for six hours, though too dry and too smooth."),
        (13.0, "Cloud tops, checked against a radar and laser satellite it never trained on, come out a little more accurate than the operational product. It raises half the false alarms, though it misses a little more real cloud."),
    ]),
    # §4.3.2, Table 2; §4.1 SLP; accuracy notes (4.6 not 5; 2.62 is averaged)
    dict(scene='Aloft', hold=0.5, beats=[
        (0.6, "But here is the turn. Compare its forecasts a few hours ahead with NOAA's own assimilation, on the same observations."),
        (8.0, "At surface stations, the two are within about ten percent."),
        (11.5, "Higher up, it falls behind. Balloon winds are two point six times worse on average, and satellite temperature channels up to about four and a half times."),
        (21.0, "Air pressure at the surface is a clear weakness too. In fairness, NOAA's system reads far more instruments, with decades of tuning behind it."),
    ]),
    # §5: patches of ~1,600 km; our arithmetic (labelled on screen)
    dict(scene='Walls', hold=0.5, beats=[
        (0.6, "The paper names two causes. First, the dynamics run on patches about one thousand six hundred kilometres wide, each with its own memory."),
        (9.0, "Our own arithmetic: a jet stream wind of fifty metres a second crosses a patch in about nine hours."),
        (16.0, "Surface winds move only a few hundred kilometres in twelve. And the paper's point: the large, slow circulation that steers winds aloft and pressure does not fit inside one patch."),
    ]),
    # §4.3.3, Fig. 8: radiosonde gains 0.1-0.26 at 100-300 hPa; RO near zero
    dict(scene='Listening', hold=0.8, vend=16.5, beats=[
        (0.6, "Second, it barely listens up there."),
        (3.5, "Near the jet stream, it moves only a tenth to a quarter of the way toward balloon readings, and almost not at all toward radio occultation."),
        (13.0, "It leans only lightly on the clues it needed most."),
    ]),
    # S6.2 latency; §4.1 MAE vs CRPS; §5 held-out neighbours; §4.1 no-station run
    dict(scene='Scoreboard', hold=0.5, beats=[
        (0.6, "Read the scoreboard with care. Its analysis is fresh every hour, while the operational forecasts are already five to seven hours old."),
        (9.0, "That measures real-world usefulness, not the forecasting engine. The European ensemble, starting at least seven hours earlier, still overtakes it on temperature."),
        (17.5, "Much of its edge comes from ensemble spread, not a better average. And many of the hidden stations have neighbours it did see."),
        (25.5, "Still, with every surface station removed, it beats the American ensemble for temperature out to eleven hours, and for wind to twelve."),
    ]),
    # §5: 1.5 min per hourly global step on one H100 (half reading data); 11 min ensemble; zero-state 12 h windows
    dict(scene='Speed', hold=0.5, beats=[
        (0.6, "And it's cheap. One global hourly update takes about a minute and a half on a single GPU, and half of that is just reading the data."),
        (8.5, "A twelve-hour ensemble forecast takes eleven minutes."),
        (12.0, "One honest limit. Every run starts from an empty memory and twelve hours of catching up. Keeping the loop running for weeks is still to come."),
    ]),
    # our questions
    dict(scene='Questions', vend=21.0, hold=1.5, beats=[
        (0.5, "A few questions to think about."),
        (2.0, "Does a model trained only on observations inherit our instruments' habits, the way reanalysis passes on a physics model's?"),
        (9.0, "How would you teach it to listen to rare, precise instruments high up?"),
        (14.5, "Could a learned picture of the present one day start the models that simulate climate?"),
    ]),
    dict(scene='End', hold=2.4, vend=11.0, beats=[
        (0.6, "The takeaway: a forecast loop can be learned from the clues alone. Near the ground it already sees well. Up high, it still has to learn to listen."),
    ]),
]
