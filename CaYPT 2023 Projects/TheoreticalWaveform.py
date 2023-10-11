import sys
import numpy as np
import matplotlib.pyplot as plt
import math


circle_waveform = []


quality = 100 # Amount of subslices per mmillesseccond

cycles = 3



frequency = int(input("Frequency: "))


pulse_width = int(input("PW: "))/100


cycle_time = math.floor((1/frequency) * 1000) # milleseconds
pulse_length = math.floor(cycle_time*pulse_width) #milleseconds
hold_length = cycle_time-pulse_length

amptitude = 1


area = 0



# First quarter
for i in range(pulse_length*quality):
    radians = i/(pulse_length*quality)
    area = area + ((math.sin(radians*math.pi*0.5)*0.04)/2.5264267293774414)*amptitude
    circle_waveform.append([area])


# Mirrors waveform
start_length = len(circle_waveform)
for i in range(start_length):
    insert_list = circle_waveform[start_length-i-1]
    circle_waveform.append(insert_list)
    
    



waveform_graph = []

pulse_length = math.floor(len(circle_waveform)*((1-pulse_width)/pulse_width))

for i in range(cycles):
    for a in circle_waveform:
        waveform_graph.append(a)
    for i in range(hold_length*quality):
        waveform_graph.append([0])

# Insert FFT transformation for theoretical waveform



"""
ii = np.arange(0, 92183680)

t = ii / (1000*quality)

#len_data = len(waveform_graph)

#channel_1 = np.zeros(2**(int(np.ceil(np.log2(len_data)))))

#channel_1[0:len_data] = waveform_graph

fourier = np.fft.fft(channel_1)

w = np.linspace(0, 1000*quality, len(fourier))

fourier_to_plot = fourier[0:len(fourier)//2]
w = w[0:len(fourier)//2]

fourier = np.fft.fft(waveform_graph)

w = np.linspace(0, 1000*quality, len(fourier))
w = w[0:len(fourier)//2]


plt.figure(1)

plt.plot(w, fourier)
plt.xlabel('frequency')
plt.ylabel('amplitude')
plt.show()
"""


plt.plot(waveform_graph)
plt.xlabel('time')
plt.ylabel('amplitude')
plt.show()