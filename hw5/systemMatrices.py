import scipy.sparse as sp
from sets import Set

def buildDofDict (dofList):
    dofSet = Set(dofList)
    dofDict= dict()
    N = 0
    for key in dofSet:
        dofDict[key]= N
        N+=1
    return dofDict
        
def buildSystemMatrix (matrixData, dofDict):
    m=len(dofDict)
    n=len(matrixData)
    q=len(matrixData[0][1])
    SystemMatrix = sp.lil_matrix((m,m))
    for i in range(n):
        for j in range(q):
            for k in range(q):
                r=dofDict[matrixData[i][1][j]]
                c=dofDict[matrixData[i][1][k]]
                SystemMatrix[r,c]+= matrixData[i][0][j,k]
    return SystemMatrix

def removeRowsCols (M,removeList):
    (x,x)=M.shape
    m=[i for i in range(x)]
    m=list(Set(m).difference(Set(removeList)))
    y=x-len(removeList)
    N=sp.lil_matrix((y,y))
    i=0
    j=0
    for x in m:
        j=0
        for y in m:
            N[i,j]=M[x,y]
            j+=1
        i+=1
    return N
