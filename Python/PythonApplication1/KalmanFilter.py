import numpy as np
import sympy as sp

sym_Ts, tau = sp.var('T_s, tau') #sym_... steht für symbolisch


A = sp.Matrix([
    [0, 1, 0],
    [0, 0, 1],
    [0, 0, 0]
]);

sym_Ad = sp.eye(3)+(A * sym_Ts)+(A*sym_Ts)**2/2

Bd = 0;

D = 0;

sym_C = sp.Matrix([
    [1,0,0]
]);

sym_Gd = sp.Matrix([
    [sym_Ts ** 3/6],
    [sym_Ts ** 2/2],
    [sym_Ts]
]);

def GiveNumericalMatrices(Ts):
    Variables = {sym_Ts:Ts}
    convert = lambda X: np.matrix(X.subs(Variables)).astype('float')
    Ad = convert(sym_Ad)
    C = convert(sym_C)    
    Gd = convert(sym_Gd)    
    return Ad, C, Gd


x0 = np.matrix([0,0,0]).T
P0 = np.diag( [10**2, 3**2, 1**2] )


def filter(y, N, Ts):

    Ad, C, Gd = GiveNumericalMatrices(Ts)
    
    #t = np.arange(N)*Ts     #Zeitvektor
    Q = 100000               #Prozessrauschen in cm/s^3 ??
    R_good = 0.68                #Sensorrauschen in cm^2 ??
    R_bad = 100000000

    x_post = []
    P_post = []
    for n in range(N):
        if n==0:
            x_post_last = x0
            P_post_last = P0
        else:
            x_post_last = x_post[n-1]
            P_post_last = P_post[n-1]

        print(P_post)
        x_prior = Ad * x_post_last
        P_prior = Ad * P_post_last * Ad.T + Gd * Q * Gd.T

        S = C * P_prior * C.T + R_good

        #if abweichung größer als 5 mal standardabweichung dann unsicherheit sehr hoch setzen
        if(abs(y[n] - C * x_prior) > 5 * np.sqrt(S)):
            R  = R_bad
        else:
            R = R_good

        S = C * P_prior * C.T + R

        K = P_prior * C.T * np.linalg.inv(S)


        x_post_n = x_prior + K * (y[n] - C * x_prior)
        P_post_n = (np.eye(3) - K * C) * P_prior

        x_post.append(x_post_n)
        P_post.append(P_post_n)
    x_post = np.array(x_post).squeeze()
    P_post = np.array(P_post).squeeze()

    return x_post, P_post
