import numpy as np

def elementMassMatrix(rhoA, L):
    M=np.array([[156,22*L,54,-13*L],[ 22*L,4*L*L,13*L,-3*L*L],[54,13*L,156,-22*L],[-13*L,-3*L*L,-22*L,4*L*L]])
    Me=rhoA*L*M/420
    return Me

def elementStiffnessMatrix(EI,L):
    K=np.array([[6,3*L,-6,3*L],[3*L,2*L*L,-3*L,1*L*L],[-6,-3*L,6,-3*L],[3*L,1*L*L,-3*L,2*L*L]]) 
    Ke=K*2*EI/(L*L*L)
    return Ke