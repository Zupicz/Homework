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

class Mock:

    def __init__(self, size, max_X, max_Y):
        self.__size = size
        self.__max_X = max_X
        self.__max_Y = max_Y

    def getPoints(self):
        points = []
        for i in range(0, self.__size):
            points.append(Point(i, randint(0, self.__max_X), randint(0, self.__max_Y)))
        return points

class Square:

    def __init__(self, origin, dim):
        self.__origin = origin
        self.__dim = dim
        self.__children = []

    def __repr__(self):
        return f"(Origin={self.__origin}, length={self.__dim}, children={self.__children})"

    def setChildren(self, children):
        self.__children = children

    def getChildren(self):
        return self.__children

    def getOrigin(self):
        return self.__origin

    def getDim(self):
        return self.__dim

class SquareManager:

    def initSquare(self, points):
        maxX = 0
        maxY = 0

        for p in points:
            maxX = max(maxX, p.getX())
            maxY = max(maxY, p.getY())

        origin = Point("AA", 0, 0)

        return Square(origin, max(maxX, maxY))

class QuadTree:

    def split(self, square):
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
        square.setChildren(children)

mock = Mock(100, 20, 20)
mock_points = mock.getPoints()

man = SquareManager()
sq = man.initSquare(mock_points)
print(sq)

qt = QuadTree()
qt.split(sq)
print(sq)
