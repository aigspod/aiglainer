"""How the hosts say words Kokoro gets wrong, shared by every project, video or podcast.

SAY maps a written word or phrase to what is synthesized: a respelling, or inline phonemes in Kokoro's notation,
[word](/phonemes/) (misaki's alphabet: A = the "ay" in "plague", I = "eye", O = "oh", ː lengthens a vowel).
A project's own SAY (in narration.py / episode.py) is applied first and can override these.

HEARD maps what Whisper writes when it hears a word said our way back to the script's spelling, so the per-line
check compares like with like (Whisper has never seen "aigs" and writes "eggs" or "Ag's").
"""

SAY = {
    # the aigs pod: "aygs", the vowel of "plague" (rhymes with "plagues"); never spelled out letter by letter
    'aigs': '[aigs](/ˈAɡz/)',
}

HEARD = {
    r"\b(?:a\.?i\.?g\.?s\.?|aigs|aegs|eggs|egg's|ags|ag's|agg?s)\s*-?\s*(pod(?:cast)?)\b": r'aigs \1',
}
