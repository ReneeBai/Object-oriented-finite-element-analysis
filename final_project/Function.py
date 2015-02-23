# New Class to contain functions and handle computation of integrals
import Node
import LineElements
import systemMatrices
import numpy as np
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
class FEModel:
    def __init__(self):
        #creat node window
        self._x = 0.
        self._y = 0.
        self._node = []
        #plot results window
        self._observers = [] 
        self._obs = []
        #creat element window
        self._E = 0.
        self._rho = 0.
        self._A = 0.
        self._I = 0.
        self._type = None
        self._eletype = ''
        self._numElements = 0
        self._elementList = []
        self._xstart = 0.
        self._ystart = 0.
        self._xend = 0.
        self._yend = 0.
        self._line = []
        #set constrain window
        self._dofList = []
        self._dofDict = {}
        self._removeDofs = []
        self._removeList = []
        #solve window
        self._M = []
        self._K = []
        self._w = []
        self._v = []
        #list results window
        self._numModes = 0.
        self._frequency = 0.
        self._shape = []

    # set and get X & Y
    def getx(self):
        return self._x
    def gety(self):
        return self._y
    def setX(self, x):
        self._x = x
    def setY(self,y):
        self._y = y  
    # create new node
    def setNode(self,x,y):
        newNode = Node.Node(x,y)
        self._node.append(newNode)
        self.updateObservers()
        print 'Creating node (%f, %f), Node Number is %d'%(x,y,newNode.getNum())
    # get node
    def getNode(self,nodeNum):
        for node in self._node:
            if node.getNum()==nodeNum:
                return node
    def getNodes(self):
        return self._node
    def getstartx(self):
        return self._xstart
    def getstarty(self):
        return self._ystart
    def getendx(self):
        return self._xend
    def getendy(self):
        return self._yend

    #set parameters
    def setE(self, E):
        self._E = E
    def setrho(self, rho):
        self._rho = rho
    def setA(self, A):
        self._A = A
    def setI(self, I):
        self._I = I
    def setnumElements(self, numElements):
        self._numElements = numElements
    def settype(self, eletype):
        if eletype == 'Rod':
            self._type = 'Rod'
        elif eletype == 'Beam':
            self._type = 'Beam'
        else:
            self._type = eletype
    #get
    def getStartNode(self):
        return self._StartNode
    def getEndNode(self):
        return self._EndNode
    def getnumElements(self):
        return self._numElements
    def gettype (self):
        return self._type
    def getNumModes(self):
        return self._numModes
    def getM(self):
        return self._M
    def getK(self):
        return self._K
    #Beam Element maker
    def BeamElementMaker(self, nodeI, nodeJ):
        return LineElements.BeamColumnElement(self._E*self._A, self._E*self._I,self._rho*self._A, nodeI,nodeJ)

    #Rod Element Maker
    def RodElementMaker (self,nodeI,nodeJ):
        return LineElements.RodElement(self._E*self._A, self._rho*self._A, nodeI, nodeJ)
        
    #Element List
    def elementlist(self,nodeStart,nodeEnd,numEle,eletype):
        nodeI = self._node[(nodeStart-1)]
        nodeJ = self._node[(nodeEnd-1)]
        self._xstart = nodeI.getX()
        self._ystart = nodeI.getY()
        self._xend = nodeJ.getX()
        self._yend = nodeJ.getY()
        self.updateObs()
        if eletype == 'Rod':
            for i in range(numEle):
                self._elementList.append(self.RodElementMaker(nodeI,nodeJ))
                self._line.append(nodeI.getNum())
                self._line.append(nodeJ.getNum())
        if eletype == 'Beam':   # Line Mesh
            xStart = nodeI.getX()
            yStart = nodeI.getY()
            xEnd = nodeJ.getX()
            yEnd = nodeJ.getY()
            dx = (xEnd - xStart)/numEle
            dy = (yEnd - yStart)/numEle
            # Create a list of nodes from which to define the elements
            self._node = []
            self._node.append(nodeI)
            self._line.append(nodeI.getNum())
            for i in range(1, numEle):
                self._node.append(Node.Node(xStart + i*dx, yStart + i*dy))
                self._line.append(i+1)
                self._line.append(i+1)
            self._node.append(nodeJ)
            self._line.append(numEle+1)
            self._elementList = [self.BeamElementMaker(self._node[i], self._node[i+1]) for i in range(numEle)]
    def getLine(self):
        return self._line

    def getElementList(self):
        return self._elementList
    # set dofDict
    def setdofDict(self):
        for element in self._elementList:
            dofs = element.getDofList()
            self._dofList += dofs
        self._dofDict = systemMatrices.buildDofDict(self._dofList)
        return self._dofDict

    #set removeList
    def setRemoveList (self, nodeNum, UX, UY, R):
        if UX:
            self._removeDofs.append('UX%d'%nodeNum)
        if UY:
            self._removeDofs.append('UY%d'%nodeNum)
        if R:
            self._removeDofs.append('R%d'%nodeNum)
        self._removeList = [self._dofDict[d] for d in self._removeDofs]
        return self._removeList

    def setNewMK(self):
        massMatrixData = []
        stiffnessMatrixData = []
        for element in self._elementList:
            dofs = element.getDofList()
            Me=element.getMassMatrix()
            Ke=element.getStiffnessMatrix()
            massMatrixData.append((Me,dofs))
            stiffnessMatrixData.append((Ke,dofs))   
        M = systemMatrices.buildSystemMatrix(massMatrixData, self._dofDict)
        K = systemMatrices.buildSystemMatrix(stiffnessMatrixData, self._dofDict)
        M = systemMatrices.removeRowsCols(M,self._removeList)
        K = systemMatrices.removeRowsCols(K,self._removeList)
        self._M = M.tocsr()
        self._K = K.tocsr()

    def solve(self,numModes,frequency):
        self._numModes = numModes
        self._w,self._v = spla.eigsh(self._K, numModes, self._M, sigma = frequency)
    def getFrequencies(self):
        return np.sqrt(self._w)
    def setNewV(self):
        self._v = list(self._v)
        for i in sorted(self._removeList):
            self._v.insert(i,[0*j for j in range(self._numModes)])
    def getShape(self, modenum):
        self._shape = []
        w = list()
        for i in range(len(self._v)):
            w.append(self._v[i][modenum-1])
        if self._type == 'Rod':
            for j in range(len(w)/2):
                index = self._dofDict['UX%d'%(j+1)]
                self._shape.append(['UX%d'%(j+1),w[index]])
                index = self._dofDict['UY%d'%(j+1)]
                self._shape.append(['UY%d'%(j+1),w[index]])
        else:
            for j in range(len(w)/3):
                index = self._dofDict['UX%d'%(j+1)]
                self._shape.append(['UX%d'%(j+1),w[index]])
                index = self._dofDict['UY%d'%(j+1)]
                self._shape.append(['UY%d'%(j+1),w[index]])
        return self._shape

    # related to plot window
    def addObs (self, obs):       #for line
        self._obs.append(obs)
    def updateObs(self):
        for obs in self._obs:
            obs()
    def addObserver (self, observer):    #for node
        self._observers.append(observer)
    def updateObservers(self):
        for observer in self._observers:
            observer()

# Class to maintain a solve window of a function
class FEDisplay:
    def __init__(self, feModel):
        self._feModel = feModel
        self._figName = 'Plotting window'
        
        import matplotlib.pyplot as plt
        plt.figure(self._figName)
        plt.show(block = False)
        feModel.addObserver(self.doPlot)
        feModel.addObs(self.doplotline)

    #close the plotting window
    def close(self):
        import matplotlib.pyplot as plt
        plt.figure(self._figName)
        plt.close()

    #plot node
    def doPlot(self):
        plt.figure(self._figName)
        x = self._feModel.getx()
        y = self._feModel.gety()
        plt.axis('equal')
        plt.grid(True)
        plt.plot(x, y,'ob')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.hold(True)
        plt.show(block=False)

    #plot lines
    def doplotline(self):
        x1 = self._feModel.getstartx()
        y1 = self._feModel.getstarty()
        x2 = self._feModel.getendx()
        y2 = self._feModel.getendy()
        plt.plot([x1,x2],[y1,y2],'b-')
        plt.show(block=False)

    #plot vibratioin mode
    def doPlotAgain(self,mn):
        plt.clf()
        plt.title('Plot Mode Vivration of Mode %d'%mn)
        plt.axis('equal')
        plt.grid(True)
        plt.xlabel('X')
        plt.ylabel('Y')
        lines = self._feModel.getLine()
        nodes=self._feModel.getNodes()
        i=0
        while i <len(lines):
            I = nodes[(lines[i]-1)]
            J = nodes[(lines[i+1]-1)]
            Ix = I.getX()
            Jx = J.getX()
            Iy = I.getY()
            Jy = J.getY()
            plt.plot([Ix,Jx],[Iy,Jy],'b--')
            i += 2
        v = self._feModel.getShape(mn)
        i=0
        xys=[]
        newxys = []
        for node in nodes:
            xys.append(node.getX())
            xys.append(node.getY())
        while i <len(v):
            newxys.append([v[i][1]+xys[i],v[i+1][1]+xys[i+1]])
            plt.plot(v[i][1]+xys[i],v[i+1][1]+xys[i+1],'or')
            i += 2
            plt.hold(True)
        i=0
        while i <len(lines):
            x1=newxys[lines[i]-1][0]
            x2=newxys[lines[i+1]-1][0]
            y1=newxys[lines[i]-1][1]
            y2=newxys[lines[i+1]-1][1]
            plt.plot([x1,x2],[y1,y2],'r-')
            i+=2
        plt.show(block=False)
