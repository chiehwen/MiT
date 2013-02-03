# -*- coding:utf8  -*-  
#TonTon Hsien-De Huang (痛痛, 黃獻德) http://TonTon.TWMAN.OrG
#Visiting Student, CSEE, Uni. of Essex | Ph. D Student, OASE Lab. CSIE, NCKU
#TaiWan Malware Analysis Net+ (臺灣惡意程式分析網+) | T W M A N + (抬丸郎+) | http://TWMAN.ORG
 
import sys
import math
import numpy as np
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
#=======================Compute Centroid Yr======================
def ComputeCentroidYr(Y, UpperBond, LowerBond):
    Y1, Y2, k2, s = 0.0, 100.0, 0, 0.0
    k1 = int(100/1.7)
    Y1 = ComputeY2(Y, k1, UpperBond, LowerBond)
    for i in range (100):
        if Y[i] <= Y1 and Y1 <= Y[i+1]:
            k2 = i
    if k2 == k1:
        Y2 = Y1
    else:
        Y2 = ComputeS2(Y, k1, k2, UpperBond, LowerBond)
    return Y2 
#===============================================================
def ComputeS2(Y, k1, k2, Up, Low):
    a, b, a1, b1, maxk, mink =0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    s = math.sin(k2 - k1)
    maxk = max(k1,k2)
    mink = min(k1,k2)
    for i in range (100):
        for i in range (0, k1+1):
            a = a + (Y[i] * Low[i])
            b = b + Low[i]
        for i in range (k1+1, 100):
            a = a + (Y[i] * Up[i])
            b = b + Up[i]
        for i in range (mink, maxk+1):
            a1 = Y[i] * (Up[i] - Low[i])
            b1 = (Up[i] - Low[i])
            a = a - (s * a1)
            b = b - (s * b1)
    if b == 0:
        return -1
    return a/b
#===============================================================
def ComputeS1(Y, k1, k2, Up, Low):
    a, b, a1, b1, maxk, mink =0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    s = math.sin(k2 - k1)
    maxk = max(k1,k2)
    mink = min(k1,k2)
    for i in range (100):
        for i in range (0, k1+1):
            a = a + (Y[i] * Up[i])
            b = b + Up[i]
        for i in range (k1+1, 100):
            a = a + (Y[i] * Low[i])
            b = b + Low[i]
        for i in range (mink, maxk+1):
            a1 = Y[i] * (Up[i] - Low[i])
            b1 = (Up[i] - Low[i])
            a = a + (s * a1)
            b = b + (s * b1)
    if b == 0:
        return -1
    return a/b
#===============================================================
def ComputeY2(Y, k, Up, Low):
    a, b, a1, b1 =0.0, 0.0, 0.0, 0.0
    for i in range (100):
        for i in range (0, k+1):
            a = a + (Y[i] * Low[i])
            b = b + Low[i]
        for i in range (k+1, 100):
            a = a + (Y[i] * Up[i])
            b = b + Up[i]
    if b == 0:
        return -1
    return a/b
#===============================================================
def ComputeY1(Y, k, Up, Low):
    a, b, a1, b1 =0.0, 0.0, 0.0, 0.0
    for i in range (100):
        for i in range (0, k+1):
            a = a + (Y[i] * Up[i])
            b = b + Up[i]
        for i in range (k+1, 100):
            a = a + (Y[i] * Low[i])
            b = b + Low[i]
    if b == 0:
        return -1
    return a/b
#=======================Compute Centroid Yl======================
def ComputeCentroidYl(Y, UpperBond, LowerBond):
    Y1, Y2, k2, s = 0.0, 100.0, 0, 0.0
    k1 = int(100/2.4)
    Y1 = ComputeY1(Y, k1, UpperBond, LowerBond)
    for i in range (100):
        if Y[i] <= Y1 and Y1 <= Y[i+1]:
            k2 = i
    if k2 == k1:
        Y2 = Y1
    else:
        Y2 = ComputeS1(Y, k1, k2, UpperBond, LowerBond)
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
print '=====================Enhanced Karnik–Mendel Algorithms Example=========='
print 'Uncertain Rule-Based Fuzzy Logic Systems: Introduction andNew Directions.'
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
    Yl = ComputeCentroidYl(Y, UpperBond, LowerBond)
    Yr = ComputeCentroidYr(Y, UpperBond, LowerBond)    
    print 'm1=%1.4f' %(m1[i]), 'm2=%1.4f' %(m2[i]), 'm2-m1=%1.4f' %(m2[i]-m1[i]), 'Yr-Yl=%1.6f' %abs((Yr-Yl)), 'Yr=%1.6f' %(Yr), 'Yl=%1.6f' %(Yl)
#=============Uncertain standard Deviation Exampl==============
mean = 5.0
d1 = np.array([1, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25], dtype=float)
d2 = np.array([1, 1.125, 1.25, 1.375, 1.5, 1.625, 1.75], dtype=float)
for i in range (7):
    GaussianMF_UncertainDeviation(Y, mean, d1[i], d2[i], UpperBond, LowerBond)
    Yl = ComputeCentroidYl(Y, UpperBond, LowerBond)
    Yr = ComputeCentroidYr(Y, UpperBond, LowerBond)    
    print 'd1=%1.6f' %(d1[i]), 'd2=%1.6f' %(d2[i]), 'd2-d1=%1.6f' %(d2[i]-d1[i]), 'Yr-Yl=%1.6f' %abs((Yr-Yl)), 'Yr=%1.6f' %(Yr), 'Yl=%1.6f' %(Yl)
#raw_input("Press Enter to quit")
