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

#reading fulldata
data = pd.read_csv('fulldatetime.csv')
data1 = pd.read_csv('fulldatetime.csv')

#Filtering for date; 2018-02-09 and hour 5-6 PM
hourdatafields = ['LUID', 'Date', 'Latitude', 'Longitude', 'Floor', 'BuildingID', 'Time']
hourdata = []
for i in range(0, len(data)):
    if(data['Date'][i] == '2018-02-09'):
        timesplit = data['Time'][i].split(':')
        filters = [timesplit[0]]
        if(timesplit[0] == "17"):
            hourdata.append({hourdatafields[j]:data.iloc[i][j] for j in range(0,len(hourdatafields))})

#Saves this data in onedayonehour file
os.remove("onedayonehour.csv")
csv_file = "onedayonehour.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=hourdatafields)
        writer.writeheader()
        for data in hourdata:
            writer.writerow(data)
except IOError:
    print("I/O error")

#one day
daydatafields = ['LUID', 'Date', 'Latitude', 'Longitude', 'Floor', 'BuildingID', 'Time']
daydata = []
for i in range(0, len(data1)):
    if(data1['Date'][i] == '2018-02-09'):
        daydata.append({daydatafields[j]:data1.iloc[i][j] for j in range(0,len(daydatafields))})

#Saves this data in onedayonehour file
#os.remove("oneday.csv")
csv_file = "oneday.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=daydatafields)
        writer.writeheader()
        for data in daydata:
            writer.writerow(data)
except IOError:
    print("I/O error")


#reading onedayonehour file
two = pd.read_csv('oneday.csv')
two.drop(columns=['Time'])
#os.remove("temporaryday.csv")
two.to_csv("temporaryday.csv", sep=',')


#reading data of one day and one hour into data
data = pd.read_csv('temporaryday.csv')

print(len(data))
data.drop_duplicates(subset=None, inplace=True)
print(len(data))


os.remove("temporaryday.csv")
mainfile = "temporaryday.csv"
data.to_csv(mainfile, sep=',')

data = pd.read_csv('temporaryday.csv')
print(len(data))
#end one day


#reading onedayonehour file
one = pd.read_csv('onedayonehour.csv')
one.drop(columns=['Time'])
os.remove("temporary.csv")
one.to_csv("temporary.csv", sep=',')


#reading data of one day and one hour into data
data = pd.read_csv('onedayonehour.csv')

print(len(data))
data.drop_duplicates(subset=None, inplace=True)
print(len(data))


os.remove("temporary.csv")
mainfile = "temporary.csv"
data.to_csv(mainfile, sep=',')

data = pd.read_csv('temporary.csv')
print(len(data))
