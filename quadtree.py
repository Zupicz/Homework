from random import randint
import json

class Point:

    def __init__(self, id, x, y):
        self.__id = id
        self.__x = x
        self.__y = y

    def __repr__(self):
        return f"(ID={self.__id}, x={self.__x}, y={self.__y})"

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

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

    def __init__(self, x0, y0, width, height, points):
        self.__x0 = x0
        self.__y0 = y0
        self.__width = width
        self.__height = height
        self.__points = points
        self.__children = []

    def __repr__(self):
        return f"(Origin={self.__x0},{self.__y0}, width={self.__width}, height={self.__height} children={self.__children})"

    def setChildren(self, children):
        self.__children = children

    def getChildren(self):
        return self.__children

    def getX0(self):
        return self.__x0

    def getY0(self):
        return self.__y0

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getPoints(self):
        return self.__points

"""class SquareManager:

    def initSquare(self, points):
        maxX = 0
        maxY = 0

        for p in points:
            maxX = max(maxX, p.getX())
            maxY = max(maxY, p.getY())

        origin = Point("AA", 0, 0)

        return Square(origin, max(maxX, maxY))"""

class QuadTree:

    def __init__(self, capacity, points):
        self.__capacity = capacity
        self.__points = points
        self.__root = Square(0, 0, 60, self.__points)

    def getPoints(self):
        return self.__points

    def split(self):
        recursive_split(self.__root, self.__capacity)

    def recursive_split(square, capacity):
        if len(square.getPoints()) <= capacity:
            return

        w_ = float(square.getWidth()/2)
        h_ = float(square.getHeight()/2)

        nodePoints = contains(square.getX0(), square.getY0(), w_, h_, square.getPoints())
        SW = Square(square.getX0(), square.getY0(), w_, h_, nodePoints)
        recursive_split(SW, capacity)

        nodePoints = contains(square.getX0(), square.getY0()+h_, w_, h_, square.getPoints())
        NW = Square(square.getX0(), square.getY0()+h_, w_, h_, nodePoints)
        recursive_split(NW, capacity)

        nodePoints = contains(square.getX0()+w_, square.getY0(), w_, h_, square.getPoints())
        SE = Square(square.getX0()+w_, square.getY0(), w_, h_, nodePoints)
        recursive_split(SE, capacity)

        nodePoints = contains(square.getX0()+w_, square.getY0()+h_, w_, h_, square.getPoints())
        NE = Square(square.getX0()+w_, square.getY0()+h_, w_, h_, nodePoints)
        recursive_split(NE, capacity)

    def contains(x, y, w, h, points):
        pts = []
        for point in points:
            if point.getX() >= x and point.getX() <= x+w and point.getY() >= y and point.getY() <= y+h:
                pts.append(point)
        return pts



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
print(point_list)

"""man = SquareManager()
sq = man.initSquare(point_list)
print(sq)

qt = QuadTree()
qt.split(sq)
print(sq)"""

