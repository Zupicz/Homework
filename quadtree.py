import json

#constant variable declaring initial cluster_id for points and nodes
def INIT_CLUSTER_ID():
    return "A"

class Point:

    def __init__(self, id, x, y):
        self.__id = id
        self.__x = x
        self.__y = y
        self.__cluster_id = INIT_CLUSTER_ID()

    def __repr__(self):
        return f"(ID={self.__id}, ClusterID={self.__cluster_id}, x={self.__x}, y={self.__y})"

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getID(self):
        return self.__id

    def getClusterID(self):
        return self.__cluster_id

    def setCluster(self, id):
        self.__cluster_id = id

class Data:

    def __init__(self, file):
        """Open the input file and save it in the class field self.__data."""
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.__data = data

    def extractPoints(self):
        """Extract the points from self.__data and save them in a new list 'points'.
        Points have 3 attributes: 'id', 'x' and 'y'."""

        points = []
        for f in self.__data['features']:
            points.append(Point(id = f['properties']['@id'], x = f['geometry']['coordinates'][0], y = f['geometry']['coordinates'][1]))
        return points

    def addClusterID(self, points):
        """Add a new property 'cluster_id' to the points in 'self.__data['features']'
        and export the result in a new file 'output.geojson'."""

        i = 0
        for feat in self.__data['features']:
            feat['properties']['cluster_id'] = points[i].getClusterID()
            i += 1

        with open('output.geojson', 'w', encoding='utf-8') as f:
            json.dump(self.__data, f, indent= 2, ensure_ascii= False)

class Square:

    def __init__(self, origin, dim, points, id):
        """
        'origin' of the Square is a Point,
        'dim' is the length, respectively the width of a Square,
        'points' are the Points belonging to the Square,
        'id' is the identificator of the Square.
        """

        self.__origin = origin
        self.__dim = dim
        self.__points = points
        self.__id = id

    def __repr__(self):
        return f"(ID={self.__id}, origin={self.__origin}, dim={self.__dim}, points={self.__points})"

    def getID(self):
        return self.__id

    def getOrigin(self):
        return self.__origin

    def getDim(self):
        return self.__dim

    def getPoints(self):
        return self.__points

class SquareUtil:

    def initSquare(self, points):
        """Create a bounding box with an origin and dimensions corresponding
        to the coordinates of the points in 'points'. Give the bounding box
        an identificator defined in INIT_CLUSTER_ID."""

        maxX = 0
        maxY = 0

        for p in points:
            maxX = max(maxX, p.getX())
            maxY = max(maxY, p.getY())

        minX = maxX
        minY = maxY

        for p in points:
            minX = min(minX, p.getX())
            minY = min(minY, p.getY())

        dim = max(maxX - minX, maxY - minY)

        return Square(Point("origin", minX, minY), dim, points, INIT_CLUSTER_ID())

class QuadTree:

    def __init__(self, capacity):
        self.__capacity = capacity

    def getPoints(self):
        return self.__points

    def createSquares(self, square, capacity):
        """Split th square into four children named SW, SE, NW, NE which have IDs
        'A', 'B', 'C' and 'D' respectively. Append children in a new list 'children'."""

        dim_ = float(square.getDim()/2)
        origin = square.getOrigin()

        children = []
        SW = Square(Point("a", origin.getX(), origin.getY()), dim_, [], "A")
        children.append(SW)

        SE = Square(Point("b", origin.getX() + dim_, origin.getY()), dim_, [], "B")
        children.append(SE)

        NW = Square(Point("c", origin.getX(), origin.getY() + dim_), dim_, [], "C")
        children.append(NW)

        NE = Square(Point("d", origin.getX() + dim_, origin.getY() + dim_), dim_, [], "D")
        children.append(NE)

        return children

    def split(self, root):
        """If there's less points in the root than amount in self.__capacity, do nothing.
        If there's more points, split the root square in four by calling the method createSquares().
        Assign points to one of four corresponding square by calling the method getSquareIndex().
        Recurse if needed."""

        if len(root.getPoints()) <= self.__capacity:
            return

        nodes = self.createSquares(root, self.__capacity)

        for point in root.getPoints():
            index = self.getSquareIndex(point, root.getOrigin(), root.getDim())
            node = nodes[index]
            point.setCluster(point.getClusterID() + node.getID())
            node.getPoints().append(point)

        for node in nodes:
            if len(node.getPoints()) > self.__capacity:
                self.split(node)

    def getSquareIndex(self, point, origin, dim):
        """Return index of one of the four squares which contains the 'point'."""
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

