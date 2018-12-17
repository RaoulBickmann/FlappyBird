#In diesen Arrays wird das Filterergebnis gespeichert
x_post = []
P_post = []
for n in range(N):
    if n==0:
        x_post_last = x0
        P_post_last = P0
    else:
        x_post_last = x_post[n-1]
        P_post_last = P_post[n-1]
    
    #Hier bitte die Kalman-Gleichungen implementieren
    
    x_prior = Ad * x_post_last
    P_prior = Ad * P_post_last * Ad.T + Gd * Q * Gd.T
    S = C * P_prior * C.T + R
    K = P_prior * C.T * np.linalg.inv(S)
    x_post_n = x_prior + K * (y[n] - C * x_prior - D)
    P_post_n = (np.eye(3) - K * C) * P_prior
    
    
    x_post.append(x_post_n)
    P_post.append(P_post_n)
x_post = np.array(x_post).squeeze()
P_post = np.array(P_post).squeeze()