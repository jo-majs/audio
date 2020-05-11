# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import math
import read_audio as ra
import librosa

# ----------------------------------------------------------------------------
# WYBÓR NAGRANIA DO ANALIZY
# nowe nagranie 10 s
# lub gotowe nagranie pręta stalowego
# lub gotowe nagranie pręta aluminiowego
def choose_recording():
    choice = input("Wybierz opcje: [default:stal] nowe_nagranie / stal / aluminium: ")
    #default - gotowe nagranie aluminiowego pręta
    if choice!= 'stal' and choice != 'aluminium' and choice != 'nowe_nagranie':
        return 'stal'
    return choice
    
option = choose_recording()
material = 'blad'

#nowe nagranie
if option == 'nowe_nagranie':
    print("Nagrywam 10s, uderz w pret kilka razy")
    rec = ra.Recorder(channels = 2)
    with rec.open('new_recording.wav', 'wb') as recfile:
        recfile.record(duration = 10.0)
    thickness = float(input("Podaj srednice preta [m]: ")) # [m]
    length = float(input("Podaj dlugosc preta [m]: ")) # [m]
    material = input("Wybierz material: stal/aluminium/nowy: ")
    if material == 'nowy':
        young = float(input("Podaj modul Younga materialu [Pa]: ")) # [Pa]
        density = float(input("Podaj gestosc materialu [kg/m^3]: ")) # [kg/m^3]
    else:
        option = material
    file_path = 'new_recording.wav'

#parametry pręta aluminiowego
if option == 'aluminium':
    # parametry aluminium:
    young = 70.0 * 10**9 # [Pa]
    density = 2710.0 # [kg/m^3]nowe_
    title = 'nowy'
    #parametry pręta z nagrania:
    if material != option:
        thickness = 0.0075 # [m]
        length = 0.41 # [m]
        title = option
        file_path = 'aluminium.wav'

#parametry pręta stalowego     
if option == 'stal':
    #parametry stali:
    young = 180.0 * 10**9 # [Pa]
    density = 8050.0 # [kg/m^3]
    title = 'nowy'
    #parametry pręta z nagrania:
    if material != option:
        thickness = 0.0075 # [m]
        length = 0.27 # [m]
        title = option
        file_path = 'steel.wav'


# ----------------------------------------------------------------------------
# teoretyczne przewidywania częstotliwosci f1 - f8
f1 = 1.028 * thickness / length**2 * math.sqrt(young / density)
mods = [f1]
for i in range(2,9):
    mods.append(0.441 * (i + 0.5)**2 * f1)

        
# ----------------------------------------------------------------------------
# ANALIZA PLIKU .WAV
samples, sampling_rate = librosa.load(file_path, sr = None)
# duration_of_sound = len(samples)/sampling_rate
# print(duration_of_sound, " seconds")
# print(sampling_rate)
# print(len(samples))
# print(len(samples)/duration_of_sound)

n = len(samples) # liczba próbek
fft = np.fft.fft(samples)[0:int(n/2)]/n #fast fourier transform
fft[1:] = 2*fft[1:] # widmo dodatnie
Pxx = np.abs(fft) # biorę częsć rzeczywistą
f = sampling_rate * np.arange((n/2))/n; # częstotliwosci

# ----------------------------------------------------------------------------
# WYKRESY
fig = plt.figure(figsize = (12,8))

# amplituda od czasu
a = fig.add_subplot(211)
a.set_xlim(0, 10)
a.set_xlabel('czas [s]')
a.set_ylabel('amplituda')
x = np.arange(len(samples))/sampling_rate
plt.plot(x, samples, 'g', linewidth = 1)

# analiza fourierowska - amplituda od częstotliwosci
b = fig.add_subplot(212)
b.set_xlim(10**2, 0.25 * 10**5)
b.set_xscale('log')
b.set_xlabel('częstotliwość [Hz]')
b.set_ylabel('amplituda')
plt.plot(f, Pxx, 'r', label = 'zmierzona intensywność dźwięku')
plt.plot(mods, np.zeros(8), 'b^', label = 'teoretyczne częstotliwości f1 - f8')
for f in mods:
    plt.annotate("{:.1f}".format(f), xy = (f,0), xytext = (f, 0.0004), color = 'b', ha = 'center', size = 'small')    
legend = b.legend(loc='upper left', shadow = True)

plt.savefig(title, dpi = 150)



