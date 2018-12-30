import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as linalg
import pandas as pd
import sympy as sp
import UtilityFunctions as uf
import KalmanFilter as kalman


def runSimulation():
    # Daten Erzeugung
    np.random.seed(1)
    Ts = 0.02               #Abtastrate
    N = 300                 #Anzahl der Messungen
    t = np.arange(N)*Ts     #Zeitvektor
    Q = 10000                   #Prozessrauschen für die Simulation ::: Varianz des Rucks
    R = 6                   #cm^2
    r = np.random.randn(N)*np.sqrt(Q)
    # a0 = 1                  #Mittlere Geschwindigkeit
    # a = a0 + r.cumsum()*Ts  #Modifikation durch den Ruck?
    a = np.arange(N)
    a[0:50]  = 100
    a[50:60]  = 50
    a[60:70]  = -50
    a[70:120]  = -200
    a[120:140]  = -50
    a[140:150]  = 50
    a[150:210]  = 100
    a[210:220]  = 50
    a[220:230]  = -50
    a[230:280]  = -100
    a[280:290]  = -50
    a[290:300]  = 50
    a = a + r.cumsum()*Ts

    t,v,y,s_true = uf.generateData_CAM(a=a, Ts=Ts, N=N, R=R)


    x, P = kalman.filter(y, N, Ts)

    uf.plot_generatedData(t, y, s_true, v, a)
    uf.plot_filterresult(t, y, s_true, v, a, x, P)

