import quadtree

# choose the treshold for the splitting algorithm
# threshold represents the maximal amount of points in one square
NodeCapacity = 50

# load data from the input file and save them in the variable 'data'
data = quadtree.Data('input.geojson')

# extract points from 'data' and save them in the list 'point_list'
point_list = data.extractPoints()

# create an object for class SquareUtil, which will in turn create the initial bounding box
SquareObject = quadtree.SquareUtil()

# create the initial bounding box 'rootSquare' with dimensions corresponding
# to the coordinates of points in 'point_list'
rootSquare = SquareObject.initSquare(point_list)

# create an object of class QuadTree,
# argument here defines the maximal capacity of the individual squares
qt = quadtree.QuadTree(NodeCapacity)

# split the object 'qt' recursively using the QuadTree algorithm
qt.split(rootSquare)

# add property 'cluster_id' to the 'features' list in the input file
# and assign corresponding values of the points in 'point_list',
# export the result as a new geojson file 'output.geojson'
data.addClusterID(point_list)

