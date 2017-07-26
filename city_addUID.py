import csv
from csv import DictWriter
from csv import DictReader
import os
import Levenshtein
from Levenshtein import jaro
import sys

#path to office holder file
officeholder_file_path = sys.argv[1]

#path to scraped files
scraped_files_path = sys.argv[2]

#opens city office holders file
office_holder_file_dictList = []
with open (os.path.join(officeholder_file_path, "City Office Holders.csv"),"r") as office_holder_csvfile:
	reader = csv.DictReader(office_holder_csvfile)
	for row in reader:
		office_holder_file_dictList.append(row)

###ocdid matching
for csv_file in os.listdir(scraped_files_path):
	csv_file = os.path.join(scraped_files_path, csv_file)
	if '.csv' in csv_file:
		dictList = []
		newdictList = []
		with open(csv_file, 'r') as scraped_csvfile:
			reader = csv.DictReader(scraped_csvfile)
			for row in reader:
				dictList.append(row)
		for dictionary in dictList:
			for state_dictionary in office_holder_file_dictList:
				#ocdids have to be the same to proceed
				if dictionary['OCDID'] == state_dictionary['OCDID']:
					#if there is a district or ward and the ocdid matches, then uid is selected
					if 'district' in dictionary['OCDID'] or 'ward' in dictionary['OCDID']:
					#matches superdistrict 8 and 9 members for memphis
						if dictionary['OCDID'] == 'ocd-division/country:us/state:tn/place:memphis/council_district:8' or dictionary['OCDID'] == 'ocd-division/country:us/state:tn/place:memphis/council_district:9':
							if dictionary['office.name'] == state_dictionary['Office Name']:
								dictionary['UID'] = state_dictionary['UID']
						else:
							dictionary['UID'] = state_dictionary['UID']
					#matches mayors from same ocdid
					if dictionary['office.name'] == 'Mayor' and state_dictionary['Office Name'] == 'Mayor':
						dictionary['UID'] = state_dictionary['UID']
					#matches controllers from same ocdid
					elif dictionary['office.name'] == 'Controller' and state_dictionary['Office Name'] == 'Controller':
						dictionary['UID'] = state_dictionary['UID']
					#matches at large houston seats
					elif dictionary['OCDID'] == 'ocd-division/country:us/state:tx/place:houston'and 'At Large' in dictionary['office.name'] and 'At Large' in state_dictionary['Office Name']:
						if dictionary['office.name'][-1] == state_dictionary['Office Name'][-1]:
							dictionary['UID'] = state_dictionary['UID']
					#matches at large jacksonville seats
					elif dictionary['OCDID'] == 'ocd-division/country:us/state:fl/place:jacksonville' and 'At-Large Group' in dictionary['office.name'] and 'At-Large' in state_dictionary['Office Name']:
						if dictionary['office.name'][-1] == state_dictionary['Office Name'][-1]:
							dictionary['UID'] = state_dictionary['UID']
					#matches at large seattle seats
					elif dictionary['OCDID'] == 'ocd-division/country:us/state:wa/place:seattle' and dictionary['office.name'] == state_dictionary['Office Name'] and dictionary['office.name'] != 'Mayor':
						dictionary['UID'] = state_dictionary['UID']
					#leaves unmatchable charlotte at large, all of columbus, detroit, and boston at large UIDs blank
					elif dictionary['OCDID'] == 'ocd-division/country:us/state:nc/place:charlotte' and 'at large representative' in dictionary['office.name']:
						dictionary['UID'] = ''
					elif dictionary['OCDID'] == 'ocd-division/country:us/state:mi/place:detroit':
						dictionary['UID'] = ''
					elif dictionary['OCDID'] == 'ocd-division/country:us/state:oh/place:columbus':
						dictionary['UID'] = ''
					elif dictionary['OCDID'] == 'ocd-division/country:us/state:ma/place:boston' and 'At-Large' in dictionary['office.name']:
						dictionary['UID'] = ''

			newdictList.append(dictionary)
		with open(csv_file,'wb') as csvfile:
			fieldnames = ['UID','state','body represents - muni','Body Name','state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', 'OCDID']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for row in newdictList:
				writer.writerow(row)


print "added uids"
