"""LAWFUL as an audio-only pilot (solo). Script in episode.py; build with: make P=lawful-pod-solo"""
KIND = 'podcast'
TITLE = 'LAWFUL: did the network learn the physics? (pilot, solo)'
OUTPUT_NAME = 'LAWFUL_pod_solo.mp3'
SUMMARY = 'A short audio pilot on LAWFUL (Chen, Parker & Arora, ICML 2026 MI workshop), for the aigs pod journal club.'
BED = 0                     # faint music under the talk, 0..1 (0: talk on silence, the podcast norm)

DESCRIPTION = """LAWFUL: did the network learn the physics? A short audio pilot for the aigs pod journal club.

A transformer that predicts radar from motion capture is accurate. Has it learned the Doppler law, does its
computation use it, and where? We walk through LAWFUL's three steps: behavior, cause and mechanism.

Paper: Kevin Chen, Kenneth W. Parker, Anish Arora (2026). LAWFUL: Law-Aligned Witness for Faithful Use of Latents.
Mechanistic Interpretability Workshop, ICML 2026. arXiv:2607.28672

Chapters
{chapters}

{voice}• An unofficial summary, not produced by the authors.
"""
