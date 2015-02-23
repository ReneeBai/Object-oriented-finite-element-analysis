import Tkinter
import Functions

# Class for top-level Finite Element GUI window
class FEGUI(Tkinter.Tk):
    def __init__(self, parent=None):
        Tkinter.Tk.__init__(self, parent)
        self._parent = parent    # Keep a reference to the containing object
        self._feModel = Functions.FEModel()
        self._feDisplay = Functions.FEDisplay(self._feModel)
        self.initialize()

    def initialize(self):
        self.grid()    # Initialize the grid layout

        # Window title
        self.title('Finite Element GUI')

        # Label within the window
        self._titleLabel = Tkinter.Label(self, text='Master Finite Element GUI')
        self._titleLabel.grid(column=0, row=0, sticky='EW')

        # Buttons to call up various functionality
        # ----------------------------------------

        # Nodes button
        self._nodesButton = Tkinter.Button(self, text='Nodes', command=self.startNodesWindow)
        self._nodesButton.grid(column=0, row=1, sticky='EW')

        # Elements button
        self._eleButton = Tkinter.Button(self, text='Elements', command=self.startElementsWindow)
        self._eleButton.grid(column=0, row=2, sticky='EW')

        # Constraints button
        self._consButton = Tkinter.Button(self, text='Constraints', command=self.startConstrainWindow)
        self._consButton.grid(column=0, row=3, sticky='EW')

        # Solve button
        self._solButton = Tkinter.Button(self, text='Solve',command=self.startSolveWindow)
        self._solButton.grid(column=0, row=4, sticky='EW')

        # Results listing button
        self._resButton = Tkinter.Button(self, text='List Results',command=self.startListResultsWindow)
        self._resButton.grid(column=0, row=5, sticky='EW')
        
        # Plot results button
        self._plotButton = Tkinter.Button(self, text='Plot Results',command=self.startPlotResultsWindow)
        self._plotButton.grid(column=0, row=6, sticky='EW')

        self.update()
        self.geometry(self.geometry())
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.cleanupAndClose)

    def cleanupAndClose(self):
        self._feDisplay.close()
        self.quit()

    def startNodesWindow(self):
        CreateNodesWindow(self._feModel)

    def startElementsWindow(self):
        CreateElementsWindow(self._feModel)

    def startConstrainWindow(self):
        SetConstraintsWindow(self._feModel)

    def startSolveWindow(self):
        SolveWindow(self._feModel)

    def startListResultsWindow(self):
        ListResultsWindow(self._feModel)
    
    def startPlotResultsWindow(self):
        PlotResultsWindow(self._feDisplay,self._feModel)
# Class for CreateNodes window
class CreateNodesWindow(Tkinter.Tk):
    def __init__(self,feModel, parent=None):
        Tkinter.Tk.__init__(self, parent)
        self._parent = parent
        self._feModel = feModel
        self.initialize()

    def initialize(self):
        self.grid()    # Use grid layout manager
        self.title('Create Nodes')        
        # Label within the window
        self._titleLabel = Tkinter.Label(self, text='Create Nodes')
        self._titleLabel.grid(column=0, row=0, columnspan=2,sticky='EW')
        # X
        self._xLabel = Tkinter.Label(self, text='X')
        self._xLabel.grid(column=0, row=1, sticky='E')
        self._xEntry = Tkinter.Entry(self)
        self._xEntry.grid(column=1, row=1, sticky='EW')
        # Y
        self._yLabel = Tkinter.Label(self, text='Y')
        self._yLabel.grid(column=0, row=2, sticky='E')
        self._yEntry = Tkinter.Entry(self)
        self._yEntry.grid(column=1, row=2, sticky='EW')
        # "Create Nodes" button
        self._setCreateNodesButton = Tkinter.Button(self, text='Create Node', command=self.setCreateNodes)
        self._setCreateNodesButton.grid(column=0, row=3,columnspan=2,sticky='EW')

        # Update window size, set size to fixed (keep it from changing
        # if size of contents changes)
        self.update()
        self.geometry(self.geometry())

        # Disable resizing of window, horizontal and vertical
        self.resizable(False, False)

    def setCreateNodes(self):
        try:
            x = float(self._xEntry.get())
            y = float(self._yEntry.get())
        except ValueError:
            print 'Error parsing create nodes'
        except:
            print 'Unexpected error in setCreateNodes'
        else:
            self._feModel.setX(x)
            self._feModel.setY(y)
            self._feModel.setNode(x,y)

# Class for CreateElements Window
class CreateElementsWindow (Tkinter.Tk):
    def __init__(self, feModel, parent = None):
        Tkinter.Tk.__init__(self, parent)
        self._parent = parent
        self._feModel = feModel
        self.initialize()
    
    def initialize(self):
        self.grid()
        
        self.title('Create Elements')

        # Label within the window
        self._titleLabel = Tkinter.Label(self, text='Create Elements')
        self._titleLabel.grid(column=0, row=0, sticky = 'EW')
        
        # material properties
        self._firstFrame = Tkinter.LabelFrame(self, text = 'Material Properties')
        self._firstFrame.grid(column=0, row=1,sticky='EW')
        self._firstFrame.grid()

        self._elamod = Tkinter.Label(self._firstFrame, text = 'Elastic Modulus')
        self._elamod.grid(column=0,row=0,sticky='EW')
        self._elamodEntry = Tkinter.Entry(self._firstFrame)
        self._elamodEntry.grid(column=1, row=0,sticky='E')

        self._density = Tkinter.Label(self._firstFrame, text = 'Density')
        self._density.grid(column=0,row=1,sticky='EW')
        self._densityEntry = Tkinter.Entry(self._firstFrame)
        self._densityEntry.grid(column=1, row=1,sticky='EW')

        # Allow resize of columns of frame
        self._firstFrame.grid_columnconfigure(0, weight=0)
        self._firstFrame.grid_columnconfigure(1, weight=1)

        #Section properties
        self._secondFrame = Tkinter.LabelFrame(self, text = 'Section Properties')
        self._secondFrame.grid(column=0, row=2,sticky = 'EW')
        self._secondFrame.grid()

        self._area = Tkinter.Label(self._secondFrame, text = 'Area')
        self._area.grid(column=0,row=0,sticky='EW')
        self._areaEntry = Tkinter.Entry(self._secondFrame)
        self._areaEntry.grid(column=1,row=0,sticky='EW')

        self._areamoment = Tkinter.Label(self._secondFrame, text = 'Second area moment')
        self._areamoment.grid(column=0,row=1,sticky='EW')
        self._areamomentEntry = Tkinter.Entry(self._secondFrame)
        self._areamomentEntry.grid(column=1,row=1,sticky='EW')

        # Allow resize of columns of frame
        self._secondFrame.grid_columnconfigure(0, weight=0)
        self._secondFrame.grid_columnconfigure(1, weight=1)

        #Mesh Generation
        self._thirdFrame = Tkinter.LabelFrame(self, text='Mesh Generation')
        self._thirdFrame.grid(column=0, row=3,sticky='EW')
        self._thirdFrame.grid()

        self._eletype = Tkinter.Label(self._thirdFrame, text = 'Element Type')
        self._eletype.grid(column=0,row=0,sticky='EW')
        self._eletypeString = Tkinter.StringVar(self._thirdFrame)
        typechoices = ['Beam', 'Rod']
        self._eletypeString.set(typechoices[0])
        self._eletypeMenu = Tkinter.OptionMenu (self._thirdFrame, self._eletypeString, *typechoices)
        self._eletypeMenu.grid(column=1, row=0,sticky='EW')

        self._numm = Tkinter.Label(self._thirdFrame, text = '# of elements between nodes')
        self._numm.grid(column=0,row=1)
        self._nummEntry = Tkinter.Entry(self._thirdFrame)
        self._nummEntry.grid(column=1,row=1,sticky='EW') 
        
        self._startnode = Tkinter.Label(self._thirdFrame, text= 'Starting node')
        self._startnode.grid(column=0,row=2,sticky='E')
        self._startnodeEntry = Tkinter.Entry(self._thirdFrame)
        self._startnodeEntry.grid(column=1,row=2,sticky='EW')

        self._endnode = Tkinter.Label(self._thirdFrame, text= 'Ending node')
        self._endnode.grid(column=0,row=3,sticky='EW')
        self._endnodeEntry = Tkinter.Entry(self._thirdFrame)
        self._endnodeEntry.grid(column=1,row=3,sticky='EW')

        # Allow resize of columns of frame
        self._thirdFrame.grid_columnconfigure(0, weight=0)
        self._thirdFrame.grid_columnconfigure(1, weight=1)
        
         # "Create Elements" button
        self._setCreateElementsButton = Tkinter.Button(self, text='Create Elements', command=self.setCreateElements)
        self._setCreateElementsButton.grid(column=0, row=4,sticky='EW')

        self.update()
        self.geometry(self.geometry())
        self.resizable(False,False)

    def setCreateElements (self):
        try:
            E = float(self._elamodEntry.get())
            rho = float(self._densityEntry.get())
            A = float(self._areaEntry.get())
            I = float(self._areamomentEntry.get())
            numElements =int(self._nummEntry.get())
            nodeStartNum = int(self._startnodeEntry.get())
            nodeEndNum = int(self._endnodeEntry.get())
            elementType = self._eletypeString.get()
        except ValueError:
            print 'Error parsing create elements'
        except:
            print 'Unexpected error in setCreateElements'
        else:
            self._feModel.setE(E)
            self._feModel.setrho(rho)
            self._feModel.setA(A)
            self._feModel.setI(I)
            self._feModel.setnumElements(numElements)
            self._feModel.settype(elementType)
            elementList = self._feModel.elementlist(nodeStartNum,nodeEndNum,numElements,elementType)
            self._feModel.setdofDict()
            print 'Created Elements Successfully'
# Class for Set Constraints window
class SetConstraintsWindow(Tkinter.Tk):
    def __init__(self,feModel, parent=None):
        Tkinter.Tk.__init__(self, parent)
        self._parent = parent
        self._feModel = feModel
        self.initialize()

    def initialize(self):
        self.grid()    # Use grid layout manager

        self.title('Constrain DOFs')

        # Label within the window
        self._titleLabel = Tkinter.Label(self, text='Constrain DOFs')
        self._titleLabel.grid(column=0, row=0,columnspan=3, sticky='EW')

        # node
        self._nodeNum = Tkinter.Label(self, text='Node')
        self._nodeNum.grid(column=0, row=1, sticky='E')
        self._nodeNumEntry = Tkinter.Entry(self)
        self._nodeNumEntry.grid(column=1, row=1, sticky='EW')

        # get modal dofs
        self._dofsLabel = Tkinter.Label(self, text='Get Modal DOFs')
        self._dofsLabel.grid(column=0, row=2,columnspan=3, sticky='EW')
        self._DOFSLabel = Tkinter.Label(self, text='Constrained degrees of freedom')
        self._DOFSLabel.grid(column=0, row=3,columnspan=3, sticky='EW')
        
        #R checkbox
        self._rflag = Tkinter.IntVar(self)
        self._rflag.set(0)
        self._rcheckbox = Tkinter.Checkbutton(self, text='R',variable = self._rflag, offvalue=0, onvalue=1)
        self._rcheckbox.grid(column=0, row=4)

        #UX checkbox
        self._uxflag = Tkinter.IntVar(self)
        self._uxflag.set(0)
        self._uxcheckbox = Tkinter.Checkbutton(self, text='UX',variable = self._uxflag, offvalue=0, onvalue=1)
        self._uxcheckbox.grid(column=1, row=4)

        #UY checkbox
        self._uyflag = Tkinter.IntVar(self)
        self._uyflag.set(0)
        self._uycheckbox = Tkinter.Checkbutton(self, text='UY',variable = self._uyflag, offvalue=0, onvalue=1)
        self._uycheckbox.grid(column=2, row=4)

        # "Set Constaints" button
        self._setSetConstraintsButton = Tkinter.Button(self, text='Set Constraints', command=self.setSetConstraints)
        self._setSetConstraintsButton.grid(column=0, row=5,columnspan=3, sticky='EW')

        # Update window size, set size to fixed (keep it from changing
        # if size of contents changes)
        self.update()
        self.geometry(self.geometry())

        # Disable resizing of window, horizontal and vertical
        self.resizable(False, False)

    def setSetConstraints(self):
        try:
            nodeNum = int(self._nodeNumEntry.get())
            UX = bool(self._uxflag.get())
            R = bool(self._rflag.get())
            UY = bool (self._uyflag.get())
        except ValueError:
            print 'Error parsing set constrains'
        except:
            print 'Error of unknown type'
        else:
            removeList = self._feModel.setRemoveList(nodeNum,UX,UY,R)
            print 'Set Constrains Successfully!'

# Class for Solve window
class SolveWindow(Tkinter.Tk):
    def __init__(self, feModel, parent=None):
        Tkinter.Tk.__init__(self, parent)
        self._parent = parent
        self._feModel = feModel
        self.initialize()

    def initialize(self):
        self.grid()    # Use grid layout manager

        self.title('Solve')

        # Label within the window
        self._titleLabel = Tkinter.Label(self, text='Solve')
        self._titleLabel.grid(column=0, row=0,columnspan=2, sticky='EW')

        # number of modes
        self._numLabel = Tkinter.Label(self, text='Number of Modes')
        self._numLabel.grid(column=0, row=1, sticky='E')
        self._numEntry = Tkinter.Entry(self)
        self._numEntry.grid(column=1, row=1, sticky='EW')

        # find modes near frequency
        self._findLabel = Tkinter.Label(self, text='Find modes near frequency')
        self._findLabel.grid(column=0, row=2, sticky='E')
        self._findEntry = Tkinter.Entry(self)
        self._findEntry.grid(column=1, row=2, sticky='EW')

        # "Solve" button
        self._setSolveButton = Tkinter.Button(self, text='Solve', command=self.setSolve)
        self._setSolveButton.grid(column=0, row=3,columnspan=2, sticky='EW')

        # Update window size, set size to fixed (keep it from changing
        # if size of contents changes)
        self.update()
        self.geometry(self.geometry())

        # Disable resizing of window, horizontal and vertical
        self.resizable(False, False)

    def setSolve(self):
        try:
            numModes = int(self._numEntry.get())
            frequency = float(self._findEntry.get())
        except ValueError:
            print 'Error'
        except:
            print 'Unexpected Error'
        else:
            self._feModel.setNewMK()
            self._feModel.solve(numModes,frequency) #Natural Frequencies
            self._feModel.setNewV()
            print 'Problem Solved'
# Class for List Results window
class ListResultsWindow(Tkinter.Tk):
    def __init__(self, feModel,parent=None):
        Tkinter.Tk.__init__(self, parent)
        self._parent = parent
        self._feModel = feModel
        self.initialize()

    def initialize(self):
        self.grid()    # Use grid layout manager

        self.title('List Results')

        # Label within the window
        self._titleLabel = Tkinter.Label(self, text='List Results')
        self._titleLabel.grid(column=0, row=0,columnspan=2, sticky='EW')

        # number of modes
        numModes = self._feModel.getNumModes()
        self._numofmodesLabel = Tkinter.Label(self, text='%d modes available'%numModes)
        self._numofmodesLabel.grid(column=0, row=1,columnspan=2, sticky='EW')
        
        # "List All Frequencies" button
        self._setListFreButton = Tkinter.Button(self, text='List All Frequencies', command=self.setListFre)
        self._setListFreButton.grid(column=0, row=2,columnspan=2, sticky='EW')

        # specific mode
        self._modenumLabel = Tkinter.Label(self, text='mode')
        self._modenumLabel.grid(column=0, row=3, sticky='E')
        self._modenumEntry = Tkinter.Entry(self)
        self._modenumEntry.grid(column=1, row=3, sticky='EW')

        # "List Mode Shape" button
        self._setListShapeButton = Tkinter.Button(self, text='List mode shape', command=self.setListShape)
        self._setListShapeButton.grid(column=0, row=4,columnspan=2, sticky='EW')

        # Update window size, set size to fixed (keep it from changing
        # if size of contents changes)
        self.update()
        self.geometry(self.geometry())

        # Disable resizing of window, horizontal and vertical
        self.resizable(False, False)

    def setListFre(self):
        try:
            FrequencyWindow (self._feModel)
        except ValueError:
            print 'Error'
        except:
            print 'Error of unknown type'

    def setListShape(self):
        try:
            modenum = int(self._modenumEntry.get())
        except ValueError:
            print 'Error'
        except:
            print 'Error of unknown type'
        else:
            ResultsWindow(modenum,self._feModel)

#class for showing all frequencies
class FrequencyWindow(Tkinter.Tk):
    def __init__(self, feModel, parent = None):
        Tkinter.Tk.__init__(self,parent)
        self._parent = parent
        self._feModel= feModel
        self.initialize()

    def initialize(self):
        self.grid()

        self.title('List All Frequencies')
        self._textBox = Tkinter.Text(self)
        fre = self._feModel.getFrequencies()
        for i in range(len(fre)):
            self._textBox.insert(Tkinter.END, 'Frequency%d : %.16e\n'%((i+1),fre[i]))
        self._textBox.grid(row=0,column=0)
        self.update()
        self.geometry(self.geometry())
        self.resizable(True,True)

#class for showing mode shape
class ResultsWindow(Tkinter.Tk):
    def __init__(self,modenum,feModel,parent=None):
        Tkinter.Tk.__init__(self,parent)
        self._parent = parent
        self._modenum = modenum
        self._feModel = feModel
        self.initialize()
    def initialize(self):
        self.grid()
        self.title('List Mode Shape')
        self._textBox = Tkinter.Text(self)        
        shape = self._feModel.getShape(self._modenum)
        self._textBox.insert(Tkinter.END,'List Mode Shape of Mode%d\n'%self._modenum)
        for i in range(len(shape)):
            self._textBox.insert(Tkinter.END,'%s : %.16e\n'%(shape[i][0],shape[i][1]))
        self._textBox.grid(row=0,column=0)
        self.update()
        self.geometry(self.geometry())
        self.resizable(True,True)  

# Class for PlotResults window
class PlotResultsWindow(Tkinter.Tk):
    def __init__(self,feDisplay,feModel, parent=None):
        Tkinter.Tk.__init__(self, parent)
        self._parent = parent
        self._feModel = feModel
        self._feDisplay = feDisplay
        self.initialize()

    def initialize(self):
        self.grid()    # Use grid layout manager

        self.title('Plot Results')

        # Label within the window
        self._titleLabel = Tkinter.Label(self, text='Plot Results')
        self._titleLabel.grid(column=0, row=0,columnspan=2, sticky='EW')

        # number of modes
        num = self._feModel.getNumModes()
        self._numofmodesLabel = Tkinter.Label(self, text='%d modes available modes'%num)
        self._numofmodesLabel.grid(column=0, row=1,columnspan=2, sticky='EW')

        # specific mode
        self._nummodeLabel = Tkinter.Label(self, text='mode')
        self._nummodeLabel.grid(column=0, row=2, sticky='E')
        self._nummodeEntry = Tkinter.Entry(self)
        self._nummodeEntry.grid(column=1, row=2, sticky='EW')

        # "Plot vibration mode" button
        self._setPlotModeButton = Tkinter.Button(self, text='Plot vibration mode', command=self.setPlotMode)
        self._setPlotModeButton.grid(column=0, row=3,columnspan=2, sticky='EW')

        # "Stop plotting vibration mode" button
        self._setStopPButton = Tkinter.Button(self, text='Stop plotting vibration mode', command=self.setStopPlotting)
        self._setStopPButton.grid(column=0, row=4,columnspan=2, sticky='EW')

        # Update window size, set size to fixed (keep it from changing
        # if size of contents changes)
        self.update()
        self.geometry(self.geometry())

        # Disable resizing of window, horizontal and vertical
        self.resizable(False, False)

    def setPlotMode(self):
        try:
            mn = int(self._nummodeEntry.get())
        except ValueError:
            print 'Error'
        except:
            print 'Unexpected error'
        else:
            self._feDisplay.doPlotAgain(mn)
    def setStopPlotting(self):
        try:
            self._feDisplay.close()
        except ValueError:
            print 'Error'
        except:
            print 'Unexpected error'

