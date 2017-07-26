import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2
from selenium import webdriver
import lxml.html as lh


url ='https://www.elpasotexas.gov'
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, 'lxml')
dictList = []

def council_scrape():
	for row in soup.select('nav.mainNav ul.mainMenu li')[2:11]:	
		cData = {}
		cData['website'] = [a.attrs.get('href') for a in row.select('a[href]')][0]
		cData['state'] = 'TX'
		cData['body represents - muni'] = 'El Paso'
		if "District" in row.get_text().encode('utf-8'):
			cData['official.name'] = row.select('a')[0].get_text().encode('utf-8').split(" - ")[1].strip()
			cData['electoral.district'] = "El Paso City Council "+ row.select('a')[0].get_text().encode('utf-8').split(" - ")[0].strip()
			cData['office.name'] = "City Council Member " + row.select('a')[0].get_text().encode('utf-8').split(" - ")[0].strip()
			cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(cData['state'].lower(), cData['body represents - muni'].lower().replace(' ','_')) + cData['electoral.district'][-2:].lower().strip()
		else:
			cData['official.name'] = row.select('a')[0].get_text().encode('utf-8').strip().replace('Mayor ','')
			cData['electoral.district'] = "El Paso"
			cData['office.name'] = 	'Mayor'		
			cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(cData['state'].lower(),cData['body represents - muni'].lower().replace(' ', '_'))
		dictList.append(cData)

council_scrape()


#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
el_paso_council_file = open('el_paso_council.csv','wb')
csvwriter = csv.DictWriter(el_paso_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

el_paso_council_file.close()
 
with open("el_paso_council.csv", "r") as el_paso_council_csv:
     el_paso_council = el_paso_council_csv.read()
