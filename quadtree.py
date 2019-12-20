import json

INIT_CLUSTER_ID = "A"

class Point:

    def __init__(self, id, x, y):
        self.__id = id
        self.__x = x
        self.__y = y
        self.__cluster_id = INIT_CLUSTER_ID

    def __repr__(self):
        return f"(ID={self.__id}, x={self.__x}, y={self.__y})"

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getID(self):
        return self.__id

    def getCluster(self):
        return self.__cluster_id

    def setCluster(self, id):
        self.__cluster_id = id

"""class Mock:

    def __init__(self, size, max_X, max_Y):
        self.__size = size
        self.__max_X = max_X
        self.__max_Y = max_Y

    def getPoints(self):
        points = []
        for i in range(0, self.__size):
            points.append(Point(i, randint(0, self.__max_X), randint(0, self.__max_Y)))
        return points"""

class Input:

    def __init__(self, file):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.__data = data

    def loadElements(self):
        elements = []
        for f in self.__data['features']:
            elements.append(f)
        return elements

    def extractPoints(self):
        points = []
        for f in self.__data['features']:
            points.append(Point(id = f['properties']['@id'], x = f['geometry']['coordinates'][0], y = f['geometry']['coordinates'][1]))
        return points

class Square:

    def __init__(self, origin, dim, points, id):
        self.__origin = origin
        self.__dim = dim
        self.__points = points
        self.__id = id

    def __repr__(self):
        return f"(ID={self.__id}, origin={self.__origin}, dim={self.__dim})"

    def getID(self):
        return self.__id

    def getOrigin(self):
        return self.__origin

    def getDim(self):
        return self.__dim

    def getPoints(self):
        return self.__points

class SquareManager:

    def initSquare(self, points):
        maxX = 0
        maxY = 0

        for p in points:
            maxX = max(maxX, p.getX())
            maxY = max(maxY, p.getY())

        dim = max(maxX, maxY)

        return Square(Point("origin", 0, 0), dim, points, INIT_CLUSTER_ID)

class QuadTree:

    def __init__(self, capacity):
        self.__capacity = capacity

    def getPoints(self):
        return self.__points

    def contains(self, origin, dim, points):
        pts = []
        for point in points:
            if point.getX() >= origin.getX() and point.getX() <= origin.getX()+dim and point.getY() >= origin.getY() and point.getY() <= origin.getY()+dim:
                pts.append(point)
        return pts

    def recursive_split(self, square, capacity):
        if len(square.getPoints()) <= capacity:
            return

        dim_ = float(square.getDim()/2)
        origin = square.getOrigin()

        children = []
        #nodePoints = self.contains(square.getX0(), square.getY0(), w_, h_, square.getPoints())
        SW = Square(Point("a", origin.getX(), origin.getY()), dim_, [], square.getID() + "A")
        children.append(SW)
        #recursive_split(SW, capacity)

        #nodePoints = self.contains(square.getX0() + w_, square.getY0(), w_, h_, square.getPoints())
        SE = Square(Point("b", origin.getX() + dim_, origin.getY()), dim_, [], square.getID() + "B")
        children.append(SE)
        #recursive_split(SE, capacity)

        #nodePoints = self.contains(square.getX0(), square.getY0()+h_, w_, h_, square.getPoints())
        NW = Square(Point("c", origin.getX(), origin.getY() + dim_), dim_, [], square.getID() + "C")
        children.append(NW)
        #recursive_split(NW, capacity)

        #nodePoints = self.contains(square.getX0()+w_, square.getY0()+h_, w_, h_, square.getPoints())
        NE = Square(Point("d", origin.getX() + dim_, origin.getY() + dim_), dim_, [], square.getID() + "D")
        children.append(NE)
        #recursive_split(NE, capacity)

        return children

    def split(self, root):
        result = self.recursive_split(root, self.__capacity)

        return result

    def getSquareIndex(self, point, origin, dim):
        index = 0
        half = dim / 2

        if point.getX() >= origin.getX() + half:
            if point.getY() >= origin.getY() + half:
                index = 3
            else:
                index = 1
        else:
            if point.getY() >= origin.getY() + half:
                index = 2

        return index


    """def split(self, square):
        halfDimension = square.getDim()/2
        children = []

        origin = square.getOrigin()
        square00 = Square(Point("A00", origin.getX(), origin.getY()), halfDimension)
        square01 = Square(Point("A01", origin.getX()+halfDimension, origin.getY()), halfDimension)
        square10 = Square(Point("A10", origin.getX(), origin.getY()+halfDimension), halfDimension)
        square11 = Square(Point("A11", origin.getX()+halfDimension, origin.getY()+halfDimension), halfDimension)

        children.append(square00)
        children.append(square01)
        children.append(square10)
        children.append(square11)
        square.setChildren(children)"""

data = Input('input.geojson')
point_list = data.extractPoints()

man = SquareManager()
root = man.initSquare(point_list)
print(root)

qt = QuadTree(50)
nodes = qt.split(root)
print(nodes)

print(len(point_list))

"""man = SquareManager()
sq = man.initSquare(point_list)
print(sq)

qt = QuadTree()
qt.split(sq)
print(sq)"""

