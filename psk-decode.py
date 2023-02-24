#
# ☮ mvxim
# A python script that decodes a phase key shifted .wav file.
# Run 'python3 decode.py' in the same directory as 'output.wav'.
# The text from the decoded audio will be displayed.
#            _       _                    _
#           | |     | |                  | |
#  _ __  ___| | ____| | ___  ___ ___   __| | ___ _ __
# | '_ \/ __| |/ / _` |/ _ \/ __/ _ \ / _` |/ _ \ '__|
# | |_) \__ \   < (_| |  __/ (_| (_) | (_| |  __/ |
# | .__/|___/_|\_\__,_|\___|\___\___/ \__,_|\___|_|
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

# Open the WAV file for reading
wavefile = wave.open("output.wav", "r")

# Read the parameters of the WAV file
nchannels, sampwidth, framerate, nframes, comptype, compname = wavefile.getparams()

# Read the audio data from the WAV file
frames = wavefile.readframes(nframes)

# Close the WAV file
wavefile.close()

# Convert the audio data to a list of samples
samples = struct.unpack_from("<" + str(nframes) + "h", frames)

# Initialize the decoded message
message = ""

# Loop over the samples
for i in range(0, len(samples), int(duration * framerate)):
    # Calculate the phase shift between the low and high frequencies
    phase_shift = math.atan2(samples[i+int(duration * framerate/4)], samples[i+int(duration * framerate/4)*3])

    # Determine if the bit is a 0 or a 1 based on the phase shift
    if phase_shift > 0:
        message += "1"
    else:
        message += "0"

# Convert the binary string to plain text
decoded_message = ""
for i in range(0, len(message), 8):
    decoded_message += chr(int(message[i:i+8], 2))

# Print the decoded message
print(decoded_message)
