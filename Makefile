# Paper explainer videos. Each video is a project under projects/; pick one with P=<name>.
#   make setup                     once: create .venv
#   make new P=mypaper             start a new video from the template
#   make P=mypaper                 build and verify its narrated cut -> projects/mypaper/out/narrated/
#   make help                      every target
P      ?= lawful
CUT    ?= narrated
PY     := $(CURDIR)/.venv/bin/python
TTS    := $(PY)
NPROC  ?= 15
EX      = -m aiglainer -p $(P) --cut $(CUT)
export PATH := $(HOME)/.pixi/bin:$(PATH)

.PHONY: all help setup new inspect data tex narration plan video audio finish verify frames preview thumbnail voices fingerprint check clean
all: tex narration video audio finish verify thumbnail

help:             ## list targets
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | sed -E 's/:.*## /\t/' | expand -t 14

setup:            ## create .venv from uv.lock (rendering + narration) and enable the commit guard
	./tools/setup.sh

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

voices:           ## audition narrator voices on voice_samples/sample.txt -> voice_samples/index.html
	$(TTS) $(EX) voices $(VOICES)

fingerprint:      ## save hashes of sampled frames, cues, placements (before an engine change)
	$(PY) -m aiglainer -p $(P) fingerprint

check:            ## after an engine change: compare against the saved fingerprint
	$(PY) -m aiglainer -p $(P) fingerprint --compare

clean:
	rm -rf projects/$(P)/out/*/seg projects/$(P)/out/*/list.txt
