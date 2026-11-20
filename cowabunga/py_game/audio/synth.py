"""Procedural synthesis of every game sound with numpy.

All functions return float arrays in [-1, 1]: shape (n,) for mono or (n, 2) for stereo.
Generating sounds in code keeps them perfectly in tune with the music theory module and
avoids shipping audio files. The music aims at a warm "indie" feel: ukulele, plucked bass,
shaker and a whistled theme, played with swing and small human imperfections, then passed
through a lo-fi chain (tape wobble, saturation, soft low-pass, vinyl crackle).
Any sound can still be replaced by a file in assets/sounds.
"""

import numpy as np

from cowabunga.py_game.audio.theory import (
    BAR_SECONDS,
    BEAT_SECONDS,
    LOOP_BARS,
    LOOP_SECONDS,
    PROGRESSION,
    THEME,
    midi_to_freq,
    swung,
)

TWO_PI = 2 * np.pi


def _time(sr: int, seconds: float) -> np.ndarray:
    return np.arange(int(sr * seconds)) / sr


def _mix(buffer: np.ndarray, start: int, sound: np.ndarray, gain: float = 1.0, pan: float = 0.0):
    """Adds a sound into a stereo buffer at sample `start`, wrapping around the end (loops).

    pan goes from -1 (left) to 1 (right) and is applied to mono sounds.
    """
    if sound.ndim == 1:
        sound = np.stack([sound * min(1.0, 1 - pan), sound * min(1.0, 1 + pan)], axis=1)
    sound = sound[: len(buffer)] * gain
    start %= len(buffer)
    first = min(len(sound), len(buffer) - start)
    buffer[start : start + first] += sound[:first]
    buffer[: len(sound) - first] += sound[first:]  # tail wraps to the loop start


def _normalize(sound: np.ndarray, peak: float) -> np.ndarray:
    top = np.max(np.abs(sound))
    return sound * (peak / top) if top > 0 else sound


def _filter(sound: np.ndarray, sr: int, low_cut: float = 0.0, high_cut: float | None = None) -> np.ndarray:
    """Smooth band filter in the frequency domain. Circular, so loops stay seamless."""
    n = len(sound)
    spectrum = np.fft.rfft(sound, axis=0)
    f = np.fft.rfftfreq(n, 1 / sr)
    gain = np.ones_like(f)
    if high_cut:
        gain /= np.sqrt(1 + (f / high_cut) ** 4)
    if low_cut:
        gain *= 1 - 1 / np.sqrt(1 + (f / low_cut) ** 4)
    if spectrum.ndim == 2:
        gain = gain[:, None]
    return np.fft.irfft(spectrum * gain, n=n, axis=0)


# ---------------------------------------------------------------- instruments


def pluck_string(freq: float, sr: int, seconds: float, brightness: float = 1.0, seed: int = 0) -> np.ndarray:
    """Nylon-string pluck (ukulele / bass): harmonics that die faster the higher they are (mono)."""
    rng = np.random.default_rng(seed)
    t = _time(sr, seconds)
    out = np.zeros(len(t))
    pluck_position = 0.2  # where the string is plucked: shapes the harmonic content
    for k in range(1, int(min(30, (sr / 2) / freq))):
        amp = abs(np.sin(np.pi * k * pluck_position)) / k**1.1
        decay = 1.5 + 0.8 * k**1.4 / brightness
        out += amp * np.exp(-t * decay) * np.sin(TWO_PI * k * freq * t + rng.uniform(0, TWO_PI))
    out += 0.08 * rng.standard_normal(len(t)) * np.exp(-t * 120)  # finger noise
    return out * np.clip(t / 0.002, 0, 1)


def _pad_voice(freq: float, sr: int, hold: float, release: float) -> np.ndarray:
    """Soft, slightly detuned stereo pad note, used as quiet glue under the ukulele."""
    t = _time(sr, hold + release)
    env = np.clip(t / 1.0, 0, 1) ** 2
    after = t > hold
    env[after] *= np.exp(-(t[after] - hold) / (release / 4))

    def voice(f):
        return np.sin(TWO_PI * f * t) + 0.2 * np.sin(TWO_PI * 2 * f * t)

    return np.stack([voice(freq * 0.9988), voice(freq * 1.0012)], axis=1) * env[:, None]


def _shaker(sr: int, rng: np.random.Generator) -> np.ndarray:
    t = _time(sr, 0.09)
    hit = rng.standard_normal(len(t)) * np.clip(t / 0.01, 0, 1) * np.exp(-t * 45)
    return _filter(hit, sr, low_cut=4000)


def whistle(freq: float, sr: int, seconds: float, seed: int = 0) -> np.ndarray:
    """Human-like whistle: pure tone, small scoop, late vibrato and breath (mono)."""
    rng = np.random.default_rng(seed)
    t = _time(sr, seconds + 0.08)
    f = freq * (1 - 0.02 * np.exp(-t * 25)) * (1 + 0.01 * np.sin(TWO_PI * 5.2 * t) * np.clip((t - 0.3) / 0.3, 0, 1))
    phase = TWO_PI * np.cumsum(f) / sr
    tone = np.sin(phase) + 0.05 * np.sin(2 * phase)
    breath = 0.1 * _filter(rng.standard_normal(len(t)), sr, high_cut=3000) * np.sin(phase)
    env = np.clip(t / 0.04, 0, 1) * np.clip((seconds + 0.08 - t) / 0.1, 0, 1)
    return (tone + breath) * env


# ---------------------------------------------------------------- lo-fi chain


def _vinyl(n: int, sr: int, rng: np.random.Generator) -> np.ndarray:
    """Soft hiss with sparse crackles (mono)."""
    hiss = 0.006 * rng.standard_normal(n)
    crackle = np.zeros(n)
    clicks = rng.integers(0, n, size=int(n / sr * 3))
    crackle[clicks] = rng.uniform(0.03, 0.12, size=len(clicks)) * rng.choice([-1, 1], size=len(clicks))
    crackle = _filter(crackle, sr, low_cut=800, high_cut=6000)
    return hiss + crackle


def lofi(loop: np.ndarray, sr: int) -> np.ndarray:
    """Tape wow/flutter, gentle saturation and a soft low-pass. Keeps the loop seamless."""
    n = len(loop)
    seconds = n / sr
    t = np.arange(n) / sr
    # wow (slow) + flutter (fast) as a time-varying delay, with whole cycles per loop
    wow = round(0.4 * seconds) / seconds
    flutter = round(6 * seconds) / seconds
    delay = sr * (0.0012 * np.sin(TWO_PI * wow * t) + 0.00012 * np.sin(TWO_PI * flutter * t))
    pos = (np.arange(n) - delay) % n
    i0 = np.floor(pos).astype(int)
    frac = (pos - i0)[:, None]
    loop = loop[i0] * (1 - frac) + loop[(i0 + 1) % n] * frac
    loop = np.tanh(1.8 * _normalize(loop, 0.9)) / np.tanh(1.8)  # tape saturation
    return _filter(loop, sr, low_cut=40, high_cut=5500)


# ---------------------------------------------------------------- background music


def _beat_to_sample(bar: int, beat: float, sr: int, rng: np.random.Generator, humanize: float = 0.012) -> int:
    seconds = bar * BAR_SECONDS + swung(beat) * BEAT_SECONDS + rng.uniform(-humanize, humanize)
    return max(0, int(seconds * sr))


def background_layers(sr: int, seed: int = 7) -> tuple[np.ndarray, np.ndarray]:
    """Renders one seamless loop of the indie background music.

    Returns two stereo layers of the same length, meant to be played in sync:
    the band (ukulele, bass, shaker, pad, vinyl) and the whistled theme, so the theme
    can be loud in the menu and quiet during the game.
    """
    rng = np.random.default_rng(seed)
    total = int(round(LOOP_SECONDS * sr))
    band = np.zeros((total, 2))
    theme = np.zeros((total, 2))
    cache: dict = {}

    def string(note: int, seconds: float, brightness: float) -> np.ndarray:
        key = (note, seconds, brightness)
        if key not in cache:
            cache[key] = pluck_string(midi_to_freq(note), sr, seconds, brightness, seed=note)
        return cache[key]

    # ukulele strum pattern (beats): Down, Down-Up, Up-Down-Up
    strums = [(0, "D"), (1, "D"), (1.5, "U"), (2.5, "U"), (3, "D"), (3.5, "U")]

    for bar in range(LOOP_BARS):
        chord = PROGRESSION[bar % len(PROGRESSION)]
        bar_start = int(bar * BAR_SECONDS * sr)

        # quiet pad as glue
        for note in chord.pad:
            _mix(band, bar_start, _pad_voice(midi_to_freq(note), sr, BAR_SECONDS, 1.5), 0.03)

        # ukulele: strings of a strum are a few ms apart, up-strums are lighter
        for beat, direction in strums:
            start = _beat_to_sample(bar, beat, sr, rng)
            strings = chord.ukulele if direction == "D" else chord.ukulele[::-1]
            velocity = (1.0 if direction == "D" else 0.55) * rng.uniform(0.8, 1.05)
            for j, note in enumerate(strings):
                offset = int(j * (0.014 if direction == "D" else 0.009) * sr)
                pan = -0.25 + 0.5 * (chord.ukulele.index(note) / 3)
                _mix(band, start + offset, string(note, 1.2, 1.3), 0.09 * velocity, pan)

        # plucked bass: root on 1, fifth on 3, a passing root on the swung "and" of 4
        for beat, interval, gain in ((0, 0, 0.5), (2, 7, 0.4), (3.5, 0, 0.25)):
            start = _beat_to_sample(bar, beat, sr, rng, humanize=0.006)
            note = chord.bass - 12 + interval
            _mix(band, start, string(note, 1.6, 0.45), gain * rng.uniform(0.9, 1.05))

        # shaker on every eighth, accented off-beats
        for eighth in range(8):
            start = _beat_to_sample(bar, eighth / 2, sr, rng, humanize=0.008)
            gain = (0.05 if eighth % 2 else 0.025) * rng.uniform(0.7, 1.1)
            _mix(band, start, _shaker(sr, rng), gain, pan=0.3)

    # whistled theme
    for bar, beat, length, note in THEME:
        start = _beat_to_sample(bar, beat, sr, rng, humanize=0.015)
        seconds = length * BEAT_SECONDS * 0.95
        _mix(theme, start, whistle(midi_to_freq(note), sr, seconds, seed=bar), 0.25, pan=-0.1)

    band += _vinyl(total, sr, rng)[:, None]
    # the same tape wobble is applied to both layers, so they stay in sync
    return _normalize(lofi(band, sr), 0.75), _normalize(lofi(theme, sr), 0.6)


# ---------------------------------------------------------------- bounce notes


def _soft_attack(t: np.ndarray, seconds: float) -> np.ndarray:
    """Raised-cosine fade in: no click or "hit" at the start of the note."""
    return 0.5 - 0.5 * np.cos(np.pi * np.clip(t / seconds, 0, 1))


def vibraphone(note: int, sr: int) -> np.ndarray:
    """Soft-mallet vibraphone: round tone with a gentle tremolo (mono)."""
    freq = midi_to_freq(note)
    t = _time(sr, 1.8)
    tone = np.sin(TWO_PI * freq * t) * np.exp(-t * 1.6) + 0.06 * np.sin(TWO_PI * 4 * freq * t) * np.exp(-t * 6)
    tremolo = 1 - 0.2 * (0.5 + 0.5 * np.sin(TWO_PI * 5 * t))
    out = tone * tremolo * _soft_attack(t, 0.012)
    return _normalize(_filter(out, sr, high_cut=3500), 0.9)


def ocarina(note: int, sr: int) -> np.ndarray:
    """Breathy ocarina: a short, soft, airy note with no attack transient (mono)."""
    rng = np.random.default_rng(note)
    freq = midi_to_freq(note)
    t = _time(sr, 0.7)
    f = freq * (1 + 0.006 * np.sin(TWO_PI * 5.5 * t) * np.clip((t - 0.1) / 0.2, 0, 1))
    phase = TWO_PI * np.cumsum(f) / sr
    tone = np.sin(phase) + 0.08 * np.sin(2 * phase) + 0.03 * np.sin(3 * phase)
    breath = 0.08 * _filter(rng.standard_normal(len(t)), sr, high_cut=2500) * (0.6 + 0.4 * np.sin(phase))
    env = _soft_attack(t, 0.035) * np.where(t < 0.2, 1.0, np.exp(-(t - 0.2) * 7))
    return _normalize((tone + breath) * env, 0.9)


def felt_piano(note: int, sr: int) -> np.ndarray:
    """Felt piano: muted hammers, warm but present, gently fading (mono).

    A soft hammer "touch" marks the start of the note, so the player clearly hears
    each bounce without the hard click of a metallic instrument.
    """
    freq = midi_to_freq(note)
    t = _time(sr, 1.6)
    out = np.zeros(len(t))
    for k in range(1, 9):
        detune = 1 + 0.0004 * k**2  # slight string stiffness
        decay = 1.8 + 1.1 * k
        out += (
            np.exp(-t * decay)
            / k**1.6
            * (np.sin(TWO_PI * k * freq * detune * t) + np.sin(TWO_PI * k * freq * detune * 1.0006 * t))
        )
    touch = 0.6 * _filter(np.random.default_rng(note).standard_normal(len(t)), sr, low_cut=300, high_cut=1500)
    out += touch * np.exp(-t * 60)  # felt hammer hitting the string
    out *= _soft_attack(t, 0.004)
    return _normalize(_filter(out, sr, high_cut=3800), 0.9)


def handpan(note: int, sr: int) -> np.ndarray:
    """Handpan (hang drum): a hand-played, tuned steel drum (mono).

    Its timbre is unlike anything in the background band (strings, whistle, pad), so the
    bounce notes stand out. Partials are the note, its octave and its twelfth, all
    consonant, each slightly detuned against a twin to get the typical shimmer.
    """
    freq = midi_to_freq(note)
    t = _time(sr, 2.0)
    out = np.zeros(len(t))
    for ratio, amp, decay in ((1, 1.0, 1.3), (2, 0.4, 2.0), (3, 0.15, 3.2)):
        f = freq * ratio
        out += amp * np.exp(-t * decay) * 0.5 * (np.sin(TWO_PI * f * t) + np.sin(TWO_PI * f * 1.0015 * t + 1.0))
    hand = 0.5 * _filter(np.random.default_rng(note).standard_normal(len(t)), sr, high_cut=350)
    out += hand * np.exp(-t * 40)  # soft thump of the hand on the steel
    out *= _soft_attack(t, 0.006)
    return _normalize(_filter(out, sr, high_cut=5000), 0.9)


BOUNCE_INSTRUMENTS = {"handpan": handpan, "vibraphone": vibraphone, "ocarina": ocarina, "felt_piano": felt_piano}


# ---------------------------------------------------------------- moo


def moo(sr: int, start_note: float, peak_note: float, end_note: float, seed: int = 0) -> np.ndarray:
    """Cartoon cow "muuu": a voice with a pitch glide and "m" -> "oo" formants (mono).

    The notes are MIDI numbers, chosen from the key so the moo sits well on the music.
    """
    rng = np.random.default_rng(seed)
    dur = 1.4
    t = _time(sr, dur)
    n = len(t)

    # pitch contour: quick rise, then a long fall, with vibrato growing at the end
    rise = 0.18
    f_start, f_peak, f_end = (midi_to_freq(x) for x in (start_note, peak_note, end_note))
    f0 = np.where(
        t < rise,
        f_start + (f_peak - f_start) * (t / rise),
        f_end + (f_peak - f_end) * (0.5 + 0.5 * np.cos(np.pi * np.clip((t - rise) / (dur - rise), 0, 1))),
    )
    f0 *= 1 + 0.015 * np.sin(TWO_PI * 5.5 * t) * np.clip((t - 0.4) / 0.6, 0, 1)
    phase = TWO_PI * np.cumsum(f0) / sr

    # mouth opening: closed "m" -> open "oo/uh"
    opening = np.clip((t - 0.05) / 0.3, 0, 1)
    f1 = 280 + 320 * opening
    f2 = 850 + 250 * opening

    def resonance(freq, centre, width):
        return np.exp(-(((freq - centre) / width) ** 2))

    voice = np.zeros(n)
    for k in range(1, 40):
        fk = k * f0
        if np.min(sr / 2 - fk) < 0:
            break
        amp = (resonance(fk, f1, 180) + 0.5 * resonance(fk, f2, 250) + 0.04) / np.sqrt(k)
        voice += amp * np.sin(k * phase)
    voice *= 0.35 + 0.65 * opening  # "m" is quieter (nasal)
    voice += 0.02 * rng.standard_normal(n) * opening  # breath

    env = np.clip(t / 0.06, 0, 1) * np.clip((dur - t) / 0.4, 0, 1)
    return _normalize(voice * env, 0.9)


# ---------------------------------------------------------------- game over


def sad_trombone(sr: int) -> np.ndarray:
    """Descending "wah wah wah waaah" for the game over (mono)."""
    notes = [(57, 0.5), (56, 0.5), (55, 0.5), (54, 1.8)]  # A3 G#3 G3 F#3
    gap = 0.05
    total = sum(d + gap for _, d in notes) + 0.3
    out = np.zeros(int(total * sr))
    pos = 0.0
    for i, (note, dur) in enumerate(notes):
        last = i == len(notes) - 1
        t = _time(sr, dur)
        freq = midi_to_freq(note) * (1 - 0.03 * np.exp(-t * 18))  # small scoop into the note
        if last:
            freq = freq * (1 + 0.02 * np.sin(TWO_PI * 6 * t) * np.clip(t / 0.5, 0, 1))  # wobble
        phase = TWO_PI * np.cumsum(freq) / sr
        # "wah": brightness opens and closes like a plunger mute
        bright = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.7
        tone = np.zeros(len(t))
        for k in range(1, 20):
            tone += np.exp(-k * (1.2 - bright) * 0.5) / k**0.3 * np.sin(k * phase)
        env = np.clip(t / 0.04, 0, 1) * np.clip((dur - t) / (0.6 if last else 0.08), 0, 1)
        start = int(pos * sr)
        out[start : start + len(t)] += tone * env
        pos += dur + gap
    return _normalize(out, 0.85)
