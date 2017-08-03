import numpy as np
import matplotlib.pyplot as plt
import Tkinter
import tkFileDialog as fd
import scipy
import scipy.signal as signal
import os.path

plt.close('all')


## Filter-Funktion
def filt(sig):
    b, a = signal.ellip(4, 0.01, 120, 0.125)
    out = signal.filtfilt(b, a, sig)
    return out


## Dateien einlesen und Funktion anwenden
# asdDir=r"D:\Files\Backup\Google Drive\Transfer\Python"
asdDir = r"C:\Users\Bob-Lap\Google Drive\Transfer\Python"
dateilist = fd.askopenfiles(initialdir=asdDir, title='Messdatei auswählen')

verlauf = np.zeros(np.size(dateilist))
filverlauf = np.zeros(np.size(dateilist))

i = 0
for datei in dateilist:  # Durchläuft alle Dateien

    # verlauf[i]=np.loadtxt(datei.name)   # Lädt Werte
    verlauf = np.loadtxt(datei.name)  # Lädt Werte

    datei.close()
    # filverlauf[i]=filt(verlauf[i]) # Filter-Funktion
    filverlauf = filt(verlauf)
    i += 1

    ## Darstellung
    # if np.size(dateilist)==1
    # j=0
    # for fil in filverlauf:

    plt.figure()
    plt.suptitle(os.path.basename(datei.name))

    plt.subplot(211)
    # plt.semilogy(verlauf[j])
    plt.semilogy(verlauf)
    plt.title('Roh-Verlauf')

    plt.subplot(212)
    # plt.semilogy(filverlauf[j])
    plt.semilogy(filverlauf)
    plt.title('Gefilterter-Verlauf')

    savepath = os.path.dirname(datei.name)
    savename = '\\filter' + os.path.basename(datei.name)[5:-4] + '.asd'

    with open(savepath + savename, "w") as outo:
        np.savetxt(savepath + savename, filverlauf)
        # j+=0

plt.show()