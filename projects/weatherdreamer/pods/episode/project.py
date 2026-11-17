"""WeatherDreamer: a single-host audio episode (the owner's personal set; an aigs pod extra, see the topic's AGENTS.md).
Script in episode.py; build with: make P=weatherdreamer/pods/episode"""
KIND = 'podcast'
TITLE = 'The Forecaster With No Answer Key'
OUTPUT_NAME = 'WeatherDreamer_pod.mp3'
SHOW = 'weatherdreamer · an explainer'   # ID3 album; the engine's default is the pod's show name, which this topic must not use
ARTIST = 'mahf708'                       # ID3 artist; likewise
SUMMARY = ('WeatherDreamer (Duffy, Penn, Ballard, Posch, Vandal): a world model that learns data assimilation and '
           'forecasting directly from observations, with no reanalysis. An unofficial explainer.')
BED = 0                     # talk on silence (the podcast norm); music only in the theme, stings and outro
# Podcasts honour duck_db but follow the voice's waveform; duck_ramp is kept for the house rule (docs/STYLES.md).
MUSIC = dict(style='silencia', duck_db=9, duck_ramp=1.2)

DESCRIPTION = """The Forecaster With No Answer Key. An unofficial explainer of the WeatherDreamer paper, for anyone curious about weather, data and learning machines.

Every weather forecast starts from a picture of the atmosphere right now, and nobody can see right now: only scattered stations, balloons twice a day, and satellites that measure light rather than temperature. Building that picture, data assimilation, is the most expensive step in forecasting, and even the famous AI forecasters start from it. This episode follows a 2026 paper that asks whether a machine can learn the whole predict-and-correct loop from the observations alone, with no answer key: what it gets right near the ground, where it falls short higher up and why, how to read its scoreboard with care, and what turns up inside its memory.

Paper: Kate Duffy, Elise Penn, Tristan Ballard, August Posch, Thomas J. Vandal (Zeus AI, Inc.). WeatherDreamer: Learning a World Model from Multimodal Earth Observations. arXiv:2611.18393v1 (13 Nov 2026). https://arxiv.org/abs/2611.18393

Chapters
{chapters}

Questions to think about
{questions}

Notes
• "The American and European ensembles" are NOAA's GEFS (31 members) and ECMWF's IFS ENS (51 members); "NOAA's assimilation system" is the Gridpoint Statistical Interpolation (GSI), scored from the diagnostic files of a 3D-Var reanalysis run. The weather balloons are radiosondes; the ocean-wind satellites, ASCAT scatterometers; the newer cloud-probing satellite (radar and lidar), EarthCARE; the cloud radar used in training, CloudSat.
• Surface results are at 534 stations (5% of the network) held out from the input. Many of them have assimilated neighbours, and the baselines were interpolated to stations without an elevation adjustment (our reading of the supplement: that favours the model at mountain stations).
• The comparison with operational ensembles uses their real delivery delays (5 to 7 hours old at the model's start time). That measures usefulness, not the quality of the learned dynamics alone.
• The upper-air numbers: weather-balloon winds 7.89 vs 3.01 m/s (2.6 times, averaged over all levels; 1.6 to 1.7 in the lowest levels and 3.2 to 3.5 at 300 to 200 hPa); temperature-sounding microwave channels up to about 4.6 times (the abstract rounds this to "up to five").
• "Our arithmetic": a 50 m/s jet-stream wind crosses a 1,600 km patch in about nine hours. That is ours, not the paper's; the paper names the patch size and the weak use of upper-air data as the two causes.
• Rain, irradiance and cloud-top height are never inputs at inference, but rain is verified against a product (IMERG) built partly from instruments the model reads, and cloud tops are learned mainly from geostationary infrared, the same radiances the operational retrieval uses. EarthCARE is the fully independent check.
• All five authors work at Zeus AI, which develops the model and may use it commercially (the paper's conflict-of-interest statement).
• The brain-as-predictor aside refers to predictive-coding accounts of perception, which the paper cites; the Kalman filter is from 1960 and was used in Apollo navigation. The closing questions are ours.
{voice}• An unofficial summary, not produced by the authors.
"""
