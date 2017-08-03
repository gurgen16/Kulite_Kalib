import numpy as np
import os
import pickle
import shutil
import Tkinter as tk
import tkMessageBox as tm
import tkFileDialog as fd
import matplotlib.pyplot as plt
from Unbehauen_Funktion import unbehauen
# from Filtertests import filt

plt.close('all')
## ASD Datei Operationen

root=tk.Tk()
root.attributes("-topmost",True)
root.withdraw()

# lader=tm.askquestion('ASD Datei?','ASD Datei oder txt mit pmess laden?(Yes=ASD, NO=nur pmess')

# if lader=='yes':
startdir=os.path.abspath("C:\Files\Programming\Python\DynamischeKalibrierung Kulites")
fpath=fd.askopenfilename(initialdir=startdir,title="ASD Datei auswählen")


with open(fpath,"r") as asd:
    Messdat=np.loadtxt(fpath,skiprows=10,converters={0:lambda x:x.replace(",","."),1:lambda x:x.replace(",",".")})
    
# else:
#     startdir=os.path.abspath("C:\Files\Programming\Python\DynamischeKalibrierung Kulites")
#     fpath=fd.askopenfilename(initialdir=startdir,title="Txt Datei mit pmess auswählen")

## Normierung

tmess=Messdat[:,0]
pmess=Messdat[:,1]
B=pmess[1:]
B=np.append(B,[0],axis=0)
diff=B-pmess
norm=diff/pmess

## Stoß-Rand-Indizes ermitteln

i0=norm.argmax()
i0_backup=i0

i1=i0
i1=np.where(pmess>np.mean(pmess[i1:i1+1000]))
i1=i1[0][0]

## Kürzen der Messdatenmatrix auf relvanten Bereich

if i0>100:
    pmess=pmess[i0-100:i0+300] #Kürzen der Matrix auf 100 Werte vor- und 300 Werte nach dem Stoß
    tmess=tmess[i0-100:i0+300]
    diff=diff[i0-100:i0+300]
    norm=norm[i0-100:i0+300]
    i1=100+i1-i0;
    i0=100;
else:  # Bedingung für den Fall, dass vor i0 keine 100 Messwerte liegen
    pmess=pmess[:i0+300]
    tmess=tmess[:i0+300]

tmess=tmess-tmess[0] # Ersten Zeitwert zu 0 setzen
    
## Lineasisierung

p0=np.mean(pmess[:i0])
p1=np.mean(pmess[i1:])


## Umrechnung in Frequenzbereich

fGang=unbehauen(tmess,pmess,i0,i1) # Liefert Frequenzgang: [Amplitudengang, Phasengang, Frequenz]
#fGang_log=np.log10(fGang)
# pmess_fil=filt(pmess)

## Plots


plt.figure(1)

plt.subplot(211)
plt.plot(np.arange(np.size(pmess)),pmess)

plt.subplot(212)
# plt.loglog(fGang[:,2],fGang[:,0],basex=10,basey=10)
plt.semilogy(np.arange(np.size(fGang[:,0])),fGang[:,0])

plt.show()


## Speichern
tm.askyesno('Speicherabfrage','Soll der Druckverlauf gespeichert werden?',master=root)
savepath=r'C:\Users\Bob-Lap\Google Drive\Transfer\Python\Testordner\\'
savename='\\pmess_'+os.path.basename(fpath[:-4])+'.asd'

with open(savepath+savename,"w") as outo:
    np.savetxt(savepath+savename,pmess)
































