# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 16:16:29 2021

@author: correia (adaptado Chang, S.W.; Memari, S.S.;
Clement, T.P. PyTheis—A Python
Tool for Analyzing Pump Test Data.
Water 2021, 13, 2180. https://
doi.org/10.3390/w13162180)
"""

import numpy as np
import math as m
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

def wufunc(r,S,T,t):
    u = (r**2)*S/(4*T*t)
    Wu=-0.5772-np.log(u)+u
    ntrm = 30
    for i in range (2, ntrm+1):
        sign = (-1)**(i-1)
        factval = float(m.factorial(i))
        Wu =Wu + sign*(u**i)/(i*factval)
    #End loop i
    
    return (Wu)
def myfunc(tt, T, S):
    
    pi = 3.14
    #Q = 1199.22 #m3/d
    Q = np.nanmean(np.copy(indata.iloc[:,2])) #Vazão
    r = 30 #m
    nrow = len(tt)
    n = nrow
    drawdown=np.zeros((n),float)

    
    
    for i in range (0,n):
        Wu_val=wufunc(r,S,T,tt[i])
        drawdown[i] = Q*Wu_val/(4*pi*T)
        #End loop i

    
    #print(Wu)     
    return (drawdown)

theis = pd.read_excel("Dados_FW(u).xlsx",
                   sheet_name = "W(u)",
                   skiprows = 2) 
#Wu_val=np.copy(theis.iloc[:,1])

    
indata = pd.read_excel("15_1.xlsx",
                   sheet_name = "Rebaixamento",
                   skiprows = 18, nrows = 10)



tempo = np.copy(indata.iloc[:,0]) # Tempo
reb = np.copy(indata.iloc[:,3]) # Rebaixamento
#Q = np.nanmean(np.copy(indata.iloc[:,2])) #Vazão


init_vals = [1, 0.00001]
best_vals, covar = curve_fit(myfunc, tempo, reb, p0=init_vals, bounds=([0.01, 0.000001], [100000, 0.1]), method = 'trf')
stdevs = np.sqrt(np.diag(covar))
plt.xscale('log')
plt.yscale('log')
print ('T, S')
print (best_vals)
'''
print ('Covariance')
print (covar)
print ('standard deviation')
print (stdevs)
'''
T = best_vals [0]
S = best_vals [1]
smodel=myfunc(tempo,T,S)
plt.plot(tempo,smodel)

plt.plot(tempo, reb, 'bo')
plt.xlabel("tempo (dia)")
plt.ylabel("rebaixamento (m)")
plt.show()
