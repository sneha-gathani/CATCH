import csv
import os
import numpy as np
import pandas as pd
import random
import matplotlib
from matplotlib import patches
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from copy import deepcopy
from scipy.spatial.distance import cdist

class Point():
    def __init__(self, x, y, LUID, BuildingID, Floor):
        self.x = x
        self.y = y
        self.LUID = LUID;
        self.BuildingID = BuildingID;
        self.Floor = Floor;

    def getPointLUID(self):
    	return self.LUID

    def getPointx(self):
        return self.x

    def getPointy(self):
        return self.y

    def getPointBuildingID(self):
        return self.BuildingID

    def getPointFloor(self):
        return self.Floor


class Node():
    def __init__(self, x0, y0, w, h, points, isleaf):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.children = []
        self.isleaf = isleaf

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_points(self):
        return self.points


class QTree():
    def __init__(self, k, n):
        num_leafnodes = 0
    	#Maximum number of points in one rectangle
        self.threshold = k
        #some random points; (x,y) and number of points are len(X)
        self.points = []
        #defining the root node having x0 = 0, y0 = 0, width = 10, height = 10, points as all the points in X and isleaf = 0
        self.root = Node(0, 0, 10, 10, self.points, 0)
    
    #used to return points but of no use
    def get_points(self):
        return self.points

	#actually performs the division    
    def subdivide(self):
        recursive_subdivide(self.root, self.threshold)
    
    #draws the graph
    def graph(self):
        fig = plt.figure(figsize=(12, 8))
        plt.title("Quadtree")
        ax = fig.add_subplot(111)
        c = find_children(self.root)
        print(c)
        print("Number of segments:")
        print(len(c))
        areas = set()
        for el in c:
            areas.add(el.width*el.height)
        print("Minimum segment area: %.3f units" %min(areas))
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        print("Number of points")
        print(len(self.points))
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]
        plt.plot(x, y, 'ro')
        plt.show()
        return

    #gets the LUID's of the leaf nodes
    def getleafinfo(self):
        dataofchildnodes = []
        LUIDs = []
        latitudes = []
        longitudes = []
        BuildingIDs = []
        Floors = []
        leafnodes = 0
        leafnodescount = []
        count = 0
        toputinfilefields = ['LeafNumber', 'Latitude', 'Longitude', 'LUID', 'BuildingID', 'Floor']
        toputinfile = []
        c = getleafnode(self.root, dataofchildnodes)
        print("Print object of leaf nodes")
        print(c[0])
        print(c[1])
        print("Print info of leaf nodes")
        for i in range(len(c)):
            for j in range(len(c[i])):
                leafnodescount.append(leafnodes)
                LUIDs.append(Point.getPointLUID(c[i][j]))
                latitudes.append(Point.getPointx(c[i][j]))
                longitudes.append(Point.getPointy(c[i][j]))
                BuildingIDs.append(Point.getPointBuildingID(c[i][j]))
                Floors.append(Point.getPointFloor(c[i][j]))
                count = count + 1
            leafnodes = leafnodes + 1

        print("Count")
        print(count)
    	####### IMPORTANT: LUID's of leaf nodes are given in the following manner: LeafNode1, LUID_1_ofleaf1, LUID_2_ofleaf1, LUID_3_ofleaf1, ..., LeafNode2, LUID_1_ofleaf2, LUID_2_ofleaf2, LUID_3_ofleaf2, ..., ... #######
        print("Length of LUIDs")
        print(len(LUIDs))
        for m in range(len(c)):
            toputinfile.append({toputinfilefields[0]:leafnodescount[m], toputinfilefields[1]:latitudes[m], toputinfilefields[2]:longitudes[m], toputinfilefields[3]:LUIDs[m], toputinfilefields[4]:BuildingIDs[m], toputinfilefields[5]:Floors[m]})
            #toputinfile.append({toputinfilefields[k]:values[j] for k in range(0,len(toputinfilefields))})
        # print("To put in file")
        # print(toputinfile)
        # print("Number of entries in file")
        # print(len(toputinfile))
    	# print("Number of leaf nodes:")
    	# print(len(c))
        os.remove("closest.csv")
        csv_file = "closest.csv"
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=toputinfilefields)
                writer.writeheader()
                for data in toputinfile:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

        return

#simply adds points using the Point class
def add_point(x, y, LUID, BuildingID, Floor):
    p = Point(x, y, LUID, BuildingID, Floor)
    return p


#actual division of tree into quadtree recursively
def recursive_subdivide(node, k):
    if len(node.points)<=k:
    	node.isleaf = 1
    	return
    
    #to divide the graph into segments
    w_ = float(node.width/2)
    h_ = float(node.height/2)

    #p is the points theat are contained in a segment
    p = contains(node.x0, node.y0, w_, h_, node.points)
    #child x1 of the node
    x1 = Node(node.x0, node.y0, w_, h_, p, 0)
    recursive_subdivide(x1, k)

    p = contains(node.x0, node.y0+h_, w_, h_, node.points)
    #child x2 of the node
    x2 = Node(node.x0, node.y0+h_, w_, h_, p, 0)
    recursive_subdivide(x2, k)

    p = contains(node.x0+w_, node.y0, w_, h_, node.points)
    #child x2 of the node
    x3 = Node(node.x0 + w_, node.y0, w_, h_, p, 0)
    recursive_subdivide(x3, k)

    p = contains(node.x0+w_, node.y0+w_, w_, h_, node.points)
   	#child x4 of the node
    x4 = Node(node.x0+w_, node.y0+h_, w_, h_, p, 0)
    recursive_subdivide(x4, k)

    node.children = [x1, x2, x3, x4]
    
#checking is points of a node lie inside a segment    
def contains(x, y, w, h, points):
    pts = []
    for point in points:
        if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
            pts.append(point)
    return pts

#finding leaf node children to plot in the segment
def find_children(node):
    if not node.children:
        return [node]
    else:
        children = []
        for child in node.children:
            children += (find_children(child))
    return children

#get the information of leafnodes
def getleafnode(node, dataofchildnodes):
    #print(len(dataofchildnodes))
    if not node.children:
            #print(len(node.points))
            dataofchildnodes.append(node.points)
            #print(len(dataofchildnodes))
            return dataofchildnodes
		# print("dataofchildnodes")
		# print(dataofchildnodes)
		# print("\n")
    else:
        for child in node.children:
            getleafnode(child, dataofchildnodes)
    return dataofchildnodes

def main():
    #reading data of one day and one hour into data
    data = pd.read_csv('temporary.csv')

	#taking 5 features: Latitude and Longitude, LUID, BuildingID and FloorID
    f1 = data['Latitude'].values
    f2 = data['Longitude'].values
    f3 = data['LUID'].values
    f4 = data['BuildingID'].values
    f5 = data['Floor'].values
    print("Len of entries")
    print(len(f1))
	#upto 5 decimal points (1.1 m)
	#now doing upto 5 decimal points
	#converting distance to readable and workable numbers
    for i in range(0, len(f1)):
        f1[i] = float(f1[i] * 10000)
        f1[i] = float(f1[i] % 1000)
    for i in range(0, len(f2)):
        f2[i] = float(f2[i] * 10000)
        f2[i] = float(f2[i] % 1000)

	#making an array of latitude and longitude
    X = np.array(list(zip(f1, f2)))


    points = []
    for i in range(0, len(X)):
        points.append(add_point(X[i][0], X[i][1], f3[i], f4[i], f5[i]))
    print(points)
    print(len(points))

    print("Confirmation")
    print(points[1])
    print(points[1].getPointLUID())
    print(points[1].getPointBuildingID())

	#making a qtree object
    qtreeobj = QTree(5, len(X))

	#adding the points to the object
    for i in range(0, len(X)):
        qtreeobj.add_point(X[i][0], X[i][1], f3[i], f4[i], f5[i])

    print("Print points")
    points = qtreeobj.get_points()
    #print(len(points))

	#subdiving the root as a quadtree
    qtreeobj.subdivide()

	#LUID's of the leaf nodes are recieved
    qtreeobj.getleafinfo()

	#sad but quadtree graph is made
    qtreeobj.graph()



if __name__ == '__main__':
    main()