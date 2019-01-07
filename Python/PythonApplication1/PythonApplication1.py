import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as linalg
import pandas as pd
import sympy as sp
import UtilityFunctions as uf
import KalmanFilter as kalman
import Simulation as sim

data = uf.ReadData('14sec_backandforth', False)

y = np.array(data.cm)
N = len(data.cm)
Ts = 0.02
t = data.time

#s_groundtruth = np.ones(N);
#s_groundtruth *= 20;

#v = np.zeros(N);
#a = np.zeros(N);

#y = uf.preFilter(y)
#y = uf.preFilter2(y)
print(np.std(y))
x, P = kalman.filter(y, N, Ts)

#uf.plot_filterresult(t, y, s_groundtruth, v, a, x, P)
#uf.plot_filteronly(t, y, x, P)

sim.runSimulation()


