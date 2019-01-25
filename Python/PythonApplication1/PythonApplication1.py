import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as linalg
import pandas as pd
import sympy as sp
import UtilityFunctions as uf
import KalmanFilter as kalman
import Simulation as sim
import ImageAnalysis as ima
data = uf.ReadData('data_movie2', False)

y = np.array(data.cm)
t = np.array(data.time)
y = np.delete(y, np.s_[1114:1148])
t = np.delete(t, np.s_[1114:1148])
N = len(y)
Ts = 0.02

dataTruth = uf.ReadData('s_truth_test', False)
s_groundtruth = np.array(dataTruth.cm)
s_groundtruth = s_groundtruth + 0.6

#s_groundtruth = np.ones(N);
#s_groundtruth *= 20;

v = np.zeros(N);
a = np.zeros(N);

#y = uf.preFilter(y)
y = uf.preFilter2(y)
x, P = kalman.filter(y, N, Ts)


uf.plot_filterresult(t, y, s_groundtruth, v, a, x, P)
#uf.plot_filteronly(t, y, x, P)

#sim.runSimulation()


#ima.analyseImage();


#data = pd.read_csv('camera_tracking.csv')

#millis = np.arange(20, 30000, 20)
#counter = 0


#outdata = pd.DataFrame(columns=['time', 'cm'])

#for n in range(len(millis)):
#    if((counter) * 33.333 < millis[n]):
#        counter = counter + 1

#    if(counter == 782):
#        break

#    #print(str(millis[n]) + " " + str(np.round(data.pixel[counter]/53 + 18, 4)))
#    #temp = [millis[n], np.round(data.pixel[counter]/53 + 18, 4)]
#    outdata = outdata.append({'time': str(millis[n]), 'cm': np.round(data.pixel[counter]/53 + 18, 4)}, ignore_index = True)

#outdata.to_csv('camera_ms_cm.csv', index=False, sep=';')

#ima.drawData()
 