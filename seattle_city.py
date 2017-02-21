import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code


root_url = 'https://www.seattle.gov'
index_url = root_url + '/council/meet-the-council'
response = requests.get(index_url)
soup = bs4.BeautifulSoup(response.text, 'lxml')
dictList = []

def council_scrape():
	for row in soup.select('div.col-sm-4 ul li'):
		cData = {}
		cData['official.name'] = row.select('a')[0].get_text().encode('utf-8').replace('\xc3\xa1l', '')
		cData['office.name'] = 'Council, ' + row.get_text().split('-')[0].strip()
		cData['website'] = root_url + [a.attrs.get('href') for a in row.select('a[href]')][0]
		cData['state'] = 'WA'
		cData['body represents - muni'] = 'Seattle'
		if "District" in cData['office.name']:
			cData['electoral.district'] = 'Seattle City Council ' + row.get_text().split('-')[0].strip()
			cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(cData['state'].lower(), cData['body represents - muni'].lower().replace(' ','_')) + cData['electoral.district'][-2:].lower().strip()
		else:
			cData['electoral.district'] = 'Seattle'
			cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(cData['state'].lower(),cData['body represents - muni'].lower().replace(' ', '_'))
		dictList.append(cData)

council_scrape()

#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
seattle_council_file = open('seattle_council.csv','wb')
csvwriter = csv.DictWriter(seattle_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

seattle_council_file.close()
 
with open("seattle_council.csv", "r") as seattle_council_csv:
     seattle_council = seattle_council_csv.read()

