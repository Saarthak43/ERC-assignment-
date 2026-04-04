## QUESTION 3

3.An iconic audio is trapped inside a noisy, chaotic audio signal —
distorted, modulated, and begging to be freed. Your mission? Use your
signal-slinging skills to build a filter and cut through the interference.
Think of it as your digital web, catching only the message and letting the
noise fall. Suit up, fire up your code, and bring it back to life. Hint given in
the repo :)

## ANSWER 3 

```cpp
import numpy as np ## calculation of FFT
import matplotlib.pyplot as plt ## plotting of graphs 
from scipy.io import wavfile ## scipy library to read and write wav files
import os ## create direcrtory for plots
os.makedirs("plots", exist_ok=True)
##load the file
sample_rate, data = wavfile.read("corrupted.wav")## reads the corrupted file
data = data.astype(float)
```
In this block of code we are importing different kinds of libraries such as 

import numpy as np
NumPy is a maths library for Python, we'll use it here for FFT calculations .
as np is used so that we write np instead of numpy everytime .

import matplotlib.pyplot as plt
Matplotlib is a graph-plotting library. It lets us draw charts and visualise our data.

from scipy.io import wavfile
SciPy is a scientific computing library
we are not importing everything from this library but only wavfile which lets us read and write .wav files - essentially the sound files

import os
OS stands for Operating System. basically powers on the python

os.makedirs("plots") — creates a folder called plots where all our graph images will be saved
exist_ok=True — means "if the folder already exists, don't crash, just continue". Without this, the code would throw an error if you ran it a second time.

### THE VARIABLES 

sample_rate — stores how many samples exist per second 

data — stores the actual raw audio as a big list of numbers

len(data) - The total number of samples in the entire audio file

```cpp
##stage 1
## time axis
N= len(data)
t = np.linspace(0,N/sample_rate,N)
## graph 1 - Time domain
plt.plot(t,data)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("My graph")
plt.savefig("plots/stage1_time_domain.png")
plt.show() 
##compute fft
freqs = np.fft.rfftfreq(N, d =1/sample_rate)
magnitude = np.abs(np.fft.rfft(data))
```


## What is stage 1 ?

This stage is purely about inspection we're not fixing anything yet, just understanding what the corrupted audio looks like visually and mathematically.
in this stage we are just diagonising the problem , first plotting the waveform wrt time domain , then wrt frequency using FFT calculations. 
It did not look like normal audio. I then calculated the FFT and found a very high peak frequency abnormal for normal speech.

```cpp
#graph 2 fft
plt.plot(freqs, magnitude)
plt.title("Stage 1 - FFT")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.savefig("plots/stage1_FFT.png")
plt.show()

## Find peak frequency
peak = freqs[np.argmax(magnitude)]
print("Peak frequency:", peak, "Hz")

##stage 2
modulated = np.cos(2 * np.pi * 7300 * t)
demodulated = data * modulated

plt.plot(t, demodulated)
plt.title("Stage 2 - After Multiplying by modulated")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.savefig("plots/stage2_intermediate.png")
plt.show()
from scipy.signal import butter, filtfilt

def lowpass(signal, cutoff, fs):
    b, a = butter(5, cutoff/(fs/2), btype='low')
    return filtfilt(b, a, signal)

stage2 = lowpass(demodulated, 4000, sample_rate)
magnitude2 = np.abs(np.fft.rfft(stage2))
```
## What is stage 2?

When I plotted the FFT in Stage 1, I could see that all the audio energy was sitting around 7300 Hz instead of the normal 0–4000 Hz range where human speech lives. This told me the signal had been AM modulated , basically someone took the original audio and artificially shifted it up to 7300 Hz during the corruption process.
To fix this, I multiplied the corrupted signal by a cosine wave at the same 7300 Hz frequency. Think of it like using the same key that locked something to now unlock it  multiplying by the same frequency that shifted the audio up is what brings it back down.
However, this multiplication has a side effect. Along with pulling the audio back down to the right place, it also creates an unwanted ghost copy of the signal up at 14600 Hz. So now I had my real audio sitting correctly at 0–4000 Hz, but with this extra junk copy floating above it.
To get rid of that ghost copy, I applied a low pass filter  which works exactly like its name suggests, it only lets low frequencies pass through and blocks everything above a certain point. I set that cutoff point at 4000 Hz, so the filter kept all the real audio and threw away everything above it including the ghost copy. The butter and filtfilt functions from SciPy are what actually built and applied that filter to the signal.

```cpp
##stage 3
plt.plot(freqs, magnitude2)
plt.title("Stage 3 - FFT after demodulation")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.savefig("plots/stage3_FFT.png")
plt.show()

peak2 = freqs[np.argmax(magnitude2)]
print("Peak after demodulation:", peak2, "Hz")

plt.plot(freqs, magnitude2)
plt.title("Stage 2 - Zoomed FFT")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim(0, 5000)
plt.savefig("plots/stage2_FFT zoomed.png")
plt.show()

from scipy.signal import iirnotch

def notch(signal, freq, fs):
    b, a = iirnotch(freq, 30, fs)
    return filtfilt(b, a, signal)

stage3 = notch(stage2, 1200, sample_rate)
stage3 = notch(stage3, 2200, sample_rate)
stage3 = notch(stage3, 4100, sample_rate)

magnitude3 = np.abs(np.fft.rfft(stage3))

plt.plot(freqs, magnitude3)
plt.title("Stage 3 - After Notch Filters")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim(0, 5000)
plt.savefig("plots/stage3_.png")
plt.show()
```

## What is stage 3?

After demodulation, I ran the FFT again on the recovered signal to check if it looked clean. The frequency plot was mostly smooth, but three suspicious sharp spikes stood out clearly at around 1200 Hz, 2200 Hz and 4100 Hz. Natural audio never produces spikes that narrow and precise  real sounds spread their energy across a range of frequencies. Spikes that sharp can only mean one thing  artificial tones were deliberately injected into the signal during corruption.
To remove them, I used a notch filter — a filter that is designed to surgically target one specific frequency and cut it out, while leaving everything around it completely untouched. Unlike a low pass filter which removes a whole range, a notch filter is very precise. I applied one notch filter for each of the three spikes, removing all three interference tones and leaving the actual audio clean underneath.

```cpp
##stage 4
plt.plot(t, stage3)
plt.title("Stage 4 - Before DC Removal (problem visible)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.savefig("plots/stage4_before.png")
plt.show()

stage4 = stage3 - np.mean(stage3)

stage4 = stage4 / np.max(np.abs(stage4))

recovered = np.int16(stage4 * 32767)

plt.plot(t, stage4)
plt.title("Stage 4 - After DC Removal (fixed)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.savefig("plots/stage4_after.png")
plt.show()

wavfile.write("recovered.wav", sample_rate, recovered)
print("Saved recovered.wav!")
```

## What is stage 4?

After Stage 3 the audio was largely clean, but something still felt slightly off. Running the FFT revealed a spike sitting at exactly 0 Hz  this is called a DC offset. It basically means the entire waveform was shifted slightly above or below the zero line instead of being perfectly centred. This kind of shift is a common leftover side effect from the demodulation step in Stage 2 and doesn't show up as a sound you can hear clearly, but it affects how the audio sits and can cause problems when playing it back on different devices.
The fix was straightforward. I subtracted the mean value of the entire signal from every sample , this effectively dragged the waveform back to being centred at zero, removing the DC offset completely. After that I normalised the signal, which means I scaled all the amplitude values to sit neatly between -1 and 1. This ensures the audio is at a consistent, standard volume level without any clipping or distortion. After both corrections the signal was finally clean, centred and ready to be saved as the recovered audio file.



