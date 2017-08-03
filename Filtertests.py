import numpy as np
import matplotlib.pyplot as plt
import Tkinter
import tkFileDialog as fd
import scipy
import scipy.signal as signal
# import os.path

plt.close('all')


# pfad='C:\Users\Bob-Lap-\Google Drive\Transfer\Python\Ye.txt' # Amplitudengang aus Matlab für 2,8mb Datei
# pfad=r"C:\Files\Programming\Ye.txt"
# os.path.isfile(pfad)
#"C:\Users\Bob-Lap\Google Drive\Transfer\Python\Ye.txt"


asdDir=r'C:\Users\Bob-Lap\Google Drive\Transfer\Python\Testordner'

datei=fd.askopenfile(initialdir=asdDir,title='Messdatei auswählen')
stoss=np.loadtxt(datei.name)
datei.close()



def filt(verlauf):

    b, a = signal.ellip(4, 0.01, 120, 0.5)
    out=signal.filtfilt(b,a,verlauf)
    return out

filt(stoss)

plt.figure(1)

plt.subplot(211)
plt.semilogy(stoss)
plt.title('Roh-Verlauf')

plt.subplot(212)
plt.semilogy(out)
plt.title('Gefilterter-Verlauf')

plt.show()