import numpy as np


def unbehauen(h_t,h,i0,i1):
    
    ## Abtastrate bestimmen
    N=np.size(h)
    delta_t=h_t[2]-h_t[1]
    abtastrate=1/delta_t*10**(-6)
    
    ## Unbehauen Funktion zur Ermittlung des Frequenzgangs
    # Matrix pv
    p_v = np.zeros([N-i0,1],dtype=float)
    for v in range(N-i0-1):
        if v==0: # Erster Wert: einseitige Differenz
            p_v[0]=h[i0+1]-h[i0]
        else: 
            if v==N-i0-1: # Letzter Wert: einseitige Differenz
                p_v[N-i0-1]= h[N-2] - h[N-1]
            else: # Alle andern Werte: beidseitige Differenzen
                p_v[v]= h[i0+v-1] - 2*h[i0+v] + h[i0+v+1]
    
    # Frequenzgang
    hvor=np.mean(h[:i0])
    hnach=np.mean(h[i1:])
    K=hnach-hvor
    
    alpha=0.05 
    delta=140
    ergebnis=np.zeros([delta,3],dtype=float) #Amplidute, Phase, n
    for n in range(delta):
        f=10**(alpha*n) # Bestimmt die Schrittweite in der Omega im Bodediagramm aufgeloest wird, Basis 10 da Bodediagramm als log10 aufgetragen wird
        omega=2*np.pi*f
        sum=0
        
        for z in range(N-i0-1):
            sum=sum+p_v[z]/delta_t * np.exp(-1j * omega * z * delta_t)
            
        G=1/K * (h[i0] + 1/(1j*omega)*sum)
        ergebnis[n,:]=[ np.abs(G) , np.angle(G)*180/np.pi , f ]
    
    
    
    
    return ergebnis

