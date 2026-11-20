"""Audio manager: plays music and sound effects in response to game events."""

import math
import random
from collections import deque
from pathlib import Path

import numpy as np
import pygame

from cowabunga.env.events import Event
from cowabunga.py_game.audio import synth
from cowabunga.py_game.audio.theory import (
    BEAT_SECONDS,
    MELODY_HIGH,
    MELODY_LOW,
    SWING,
    chord_at,
    melody_notes,
)

SOUNDS_DIR = Path(__file__).parent / ".." / "assets" / "sounds"


class BounceSequencer:
    """Turns paddle bounces into a melody that never clashes with the music.

    - Every note is a chord tone of the chord the music is playing at that moment.
    - The melody walks up and down the chord (arpeggio), one step per note.
    - Every bounce plays an accented note immediately, so the player hears the confirmation.
    - The more often cows bounce, the more lighter fill notes follow each bounce and the
      shorter the gap between them: the melody speeds up with the action.
    - Extra notes fall on the music's rhythmic grid, so they stay in time too.

    Times are in seconds on the music clock (0 = start of the music loop).
    """

    RATE_WINDOW = 4.0  # seconds used to measure the bounce rate
    # (min bounces per second, notes per bounce, gap between notes in beats)
    TIERS = (
        (0.0, 1, 1 / 2),  # calm: one note per bounce
        (0.6, 2, 1 / 2),  # eighth notes
        (1.2, 2, 1 / 4),  # sixteenth notes
        (2.0, 3, 1 / 4),
        (3.0, 4, 1 / 6),  # sixteenth-note triplets
    )
    MAX_PENDING = 6  # avoids long queues when many cows bounce together
    RESET_AFTER = 4.0  # seconds of silence after which the melody restarts from the bottom

    def __init__(self):
        self.reset()

    def reset(self):
        """Clears the sequencer state."""
        self.bounce_times: deque[float] = deque()
        self.pending = 0
        self.next_time = -math.inf
        self.position = 0
        self.direction = 1
        self.last_note_time = -math.inf

    def tier(self, now: float) -> int:
        """Returns the intensity level (index of TIERS) from the recent bounce rate."""
        while self.bounce_times and now - self.bounce_times[0] > self.RATE_WINDOW:
            self.bounce_times.popleft()
        rate = len(self.bounce_times) / self.RATE_WINDOW
        return max(i for i, (min_rate, _, _) in enumerate(self.TIERS) if rate >= min_rate)

    def _next_grid_time(self, now: float, tier: int) -> float:
        """Next point of the rhythmic grid. Eighth notes swing like the music."""
        step_beats = self.TIERS[tier][2]
        step = step_beats * BEAT_SECONDS
        swing = SWING * BEAT_SECONDS if step_beats == 1 / 2 else 0.0
        k = math.floor(now / step)
        while True:
            k += 1
            t = k * step + (swing if k % 2 else 0.0)
            if t - now >= step * 0.5:  # not too close to the note just played
                return t

    def on_bounce(self, now: float) -> list[tuple[int, int, bool]]:
        """Registers a bounce. Returns the notes to play immediately as (midi, tier, accent).

        Every bounce plays an accented note right away: it confirms the bounce to the
        player. The extra notes of faster tiers are queued as lighter fills.
        """
        self.bounce_times.append(now)
        tier = self.tier(now)
        notes_per_bounce = self.TIERS[tier][1]
        self.pending = min(self.MAX_PENDING, self.pending + notes_per_bounce - 1)
        self.next_time = self._next_grid_time(now, tier)  # fills restart after this note
        return [(self._next_note(now), tier, True)]

    def update(self, now: float) -> list[tuple[int, int, bool]]:
        """Called every frame. Returns the queued fill notes due now as (midi, tier, accent)."""
        if self.pending == 0 or now < self.next_time:
            return []
        tier = self.tier(now)
        self.pending -= 1
        self.next_time = self._next_grid_time(now, tier)
        return [(self._next_note(now), tier, False)]

    def _next_note(self, now: float) -> int:
        if now - self.last_note_time > self.RESET_AFTER:
            self.position, self.direction = 0, 1
        self.last_note_time = now
        notes = melody_notes(chord_at(now))
        self.position = min(self.position, len(notes) - 1)
        note = notes[self.position]
        # bounce back at the ends of the range (ping-pong arpeggio)
        if not 0 <= self.position + self.direction < len(notes):
            self.direction = -self.direction
        self.position += self.direction
        return note


class AudioManager:
    """Loads/generates all sounds and plays them according to game state and events.

    If the audio device is not available the manager stays silent instead of crashing.
    A file in assets/sounds (music.ogg, moo.ogg, game_over.ogg) replaces the generated sound.
    """

    MUSIC_VOLUME = 0.4
    MUSIC_VOLUME_PAUSED = 0.5  # music is halved while the game is paused
    THEME_VOLUME_MENU = 0.5  # whistled theme: in front in the menu...
    THEME_VOLUME_GAME = 0.12  # ...in the background while playing
    # instrument of the bounce melody: "handpan", "vibraphone", "ocarina" or "felt_piano".
    # The handpan is not part of the background band, so bounces are easy to recognize.
    BOUNCE_INSTRUMENT = "handpan"
    # volume of each instrument, balanced so notes are clearly heard but not harsh over the music
    NOTE_VOLUMES = {"handpan": 0.65, "vibraphone": 0.33, "ocarina": 0.32, "felt_piano": 0.52}
    DEFAULT_LEVEL = 0.8  # default player volume settings (0 = mute, 1 = full)
    FILL_VOLUME = 0.6  # extra notes between bounces, relative to the bounce note
    MOO_VOLUME = 0.8
    GAME_OVER_VOLUME = 0.8
    MUSIC_FADE_IN_MS = 2500
    MUSIC_FADE_OUT_MS = 1500

    def __init__(self):
        self.enabled = False
        self.music_on = False
        self.music_start_ms = pygame.time.get_ticks()
        self.paused = False
        self.in_menu = True
        self.volumes = {"band": 0.0, "theme": 0.0}  # current (smoothed) volumes of the two music layers
        # player settings, from 0 (mute) to 1 (full): scale the balanced volumes above
        self.music_level = self.DEFAULT_LEVEL
        self.sfx_level = self.DEFAULT_LEVEL
        self.sequencer = BounceSequencer()
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self._build_sounds()
            pygame.mixer.set_num_channels(32)
            pygame.mixer.set_reserved(2)
            self.music_channels = {"band": pygame.mixer.Channel(0), "theme": pygame.mixer.Channel(1)}
            self.enabled = True
        except Exception as e:
            print(f"Audio disabled: {e}")

    # ------------------------------------------------------------ setup

    def _to_sound(self, samples: np.ndarray) -> pygame.mixer.Sound:
        """Converts a float array in [-1, 1] to a Sound in the mixer's format."""
        _, size, channels = pygame.mixer.get_init()
        if samples.ndim == 1:
            samples = np.repeat(samples[:, None], channels, axis=1)
        elif samples.shape[1] != channels:
            samples = np.repeat(samples.mean(axis=1, keepdims=True), channels, axis=1)
        samples = np.clip(samples, -1, 1)
        if size == 32:
            data = samples.astype(np.float32)
        elif size == 8:
            data = ((samples + 1) * 127.5).astype(np.uint8)
        elif size == -8:
            data = (samples * 127).astype(np.int8)
        elif size == 16:
            data = ((samples + 1) * 32767.5).astype(np.uint16)
        else:
            data = (samples * 32767).astype(np.int16)
        return pygame.mixer.Sound(buffer=np.ascontiguousarray(data).tobytes())

    def _load_or_generate(self, name: str, generate) -> pygame.mixer.Sound:
        path = SOUNDS_DIR / f"{name}.ogg"
        if path.exists():
            try:
                return pygame.mixer.Sound(path)
            except Exception as e:
                print(f"Unable to load {path}, using generated sound: {e}")
        return self._to_sound(generate())

    def _build_sounds(self):
        sr = pygame.mixer.get_init()[0]
        music_file = SOUNDS_DIR / "music.ogg"
        if music_file.exists():  # a recorded track replaces both generated layers
            self.music = {"band": pygame.mixer.Sound(music_file), "theme": None}
        else:
            band, theme = synth.background_layers(sr)
            self.music = {"band": self._to_sound(band), "theme": self._to_sound(theme)}
        self.notes = {
            n: self._to_sound(synth.BOUNCE_INSTRUMENTS[self.BOUNCE_INSTRUMENT](n, sr))
            for n in range(MELODY_LOW, MELODY_HIGH + 1)
        }
        # a few variations, all moving between notes of the key (D major)
        variants = [(47, 50, 45), (50, 52, 45), (45, 50, 42)]
        self.moos = [
            self._load_or_generate("moo", lambda v=v, i=i: synth.moo(sr, *v, seed=i)) for i, v in enumerate(variants)
        ]
        self.game_over_sound = self._load_or_generate("game_over", lambda: synth.sad_trombone(sr))

    # ------------------------------------------------------------ helpers

    def music_time(self) -> float:
        """Seconds since the music loop started (the clock the melody follows)."""
        return (pygame.time.get_ticks() - self.music_start_ms) / 1000

    def _play(self, sound: pygame.mixer.Sound, volume: float, pan: float = 0.0):
        """Plays a sound effect on a free channel. pan goes from -1 (left) to 1 (right)."""
        volume *= self.sfx_level
        if volume <= 0:
            return
        channel = sound.play()
        if channel is not None:
            channel.set_volume(volume * min(1.0, 1 - pan), volume * min(1.0, 1 + pan))

    def _play_notes(self, notes: list[tuple[int, int, bool]]):
        for note, tier, accent in notes:
            # the bounce note is loud and clear (feedback for the player), fills are lighter
            volume = self.NOTE_VOLUMES[self.BOUNCE_INSTRUMENT] * (1.0 if accent else self.FILL_VOLUME)
            volume *= (1 + 0.05 * tier) * random.uniform(0.92, 1.03)
            pan = (note - (MELODY_LOW + MELODY_HIGH) / 2) / (MELODY_HIGH - MELODY_LOW)  # high notes right
            self._play(self.notes[note], volume, pan * 0.6)

    # ------------------------------------------------------------ public API

    def start_music(self):
        """Starts the background music loop if it isn't already playing."""
        if not self.enabled or self.music_on:
            return
        self.volumes = {name: self._target_volume(name) for name in self.volumes}
        for name, channel in self.music_channels.items():
            channel.stop()
            if self.music[name] is not None:
                # both layers start together so they stay in sync
                channel.play(self.music[name], loops=-1, fade_ms=self.MUSIC_FADE_IN_MS)
                channel.set_volume(self.volumes[name])
        self.music_start_ms = pygame.time.get_ticks()
        self.sequencer.reset()
        self.music_on = True

    def set_paused(self, paused: bool):
        """Lowers the music while the game is paused."""
        self.paused = paused

    def set_menu(self, in_menu: bool):
        """Brings the whistled theme to the front in the menu and back during the game."""
        self.in_menu = in_menu

    def set_music_level(self, level: float):
        """Sets the player's music volume, from 0 (mute) to 1 (full)."""
        self.music_level = min(1.0, max(0.0, level))

    def set_sfx_level(self, level: float):
        """Sets the player's sound effects volume, from 0 (mute) to 1 (full)."""
        self.sfx_level = min(1.0, max(0.0, level))

    def preview_sfx(self):
        """Plays a bounce note, so the player hears the effects volume they chose."""
        if self.enabled:
            notes = melody_notes(chord_at(self.music_time()))
            self._play(self.notes[notes[len(notes) // 2]], self.NOTE_VOLUMES[self.BOUNCE_INSTRUMENT])

    def _target_volume(self, layer: str) -> float:
        volume = self.MUSIC_VOLUME * self.music_level
        if self.paused:
            volume *= self.MUSIC_VOLUME_PAUSED
        if layer == "theme":
            volume *= self.THEME_VOLUME_MENU if self.in_menu else self.THEME_VOLUME_GAME
        return volume

    def game_over(self):
        """Fades the music out and plays the game over sound."""
        if not self.enabled:
            return
        for channel in self.music_channels.values():
            channel.fadeout(self.MUSIC_FADE_OUT_MS)
        self.music_on = False
        self.sequencer.reset()
        self._play(self.game_over_sound, self.GAME_OVER_VOLUME)

    def process_events(self, events: list[Event]):
        """Plays the sounds for the events of one env step."""
        if not self.enabled:
            return
        for event in events:
            if event == Event.BOUNCE:
                self._play_notes(self.sequencer.on_bounce(self.music_time()))
            elif event == Event.COW_LOST:
                self._play(random.choice(self.moos), self.MOO_VOLUME, random.uniform(-0.3, 0.3))
            elif event == Event.GAME_OVER:
                self.game_over()

    def update(self):
        """Called once per frame: plays queued melody notes and smooths music volume."""
        if not self.enabled:
            return
        self._play_notes(self.sequencer.update(self.music_time()))
        if not self.music_on:
            return
        for name, channel in self.music_channels.items():
            target = self._target_volume(name)
            if self.volumes[name] != target:
                self.volumes[name] += (target - self.volumes[name]) * 0.12  # smooth fade
                if abs(self.volumes[name] - target) < 0.003:
                    self.volumes[name] = target
                channel.set_volume(self.volumes[name])
