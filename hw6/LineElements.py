import numpy as np

class LineElement:
    def __init__(self,nodeI,nodeJ):
        self._nodeI=nodeI
        self._nodeJ=nodeJ
    def getLength(self):
        import math
        x=(self._nodeI.getX()-self._nodeJ.getX())**2
        y=(self._nodeI.getY()-self._nodeJ.getY())**2
        l=math.sqrt(x+y)
        return l
    def getNodeI(self):
        return self._nodeI
    def getNodeJ(self):
        return self._nodeJ
class BeamElement(LineElement):
    def __init__(self,EI,rhoA,nodeI,nodeJ):
        self._EI=EI
        self._rhoA=rhoA
        LineElement.__init__(self,nodeI,nodeJ)
    def getDofList(self):
        i=self._nodeI.getNum()
        j=self._nodeJ.getNum()
        dofs = ['W%d'%i, 'R%d'%i, 'W%d'%j, 'R%d'%j]
        return dofs
    def getMassMatrix(self):
        L=self.getLength()
	M=np.zeros((4,4))
        M[0,0] = 156.
    	M[0,1] = 22.*L
    	M[0,2] = 54.
    	M[0,3] = -13.*L
    	M[1,0] = M[0,1]
    	M[2,0] = M[0,2]
    	M[3,0] = M[0,3]
    	M[1,1] = 4.*L**2
    	M[1,2] = 13.*L
    	M[1,3] = -3.*L**2	
    	M[2,1] = M[1,2]
    	M[3,1] = M[1,3]
    	M[2,2] = 156.
    	M[2,3] = -22.*L
    	M[3,2] = M[2,3]
    	M[3,3] = 4.*L**2
	Me=self._rhoA*L*M/420.
        return Me
    def getStiffnessMatrix(self):
        L=self.getLength()
        K = np.zeros((4,4))
	K[0,0] = 6.
    	K[0,1] = 3.*L
    	K[0,2] = -6.
    	K[0,3] = 3.*L  
    	K[1,0] = K[0,1]
    	K[2,0] = K[0,2]
    	K[3,0] = K[0,3]
    	K[1,1] = 2.*L**2
    	K[1,2] = -3.*L
    	K[1,3] = L**2
    	K[2,1] = K[1,2]
    	K[3,1] = K[1,3]
    	K[2,2] = 6.
    	K[2,3] = -3.*L
    	K[3,2] = K[2,3]
    	K[3,3] = 2.*L**2
	Ke=(2.*self._EI/L**3)*K
        return Ke
