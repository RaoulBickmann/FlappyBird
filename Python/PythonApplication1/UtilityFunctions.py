import pandas as pd
import numpy as np

def generateData_CAM(a=1, Ts=0.1, N=10, R=0):
    """
    Diese Funktionen erzeugt Entfernungsmessdaten für das ConstantAccelerationModel
    a: Beschleunigung
    Ts: Abtastperiode
    N: Anzahl der Abtastungen
    R: Varianz des Messrauschens (Gaußverteilt, mittelwertfrei)
    Rückgabe:
      (t,s,s_groundtruth)
      t: Vektor mit den Zeiten 0, Ts, ... , (N-1)*Ts
      v: Vektor mit Geschwindigkeitsmessungen (verrauscht)
      v_groundtruth: Vektor mit wahren Geschwindigkeiten
      s: Vektor mit den Distanzmessungen (verrauscht)
      s_groundtruth: Vektor mit den wahren Distanzen
    """
    t = np.arange(N)*Ts
    temp = np.concatenate( ([0], np.ones(N-1)) )
    a = temp*a
    v = (a*Ts).cumsum()
    s_groundtruth = (v*Ts).cumsum() 
    s = s_groundtruth + np.random.randn(N)*np.sqrt(R)
    return t,v,s,s_groundtruth

def plot_generatedData(t,y,s_groundtruth, v, a, figsize=(10, 4), dpi=90):
    v = np.ones(len(t))*v
    fig, axs = plt.subplots(1, 1, squeeze=False, figsize=figsize, dpi=dpi)
    axs = axs.flatten()
    ax = axs[0]
    ax.plot(t,y, '.', label='Messungen')
    ax.plot(t,s_groundtruth, label='s(t)')
    ax.set_xlabel('t'); ax.set_ylabel('Ort [m]')
    ax.legend(); ax.grid()
#     ax = ax.twinx()
    ax.plot(t, v, color='green', label='v(t)')
    ax.legend(loc='lower right')
    ax.set_ylabel('Geschwindigkeit [m/s]')
    
    ax = ax.twinx()
    ax.spines["right"].set_position(("axes", 1.1))
    ax.plot(t, a, color='blue', label='a(t)')
    ax.legend(loc='upper right')
    ax.set_ylabel('Beschleunigung [m/s**2]')

def ReadData(NameDerMessreihe, tstart=0, tend=None, info=False):
    '''
    Diese Funktion liest die Daten aus einer Arduino-Ausgabe ein.
    Sie müssen also CSV-Datei mit dem Namen <NameDerMessreihe>_daten.csv vorliegen. Außerdem muss
    eine kurze Textdatei mit dem Namen <NameDerMessreihe>_beschreibung.txt existieren.
    
    Alle Zeiten werden relativ zum Anfang der Messreihe interpretiert. Die erste Messung 
    ist also immer zur Zeit t=0s.
    
    tstart: Es wird die Messreihe ab dieser Startzeit gelesen
    tend:   Es wird die Messreihe bis zu dieser Zeit gelesen
    info:   Wenn True => Gibt eine Textinfo bzgl. des Inhalts aus (Inklusive Beschreibungsdatei)
    
    Rückgabe: Datensatz
    '''
    data = pd.read_csv('%s_daten.csv'%NameDerMessreihe)
    data.time /= 1000
    data.time -= data.time[0]
    data = data[data.time>=tstart]
    if tend is not None:
        data = data[data.time<=tend]
    return data