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

#set up
root_url = 'http://lacity.org/city-government/elected-official-offices/city-council/council-directory'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)
dictList = []

if checkURL(root_url) == 404:
    print '404 error. Check the url for {0}'.format(root_url)

def get_councilor_data():
	for x in range(0,15):
		newDict = {}
		try:
			if x < 9:
				newDict['official.name'] = soup.findAll('td', {'class': 'views-field views-field-title'})[x].get_text().encode('utf-8').strip()[18:]
			else:
				newDict['official.name'] = soup.findAll('td', {'class': 'views-field views-field-title'})[x].get_text().encode('utf-8').strip()[19:]
			newDict['address'] = soup.findAll('td', {'class': 'views-field views-field-field-headquarters-location'})[x].get_text().encode('utf-8').replace('\n', '').replace('Los Angeles', ' Los Angeles').replace("Office", "Office ").title().replace('Hall200', 'Hall 200')
			newDict['email'] = [a.attrs.get('href') for a in soup.select('a[href^=mailto:]')][x].replace("mailto:", "")
			newDict['website'] = [a.attrs.get('href') for a in soup.select('a[href^=http://cd]')][x]
			newDict['phone'] = '(213) 473-3231'
			newDict['electoral.district'] = "Los Angeles City "+soup.findAll('td', {'class': 'views-field views-field-title'})[x].select('a')[0].get_text().encode('utf-8')
			newDict['office.name'] = 'City Councilmember' + soup.findAll('td', {'class': 'views-field views-field-title'})[x].select('a')[0].get_text().encode('utf-8').replace('Council', '')
		except:
			pass
		dictList.append(newDict)
	return dictList

get_councilor_data()

#adds state
for dictionary in dictList:
    dictionary['state'] = 'CA'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
los_angeles_council_file = open('los_angeles_council.csv','wb')
csvwriter = csv.DictWriter(los_angeles_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

los_angeles_council_file.close()
 
with open("los_angeles_council.csv", "r") as los_angeles_council_csv:
     los_angeles_council = los_angeles_council_csv.read()

#print los_angeles_council 
