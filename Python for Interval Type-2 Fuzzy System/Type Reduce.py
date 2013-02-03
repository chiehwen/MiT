# -*- coding:utf8  -*-  
#TonTon Hsien-De Huang (痛痛, 黃獻德) http://TWMAN.OrG
#Visiting Student, CSEE, Uni. of Essex | Ph. D Student, OASE Lab. CSIE, NCKU
#TaiWan Malware Analysis Net+ (臺灣惡意程式分析網+) | T W M A N + (抬丸郎+) | http://TWMAN.ORG
import sys
import math
import numpy as np
import scipy
#===============SumMul===================================
def SumMul(F, Y):
    t1, t2 = 0.0, 0.0
    for i in range (25):
      t1 += (F[i] * Y[i])
      t2 += F[i]
    if t2 == 0:
      return -1
    return t1/t2
#==============Start============================
fR = np.zeros([25],dtype=float)
yrk, yrk1, yrk2 = 0.0, 0.0, 100.0

fL = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2428, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
fU = np.array([0, 0.0947, 0, 0.2562, 0, 0.0956, 0.1601, 0, 0, 0, 0.4331, 0.0701, 0, 0.1617, 0.1897, 0, 0, 0, 0.0708, 0, 0, 0, 0, 0, 0], dtype=float)
yLk = np.array([1.8512, 4.0076, 5.0045, 2.8590, 4.8439, 5.3805, 3.8443, 5.3449, 6.5792, 1.5420, 5.8572, 2.0667, 5.9247, 3.7161, 6.6022, 4.2213, 4.4085, 6.3829, 7.4373, 7.6237, 4.8291, 5.1887, 6.6488, 7.6145, 8.0250], dtype=float)
yRk = np.array([2.3479, 4.6347, 5.6046, 3.4628, 5.4706, 5.9429, 4.4902, 5.8986, 7.0699, 2.0043, 6.4060, 2.5683, 6.4648, 4.3554, 7.0998, 4.8085, 5.3922, 6.8890, 7.8841, 8.0556, 5.4329, 5.7557, 7.1413, 8.0523, 8.4443], dtype=float)
yLk.sort()
yRk.sort()
#==============Compute Yrk============================
for i in range (25):
    fR[i] = (fL[i]+fU[i])/2 
yrk1 = yrk = SumMul(fR, yRk)
cn, R = 0, 0
while (abs(yrk2-yrk1) > 0.1):
    cn = cn + 1
    if cn > 1:
        yrk1 = yrk2
    for i in range (24):
        if yRk[i] <= yrk1 and yrk1 <= yRk[i+1]:
            R = i
            break
    for i in range(R):
        fR[i] = fL[i]
    for i in range (R, 25):
        fR[i] = fU[i]
    yrk2 = yrk = SumMul(fR, yRk)
    if cn == 25:
        break
#==============Compute Ylk============================
ylk, ylk1, ylk2 = 0.0, 0.0, 100.0
for i in range (25):
    fR[i] = (fL[i]+fU[i])/2
ylk1 = ylk = SumMul(fR, yLk)
cn, R = 0.0, 0.0
while (abs(ylk2-ylk1) > 0.1):
    cn = cn + 1
    if cn > 1:
        ylk1 = ylk2
    for i in range (24):
        if yLk[i] <= ylk1 and ylk1 <= yLk[i+1]:
            R = i
            break
    for i in range (R):
        fR[i] = fU[i]
    for i in range(R, 25):
        fR[i] = fL[i]
    ylk2 = ylk = SumMul(fR, yLk)
    if cn == 25:
        break
print 'The result are ylk : ' + str(ylk) + ' yrk : ' + str(yrk) + 'Average : ' + str((ylk+yrk)/2)
#raw_input("Press Enter to quit")
