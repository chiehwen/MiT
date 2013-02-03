# -*- coding:utf8  -*-  
#TonTon Hsien-De Huang (痛痛, 黃獻德) http://TWMAN.OrG
#Visiting Student, CSEE, Uni. of Essex | Ph. D Student, OASE Lab. CSIE, NCKU
#TaiWan Malware Analysis Net+ (臺灣惡意程式分析網+) | T W M A N + (抬丸郎+) | http://TWMAN.ORG 
import sys
import math
import numpy as np
import scipy
#===============GaussianMF_UncertainDeviation===============
def GaussianMF_UncertainDeviation(X, mean, sigma1, sigma2, UpperBond, LowerBond):
    d1 = min(sigma1, sigma2)
    d2 = max(sigma1, sigma2)
    t1, t2 = 0, 0
    for i in range (100):
        t1 = Gaussian(X[i], d1, mean)
        t2 = Gaussian(X[i], d2, mean)
        UpperBond[i] = max(t1, t2)
        LowerBond[i] = min(t1, t2)
#=======================
def Sum(Y, Theta):
    t1, t2 =0.0, 0.0
    for i in range (100):        
        t1 += (Y[i] * Theta[i])
        t2 += Theta[i]
    if t2 == 0:
        return -1
    return t1/t2
#=======================Compute Centroid======================
def ComputeCentroid(Y, UpperBond, LowerBond, MaxMin):
    Y1, Y2 = 0.0, 100.0
    Theta, Delta, h = np.zeros([100],dtype=float), np.zeros([100],dtype=float), np.zeros([100],dtype=float)
    for i in range (100):
        Theta[i] = h[i] = (UpperBond[i] + LowerBond[i])/2
        Delta[i] = (UpperBond[i] - LowerBond[i])/2    
    Y1 = Sum(Y, h)
    cn = 0
    while (abs(Y2-Y1) > 0.000000001):
        cn = cn + 1
        if cn > 1:
            Y1 = Y2
        e = 0
        for i in range (100):
            if Y[i] <= Y1 and Y1 <= Y[i+1]:
                e =i
                break
        for i in range (e):
            if MaxMin > 0:
                Theta[i] = h[i] - Delta[i]
            else:
                Theta[i] = h[i] + Delta[i]
        for i in range(e,100):
            if MaxMin > 0:
                Theta[i] = h[i] + Delta[i]
            else:
                Theta[i] = h[i] - Delta[i]
        Y2 = Sum(Y, Theta)
    return Y2
#=============Gaussian Function Definition=============
def Gaussian(x, sigma, mean):
    if sigma == 0:
        return -1
    Gaussian = 2.71828183 ** (-0.5 * (pow(((x-mean)/sigma),2)))
    return Gaussian
#===============GaussianMF_UncertainMean===============
def GaussianMF_UncertainMean(X, sigma, mean1, mean2, UpperBond, LowerBond):
    m1 = min(mean1, mean2)
    m2 = max(mean1, mean2)
    t1, t2 =0, 0
    for i in range (100):
        if X[i] < m1:
            t1 = Gaussian(X[i], sigma, m1)
            t2 = Gaussian(X[i], sigma, m2)
        elif X[i] >= m1 and X[i] <= (m1+m2)/2:
            t1 = 1
            t2 = Gaussian(X[i], sigma, m2)
        elif X[i] > (m1+m2)/2 and X[i] <= m2:
            t1 = 1
            t2 = Gaussian(X[i], sigma, m1)
        elif X[i] > m2:
            t1 = Gaussian(X[i], sigma, m2)
            t2 = Gaussian(X[i], sigma, m1)
        UpperBond[i] = max(t1, t2)
        LowerBond[i] = min(t1, t2)
print '=====================Karnik-Mendel Algorithm Example===================='
print 'Uncertain Rule-Based Fuzzy Logic Systems: Introduction and New Directions.'
print '========================================================================'
Y, Yl, Yr = np.zeros([100],dtype=float), np.zeros([100],dtype=float), np.zeros([100],dtype=float)
UpperBond, LowerBond = np.zeros([100],dtype=float), np.zeros([100],dtype=float)
for i in range (1, 100):
    Y[i] = Y[i-1] + 0.1
#===================Uncertain Mean Example=====================
m1 = np.array([5, 4.875, 4.75, 4.625, 4.5, 4.25, 4, 3.75, 3.5], dtype=float)
m2 = np.array([5, 5.125, 5.25, 5.375, 5.5, 5.75, 6, 6.25, 6.5], dtype=float)
for i in range (9):
    GaussianMF_UncertainMean(Y, 1, m1[i], m2[i], UpperBond, LowerBond)      
    Yl = ComputeCentroid(Y, UpperBond, LowerBond, 0)
    Yr = ComputeCentroid(Y, UpperBond, LowerBond, 1)
    print 'm1=%1.4f' %(m1[i]), 'm2=%1.4f' %(m2[i]), 'm2-m1=%1.4f' %(m2[i]-m1[i]), 'Yr-Yl=%1.6f' %abs((Yr-Yl)), 'Yr=%1.6f' %(Yr), 'Yl=%1.6f' %(Yl)
#=============Uncertain standard Deviation Exampl==============
mean = 5.0
d1 = np.array([1, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25], dtype=float)
d2 = np.array([1, 1.125, 1.25, 1.375, 1.5, 1.625, 1.75], dtype=float)
for i in range (7):
    GaussianMF_UncertainDeviation(Y, mean, d1[i], d2[i], UpperBond, LowerBond)
    Yl = ComputeCentroid(Y, UpperBond, LowerBond, 0)
    Yr = ComputeCentroid(Y, UpperBond, LowerBond, 1)
    print 'd1=%1.6f' %(d1[i]), 'd2=%1.6f' %(d2[i]), 'd2-d1=%1.6f' %(d2[i]-d1[i]), 'Yr-Yl=%1.6f' %abs((Yr-Yl)), 'Yr=%1.6f' %(Yr), 'Yl=%1.6f' %(Yl)
#raw_input("Press Enter to quit")