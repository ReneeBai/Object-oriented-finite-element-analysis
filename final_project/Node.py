class Node:
    _nextNode = 1    # Number of next node to be created

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._num = Node._nextNode
        Node._nextNode = Node._nextNode + 1

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getNum(self):
        return self._num
