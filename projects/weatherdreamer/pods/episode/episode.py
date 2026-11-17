"""WeatherDreamer: the full single-host episode (about 24 min). An aigs pod extra: see projects/weatherdreamer/AGENTS.md
(numbers, accuracy notes, the review check). Every claim traces to arXiv:2611.18393v1 or to background listed there:
- Cold open: predict-correct as how you find your way in a dark room (an "imagine" scenario); predictive-coding
  accounts of perception (§3.1 cites Friston 2010, Clark 2013).
- Stakes: analysis = best estimate of now; sparse, indirect observations (satellites measure radiances, §1); ~11,000
  stations, balloons twice a day (§2.1); 6-hourly global analyses that arrive hours late; hand-built observation
  operators, bias corrections, error models, heavy thinning (§1); AI forecasters start from analyses (§1, §5);
  WeatherNext3 starts from an analysis nearly 6 h old (§1).
- Craft: Kalman 1960 (Eq. 1-3; Apollo is background); background, analysis, gain from B and R (§3.1).
- Apprentice: no reanalysis; 18 systems; Dreamer (Hafner et al.); memory 512 / latent 64 per ~50 km cell; posterior
  attends to observations conditioned on memory; masking; three losses incl. "the prior can match the posterior only
  by anticipating" (§3); 2020-2023; 50 M parameters (+ 99 M frozen tokenizers, show notes).
- Results: §4.1 (wind 1.09 / 1.31 / 1.15; T2m best 8 h; spread vs mean; spread-skill; no-stations still beats GEFS),
  §4.2 (rain best to 6 h, two-thirds, smooth; cloud tops vs EarthCARE r 0.73 vs 0.70, half the false alarms),
  §4.3.2 / Table 2 (balloon winds 2.6x; sounding channels up to ~4.6x; surface within 10%), §4.1 SLP weakness,
  §5 (two causes), our arithmetic (labelled), §4.3.3 gains, S6.2 latency, S6.4 held-out / elevation, §5 caveats,
  COI statement; §4.3.3 σ_O at instrument noise, k 0.64 vs 0.82, ASCAT 0.9 vs 0.8; §4.4 limb darkening 83-96%,
  six vs twenty-two kelvin; Fig. S3; §5 speed, restart, continuous cycling as future work, "initial condition for
  other models". The closing questions are ours.

A role ending in '?' ('H?') marks a question to think about; it is listed in the show notes. ('~', 'rest') is a pause
between ideas (PACE['rest'] seconds).
"""

HOSTS = {'H': 'bella-nicole'}   # Bella blended 70/30 with Nicole
SPEED = 0.92                    # unhurried
PACE = dict(sentence=0.45, same=0.7, turn=0.35, segment=1.8, question=0.5, rest=1.2)

SAY = {
    'Kalman': 'Kahlman',
}

REST = ('~', 'rest')

SEGMENTS = [
    # ---------------------------------------------------------------- cold open: the dark room
    dict(title='Cold open', music=None, lines=[
        ('H', "Imagine you wake up in the middle of the night, in a room you know well. It's completely dark."),
        ('H', "You still know roughly where the door is. You carry a picture of the room in your head, and you move by it."),
        ('H', "Then your hand brushes the edge of the dresser, a little sooner than you expected. You don't start over. You nudge the picture, and keep going."),
        REST,
        ('H', "Predict, then correct. It's so natural you never notice it. Some accounts of perception say your brain does this all day: it guesses what your senses will report, and learns from the mismatch."),
        ('H', "Now scale that room up to the whole planet.", 0.5),
        ('H', "Every weather forecast you've ever seen starts from a picture of the atmosphere right now. And nobody can see right now."),
        ('H', "This episode is about a machine that learned to build that picture on its own, from scattered clues, without ever being shown the answer."),
    ]),

    # ---------------------------------------------------------------- welcome
    dict(title='Welcome', music='theme', lines=[
        ('H', "Hi, and welcome. Get comfortable. This one's a story about the weather, and about what a learning machine carries in its head."),
        ('H', "It follows a paper from November 2026, by Kate Duffy and four colleagues at a company called Zeus AI. The model is called WeatherDreamer."),
        ('H', "Here's the question we'll carry the whole way. Can a machine learn to see the weather right now, from the raw clues alone, with no answer key?"),
        ('H', "And if it can, what is it actually remembering?"),
    ]),

    # ---------------------------------------------------------------- 1. the problem of now
    dict(title='Nobody can see right now', music='sting', lines=[
        ('H', "So let's start with the clues, because they're stranger than you might think."),
        ('H', "There are about eleven thousand weather stations on land that report every hour. But most of the planet is ocean, and the stations sit in the bottom few meters of the air."),
        ('H', "Weather balloons climb through the whole atmosphere. But only about six hundred and fifty of them go up at a time, twice a day."),
        ('H', "And then there are satellites, which see almost everything. Here's the catch. A satellite doesn't measure temperature, or humidity, or wind. It measures light. Infrared, microwaves. Glow from a column of air, blended over many kilometers of height."),
        ('H', "So the clues are sparse, they arrive at odd times, and many of them are indirect."),
        REST,
        ('H', "Turning those clues into one complete picture is called data assimilation. The picture it produces is called the analysis."),
        ('H', "And it is, quietly, one of the most expensive parts of weather forecasting. Much of the improvement in forecasts over the past few decades came from getting better at it."),
        ('H', "Now, you may have heard that artificial intelligence has taken over weather forecasting. Models from Google and others now match the big physics-based forecasts, at a tiny fraction of the cost."),
        ('H', "That's true. But most of them start from an analysis built by the old, physics-based machinery. They learned to forecast. They never learned to see."),
        ('H', "Even a recent one that reads satellite data every hour still starts from an analysis that's nearly six hours old. A few research models do forecast straight from raw observations, but each forecast is built in one pass over a fixed window of data, with no running memory carried from hour to hour."),
    ]),

    # ---------------------------------------------------------------- 2. the old craft
    dict(title='Predict, then correct', music=None, lines=[
        ('H', "So how does the old machinery work? It's the dark room again."),
        ('H', "Step one, predict. Take your last best picture of the atmosphere, and run a physics model forward a few hours. That forecast is called the background."),
        ('H', "Step two, correct. When new observations arrive, compare them with what the background expected to see, and nudge the picture toward them."),
        ('H', "The mathematics behind this goes back to 1960, to Rudolf Kalman's filter. Versions of it helped navigate the Apollo spacecraft to the Moon."),
        REST,
        ('H', "The heart of it is a question of trust. How far should you move toward each new observation?"),
        ('H', "Imagine your forecast says twenty degrees, and a thermometer says twenty-two. If your forecast is usually off by a degree, and the thermometer only by half a degree, you should move most of the way toward the thermometer. If the thermometer is the shaky one, you barely move."),
        ('H', "That fraction is called the gain. To get it right, you need to know how wrong each of your instruments tends to be, and how wrong your own forecast tends to be."),
        REST,
        ('H', "In practice, people build all of this by hand. Every instrument needs its own translator, a model of how the atmosphere would look to that instrument. Every instrument needs a correction for its biases, and an estimate of its errors."),
        ('H', "Observations get thinned out, because their errors are tangled together in ways that are hard to describe."),
        ('H', "And it's so expensive that global centers run the cycle every six hours. By the time an analysis is ready, the atmosphere it describes is already hours in the past."),
    ]),

    # ---------------------------------------------------------------- 3. the apprentice
    dict(title='An apprentice with no answer key', music='sting', lines=[
        ('H', "Now the new idea."),
        ('H', "WeatherDreamer is trained on raw observations from eighteen observing systems: weather stations, balloons and several kinds of satellite, plus two gridded products."),
        ('H', "What it never sees is an answer key. Most AI weather models learn from a reanalysis, a decades-long, physics-built reconstruction of past weather. That reconstruction carries the physics model's own habits and biases. This model never touches one."),
        ('H', "It only ever sees the clues."),
        REST,
        ('H', "Its design borrows from robotics and game-playing research, from a family of so-called world models called Dreamer. A Dreamer agent learns a compact inner picture of its world, and how that picture changes, so it can imagine what happens next."),
        ('H', "Here, the world is the atmosphere. The globe is cut into cells about fifty kilometers across. Each cell carries two things."),
        ('H', "One is a wide memory, five hundred and twelve numbers, that carries what the model has learned from earlier hours. The other is a narrow summary of the weather in that cell right now, sixty-four numbers."),
        ('H', "Every hour, the memory steps forward and makes a guess: the background. Then the observations from that hour arrive, and a learned correction step looks at the nearby ones, through the lens of what the memory already believes, and produces the analysis."),
        ('H', "Predict, then correct. Except this time, nobody wrote down the gain. The network has to learn how far to trust each instrument by itself."),
        REST,
        ('H', "How do you teach that, with no answer key? The authors use three lessons."),
        ('H', "Lesson one: from your inner picture, reproduce what the instruments actually saw. And during training, they often hide whole instruments, or blocks of the map, and still ask for them back. Guessing what you weren't shown counts extra."),
        ('H', "Lesson two: make your guess for the next hour match the picture you'll have once that hour's observations arrive. As the paper puts it, the only way to do that is to anticipate the observations before they come. That's how the model learns to forecast."),
        ('H', "Lesson three: run on your own for several hours with no observations at all, as a small ensemble of possible futures, and get scored on how well that spread of futures matches what really happened."),
        ('H', "It's trained on four years of observations, 2020 to 2023, and tested on 2024 and 2025."),
    ]),

    # ---------------------------------------------------------------- 4. what it got right
    dict(title='Down here, it works', music=None, lines=[
        ('H', "So, does it work? Near the ground, yes, remarkably well."),
        ('H', "The authors hide about five hundred stations from the model entirely, and forecast the weather at those spots for the next twelve hours."),
        ('H', "For surface wind, it beats both the American and the European operational ensembles at every hour out to twelve."),
        ('H', "For temperature, it beats the American ensemble all the way, and the European one for the first eight hours. After that, the European ensemble pulls ahead."),
        ('H', "Its sense of its own uncertainty is better than both. When it says it isn't sure, that matches its real errors much more closely, though all three are still a bit overconfident."),
        REST,
        ('H', "Then there are the things it was never shown at all, at least not while forecasting."),
        ('H', "Rainfall, sunlight reaching the ground, and the height of cloud tops are never fed in. They have to be read out of the inner picture."),
        ('H', "For rain, it's the most skillful of the three ensembles for the first six hours. But it's too dry, about two thirds of the observed rain, and too smooth."),
        ('H', "For cloud tops, the authors check against a newer satellite that probes clouds with radar and laser, one the model never saw in training. Its heights are a little better than the operational satellite product. It raises half as many false alarms about clouds that aren't there, though it also misses a bit more real cloud."),
        ('H', "And all of this from one graphics processor. A fresh global analysis takes about a minute and a half, every hour."),
    ]),

    # ---------------------------------------------------------------- 5. the turn: up there
    dict(title='Up there, it falters', music='sting', lines=[
        ('H', "So far, a success story. But here's where it turns.", 0.4),
        ('H', "Go up, away from the ground, and things change."),
        ('H', "The authors compare their short forecasts with the background from NOAA's assimilation system, a few hours ahead, scored against exactly the same observations."),
        ('H', "At surface weather stations, the two are within about ten percent of each other. For the microwave channels that sense moisture, within about twenty-five percent."),
        ('H', "But for the satellite channels that sense temperature high in the atmosphere, its errors are up to about four and a half times larger. And for winds measured by weather balloons, two point six times larger on average, and more than three times larger near the jet stream."),
        ('H', "And at the surface, there's one more weak spot: air pressure. Forecasts of how pressure changes over the next six to twelve hours are clearly worse than the operational ones."),
        REST,
        ('H', "Why? The paper points to two culprits, and I find both of them illuminating."),
        ('H', "The first is the walls. To keep things affordable, the model's dynamics run on patches about one thousand six hundred kilometers across, and each patch keeps its own memory. The paper says that's too small to hold the large, slowly evolving circulation that steers winds up high and the big pressure patterns."),
        ('H', "Here's a bit of our own arithmetic, not the paper's. Winds high up, near the jet stream, often blow at fifty meters a second. That crosses one thousand six hundred kilometers in about nine hours. Near the ground, a typical wind moves a few hundred kilometers in twelve hours."),
        ('H', "So, in our reading, a patch is a big world for the slow winds near the ground. But high up, weather can blow in from beyond the wall. And pressure patterns, which are huge, don't fit inside one at all."),
        ('H', "The second culprit is listening. When the authors measure how much the model actually moves toward each kind of observation, they find it barely listens to the instruments high up. For balloon temperature and wind near the jet stream, the gain is a tenth to a quarter. For one satellite technique that measures the upper air very precisely, called radio occultation, it's close to zero."),
        ('H', "It learned to lean only lightly on exactly the clues it needed most up there."),
    ]),

    # ---------------------------------------------------------------- 6. reading the scoreboard
    dict(title='Reading the scoreboard', music=None, lines=[
        ('H', "Before we go further, let's read the scoreboard the way a careful reviewer would. The authors flag most of this themselves, which I appreciate."),
        ('H', "First, freshness. This model gets a fresh analysis every hour. The operational ensembles are compared as they'd really be delivered: their forecasts are already five to seven hours old at the start."),
        ('H', "That's fair if you ask what's useful on a given morning. But it doesn't tell you whose forecasting engine is better. In fact, the European ensemble overtakes it on temperature after about eight hours, even though by then the European forecast is more than fifteen hours old."),
        ('H', "Second, much of its edge comes from the spread of its ensemble, not from a more accurate average. Measured by the average forecast alone, it beats the European ensemble only for temperature, and only for about three hours."),
        ('H', "Part of that spread advantage is a home game. It's trained to predict individual stations, while the big models describe whole grid boxes."),
        REST,
        ('H', "Third, the hidden stations are a random five percent of the network, so many have neighbors the model did see. In fact, the model only improves its picture at a hidden station when a station it does see is within about two hundred kilometers."),
        ('H', "And there's one more detail, tucked into the supplement. The operational forecasts were matched to stations without adjusting for elevation, while WeatherDreamer knows each station's height. Our reading is that this tilts things its way at mountain stations."),
        ('H', "Fourth, the rain check isn't fully independent: the rain product it's scored against is built partly from the same satellites it reads. The newer satellite's cloud check is the clean one."),
        ('H', "And finally, all five authors work at the company that develops it. They say so, as they should."),
        REST,
        ('H', "In fairness, some of it cuts the other way. NOAA's system draws on far more instruments, including aircraft, and on decades of tuning. And even with every surface station taken away, it still beats the American ensemble for temperature out to eleven hours, and for wind all the way out to twelve. That part holds up."),
    ]),

    # ---------------------------------------------------------------- 7. what it learned to trust
    dict(title='What it learned to trust', music='sting', lines=[
        ('H', "Now, the part I like most. What did it actually learn?"),
        ('H', "Remember the gain, the question of trust? Nobody told this model how noisy any instrument is. But you can work backwards. A classic diagnostic from data assimilation looks at the model's corrections and asks: what instrument error must this system be assuming?"),
        ('H', "For the microwave channels that sense temperature, in clear skies, the answer is about two to four tenths of a degree. That's the actual measured noise of those instruments in orbit."),
        ('H', "For the satellite winds over the ocean, it's close to the known error too. Nobody told it. It worked that out from the data."),
        ('H', "It's not perfect. For the temperature channels, it's too timid: it moves about sixty-four percent of the way, where the best choice would be about eighty-two. For the ocean winds, it's too trusting. It forgets that a satellite's wind measurement isn't quite the same thing as the wind in a fifty kilometer cell."),
        REST,
        ('H', "It also learned some geometry. When a satellite looks at the Earth at a slant, its view passes through more air and sees higher, colder layers. Images go cold toward the edges, and you get seams where one satellite hands off to the next."),
        ('H', "WeatherDreamer is told each satellite's viewing angle, and can decode its inner picture at any angle it likes, including straight down. Do that, and it removes between eighty-three and ninety-six percent of that edge cooling, with more correction where the air absorbs more, from about six degrees in the channel that sees most clearly down to the surface, to over twenty in a channel that senses ozone, which absorbs strongly. The seams disappear."),
        ('H', "It learned this because the same spot is often seen by two satellites at once, from different angles. Comparing the two views is how it learned the geometry."),
    ]),

    # ---------------------------------------------------------------- 8. what's in its head
    dict(title="What's in its memory", music=None, lines=[
        ('H', "Which brings us to the strangest picture in the paper.", 0.4),
        ('H', "The authors open up the model's memory at one moment, and map a few of its five hundred and twelve channels across the globe."),
        ('H', "Some of them look like weather: swirls and fronts. Some show the line between day and night, or land and sea."),
        ('H', "And some show neither. They show round footprints, where each geostationary satellite sees the Earth. And long diagonal stripes, the tracks of polar-orbiting satellites as they pass overhead."),
        ('H', "The model is remembering where its instruments have been looking."),
        REST,
        ('H', "At first, that sounds like a flaw. Is it learning the atmosphere, or just learning our satellites?"),
        ('H', "But think about the dark room again. If you touched the dresser a second ago, you're sure where it is. If you haven't touched anything for a while, you should be less sure."),
        ('H', "A good filter has to know where it has recently looked, because that's how it knows how much to trust its own picture. The classical filter keeps that in its error estimates. The authors make exactly this comparison."),
        ('H', "And the narrow summary, the sixty-four numbers that the decoders read, is mostly weather, with only a faint trace of where the satellites were."),
        ('H', "So the real question isn't atmosphere versus satellites. It's whether the weather part stays the same when you change the instruments. Swap one satellite for another, or take one away, and does the model's picture of the atmosphere hold still? The paper points out that such experiments are cheap, and it does remove all the stations once. But it never checks whether the inner picture itself holds still."),
    ]),

    # ---------------------------------------------------------------- 9. close
    dict(title='Waking up every hour', music='sting', lines=[
        ('H', "Let's gather it up."),
        ('H', "Weather forecasting has always started with a picture of now, built by expensive, hand-made machinery, every six hours, hours late. The AI revolution in forecasting still leaned on it."),
        ('H', "The new model learns the whole loop, predict and correct, from the clues alone. Near the ground, it's already competitive. Up high, it isn't yet, because its patches are too small for the big, slow circulation, and because it leans only lightly on the upper-air clues."),
        ('H', "One more honest limit. Every run in the paper starts with an empty memory and twelve hours of catching up. A filter that keeps running for days and weeks without drifting is still to be shown."),
        ('H', "But a fresh global analysis in a minute and a half, every hour, on one machine, is a real change in what's possible."),
        REST,
        ('H', "Here are a few things to sit with."),
        ('H?', "If you could run one experiment to tell whether its inner picture is the atmosphere or just our instruments, what would it be?"),
        ('H?', "Training on reanalysis passes on a physics model's biases. Training on raw observations passes on the habits of our instruments. Which would you rather inherit?"),
        ('H?', "It leaned only lightly on the clues it needed most up high. How would you teach a model to listen to a rare, precise instrument?"),
        ('H?', "And could a picture like this, built only from observations, one day start other models, the ones that simulate climate?"),
        ('H', "Back to the dark room.", 2.0),
        ('H', "You don't know where everything is. You carry a guess, and every touch corrects it. This model learned to do that for a whole planet, from the touches alone, without anyone ever turning on the light."),
        ('H', "Thanks for listening.", 1.0),
    ]),
]
