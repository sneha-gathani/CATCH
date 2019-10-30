NOTES ABOUT WHAT FILE IS WHAT

1. AppParticipation_year2.csv and EstIndoorLocation_year2.csv are the data files got.
AppParticipation_year2.csv has -
LUID, Date, Hour, Instances
EstIndoorLocation_year2.csv has -
LUID, Device Time, Latitude, Longitude, Floor, BuildingID

2. InitialFiltering.ipynb
Takes AppParticipation_year2.csv and EstIndoorLocation_year2.csv files and filters participants having minimum of 10 instances. Creates file fulldatetime.csv.

3. filtering.py
Takes fulldatetime.csv and forms temporary.csv which has data of one day and one hour only.

4. cleancleanclean.py
Takes temporary.csv and removes duplicates such that unique LUIDS, BuildingID, Floor, Latitude and Longitude are maintained.