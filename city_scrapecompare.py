import csv
from csv import DictWriter
from csv import DictReader
import os
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

#empty list for the text file that will be emailed
txt_file = []

#compare city files with office holder file
checkList = []
GPmissingList = []

#empty lists to compare at large councils
charlotte_file = []
charlotte_scrape = []
columbus_file = []
columbus_scrape = []
detroit_file = []
detroit_scrape = []
boston_file = []
boston_scrape = []
######

scraped_dictList = []

for csv_file in os.listdir(scraped_files_path):
	csv_file = os.path.join(scraped_files_path, csv_file)
	if '_council' in csv_file:
		with open(csv_file, 'r') as scraped_csvfile:
			reader = csv.DictReader(scraped_csvfile)
			for row in reader:
				scraped_dictList.append(row)

#loops through scraped dicts
for scraped_dict in scraped_dictList:
	#puts at large charlotte dicts in a separate dictList
	if scraped_dict['OCDID'] == 'ocd-division/country:us/state:nc/place:charlotte' and scraped_dict['office.name'] != 'Mayor':
		if scraped_dict not in charlotte_scrape:
			charlotte_scrape.append(scraped_dict)
	#puts all columbus dicts besides in a separate dictList
	elif scraped_dict['OCDID'] == 'ocd-division/country:us/state:oh/place:columbus' and scraped_dict['office.name'] != 'Mayor':
		if scraped_dict not in columbus_scrape:
			columbus_scrape.append(scraped_dict)
	#puts at large detroit dicts in a separate dictList
	elif scraped_dict['OCDID'] == 'ocd-division/country:us/state:mi/place:detroit' and scraped_dict['office.name'] != 'Mayor':
		if scraped_dict not in detroit_scrape:
			detroit_scrape.append(scraped_dict)
	#puts at large boston dicts in a separate dictList
	elif scraped_dict['OCDID'] == 'ocd-division/country:us/state:ma/place:boston' and scraped_dict['office.name'] != 'Mayor':
		if scraped_dict not in boston_scrape:
			boston_scrape.append(scraped_dict)
	#puts scraped dicts without a UID that are not intentially blank because of at large districts
	elif scraped_dict['UID'] == '':
		GPmissingList.append(scraped_dict['electoral.district'])
	else:
		#now starts looping through office holder dicts
		for office_holder_dict in office_holder_file_dictList:
			#puts charlotte at large ***office holder*** dicts in a separate dictList
			if office_holder_dict['OCDID'] == 'ocd-division/country:us/state:nc/place:charlotte' and office_holder_dict['Office Name'] == 'Council':
				if office_holder_dict not in charlotte_file:
					charlotte_file.append(office_holder_dict)
			#puts all columbus council ***office holder*** dicts in a separate dictList
			elif office_holder_dict['OCDID'] == 'ocd-division/country:us/state:oh/place:columbus' and office_holder_dict['Office Name'] == 'Board Of Directors':
				if office_holder_dict not in columbus_file:
					columbus_file.append(office_holder_dict)
			#puts detroit at large ***office holder*** dicts in a separate dictList
			elif office_holder_dict['OCDID'] == 'ocd-division/country:us/state:mi/place:detroit' and office_holder_dict['Office Name'] != 'Mayor':
				if office_holder_dict not in detroit_file:
					detroit_file.append(office_holder_dict)
			#puts boston at large ***office holder*** dicts in a separate dictList
			elif office_holder_dict['OCDID'] == 'ocd-division/country:us/state:ma/place:boston' and office_holder_dict['Office Name'] != 'Mayor':
				if office_holder_dict not in boston_file:
					boston_file.append(office_holder_dict)
			#if the dicts have UIDs, and are not charlotte at large, detroit at large, boston at large, or columbus council members, then start string comparison
			else:
				if scraped_dict['UID'] == office_holder_dict['UID']:
					if scraped_dict['official.name'] == office_holder_dict['Official Name']:
						print office_holder_dict['UID'],"scraped name: ", scraped_dict['official.name'], "file name: ",office_holder_dict['Official Name'], '\n\t>>>all good, exact match'
					elif jaro(scraped_dict['official.name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',',''),office_holder_dict['Official Name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',','')) > .65:
						print office_holder_dict['UID'], scraped_dict['official.name'],office_holder_dict['Official Name'], '\n\t>>>not exact match, but high lev score'
					else:
						print "\n\t>>>found a difference!"
						print office_holder_dict['UID'],"scraped name: ", scraped_dict['official.name'], "file name: ",office_holder_dict['Official Name']
						print jaro(scraped_dict['official.name'],office_holder_dict['Official Name'])
						#answer = raw_input("\n\t>>>is this a meaningful difference? Y/N")
						#if answer == "Y" or answer == "y":
						checkList.append(office_holder_dict['UID'])

###output from initial scrape compare string comparisons
txt_file.append("\nCheck List: "+ ",".join(checkList))
txt_file.append("\nNo UID for:"+ ",".join(GPmissingList))



###now compares at large offices
charlotte_member_count = len(charlotte_file)
charlotte_good_jaro = 0

for file_dict in charlotte_file:
	for scraped_dict in charlotte_scrape:
		if jaro(file_dict['Official Name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',',''), scraped_dict['official.name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',','')) > .65:
			charlotte_good_jaro += 1
			#print file_dict['Official Name'], scraped_dict['official.name']

if charlotte_member_count != charlotte_good_jaro:
	txt_file.append("\nCheck Charlotte At Large Council Members")
else:
	txt_file.append("\nCharlotte At Large Council Members are all good")

columbus_member_count = len(columbus_file)
columbus_good_jaro = 0

for file_dict in columbus_file:
	for scraped_dict in columbus_scrape:
		if jaro(file_dict['Official Name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',',''), scraped_dict['official.name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',','')) > .75:
			columbus_good_jaro += 1
			#print file_dict['Official Name'], scraped_dict['official.name']

if columbus_member_count != columbus_good_jaro:
	txt_file.append("\nCheck Columbus At Large Council Members")
else:
	txt_file.append("\nColumbus At Large Council Members are all good")


detroit_member_count = len(detroit_file)
detroit_good_jaro = 0

for file_dict in detroit_file:
	for scraped_dict in detroit_scrape:
		if jaro(file_dict['Official Name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',',''), scraped_dict['official.name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',','')) > .65:
			detroit_good_jaro += 1
			#print file_dict['Official Name'], scraped_dict['official.name']

if detroit_member_count != detroit_good_jaro:
	txt_file.append("\nCheck Detroit At Large Council Members")
else:
	txt_file.append("\nDetroit At Large Council Members are all good")

boston_member_count = len(boston_file)
boston_good_jaro = 0

for file_dict in boston_file:
	for scraped_dict in boston_scrape:
		if jaro(file_dict['Official Name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',',''), scraped_dict['official.name'].lower().replace(' ', '').replace('"','').replace('.','').replace(',','')) > .8:
			boston_good_jaro += 1
			#print file_dict['Official Name'], scraped_dict['official.name']

if boston_member_count != boston_good_jaro:
	txt_file.append("\nCheck Boston At Large Council Members")
else:
	txt_file.append("\nBoston At Large Council Members are all good")


txt_filestring = " ".join(txt_file)
print txt_filestring

###end here if all you want is a printed string of the results. if you want it emailed to you, uncomment out everything through line 200, fill in your email from address in line 180, your email to address in line 181, and your log in info (from address, then password as strings) in line 195


###send email
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEText import MIMEText
#import smtplib

#import time

#fromaddr = ""
#toaddr = ""
#msg = MIMEMultipart()
#msg['From'] = fromaddr
#msg['To'] = toaddr
#msg['Subject'] = "Scrape compare results {0} - {1}".format(time.strftime("%m/%d/%Y"),time.strftime("%I:%M:%S"))

#body = txt_filestring
#msg.attach(MIMEText(body, 'plain'))

#server = smtplib.SMTP('smtp.gmail.com', 587)
#server.ehlo()
#server.starttls()
#server.ehlo()
#server.login("", "")
#text = msg.as_string()

#server.sendmail(fromaddr, toaddr, text)
#print "scrape compare complete. check your email!"
