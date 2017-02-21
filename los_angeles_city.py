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
root_url = 'https://www.lacity.org/city-government/city-council/council-directory'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text, 'lxml')
dictList = []


def get_councilor_data():
	if checkURL(root_url) == 404:
		print '404 error. Check the url for {0}'.format(root_url)
	else:
		for x in range(1,16):
			newDict = {}
			row = soup.select('div.field-item tr')[x]
			newDict['official.name'] = row.select('a')[0].get_text().encode('utf-8')
			newDict['office.name'] = 'City Councilmember ' + row.select('td')[0].get_text().encode('utf-8')
			newDict['electoral.district'] = "Los Angeles City " + row.select('td')[0].get_text().encode('utf-8')
			newDict['website'] = [a.attrs.get('href') for a in row.select('a[href^=http://cd]')][0]
			newDict['email'] = [a.attrs.get('href') for a in row.select('a[href^=mailto:]')][0].replace("mailto:", "")
			newDict['phone'] = '(213) 473-3231'
			newDict['state'] = 'CA'
			newDict['body represents - muni'] = 'Los Angeles'
			newDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(newDict['state'].lower(), newDict['body represents - muni'].lower().replace(' ','_')) + newDict['electoral.district'][-2:].lower().strip()
			try:
				newDict['facebook'] = [a.attrs.get('href') for a in row.select('a[href^=http://facebook]')][0]
			except:
				pass
			try:
				newDict['twitter'] = [a.attrs.get('href') for a in row.select('a[href^=http://twitter]')][0]
			except:
				pass
			#print newDict
			dictList.append(newDict)

get_councilor_data()


#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.lamayor.org/'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('h1')[0].get_text().encode('utf-8').replace('Office of Los Angeles Mayor ','')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Los Angeles"
        mayorDict['address'] = '200 N. Spring St. Los Angeles, CA 90012'
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = '(213) 978-0600'
        mayorDict['email'] = 'mayor.garcetti@lacity.org'
        mayorDict['state'] = 'CA'
    	mayorDict['body represents - muni'] = 'Los Angeles'
    	mayorDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(mayorDict['state'].lower(),mayorDict['body represents - muni'].lower().replace(' ','_'))
        dictList.append(mayorDict)

mayor_page()



#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
los_angeles_council_file = open('los_angeles_council.csv','wb')
csvwriter = csv.DictWriter(los_angeles_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

los_angeles_council_file.close()
 
with open("los_angeles_council.csv", "r") as los_angeles_council_csv:
     los_angeles_council = los_angeles_council_csv.read()

#print los_angeles_council 
