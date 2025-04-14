"""
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
rate, data = wav.read('/home/chrysanthemum/Downloads/CaYPT Siren Recordings/24h40rps.wav')
fft_out = fft(data)
#matplotlib inline
plt.plot(data, np.abs(fft_out))
plt.show()

"""

import sys
from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

arg = sys.argv[1]
rate, aud_data = wav.read(
    "/home/chrysanthemum/Downloads/CaYPT Siren Recordings/" + arg + ".wav"
)
rate_noise, noise_data = wav.read(
    "/home/chrysanthemum/Downloads/CaYPT Siren Recordings/MotorSoundTest.wav"
)

ii = np.arange(0, 92183680)
ii_noise = np.arange(0, 92183680)


t = ii / rate
t_noise = ii_noise / rate_noise

len_data = len(aud_data)

len_noisedata = len(noise_data)

channel_1 = np.zeros(2 ** (int(np.ceil(np.log2(len_data)))))
channel_1[0:len_data] = aud_data

channel1_noise = np.zeros(2 ** (int(np.ceil(np.log2(len_noisedata)))))
channel1_noise[0:len_noisedata] = noise_data

fourier = np.fft.fft(channel_1)
fourier_noise = np.fft.fft(channel1_noise)


w = np.linspace(0, 44000, len(fourier))
w_noise = np.linspace(0, 44000, len(fourier_noise))


fourier_to_plot = fourier[0 : len(fourier) // 2]
w = w[0 : len(fourier) // 2]


fourier_noise_to_plot = fourier_noise[0 : len(fourier_noise) // 2]
w_noise = w_noise[0 : len(fourier_noise) // 2]


# Subtract Noise FFT from Siren FFT

"""
print(len(fourier_noise_to_plot))
for i in range(len(fourier_to_plot)):
    print(i)
    fourier_to_plot[i] = fourier_to_plot - fourier_noise_to_plot[i]

for i in range(len(w)):
    w[i] = w[i] - w_noise[i]
"""
plt.figure(1)

plt.plot(w, fourier_to_plot)
plt.xlabel("frequency")
plt.ylabel("amplitude")
plt.show()
