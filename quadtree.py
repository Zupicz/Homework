import json

INIT_CLUSTER_ID = "A"

class Point:

    def __init__(self, id, x, y):
        self.__id = id
        self.__x = x
        self.__y = y
        self.__cluster_id = INIT_CLUSTER_ID

    def __repr__(self):
        return f"(ID={self.__id}, ClusterID={self.__cluster_id}, x={self.__x}, y={self.__y})"

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

    def addCluster(self, points):
        cluster_IDs = []

        for point in points:
            cluster_IDs.append(point.getCluster())

        i = 0
        for feat in self.__data['features']:
                feat['properties']['cluster_id'] = cluster_IDs[0+i]
                i = i+1

        """for feat in self.__data['features']:
            for i in range(len(cluster_IDs)):
                feat['properties']['cluster_id'] = cluster_IDs[i]"""

        with open('output.geojson', 'w', encoding='utf-8') as f:
            json.dump(self.__data, f, indent= 2, ensure_ascii= False)

class Square:

    def __init__(self, origin, dim, points, id):
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

class SquareManager:

    def initSquare(self, points):
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

        return Square(Point("origin", minX, minY), dim, points, INIT_CLUSTER_ID)

class QuadTree:

    def __init__(self, capacity):
        self.__capacity = capacity

    def getPoints(self):
        return self.__points

    def recursive_split(self, square, capacity):
        if len(square.getPoints()) <= capacity:
            return

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
        nodes = self.recursive_split(root, self.__capacity)

        for point in root.getPoints():
            index = qt.getSquareIndex(point, root.getOrigin(), root.getDim())
            node = nodes[index]
            point.setCluster(point.getCluster() + node.getID())
            node.getPoints().append(point)

        capacity = 50
        for node in nodes:
            if len(node.getPoints()) > capacity:
                qt.split(node)

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

data = Input('input.geojson')
point_list = data.extractPoints()

sm = SquareManager()
root = sm.initSquare(point_list)

qt = QuadTree(50)
qt.split(root)

print(point_list)

data.addCluster(point_list)

