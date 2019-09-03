import math

# Class to store Node data
class NodeData:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data

# Class for Node
class Node:
    def __init__(self, parent, x0, y0, w, h, data):
        self.parent = parent
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.data = data
        self.NWchild = None
        self.NEchild = None
        self.SEchild = None
        self.SWchild = None

    def isLeaf(self):
        if self.NWchild is None and self.NEchild is None and self.SEchild is None and self.SWchild is None:
            return True
        else: return False

    def isRoot(self):
        if self.parent is None: return True
        else: return False

    def searchForDataXY(self, data):
        if self.isLeaf():
            if self.data.x == data.x and self.data.y == data.y:
                return self
            else: return None
        else:
            dataTile = self.checkBoundaries(data)
            if dataTile == 1:
                if self.NWchild is None: return None
                return self.NWchild.searchForDataXY(data)
            if dataTile == 2:
                if self.NEchild is None: return None
                return self.NEchild.searchForDataXY(data)
            if dataTile == 3:
                if self.SEchild is None: return None
                return self.SEchild.searchForDataXY(data)
            if dataTile == 4:
                if self.SWchild is None: return None
                return self.SWchild.searchForDataXY(data)

    def checkBoundaries(self, data):
        halfWX = self.x0 + math.floor(self.width / 2)
        halfHY = self.y0 + math.floor(self.height / 2)
        if data.x <= halfWX and data.y <= halfHY: return 1
        if data.x > halfWX and data.y <= halfHY: return 2
        if data.x > halfWX and data.y > halfHY: return 3
        if data.x <= halfWX and data.y > halfHY: return 4

    def addData(self, data):
        halfW = math.floor(self.width / 2)
        halfH = math.floor(self.height / 2)
        newDataTile = self.checkBoundaries(data)
        selfDataTile = None
        if self.data is not None:
            selfDataTile = self.checkBoundaries(self.data)
        if self.isLeaf():
            if selfDataTile == 1:
                self.NWchild = Node(self, self.x0, self.y0, halfW, halfH, self.data)
            if selfDataTile == 2:
                self.NEchild = Node(self, self.x0 + halfW, self.y0, halfW, halfH, self.data)
            if selfDataTile == 3:
                self.SEchild = Node(self, self.x0 + halfW, self.y0 + halfH, halfW, halfH, self.data)
            if selfDataTile == 4:
                self.SWchild = Node(self, self.x0, self.y0 + halfH, halfW, halfH, self.data)
            self.data = None

        if newDataTile == 1:
            if self.NWchild is not None:
                self.NWchild.addData(data)
            else:
                self.NWchild = Node(self, self.x0, self.y0, halfW, halfH, data)
        if newDataTile == 2:
            if self.NEchild is not None:
                self.NEchild.addData(data)
            else:
                self.NEchild = Node(self, self.x0 + halfW, self.y0, halfW, halfH, data)
        if newDataTile == 3:
            if self.SEchild is not None:
                self.SEchild.addData(data)
            else:
                self.SEchild = Node(self, self.x0 + halfW, self.y0 + halfH, halfW, halfH, data)
        if newDataTile == 4:
            if self.SWchild is not None:
                self.SWchild.addData(data)
            else:
                self.SWchild = Node(self, self.x0, self.y0 + halfH, halfW, halfH, data)

# Class for Quadtree
class QuadTree:
    def __init__(self, x0, y0, w, h):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.root = None

    def addData(self, data):
        if self.root is None:
            self.root = Node(None, self.x0, self.y0, self.width, self.height, data)
        else:
            self.root.addData(data)







