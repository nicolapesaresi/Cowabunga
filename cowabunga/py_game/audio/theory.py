"""Shared musical rules for every sound in the game.

Background music and bounce notes are both built from these constants, so the bounce
melody always uses notes of the chord the music is playing at that moment and can
never clash with it.
"""

from dataclasses import dataclass

TEMPO_BPM = 72
BEATS_PER_BAR = 4
BEAT_SECONDS = 60 / TEMPO_BPM
BAR_SECONDS = BEAT_SECONDS * BEATS_PER_BAR
# Swing: off-beat eighth notes are played this many beats late (0.1 -> lazy 60/40 feel).
SWING = 0.1


@dataclass(frozen=True)
class Chord:
    """A chord of the background progression."""

    name: str
    pitch_classes: tuple[int, ...]  # chord tones, 0 = C ... 11 = B
    bass: int  # MIDI note of the bass root
    pad: tuple[int, ...]  # MIDI notes of the pad voicing
    ukulele: tuple[int, ...]  # MIDI notes strummed by the ukulele, low to high


# Relaxing I - vi - IV - V progression in D major, one bar per chord.
PROGRESSION: tuple[Chord, ...] = (
    Chord("Dmaj7", (2, 6, 9, 1), bass=50, pad=(54, 57, 61, 64), ukulele=(62, 66, 69, 73)),
    Chord("Bm7", (11, 2, 6, 9), bass=47, pad=(57, 59, 62, 66), ukulele=(62, 66, 69, 71)),
    Chord("Gmaj7", (7, 11, 2, 6), bass=43, pad=(59, 62, 66, 69), ukulele=(62, 67, 71, 74)),
    Chord("A6", (9, 1, 4, 6), bass=45, pad=(57, 61, 64, 66), ukulele=(61, 64, 66, 69)),
)
LOOP_BARS = 8  # the progression is played twice per music loop
LOOP_SECONDS = BAR_SECONDS * LOOP_BARS

# Whistled theme over the 8 bars: (bar, beat, length in beats, MIDI note).
THEME: tuple[tuple[int, float, float, int], ...] = (
    (0, 0, 1.5, 78), (0, 1.5, 0.5, 76), (0, 2, 1, 74), (0, 3, 1, 69),
    (1, 0, 1, 71), (1, 1, 1, 74), (1, 2, 1.5, 78), (1, 3.5, 0.5, 76),
    (2, 0, 1.5, 74), (2, 1.5, 0.5, 78), (2, 2, 2, 79),
    (3, 0, 1, 78), (3, 1, 1, 76), (3, 2, 2, 73),
    (4, 0, 1.5, 78), (4, 1.5, 0.5, 76), (4, 2, 1, 74), (4, 3, 1, 78),
    (5, 0, 1.5, 81), (5, 1.5, 0.5, 78), (5, 2, 2, 74),
    (6, 0, 1, 71), (6, 1, 1, 74), (6, 2, 1, 79), (6, 3, 1, 78),
    (7, 0, 3, 76),
)  # fmt: skip

# Range of the bounce melody (D5 - A6): just above the ukulele, so it stands out without being shrill.
MELODY_LOW = 74
MELODY_HIGH = 93


def midi_to_freq(note: float) -> float:
    """Converts a MIDI note number to its frequency in Hz."""
    return 440.0 * 2 ** ((note - 69) / 12)


def swung(beat: float) -> float:
    """Applies swing to a position in beats: off-beat eighth notes are delayed."""
    if abs(beat * 2 - round(beat * 2)) < 1e-6 and round(beat * 2) % 2 == 1:
        return beat + SWING
    return beat


def chord_at(music_time: float) -> Chord:
    """Returns the chord the background music is playing at the given time (s)."""
    bar = int(music_time // BAR_SECONDS) % len(PROGRESSION)
    return PROGRESSION[bar]


def melody_notes(chord: Chord) -> list[int]:
    """Returns the ascending MIDI notes of the chord inside the melody range."""
    return [n for n in range(MELODY_LOW, MELODY_HIGH + 1) if n % 12 in chord.pitch_classes]
