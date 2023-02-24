#
# ☮ mvxim
# An adaptation of a script that converts an image into a frequency pattern on a spectrogram.
# Run with: python3 spectrogen.py /path/to/imagename.jpg /output/path/filename.wav
#                      _                              
#                     | |                             
#  ___ _ __   ___  ___| |_ _ __ ___   __ _  ___ _ __  
# / __| '_ \ / _ \/ __| __| '__/ _ \ / _` |/ _ \ '_ \ 
# \__ \ |_) |  __/ (__| |_| | | (_) | (_| |  __/ | | |
# |___/ .__/ \___|\___|\__|_|  \___/ \__, |\___|_| |_|
#     | |                             __/ |           
#     |_|                            |___/           
#

import wave, struct, math
import numpy as np
from PIL import Image

import scipy.ndimage

def loadPicture(size, file, contrast=True, highpass=False, verbose=1):
    img = Image.open(file)
    img = img.convert("L")
    
    imgArr = np.array(img)
    imgArr = np.flip(imgArr, axis=0)
    if verbose:
        print("Image original size: ", imgArr.shape)
        
    if contrast:
        imgArr = 1/(imgArr+10**15.2)
    else:
        imgArr = 1 - imgArr

    imgArr -= np.min(imgArr)
    imgArr = imgArr/np.max(imgArr)

    if highpass:
        removeLowValues = np.vectorize(lambda x: x if x > 0.5 else 0, otypes=[np.float])
        imgArr = removeLowValues(imgArr)

    if size[0] == 0:
        size = imgArr.shape[0], size[1]
    if size[1] == 0:
        size = size[0], imgArr.shape[1]
    resamplingFactor = size[0]/imgArr.shape[0], size[1]/imgArr.shape[1]
    if resamplingFactor[0] == 0:
        resamplingFactor = 1, resamplingFactor[1]
    if resamplingFactor[1] == 0:
        resamplingFactor = resamplingFactor[0], 1
    

    imgArr = scipy.ndimage.zoom(imgArr, resamplingFactor, order=0)
    
    if verbose:
        print("Resampling factor", resamplingFactor)
        print("Image resized :", imgArr.shape)
        print("Max intensity: ", np.max(imgArr))
        print("Min intensity: ", np.min(imgArr))
    return imgArr

def genSoundFromImage(file, output="sound.wav", duration=5.0, sampleRate=44100.0, intensityFactor=1, min_freq=0, max_freq=22000, invert=False, contrast=True, highpass=True, verbose=False):
    wavef = wave.open(output,'w')
    wavef.setnchannels(1)
    wavef.setsampwidth(2) 
    wavef.setframerate(sampleRate)
    
    max_frame = int(duration * sampleRate)
    max_intensity = 32767 
    
    stepSize = 400 
    steppingSpectrum = int((max_freq-min_freq)/stepSize)
    
    imgMat = loadPicture(size=(steppingSpectrum, max_frame), file=file, contrast=contrast, highpass=highpass, verbose=verbose)
    if invert:
        imgMat = 1 - imgMat
    imgMat *= intensityFactor
    imgMat *= max_intensity 
    if verbose:
        print("Input: ", file)
        print("Duration (in seconds): ", duration)
        print("Sample rate: ", sampleRate)
        print("Computing each soundframe sum value..")
    for frame in range(max_frame):
        if frame % 60 == 0: 
            print("Progress: ==> {:.2%}".format(frame/max_frame), end="\r")
        signalValue, count = 0, 0
        for step in range(steppingSpectrum):
            intensity = imgMat[step, frame]
            if intensity < 0.1*intensityFactor:
                continue
         
            currentFreq = (step * stepSize) + min_freq
            nextFreq = ((step+1) * stepSize) + min_freq
            if nextFreq - min_freq > max_freq: 
                nextFreq = max_freq
            for freq in range(currentFreq, nextFreq, 1000):
                signalValue += intensity*math.cos(freq * 2 * math.pi * float(frame) / float(sampleRate))
                count += 1
        if count == 0: count = 1
        signalValue /= count
        
        data = struct.pack('<h', int(signalValue))
        wavef.writeframesraw( data )
        
    wavef.writeframes(''.encode())
    wavef.close()
    print("\nProgress: ==> 100%")
    if verbose:
        print("Output: ", output)

import sys
import argparse

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("inputImage", help="Input image in any PIL supported format (JPG, PNG (with and without alpha), BMP etc...)")
    parser.add_argument("outputFile", help="path where to output the soundfile in WAV format")
    parser.add_argument("-d", "--duration", help="Duration of the sound to output, in whole seconds, default: 5", type=int)
    parser.add_argument("-n", "--minFreq", help="Minimum frequency to use, in Hz, default: 0", type=int)
    parser.add_argument("-x", "--maxFreq", help="Maximum frequency to use, in Hz, default: 22000", type=int)
    parser.add_argument("-s", "--samplerate", help="Sample rate of the sound to output, in Hertz, default: 44100", type=int)
    parser.add_argument("-if", "--intensityFactor", help="Factory by which multiply the image intensity, in decimal, default: 1.0", type=float)
    parser.add_argument("-i", "--invert", help="Invert the image intensity, resulting in an inverted spectrum", action="store_true")
    parser.add_argument("-c", "--contrast", help="Increases image's contrast before converting it, can enhance the resulting spectrum", action="store_true")
    parser.add_argument("-hi", "--highintensity", help="Cut low intensity pixels, can enhance result", action="store_true")
    parser.add_argument("-v", "--verbose", help="Display verbose", action="store_true")
    args = parser.parse_args()
    
    img = args.inputImage
    output = args.outputFile
    duration = 5 if not args.duration else args.duration
    min_freq = 0 if not args.minFreq else args.minFreq
    max_freq = 22000 if not args.maxFreq else args.maxFreq
    sampleRate = 44100 if not args.samplerate else args.samplerate
    intensityFactor = 1 if not args.intensityFactor else args.intensityFactor
    invert = args.invert
    contrast = args.contrast
    highpass = args.highintensity 
    verbose = args.verbose

    genSoundFromImage(
            file=img, 
            output=output, 
            duration=duration, 
            sampleRate=sampleRate,
            min_freq=min_freq,
            max_freq=max_freq,
            contrast=contrast, 
            invert=invert, 
            intensityFactor=intensityFactor,
            highpass=highpass, 
            verbose=verbose)

if __name__ == "__main__":
    main(sys.argv[1:])