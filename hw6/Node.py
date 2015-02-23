class Node:
    ''' A class that contain data for a finite element node - its coordinates and its ID number.'''
    _node = 0
    def __init__(self, x, y):
        self._x=x
        self._y=y
        Node._node += 1
        self._node=Node._node
    def getX(self):
        return self._x
    def getY(self):
        return self._y
    def getNum(self):
        return self._node