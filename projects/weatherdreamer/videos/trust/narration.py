"""What Did It Learn to Trust?: what the host says over each scene. Beats are (visual_time, text), visual_time pointing
at the moment in the scene's authored timeline when the thing the line talks about appears.

Facts: arXiv:2611.18393v1 (section, table or figure noted per scene); projects/weatherdreamer/AGENTS.md lists them with
the accuracy notes. "Our reading" and "our arithmetic" are ours and are said to be. Names Whisper can't hear
(Desroziers, Hollingsworth-Lönnberg, EarthCARE, ASCAT, IMERG, GEFS, IFS, GSI) are on screen only.
"""

VOICE = 'am_michael'
SPEED = 1.0
LANG = 'a'
SAY = {}

SCENES = [
    # Fig. S3a (memory h channels at 2024-08-20 00 UTC)
    dict(scene='ColdOpen', smax=1.3, hold=0.6, beats=[
        (0.6, "This is the inside of a weather model's memory, at one moment, spread across the globe."),
        (6.5, "Some of its channels look like weather: swirls, fronts, bands of storms."),
        (11.5, "But look at these. Round footprints. Long diagonal stripes."),
        (16.5, "They mark where satellites were looking: the disks that geostationary satellites see, and the tracks of satellites in polar orbit."),
        (24.5, "Why would a weather model remember where the satellites were looking?"),
    ]),
    dict(scene='Title', hold=0.9, vend=8.0, beats=[
        (0.7, "The model is WeatherDreamer, from Kate Duffy and colleagues at Zeus AI, posted in November 2026."),
        (6.0, "To crack the case, we have to ask what it learned to trust."),
    ]),
    # §1, §3.1 (Eq. 1-7), §2.1 (18 observing systems), no reanalysis, no prescribed error statistics
    dict(scene='CaseFile', hold=0.5, beats=[
        (0.6, "First, the case file. Every weather forecast starts from a best guess of the atmosphere right now, called the analysis."),
        (8.0, "It's built in a loop. Predict the next hour from the last guess, then correct that prediction with whatever the instruments just measured."),
        (16.5, "Weather services run that loop with physics models, and hand-built rules for every instrument."),
        (22.5, "Most AI forecasters start from that physics-built analysis. WeatherDreamer learns the whole loop itself, from raw observations of eighteen observing systems, with no reanalysis to copy, and no table of instrument errors."),
    ]),
    # Eq. 2-3 (Kalman gain from B and R); the thermometer numbers are an illustration
    dict(scene='Gain', hold=0.5, beats=[
        (0.6, "The correct step hides a question of trust. How far should you move toward each new measurement?"),
        (7.0, "Say your forecast reads twenty degrees, and a thermometer reads twenty-two."),
        (12.0, "If the forecast is usually off by one degree, and the thermometer by half a degree, you move eighty percent of the way."),
        (20.5, "That fraction is the gain. Classical systems compute it from error statistics that people specify by hand. This model was never given any."),
    ]),
    # §4.3.3, Text S6.10, Fig. 8a,c
    dict(scene='Diagnostics', hold=0.5, beats=[
        (0.6, "Clue one. Can we read that trust back out of a black box?"),
        (5.5, "There's a classic diagnostic. Compare each measurement with the model's guess before the correction, and after it."),
        (13.0, "How those two misses line up tells you how noisy the model is acting as if that instrument is. A second method, built on how errors spread out in space, gives an independent check."),
        (24.0, "For the microwave channels that sense temperature in clear skies, the answer is two to four tenths of a degree: the measured noise of those instruments in orbit."),
        (33.0, "For satellite winds over the ocean, it lands close to the known error too. Nobody told it either number."),
    ]),
    # §4.3.3, Fig. 8d,f: k 0.64 vs 0.82 (MW temperature sounding), 0.9 vs 0.8 (ASCAT); radiosonde 0.1-0.26 at 100-300 hPa; RO ~0
    dict(scene='Reversal', hold=0.5, beats=[
        (0.6, "Case closed? Not quite."),
        (3.5, "Compare the gain it uses with the best gain those same diagnostics imply."),
        (8.5, "For temperature sounding, it moves sixty-four percent of the way, where eighty-two would be best. Too timid."),
        (16.0, "For ocean winds, about ninety percent, where eighty would be best. Too trusting: a satellite's wind isn't quite the wind across a whole fifty kilometer cell."),
        (26.0, "And higher up, it leans only lightly on what it's told. Balloon temperature and wind near the jet stream move it a tenth to a quarter of the way. Radio occultation, a precise upper-air technique, moves it almost not at all."),
    ]),
    # §4.3.2, Table 2 (SD of O-F, WD / GSI), Table S5 (radiosonde wind by level)
    dict(scene='Departures', hold=0.5, beats=[
        (0.6, "That leaves a trace. Scored against NOAA's operational system, which uses many more instruments and decades of tuning, on the same observations a few hours ahead,"),
        (10.5, "at surface stations its errors are within about ten percent, though satellite winds over the ocean are worse."),
        (17.0, "But for balloon winds, they're two point six times larger on average, and more than three times larger near the jet stream."),
        (25.5, "For the temperature-sounding satellite channels, up to about four and a half times."),
    ]),
    # §5 (two causes); the crossing time is our arithmetic
    dict(scene='Suspects', hold=0.5, beats=[
        (0.6, "The paper names two suspects. One: the correction step draws little from the upper-air clues."),
        (7.0, "Two: the dynamics run on patches about one thousand six hundred kilometers across, each with its own memory, too small to hold the large, slow circulation that steers upper winds and big pressure changes."),
        (17.5, "By our arithmetic, a fifty meter per second wind near the jet stream crosses a patch in about nine hours."),
    ]),
    # §4.4 (limb darkening); §3.3, §3.6 (excess air mass, zero-anchored conditioning); the geometry is an illustration
    dict(scene='Limb', hold=0.5, beats=[
        (0.6, "Clue two is geometry."),
        (3.0, "A satellite looking straight down sees through a short column of air. Looking at a slant, its view crosses more air, and it sees higher, colder layers."),
        (12.5, "So images go cold toward their edges, and seams appear where one satellite hands off to the next."),
        (19.0, "WeatherDreamer is told each view's angle, and can decode its picture at any angle, even straight down. It can learn this because the same spot is often seen from two angles at once."),
    ]),
    # §4.4, Fig. 9b (≈80°: 6, 14, 16, 22 K), 83-96%; Fig. S7e,j crossover slopes
    dict(scene='LimbResult', hold=0.5, beats=[
        (0.6, "Decoded straight down, it removes eighty-three to ninety-six percent of the observed edge cooling."),
        (7.5, "And its correction follows the physics. Near the edge of the disk: about six degrees in the clear window channel, fourteen for water vapor, sixteen for carbon dioxide, twenty-two for ozone. More absorbing air, more correction."),
        (20.5, "Where two microwave satellites cross paths, their readings disagree by thirteen point six degrees per unit of slant. Decoded straight down, by three tenths of a degree."),
    ]),
    # Fig. S7a,c (observed vs nadir decode, ATMS ch 7); §4.4 (parallax remains)
    dict(scene='Stripes', hold=0.5, beats=[
        (0.6, "On the map, the stripes of the satellite tracks simply vanish."),
        (5.5, "One limit: it corrects brightness, not position. Tall clouds seen at a slant still sit slightly out of place."),
    ]),
    # §4.2, Fig. 6 (cloud tops vs EarthCARE), §4.2.1 (precipitation vs IMERG)
    dict(scene='Unseen', hold=0.5, beats=[
        (0.6, "Clue three: things it never sees while forecasting. Cloud tops, rain and sunlight are never inputs. They're read out of its inner state."),
        (9.0, "Against a newer satellite that probes clouds with radar and laser, one it never saw in training, its cloud-top heights correlate at zero point seven three, against zero point seven for the operational product."),
        (19.5, "It raises half as many false alarms about clouds that aren't there, though it also catches fewer of the real ones."),
        (27.0, "Rain: the best of three ensembles for six hours, but only about two thirds as wet as observed, and too smooth."),
    ]),
    # Text S5.3 (CloudSat head, principally geostationary IR), §4.2.3 (ACHA from GOES), §4.2.1 (IMERG uses ATMS and geo IR);
    # NSRDB derived from GOES is background; USCRN/SOLRAD and EarthCARE are independent
    dict(scene='Twist', hold=0.5, beats=[
        (0.6, "Here's the twist. Inferred isn't the same as clairvoyant."),
        (5.0, "The cloud-top readout learned mostly from geostationary infrared, the same light the operational product is built from."),
        (12.0, "The rain it's scored against is built partly from satellites it reads, and the sunlight data it learned from is itself derived from those satellites."),
        (20.5, "That's learned retrieval, and good retrieval. The independent checks are that radar satellite, and the sunlight sensors on the ground."),
    ]),
    # §4.1, Fig. 4, Text S6.2 (latency: GEFS >= 5 h, IFS ENS >= 7 h old)
    dict(scene='Clocks', hold=0.5, beats=[
        (0.6, "Now read the scoreboard like a detective. Near the ground, it beats the American ensemble for temperature, dew point and wind, out to twelve hours."),
        (9.5, "But check the clocks. It gets a fresh analysis every hour. The American forecast it's compared with is at least five hours old, and the European one at least seven."),
        (19.0, "The European ensemble still overtakes it on temperature after about eight hours, when that forecast is more than fifteen hours old."),
        (26.5, "And most of its edge comes from the spread of its ensemble. On the average forecast alone, it beats the European ensemble only for temperature, and only for three hours."),
    ]),
    # §4.1, §5 (representativeness, held-out stations, ~200 km), Text S6.4 (no lapse-rate adjustment: our reading), COI
    dict(scene='FinePrint', hold=0.5, beats=[
        (0.6, "More fine print. It predicts individual stations, while the big models describe whole grid boxes."),
        (6.5, "The hidden test stations are a random five percent, many with neighbors it did see. The help from those neighbors fades beyond about two hundred kilometers."),
        (15.0, "The supplement says the other forecasts weren't adjusted for station elevation. Our reading: that helps it at mountain stations."),
        (22.5, "And all five authors work at the company that builds it, as they disclose."),
        (27.0, "What survives? With every surface station removed, it still beats the American ensemble for temperature out to eleven hours, and for wind to twelve."),
    ]),
    # Fig. S3 (memory h vs latent z), Text S3 caption: "analogous to the observation-density information a conventional
    # filter carries in its error covariance"; z "dominated by meteorological structure with a weak residual imprint"
    dict(scene='Reveal', hold=0.5, beats=[
        (0.6, "Back to the memory, and those stripes."),
        (4.0, "A good filter has to know where it has recently looked. A region seen a minute ago is well known. One unseen for hours is not."),
        (12.5, "Classical filters keep that in their error statistics, and the authors make the same comparison: the memory carries the observing network, as a filter's error estimates would."),
        (22.0, "And the narrow state the decoders read, sixty-four numbers per cell, is mostly weather, with only a faint trace of where the satellites were."),
        (30.0, "So remembering the satellites isn't the crime. It's part of how a filter knows how sure to be."),
    ]),
    # §5 (data denial is cheap; continuous cycling is future work); §3.5 (zero state, 12 h window)
    dict(scene='RealTest', hold=0.5, beats=[
        (0.6, "So is it learning the atmosphere, or our instruments? That's a false choice. The real test is whether the weather state holds still when the instruments change."),
        (10.5, "Withholding instruments is cheap with this model, and the paper does it for surface stations. What it never checks is whether the weather state itself stays put."),
        (18.0, "And every run starts from an empty memory, with twelve hours of observations. A filter that keeps running for weeks is still to be shown."),
    ]),
    dict(scene='Questions', vend=22.0, hold=1.5, beats=[
        (0.5, "A few questions to think about."),
        (2.0, "What experiment would convince you its inner state is the atmosphere, and not the observing network?"),
        (8.5, "It learned to trust instruments well near the ground, and to lean only lightly on them high up. Why might training produce that?"),
        (15.5, "Should an ensemble get credit for spread that comes from predicting single stations?"),
    ]),
    dict(scene='End', hold=2.4, vend=11.0, beats=[
        (0.6, "The verdict: it learned whom to trust near the ground, and where it had been looking. It hasn't yet learned to listen closely high up."),
    ]),
]
