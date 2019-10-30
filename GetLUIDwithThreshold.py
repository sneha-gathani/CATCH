import csv
import numpy as np
import os

#File1 - Participant Data
AppParticipationFields = ['LUID', 'Date', 'Hour', 'Instances']

AppParticipation = [] #Array of dictionary having List of rows in file
intermediate = [] #intermediate array to make numpy
with open('AppParticipation_year2.csv', 'r') as f:
	csv_f = csv.reader(f)
	fields = next(csv_f)
	mylist = list(csv_f)
for i in range(0, len(mylist)):
	string = mylist[i]
	values = string[0].split('\t')
	# intermediate.append(values)
	AppParticipation.append({AppParticipationFields[j]:values[j] for j in range(0,len(AppParticipationFields))})
#print(AppParticipation)

#File2 - Location Data
LocationFields = ['LUID', 'Date', 'Latitude', 'Longitude', 'Floor', 'BuildingID', 'Time']

LocationData = [] #Array of dictionary having List of rows in file
with open('EstIndoorLocation_year2.csv', 'r') as f1:
	csv_f1 = csv.reader(f1)
	fields1 = next(csv_f1)
	mylist1 = list(csv_f1)
for i in range(0, len(mylist1)):
	string1 = mylist1[i]
	values = string1[0].split('\t')
	datetime = values[1].split(" ")
	date = datetime[0]
	time = datetime[1]
	time = time.split(':')
	values[1] = date
	values.append(time[0])
	LocationData.append({LocationFields[j]:values[j] for j in range(0,len(LocationFields))})


# threshhold = 10 #threshhold for minimum number of instances
# #What is happening - If the minimum threshold is not met in the Participation array, remove the user from the Location array
i=0
j=0
count = len(LocationData)-1
print(len(LocationData))
print(len(AppParticipation))

while i<len(LocationData):
	while j<len(AppParticipation):
		if(AppParticipation[j]["LUID"] == LocationData[i]["LUID"] and (int(AppParticipation[j]["Instances"]))<10):
			# print(AppParticipation[j])
			count=count-1
			del LocationData[i]
		j=j+1
	i=i+1

# #Writing final data to csv file
print(count)
os.remove("Finalcopy.csv")
csv_file = "Finalcopy.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LocationFields)
        writer.writeheader()
        for data in LocationData:
            writer.writerow(data)
except IOError:
    print("I/O error")
	

