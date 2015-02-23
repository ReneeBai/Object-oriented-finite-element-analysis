import Node

def meshLine(nodeStart, nodeEnd, numElements, elementMaker):
    meshline=[i for i in range(numElements)]
    nodes=[j for j in range(numElements+1)]
    nodes[0]=(nodeStart)
    X=nodeEnd.getX()-nodeStart.getX()
    Y=nodeEnd.getY()-nodeStart.getY()
    for i in range(1,numElements):
        x=nodeStart.getX()+X*i/numElements
        y=nodeStart.getY()+Y*i/numElements
        new_Node=Node.Node(x,y)
        nodes[i]=(new_Node)
    nodes[numElements]=(nodeEnd)
    for k in range(numElements):
        meshline[k]=elementMaker(nodes[k],nodes[k+1])
    return meshline