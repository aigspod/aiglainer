"""Thumbnail: the striped memory (Fig. S3a, polar-orbit swath channel) as the focal image, three big words.
Nothing important in the bottom-right (YouTube's duration badge)."""
from trustkit import *
from scenes1 import s3map

def draw(c):
    x, y, w = 960, 120, 880
    figcard(c, 'figS3', x, y, w, 1, None, src=s3map(1, 4), pad=14)
    text(c, 'its memory, striped', x, y + 520, 40, 700, 'y', 1, kind='mono')
    text(c, 'What did', 90, 330, 140, 800, 'ink', kind='heavy', tracking=-0.01)
    text(c, 'it learn', 90, 500, 140, 800, 'ink', kind='heavy', tracking=-0.01)
    w2 = text(c, 'to trust?', 90, 690, 170, 700, 'y', kind='italic')
    swash(c, 100, 90 + w2, 740, 'y', 1, 1, w=12)
    kicker(c, 'weatherdreamer', 100, 850, 1, 'muted', 46)
