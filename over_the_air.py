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
        self.volume = volume
        self.freq = freq
        self.playing = False
        pygame.mixer.init(44100,-16,2,512)
        self.generate_sound(volume, freq)
        
    def generate_sound(self, volume, freq):
        arr = np.array([4096 * volume * np.sin(2.0 * np.pi * freq * x / 44100) for x in range(0, 44100)]).astype(np.int16)
        arr2 = np.c_[arr,arr]
        self.sound = pygame.sndarray.make_sound(arr2)

    def set_freq(self, new_freq):
        self.freq = new_freq
        self.generate_sound(self.volume, new_freq)

    def set_vol(self, new_vol):
        self.freq = new_vol
        self.generate_sound(new_vol, self.freq)

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


def bin2dec(v: str):
    """Convert a binary number (as string) to decimal"""
    assert all(l in "01" for l in v), "Binary string had digit that wasn't 0 or 1."
    assert len(v) == 8, "Binary string must represent a single byte."
    return sum(int(v[-(i+1)]) * (2**i) for i in range(8))

def dec2bin(v: int):
    """Convert a decimal number to binary number (as string)"""
    assert 0 <= v <= 255, f"Value {v} must be within the size of a byte, and can't be negative."
    b = ["0"] * 8
    for i in range(8):
        d = 2 ** (7-i)
        if v >= d:
            v -= d
            b[i] = "1"
    
    assert v == 0, "Something went horribly wrong."

    return "".join(b)

class OTA():
    """
        Represents an over-the-air communications
        management object.
    """
    def __init__(self, bit_length, byte_sep):
        """Constructor for OTA object."""
        self.bit_length = bit_length
        self.byte_sep = byte_sep

        self.tone_player = TonePlayer(1, 440)

    def get_bit_play_instructions(self, bitstr, padded = True) -> list:
        padding = [sound_on(self.bit_length)] if padded else []

        return padding + [
            sound_on(self.bit_length) if int(v) else sound_off(self.bit_length)
            for v in bitstr
        ] + padding

    def emit_bits(self, bitstr, padded = True):
        """
            Plays a series of bits using the sound system and
            the bit length option provided.
            Pads each end with ON by default so that it can be understood
        """
        sound_instructions = self.get_bit_play_instructions(bitstr, padded)
        self.tone_player.play_instructions(*sound_instructions)

    def emit_byte_series(self, lst_bitstrs):
        """
            Plays a series of bytes
        """
        assert all(len(x) == 8 and all(c in "01" for c in x) for x in lst_bitstrs), "All sequences must be valid bytes."
        sound_instructions = []
        for bitstr in lst_bitstrs:
            sound_instructions.extend(self.get_bit_play_instructions(bitstr, True) + [sound_off(self.byte_sep)])

        self.tone_player.play_instructions(*sound_instructions)
        
    def emit_string(self, string):
        """Plays a string by emiting each character as a byte"""
        charbytes = list(map(dec2bin, [ord(c) for c in string]))
        self.emit_byte_series(charbytes)

    def config_instructions(self):
        """Encode config info to sound and play it."""
        # First, emit 10 alternating bits, twice
        self.emit_bits("10" * 10, padded = False)

# --- TESTING ---

def test_timing():
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

def test_byte_emission():
    ota = OTA(0.08, 1)
    ota.emit_string("a")

def main():
    test_timing()
    test_byte_emission()
    time.sleep(1)
    

if __name__ == '__main__': main()
