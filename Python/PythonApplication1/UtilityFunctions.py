import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as linalg
import pandas as pd
import sympy as sp
import UtilityFunctions as uf
import KalmanFilter as kalman

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

    plt.show()


def plot_filteronly(t,y,x,P):
    fig = plt.figure(figsize=(14, 7))
    
    ax1 = plt.subplot(231)
    ax2 = plt.subplot(232)
    ax2a = plt.subplot(233)

    
    ax = ax1
    s = np.sqrt(P[:,1,1])
    ax.fill_between(t, x[:,0]-s, x[:,0]+s, color='yellow')
    ax.plot(t, x[:,0]+s, lw=1, ls='-', color='lightgray')
    ax.plot(t, x[:,0]-s, lw=1, ls='-', color='lightgray')
    ax.plot(t, y, '.', color='lightblue', label='Messungen')
    ax.plot(t, x[:,0], color='black', label='Filter')
    ax.set_ylabel('s(t) [cm]')    
    ax.legend()
    ax.grid()
    ax.set_title('Schätzung der Distanz')

    ax = ax2
    s = np.sqrt(P[:,1,1])
    ax.fill_between(t, x[:,1]-s, x[:,1]+s, color='yellow')
    ax.plot(t, x[:,1]+s, lw=1, ls='-', color='lightgray')
    ax.plot(t, x[:,1]-s, lw=1, ls='-', color='lightgray')

    ax.plot(t, x[:,1], color='black', label='Filter')
    ax.set_ylabel('v(t) [cm/s]')    
    ax.legend()    
    ax.grid()
#     ax.set_ylim([0,4])
    ax.set_title('Schätzung der Geschwindigkeit')
    
    ax = ax2a
    s = np.sqrt(P[:,1,1])
    ax.fill_between(t, x[:,2]-s, x[:,2]+s, color='yellow')
    ax.plot(t, x[:,2]+s, lw=1, ls='-', color='lightgray')
    ax.plot(t, x[:,2]-s, lw=1, ls='-', color='lightgray')

    ax.plot(t, x[:,2], color='black', label='Filter')
    ax.set_ylabel('a(t) [cm/s**2]')    
    ax.legend()    
    ax.grid()
#     ax.set_ylim([0,6])
    ax.set_title('Schätzung der Beschleunigung')

    plt.show()

    

def plot_filterresult(t,y,s_groundtruth,v,a,x,P):
    v = np.ones(len(t))*v
    fig = plt.figure(figsize=(14, 7))
    
    ax1 = plt.subplot(231)
    ax2 = plt.subplot(232)
    ax2a = plt.subplot(233)
    ax3 = plt.subplot(212)    

    
    ax = ax1
    ax.plot(t, y, '.', color='lightblue', label='Messungen')
    ax.plot(t, x[:,0], color='black', label='Filter')
    ax.plot(t, s_groundtruth, color='green', label='Ground Truth')
    ax.set_ylabel('s(t) [cm]')    
    ax.set_xlabel('t [s]')    
    ax.legend()
    ax.grid()
    ax.set_title('Schätzung der Distanz')

    ax = ax2
    s = np.sqrt(P[:,1,1])
    ax.fill_between(t, x[:,1]-s, x[:,1]+s, color='yellow')
    ax.plot(t, x[:,1]+s, lw=1, ls='-', color='lightgray')
    ax.plot(t, x[:,1]-s, lw=1, ls='-', color='lightgray')

    ax.plot(t, x[:,1], color='black', label='Filter')
    ax.plot(t, v, color='green', label='Ground Truth')
    ax.set_ylabel('v(t) [cm/s]')   
    #ax.set_xlabel('t [s]')    
    ax.legend()    
    ax.grid()
#     ax.set_ylim([0,4])
    ax.set_title('Schätzung der Geschwindigkeit')
    
    ax = ax2a
    s = np.sqrt(P[:,1,1])
    ax.fill_between(t, x[:,2]-s, x[:,2]+s, color='yellow')
    ax.plot(t, x[:,2]+s, lw=1, ls='-', color='lightgray')
    ax.plot(t, x[:,2]-s, lw=1, ls='-', color='lightgray')

    ax.plot(t, x[:,2], color='black', label='Filter')
    ax.plot(t, a, color='green', label='Ground Truth')
    ax.set_ylabel('a(t) [cm/s**2]')   
    ax.set_xlabel('t [s]')    
    ax.legend()    
    ax.grid()
#     ax.set_ylim([0,6])
    ax.set_title('Schätzung der Beschleunigung')
    
    ax = ax3
    ax.plot(t, x[:,0]-s_groundtruth, color='black', label='Residual (s(t) - s_truth(t))')
    s = np.sqrt(P[:,0,0])
    ax.set_xlabel('t [s]')    
    ax.fill_between(t, -s, s, color='yellow')
    #ax.set_ylim([-2,2])
#    ax.plot(t, s, ls='--', color='gray')
#    ax.plot(t, -s, ls='--', color='gray')
    ax.legend(); ax.grid()
    ax.set_title('Differenz der Distanz zwischen Filter und Realität')

    plt.show()



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
    data = pd.read_csv('%s.csv'%NameDerMessreihe)
    data.time /= 1000
    data.time -= data.time[0]
    data = data[data.time>=tstart]
    if tend is not None:
        data = data[data.time<=tend]
    return data

f = 6

def preFilter(y):
    newY = np.copy(y)

    for n in range(y.size):
        if((n > f) and (n < y.size - (f+1))):
            temp = y[n-f:n+(f+1)]
            temp = sorted(temp)
            #print(temp)
            newY[n] = temp[f]
    return newY

def preFilter2(y):
    for n in range(y.size):
        if(n > 0) and (np.absolute(y[n] - y[n-1]) > 10):
            y[n] = y[n-1]
    print(y)
    return y