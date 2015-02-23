import numpy as np
import math
class LineElement:
    def __init__(self,nodeI,nodeJ):
        self._nodeI=nodeI
        self._nodeJ=nodeJ
    def getLength(self):
        from math import sqrt
        x=(self._nodeI.getX()-self._nodeJ.getX())**2
        y=(self._nodeI.getY()-self._nodeJ.getY())**2
        l=math.sqrt(x+y)
        return l
    def getNodeI(self):
        return self._nodeI
    def getNodeJ(self):
        return self._nodeJ
    def getAngle(self):
        y=self._nodeJ.getY()-self._nodeI.getY()
        x=self._nodeJ.getX()-self._nodeI.getX()
        cos=float(x/math.sqrt(x**2+y**2))
        theta=math.acos(cos)
        return theta
    def getCoordinateTransform(self):
        dof = self.getLocalDofList()
        theta=self.getAngle()
        cos = math.cos(theta)
        sin = math.sin(theta)
        n = len(dof)
        T=np.zeros((n,n))
        for i in range(n):
            if dof[i][0] == 'R':
                T[i,i] = 1
            else:
                T[i,i]=cos
            for j in range(n):
                if dof[i]=='UYI' and dof[j]=='UXI':
                    T[i,j]=sin
                    T[j,i]=-sin
                if dof[i]=='UYJ' and dof[j]=='UXJ':
                    T[i,j]=sin
                    T[j,i]=-sin
        return T
    def getGlobalMatrix(self,localMat):
        T = self.getCoordinateTransform()
        T_tran = T.transpose()
        a=np.dot(T,localMat)
        globalMat = np.dot(a,T_tran)
        return globalMat
    def getDofList(self):
        Dof = self.getLocalDofList()
        i=self.getNodeI().getNum()
        j=self.getNodeJ().getNum()
        for h in range(len(Dof)):
            for k in range(len(Dof[h])):
                if Dof[h][k] == 'I':
                    Dof[h]=Dof[h].replace('I','%d'%i)
                if Dof[h][k] == 'J':
                    Dof[h]=Dof[h].replace('J','%d'%j)
        return Dof
    def getMassMatrix(self):
        MM = self.getLocalMassMatrix()
        return self.getGlobalMatrix(MM)
    def getStiffnessMatrix(self):
        SM = self.getLocalStiffnessMatrix()
        return self.getGlobalMatrix(SM)
        
class RodElement(LineElement):
    def __init__(self,EA,rhoA,nodeI,nodeJ):
        self._EA = EA
        self._rhoA = rhoA
        LineElement.__init__(self,nodeI,nodeJ)
    def getLocalDofList(self):
        dofs=['UXI','UYI','UXJ','UYJ']
        return dofs
    def getLocalStiffnessMatrix(self):
        K=np.array([[1.,0.,-1.,0.],[0.,0.,0.,0.],[-1.,0.,1.,0.],[0.,0.,0.,0.]])
        L=self.getLength()
        Ke = self._EA*K/L
        return Ke
    def getLocalMassMatrix(self):
        L=self.getLength()
        M=np.array([[2.,0.,1.,0.],[0.,2.,0.,1.],[1.,0.,2.,0.],[0.,1.,0.,2.]])
        Me=self._rhoA*L*M/6.
        return Me

class BeamColumnElement(LineElement):
    def __init__(self,EA,EI,rhoA,nodeI,nodeJ):
        self._EA = EA
        self._EI = EI
        self._rhoA = rhoA
        LineElement.__init__(self,nodeI,nodeJ)
    def getLocalDofList(self):
        dofs = ['UYI','RI','UYJ','RJ','UXI','UXJ']
        return dofs
    def getLocalStiffnessMatrix(self):
        K_bc=np.zeros((6,6))
        L=self.getLength()
        K_t=np.array([[1,-1],[-1,1]])
        K_axial = (self._EA/L)*K_t
        K = np.zeros((4,4))
        K[0,0]=6.
        K[0,1]=3.*L
        K[0,2]=-6
        K[0,3]=3.*L
        K[1,0]=K[0,1]
        K[2,0]=K[0,2]
        K[3,0]=K[0,3]
        K[1,1]=2.*L**2
        K[1,2]=-3.*L
        K[1,3]=L**2
        K[2,1]=K[1,2]
        K[3,1]=K[1,3]
        K[2,2]=6.
        K[2,3]=-3.*L
        K[3,2]=K[2,3]
        K[3,3]=2.*L**2
        K=(2.*self._EI/L**3)*K
        K_bc[0:4,0:4]=K
        K_bc[4:,4:]=K_axial
        return K_bc
    def getLocalMassMatrix(self):
        M_bc=np.zeros((6,6))
        L=self.getLength()
        M_t=np.array([[2,1],[1,2]])
        M_axial=(self._rhoA*L/6.)*M_t
        M=np.zeros((4,4))
        M[0,0]=156.
        M[0,1]=22.*L
        M[0,2]=54.
        M[0,3]=-13.*L
        M[1,0]=M[0,1]
        M[2,0]=M[0,2]
        M[3,0]=M[0,3]
        M[1,1]=4.*L**2
        M[1,2]=13.*L
        M[1,3]=-3.*L**2
        M[2,1]=M[1,2]
        M[3,1]=M[1,3]
        M[2,2]=156.
        M[2,3]=-22.*L
        M[3,2]=M[2,3]
        M[3,3]=4.*L**2
        M=(self._rhoA*L/420.)*M
        M_bc[:4,:4]=M
        M_bc[4:,4:]=M_axial
        return M_bc