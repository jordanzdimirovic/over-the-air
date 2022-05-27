# Library for encoding, decoding and playing text to sound

### IMPORTS
from math import log2
import time
import pygame
import numpy as np
### SRC
### Helpers for instruction following
sound_on = lambda sec: (True, sec)
sound_off = lambda sec: (False, sec)

class TonePlayer():
    """
        A player object that can play tones.
    """
    def __init__(self, volume, freq):
        self.pitch = 2 * log2(freq / 440) + 9
        self.decib = 20 * log2(volume)
        self.playing = False
        # Cap at 0 decibels
        self.decib = 0 if self.decib > 0 else self.decib
        
        pygame.mixer.init(44100,-16,2,512)

        arr = np.array([4096 * np.sin(2.0 * np.pi * freq * x / 44100) for x in range(0, 44100)]).astype(np.int16)
        arr2 = np.c_[arr,arr]
        self.sound = pygame.sndarray.make_sound(arr2)

    def set_pitch(self, new_pitch):
        self.pitch = new_pitch
        self.sw.set_pitch(self.pitch)

    def play_s(self, sec):
        self.sound_on()
        time.sleep(sec)
        self.sound_off()

    def play_ms(self, msec):
        self.play_s(msec / 1000)

    def sound_on(self):
        self.sound.play(-1)
        self.playing = True
    
    def sound_off(self):
        self.sound.stop()
        self.playing = False

    def play_instructions(self, *instr):
        for v in instr:
            if v[0]: # If play
                if not self.playing:
                    self.sound_on()
                time.sleep(v[1])
            else:
                self.sound_off()
                time.sleep(v[1])

        self.sound_off()

    def hello(self):
        self.play_instructions(
            sound_on(0.2),
            sound_off(0.1),
            sound_on(0.2),
            sound_off(0.7),

            sound_on(0.2),
            sound_off(0.1),
            sound_on(0.2),
            sound_off(0.7),

            sound_on(1.1),
            sound_off(0.2),

            sound_on(0.2),
            sound_off(0.1),
            sound_on(0.2)
        )


class OTA():
    """
        Represents an over-the-air communications
        management object.
    """
    def __init__(self, bit_length, byte_sep):
        """Constructor for OTA object."""
        pass

    def config_instructions(self):
        """Encode config info to sound and play it."""
        pass


def main():
    from timeit import default_timer
    # Create sound player
    # Test tone length
    
    tp = TonePlayer(0.2, 3400)

    t1 = default_timer()
    
    n = 0.08
    ttlen = n * 8
    tp.play_instructions(
        sound_on(n),
        sound_off(n),
        sound_on(n),
        sound_off(n),
        sound_on(n),
        sound_off(n),
        sound_on(n),
        sound_off(n),
    )

    t2 = default_timer()
    ttaken = t2 - t1
    print(f"Requested: {ttlen} seconds.")
    print(f"Actual: {ttaken} seconds.")
    print(f"Diff: {abs(ttlen - ttaken)} seconds.")
    print(f"Ratio: {abs(ttlen - ttaken)/ttlen}%.")
    
    

if __name__ == '__main__': main()
