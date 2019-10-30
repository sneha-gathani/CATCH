import csv
import os
import sys
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
    def __init__(self, x, y, LUID, BuildingID, Floor, Date, Time):
        self.x = x
        self.y = y
        self.LUID = LUID;
        self.BuildingID = BuildingID;
        self.Floor = Floor;
        self.Date = Date;
        self.Time = Time;

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

    def getPointDate(self):
        return self.Date

    def getPointTime(self):
        return self.Time


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

    def get_numpoints(self):
        return len(self.points)


class QTree():
    def __init__(self, k, n, points):
        num_leafnodes = 0
        #Maximum number of points in one rectangle
        self.threshold = k
        #some random points; (x,y) and number of points are len(X)
        self.points = points
        #defining the root node having x0 = 0, y0 = 0, width = 10, height = 10, points as all the points in X and isleaf = 0
        self.root = Node(900, 560, 40, 90, self.points, 0)
    
    #used to return points but of no use
    def get_points(self):
        return self.points

    def get_rootpoints(self):
        return Node.get_points(self.root)
    #actually performs the division    
    def subdivide(self):
        recursive_subdivide(self.root, self.threshold)
    
    #draws the graph
    def graph(self):
        fig = plt.figure(figsize=(12, 8))
        plt.title("Quadtree")
        ax = fig.add_subplot(111)
        c = find_children(self.root)
        areas = set()
        for el in c:
            areas.add(el.width*el.height)
        # print("Minimum segment area: %.3f units" %min(areas))
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        # print("Number of points")
        # print(len(self.points))
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
        iterator = 1

        c = getleafnode(self.root, dataofchildnodes)
        print("Entire clustered data: ")
        print(c)
        numpointscount = 0 
        temp = []
        
        for i in range(len(c)):
            if(len(c[i]) != 0):
                leafnodescount.append(len(c[i]))
                LUIDs.append(iterator)
                iterator = iterator + 1
            for j in range(len(c[i])):
                temp.append(Point.getPointLUID(c[i][j]))
                latitudes.append(Point.getPointx(c[i][j]))
                longitudes.append(Point.getPointy(c[i][j]))
                BuildingIDs.append(Point.getPointBuildingID(c[i][j]))
                Floors.append(Point.getPointFloor(c[i][j]))
                count = count + 1
            LUIDs.append(temp)
            temp = []
            leafnodes = leafnodes + 1

        print("Total number of entries of points in the clustered array = ", count)

        #prints NULL arrays also
        # print("LUIDs = ", LUIDs)

        #final result which is array having row number followed by array of closest points; removing NULL arrays
        result = [x for x in LUIDs if x != []]

        print("Final neighbouring points LUIDs:")
        print(result)
        return

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

    p = contains(node.x0, node.y0 + h_, w_, h_, node.points)
    
    #child x2 of the node
    x2 = Node(node.x0, node.y0 + h_, w_, h_, p, 0)
    recursive_subdivide(x2, k)

    p = contains(node.x0 + w_, node.y0, w_, h_, node.points)
    
    #child x2 of the node
    x3 = Node(node.x0 + w_, node.y0, w_, h_, p, 0)
    recursive_subdivide(x3, k)

    p = contains(node.x0 + w_, node.y0 + h_, w_, h_, node.points)
    
    #child x4 of the node
    x4 = Node(node.x0 + w_, node.y0 + h_, w_, h_, p, 0)
    recursive_subdivide(x4, k)

    node.children = [x1, x2, x3, x4]
    
#checking is points of a node lie inside a segment    
def contains(x, y, w, h, points):
    pts = []
    i = 0
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
    if(node.isleaf == 1):
        appendleafdata(node.points, dataofchildnodes)
    else:
        for child in node.children:
            getleafnode(child, dataofchildnodes)
    return dataofchildnodes

def appendleafdata(points, dataofchildnodes):
    dataofchildnodes.append(points)
    return dataofchildnodes


#simply adds points using the Point class
def add_point(x, y, LUID, BuildingID, Floor, Date, Time):
    p = Point(x, y, LUID, BuildingID, Floor, Date, Time)
    return p


def main():

    # for i in range(0, 23):
    #     print(i)
    #     filename = "/Users/snehagathani/Desktop/Lab/Cleaning_Data/hourly_data/filteredonedayhour"+str(i)+".csv"
        #reading data of one day and one hour into data
    data = pd.read_csv("/Users/snehagathani/Desktop/Lab/Cleaning_Data/hourly_data/filteredonedayhour1.csv")

	#taking 5 features: Latitude and Longitude, LUID, BuildingID and FloorID
    f1 = data['Latitude'].values
    f2 = data['Longitude'].values
    f3 = data['LUID'].values
    f4 = data['BuildingID'].values
    f5 = data['Floor'].values
    f6 = data['Date'].values
    f7 = data['Time'].values

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
        points.append(add_point(X[i][0], X[i][1], f3[i], f4[i], f5[i], f6[i], f7[i]))

    #making a qtree object
    qtreeobj = QTree(2, len(X), points)

    p = qtreeobj.get_points()
    # print("Number of points in the file, added for clustering = ", len(p))

    q = qtreeobj.get_rootpoints()
    # print("Number of points recieved in the instance = ", len(q))

    #subdiving the root as a quadtree
    qtreeobj.subdivide()

    #LUID's of the leaf nodes are recieved
    qtreeobj.getleafinfo()

    #sad but quadtree graph is made
    #qtreeobj.graph()

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    main()