"""The event's facts, in one place. Change WHEN here and rebuild (`make P=hackathon/videos/invite`): the end card, the
title drop, the narration's last line, the thumbnail and the description all read it."""
import re

EVENT = 'the aigs hackathon'
WHEN = 'Week of November 16'
MORE = 'details soon'


def spoken(s):
    """What the narrator says for a date: '16' -> '16th', so Kokoro says "sixteenth" and Whisper's '16th' matches."""
    def th(m):
        n = int(m.group(0))
        suf = 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f'{n}{suf}'
    return re.sub(r'\b\d{1,2}\b(?!\w)', th, s)
