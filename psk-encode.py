#
# ☮ mvxim
# A python script that converts a message into a phase key shifted .wav file.
# Enter the message below, and run 'python3 pskgen.py' in the same directory as the file.
# A file called output.wav will be saved.
#            _                            _
#           | |                          | |
#  _ __  ___| | _____ _ __   ___ ___   __| | ___ _ __
# | '_ \/ __| |/ / _ \ '_ \ / __/ _ \ / _` |/ _ \ '__|
# | |_) \__ \   <  __/ | | | (_| (_) | (_| |  __/ |
# | .__/|___/_|\_\___|_| |_|\___\___/ \__,_|\___|_|
# | |
# |_|
#

import wave
import struct
import math

# Define the frequency and duration of the tones
freq_low = 500
freq_high = 1500
duration = 0.1

# Open a WAV file for writing
wavefile = wave.open("output.wav", "w")

# Set the parameters of the WAV file
wavefile.setnchannels(1)     # mono
wavefile.setsampwidth(2)     # 16-bit
wavefile.setframerate(44100) # CD quality

# Define the message to be encoded
message = "a message here"

# Loop over each character in the message
for char in message:
    # Convert the character to a binary string
    binary = bin(ord(char))[2:].zfill(8)

    # Loop over each bit in the binary string
    for bit in binary:
        # Calculate the frequency of the tone based on the bit value
        if bit == '0':
            freq = freq_low
        else:
            freq = freq_high

        # Generate the tone and write it to the WAV file
        for i in range(int(duration * 44100)):
            sample = int(32767 * math.sin(freq * 2 * math.pi * i / 44100))
            data = struct.pack("<h", sample)
            wavefile.writeframesraw(data)

# Close the WAV file
wavefile.close()
