import csv
import os
import sys
import numpy as np
import pandas as pd
import random
import matplotlib
import scipy.spatial.KDTree

def main():
    #reading data of one day and one hour into data
    data = pd.read_csv('temporary.csv')

	#taking 5 features: Latitude and Longitude, LUID, BuildingID and FloorID
    f1 = data['Latitude'].values
    f2 = data['Longitude'].values
    f3 = data['LUID'].values
    f4 = data['BuildingID'].values
    f5 = data['Floor'].values

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