import systemMatrices
import simpleBeam
import numpy as np
import scipy.sparse.linalg as spla

E = 210e9
I = 2.7009842839238267e-05
rho = 7800.
A = 0.005969026041820614
L = 10.

numElements = 20

nodeLocs = np.linspace(0., L, numElements+1)

massMatrixData = []
stiffnessMatrixData = []
dofList = []

for i in xrange(numElements):
    # DOF IDs for each node
    dofs = ['W%d'%i, 'R%d'%i, 'W%d'%(i+1), 'R%d'%(i+1)]

    # Element mass and stiffness matrices
    Me = simpleBeam.elementMassMatrix(rho*A, nodeLocs[i+1] - nodeLocs[i])
    Ke = simpleBeam.elementStiffnessMatrix(E*I, nodeLocs[i+1] - nodeLocs[i])

    # Package for assembly
    massMatrixData.append((Me, dofs))
    stiffnessMatrixData.append((Ke, dofs))
    dofList = dofList + dofs

# Assemble system matrices
dofDict = systemMatrices.buildDofDict(dofList)
M = systemMatrices.buildSystemMatrix(massMatrixData, dofDict)
K = systemMatrices.buildSystemMatrix(stiffnessMatrixData, dofDict)

# Remove the DOFs constrained by the beam being fixed at the bottom
removeDofs = ['W0', 'R0']
removeList = [dofDict[d] for d in removeDofs]
M = systemMatrices.removeRowsCols(M, removeList)
K = systemMatrices.removeRowsCols(K, removeList)

# Make sure K and M are in CSR format for efficient matrix-vector
# multiplication
M = M.tocsr()
K = K.tocsr()

# Solve for the first three vibration modes and frequencies
w, v = spla.eigsh(K, 3, M, sigma=0.)

print 'Natural frequencies:'
print np.sqrt(w)
