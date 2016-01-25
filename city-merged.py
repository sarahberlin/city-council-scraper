import brewery
from brewery import ds
import sys
import csv
from csv import DictWriter
from csv import DictReader
import os
import datetime

#establishes today's date, which will be included in the file name
today = datetime.date.today()

path = '/Users/sarahberlin/Dropbox/GovProj Scraping/City_scripts'
os.listdir(path)

#run all of the python files in this directory so that the csv's are up to date
for py_file in os.listdir(path):
    if ".py" in py_file and 'merged' not in py_file:
        os.system("python {0}".format(py_file))
        print py_file

#get names of csv files so they can be merged
csv_files = []
for csv_file in os.listdir(path):
    if ".csv" in csv_file and 'merged' not in csv_file:
        csv_files.append(csv_file)

sources = []

for csv_file in csv_files:
    newDict = {}
    newDict['file'] = csv_file
    newDict['fieldnames'] = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
    sources.append(newDict)


# creates list of all fields and adds filename to store information
#all_fields = brewery.FieldList(["file"])
all_fields = []
#all_fields.append('file')
for source in sources:
    for field in source["fieldnames"]:
        if field not in all_fields:
            all_fields.append(field)


#gets each row in each csv file and puts it in a list
all_rows = []
for source in sources:
    for row in csv.DictReader(open(source['file'], 'rb')):
        all_rows.append(row)

#for row in all_rows:
#    for source in sources:
#        row['file'] = source['file']

#tries to write each of those rows to the new csv and then close the csv
fieldnames = all_fields
city_merged_file = open('city_merged_file-{0}.csv'.format(today),'wb')
csvwriter = csv.DictWriter(city_merged_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in all_rows:
    csvwriter.writerow(row)

city_merged_file.close()


with open("city_merged_file-{0}.csv".format(today), "r") as city_merged_file_csv:
     city_merged_file = city_merged_file_csv.read()

#print city_merged_file
print "Scraping complete"



#these are all of the cities that should be in the merged file. this list will be used to check future iterations of the file against

master_cities = ['Austin', 'Charlotte', 'Chicago', 'Columbus', 'Dallas', 'Houston', 'Jacksonville', 'Los Angeles', 'New York', 'Philadelphia', 'Phoenix', 'San Antonio', 'San Diego', 'San Francisco', 'San Jose']


#these are all of the cities in the current version of the file
cities_in_file= []
for row in csv.DictReader(open('city_merged_file.csv', 'r')):
    if row['electoral.district'].split(' City')[0] not in cities_in_file:
        cities_in_file.append(row['electoral.district'].split(' City')[0])

#print cities_in_file

#check current file against master file
count = 0
#displays message if we are missing a city
for city in master_cities:
    if city not in cities_in_file:
        print "We are missing " + city + " city"
    else:
        count += 1
#displays message if we have all the cities
if count == len(master_cities):
    print "All the cities that should be in the file are in the file"
