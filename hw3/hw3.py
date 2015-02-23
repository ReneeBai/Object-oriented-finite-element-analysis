#!/usr/bin/env python
import os,sys
import numpy as np
from numpy import loadtxt
import numpy.linalg as la
import matplotlib.pyplot as plt

report = open('report.txt','w')
for n in range(1,6):
    data = loadtxt('test%d.txt'%n)
    #for arg in sys.argv[1:]:
    #     data=loadtxt[arg]
    strain = data[:100,0]
    stress = data[:100,1]
    
    N = 1
    strain=np.reshape(strain,(100,1))
    new = la.pinv(strain)
    E = np.dot(new,stress)
    r = stress - np.dot(strain,E)
    R = np.dot(r,r)
    
    N = 2
    while True:
        strain = np.hstack((strain,strain**N))
        strain_inv = la.pinv(strain)
        E_est = np.dot(strain_inv, stress)
        r = stress - np.dot(strain, E_est)
        new_R = np.dot(r,r)
        if abs(new_R-R)/R<0.1:
            break   
        N += 1
        R = new_R
    plt.plot(data[:,0],data[:,1],'g-', label='Given Data')
    plt.plot(data[:100,0],E_est[0]*data[:100,0],'b-',label='E=%e'%E_est[0])
    plt.plot(data[:100,0],np.dot(strain,E_est),'r--',label='Nonlinear Fit')
    plt.text(0.002,3.2e8,'E=%e'%E_est[0])
    plt.xlabel('strain')
    plt.ylabel('stress(Pa)')
    plt.title('noisy data from a tensile test of a metal')
    plt.legend(loc=4)
    
    fname = os.path.splitext('test%d.txt'%n)[0]
    plt.savefig('%s.png'%fname, bbox_inches="tight")
    report.write('%s: E=%e\n'%(fname, E_est[0]))
report.close()
