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

root_url = 'http://fortworthtexas.gov'
index_url = root_url + '/government/'

response = requests.get(index_url)
soup = bs4.BeautifulSoup(response.text, 'lxml')

dictList = []

def official_scrape():
	for x in range(0,len(soup.select('ul.image-nav li'))):
		row = soup.select('ul.image-nav li')[x]
		cData = {}
		cData['official.name'] = row.get_text().encode('utf-8').split('(')[0].strip()
		cData['website'] =  root_url + [a.attrs.get('href') for a in row.select('a[href]')][0]
		cData['state'] = 'TX'
		cData['body represents - muni'] = 'Fort Worth'
		if row.get_text().encode('utf-8').split('(')[1].replace(')', '').strip() == 'Mayor':
			cData['office.name'] = row.get_text().encode('utf-8').split('(')[1].replace(')', '').strip()
			cData['electoral.district'] = 'Forth Worth'
			cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(cData['state'].lower(),cData['body represents - muni'].lower().replace(' ', '_'))
		else:
			cData['office.name'] = "City Council Member" + row.get_text().encode('utf-8').split('(')[1].replace(')', '').strip()
			cData['electoral.district'] ='Fort Worth City Council ' + row.get_text().encode('utf-8').split('(')[1].replace(')', '').strip()
			cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(cData['state'].lower(), cData['body represents - muni'].lower().replace(' ', '_')) + cData['electoral.district'][-2:].strip()
		dictList.append(cData)

official_scrape()


#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
ft_worth_council_file = open('ft_worth_council.csv','wb')
csvwriter = csv.DictWriter(ft_worth_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

ft_worth_council_file.close()
 
with open("ft_worth_council.csv", "r") as ft_worth_council_csv:
     ft_worth_council = ft_worth_council_csv.read()