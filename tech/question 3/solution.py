
import numpy as np ## calculation of FFT
import matplotlib.pyplot as plt ## plotting of graphs 
from scipy.io import wavfile ## scipy library to read and write wav files
import os ## create direcrtory for plots
os.makedirs("plots", exist_ok=True)
##load the file
sample_rate, data = wavfile.read("corrupted.wav")## reads the corrupted file
data = data.astype(float) 
## info got from file 
print("Sample rate:", sample_rate) ## The number of audio samples captured per second
print("Data shape:", data.shape)## Whether the audio is mono or stereo
print("Data length:", len(data))##The total number of samples in the entire audio file
##stage 1
## time axis
N= len(data)
t = np.linspace(0,N/sample_rate,N)
## graph 1 - Time domain
plt.plot(t,data)## plot the aomplitude of the audio signal against time 
plt.xlabel("Time (s)") ## label for x axis 
plt.ylabel("Amplitude")## label for y axis 
plt.title("stage 1 - time domain")## title for graph
plt.savefig("plots/stage1_time_domain.png")
plt.show() ## display the graph 
##compute fft
freqs = np.fft.rfftfreq(N, d =1/sample_rate)## calculates corresponding frequency from time domain
magnitude = np.abs(np.fft.rfft(data))
#graph 2 fft
plt.plot(freqs, magnitude)
plt.title("Stage 1 - FFT- in frequency domain")
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
