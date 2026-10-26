# Paper explainer videos. Each video is a project under projects/; pick one with P=<name>.
#   make setup                     once: pixi install (+ the commit guard)
#   make new P=mypaper             start a new video from the template
#   make P=mypaper                 build and verify its narrated cut -> projects/mypaper/out/narrated/
#   make help                      every target
P      ?= lawful
CUT    ?= narrated
# Python: the pixi environment if `pixi install` has run, otherwise whatever python3 is active (a venv you made).
# Override with `make PY=/path/to/python`.
ENV    := $(CURDIR)/.pixi/envs/default
ifneq ($(wildcard $(ENV)/bin/python),)
PY     ?= $(ENV)/bin/python
export PATH := $(ENV)/bin:$(PATH)            # the project's own ffmpeg and tectonic
else
PY     ?= python3
endif
TTS    := $(PY)
NPROC  ?= 15
EX      = -m aiglainer -p $(P) --cut $(CUT)

all:              ## build and verify $(P): the video, or the episode for a podcast project
	@if grep -qs "^KIND *= *'podcast'" projects/$(P)/project.py; then $(MAKE) --no-print-directory podcast P=$(P); \
	else $(MAKE) --no-print-directory tex narration video audio finish verify thumbnail P=$(P) CUT=$(CUT); fi

.PHONY: all podcast help setup doctor new inspect data tex narration plan video audio finish verify frames preview thumbnail voices fingerprint check clean

help:             ## list targets
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | sed -E 's/:.*## /\t/' | expand -t 14

setup:            ## pixi install from pixi.lock, and enable the commit guard
	./tools/setup.sh

doctor:           ## check this machine: tools, libraries, speech models (and fix espeak's data path)
	$(PY) -m aiglainer doctor

new:              ## scaffold projects/$(P) from the template: make new P=name TITLE="Paper Title"
	$(PY) -m aiglainer new $(P) "$(TITLE)"

inspect:          ## list vector paths and images on a PDF page: make inspect PDF=path PAGE=8
	$(PY) -m aiglainer inspect $(PDF) $(PAGE)

data:             ## run the project's own extract_paper.py, if it has one
	@if [ -f projects/$(P)/extract_paper.py ]; then $(PY) projects/$(P)/extract_paper.py; else echo "no extract_paper.py in projects/$(P)"; fi

tex:              ## typeset eqs.py (skipped when unchanged; needs tectonic)
	$(PY) $(EX) tex

narration:        ## synthesize every line (cached) and Whisper-verify it; fails on mismatches
	@if [ "$(CUT)" = narrated ]; then $(TTS) $(EX) tts; fi

plan:             ## print the narrated timing plan without rendering
	$(PY) $(EX) plan

video:            ## render frames -> out/$(CUT)/video_noaudio.mp4
	NPROC=$(NPROC) $(PY) $(EX) render

audio:            ## score, sound effects, narration and ducking -> audio.wav
	$(PY) $(EX) audio

finish:           ## mux at -14 LUFS, captions.srt, youtube_description.txt
	$(PY) $(EX) finish

verify:           ## Whisper the final mix line by line: word errors and sync
	@if [ "$(CUT)" = narrated ]; then $(TTS) $(EX) verify; fi

frames:           ## contact sheets, one frame per narration line -> out/$(CUT)/qa/
	$(PY) $(EX) frames

preview:          ## contact sheet of one scene: make preview SCENE=Fig4a T="5 12 20"
	$(PY) $(EX) preview $(SCENE) $(T)

thumbnail:        ## YouTube thumbnail -> out/thumbnail.png (+ thumbnail_sizes.png legibility check)
	$(PY) $(EX) thumbnail

podcast:          ## audio-only episode -> out/podcast/ (MP3 with chapters, transcript, show notes), then verify
	$(TTS) -m aiglainer -p $(P) podcast

voices:           ## audition narrator voices on voice_samples/sample.txt -> voice_samples/index.html
	$(TTS) $(EX) voices $(VOICES)

fingerprint:      ## save hashes of sampled frames, cues, placements (before an engine change)
	$(PY) -m aiglainer -p $(P) fingerprint

check:            ## after an engine change: compare against the saved fingerprint
	$(PY) -m aiglainer -p $(P) fingerprint --compare

clean:
	rm -rf projects/$(P)/out/*/seg projects/$(P)/out/*/list.txt
