class LineElement:
    '''Common superclass for line elements -- beams and truss members.
    Not functional as a standalone class -- some methods are missing.
    These must be filled in by subclasses.  Subclasses must define
    getLocalMassMatrix(), getLocalStiffnessMatrix(), and
    getLocalDofList().'''

    def __init__(self, nodeI, nodeJ):
        self._nodeI = nodeI
        self._nodeJ = nodeJ

    def getNodeI(self):
        return self._nodeI

    def getNodeJ(self):
        return self._nodeJ

    def getLength(self):
        from math import sqrt
        return sqrt((  self._nodeJ.getX() - self._nodeI.getX())**2
                    + (self._nodeJ.getY() - self._nodeI.getY())**2)

    def getAngle(self):
        from math import atan2
        return atan2(self._nodeJ.getY() - self._nodeI.getY(),
                     self._nodeJ.getX() - self._nodeI.getX())

    def getCoordinateTransform(self):
        '''Get coordinate transform matrix from element-local to
        global coordinates.'''

        from math import sin, cos
        import numpy as np

        dofList = self.getLocalDofList()
        nDofs = len(dofList)
        ix1 = dofList.index('UXI')
        iy1 = dofList.index('UYI')
        ix2 = dofList.index('UXJ')
        iy2 = dofList.index('UYJ')

        theta = self.getAngle()
        c = cos(theta)
        s = sin(theta)

        T = np.eye(nDofs)
        for ix, iy in [(ix1, iy1), (ix2, iy2)]:
            T[ix, ix] =  c
            T[ix, iy] = -s
            T[iy, ix] =  s
            T[iy, iy] =  c

        return T

    def getGlobalMatrix(self, localMat):
        import numpy as np

        # Get coordinate transform matrix
        T = self.getCoordinateTransform()

        # Transform element matrix to global
        globalMat = np.dot(T, np.dot(localMat, T.T))

        return globalMat

    def getDofList(self):
        # Transform DOF IDs to global
        localDofList = self.getLocalDofList()
        globalDofList = []
        for dof in localDofList:
            if dof[0] == 'U':
                if dof[2] == 'I':
                    globalDofList.append('U'+dof[1]+str(self._nodeI.getNum()))
                else:
                    globalDofList.append('U'+dof[1]+str(self._nodeJ.getNum()))
            else:
                if dof == 'RI':
                    globalDofList.append('R'+str(self._nodeI.getNum()))
                elif dof == 'RJ':
                    globalDofList.append('R'+str(self._nodeJ.getNum()))
                else:
                    globalDofList.append(dof)    # Pass through without change

        return globalDofList

    def getMassMatrix(self):
        M = self.getLocalMassMatrix()
        return self.getGlobalMatrix(M)

    def getStiffnessMatrix(self):
        K = self.getLocalStiffnessMatrix()
        return self.getGlobalMatrix(K)


class RodElement(LineElement):
    def __init__(self, EA, rhoA, nodeI, nodeJ):
        self._EA = EA
        self._rhoA = rhoA
        LineElement.__init__(self, nodeI, nodeJ)

    def getLocalDofList(self):
        return ['UXI', 'UYI', 'UXJ', 'UYJ']

    def getLocalStiffnessMatrix(self):
        import numpy as np
        K = np.zeros((4,4))
        L = self.getLength()
        k = self._EA/L

        K[0,0] =  k
        K[0,2] = -k
        K[2,0] = -k
        K[2,2] =  k

        return K

    def getLocalMassMatrix(self):
        import numpy as np
        M = np.zeros((4,4))
        L = self.getLength()
        m = self._rhoA*L/6.

        M[0,0] = 2*m
        M[0,2] =   m
        M[2,0] =   m
        M[2,2] = 2*m

        M[1,1] = 2*m
        M[1,3] =   m
        M[3,1] =   m
        M[3,3] = 2*m

        return M


class BeamColumnElement(LineElement):
    def __init__(self, EA, EI, rhoA, nodeI, nodeJ):
        self._EA = EA
        self._EI = EI
        self._rhoA = rhoA
        LineElement.__init__(self, nodeI, nodeJ)

    def getLocalDofList(self):
        return ['UYI', 'RI', 'UYJ', 'RJ', 'UXI', 'UXJ']

    def getLocalStiffnessMatrix(self):
        import numpy as np
        K = np.zeros((6,6))
        L = self.getLength()
        ka = self._EA/L

        # Bending stiffness
        # 1st row
        K[0,0] = 6.
        K[0,1] = 3.*L
        K[0,2] = -6.
        K[0,3] = 3.*L
        # 1st column by symmetry
        K[1,0] = K[0,1]
        K[2,0] = K[0,2]
        K[3,0] = K[0,3]

        # 2nd row
        K[1,1] = 2.*L**2
        K[1,2] = -3.*L
        K[1,3] = L**2
        # 2nd column by symmetry
        K[2,1] = K[1,2]
        K[3,1] = K[1,3]

        # 3rd row
        K[2,2] = 6.
        K[2,3] = -3.*L
        # 3rd column by symmetry
        K[3,2] = K[2,3]

        # Last entry
        K[3,3] = 2.*L**2

        # Scale
        K = (2.*self._EI/L**3)*K

        # Axial stiffness
        K[4,4] =  ka
        K[4,5] = -ka
        K[5,4] = -ka
        K[5,5] =  ka

        return K

    def getLocalMassMatrix(self):
        import numpy as np
        M = np.zeros((6,6))
        L = self.getLength()
        ma = self._rhoA*L/6.
        mb = self._rhoA*L/420.

        # Bending mass matrix
        # 1st row
        M[0,0] = 156.
        M[0,1] = 22.*L
        M[0,2] = 54.
        M[0,3] = -13.*L
        # Fill 1st column by symmetry
        M[1,0] = M[0,1]
        M[2,0] = M[0,2]
        M[3,0] = M[0,3]

        # 2nd row
        M[1,1] = 4.*L**2
        M[1,2] = 13.*L
        M[1,3] = -3.*L**2
        # Fill 2nd column by symmetry
        M[2,1] = M[1,2]
        M[3,1] = M[1,3]

        # 3rd row
        M[2,2] = 156.
        M[2,3] = -22.*L
        # Fill 3rd column by symmetry
        M[3,2] = M[2,3]

        # Last entry
        M[3,3] = 4.*L**2

        # Scale the whole thing
        M = mb*M

        # Axial motion mass matrix
        M[4,4] = 2.*ma
        M[4,5] =    ma
        M[5,4] =    ma
        M[5,5] = 2.*ma

        return M
