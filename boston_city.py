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


root_url = 'https://www.boston.gov'
index_url = root_url + '/departments/city-council'

soup = bs4.BeautifulSoup(requests.get(index_url).text, 'lxml')


dictList = []

def council_scrape():
    for person in soup.select('div.section-grid-of-people article')[0:13]:
        cData = {}
        cData['office.name'] = 'City Council Member ' + person.select('div.person-profile-position-title-list')[0].get_text().encode('utf-8').strip().replace('President, ','')
        cData['official.name'] = person.select('div.person-profile-display-name')[0].get_text().encode('utf-8').strip()
        cData['website'] = root_url + [a.attrs.get('href') for a in person.select('a[href^=/departments/city-council/]')][0]
        cData['body represents - muni'] = 'Boston'
        cData['state'] = 'MA'
        if "At-Large" in person.select('div.person-profile-position-title-list')[0].get_text().encode('utf-8').strip():
        	cData['electoral.district'] = "Boston"
        	cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(cData['state'].lower(),cData['body represents - muni'].lower().replace(' ', '_'))
        else:
        	cData['electoral.district'] = "Boston City Council " + person.select('div.person-profile-position-title-list')[0].get_text().encode('utf-8').strip()
        	cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(cData['state'].lower(), cData['body represents - muni'].lower().replace(' ','_')) + cData['electoral.district'][-2:].lower().strip().replace(' ', '_')
        dictList.append(cData)

council_scrape()

#scrape mayor page
def mayor_page():
    mayor_url = 'https://www.boston.gov/departments/mayors-office'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('span.lo-t')[0].get_text().encode('utf-8').replace('Mayor ','')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Boston"
        mayorDict['state'] = "MA"
        mayorDict['website'] = mayor_url
        mayorDict['body represents - muni'] = 'Boston'
        mayorDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(mayorDict['state'].lower(),mayorDict['body represents - muni'].lower().replace(' ','_'))  
        dictList.append(mayorDict)

mayor_page()



#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
boston_city_council_file = open('boston_city_council.csv','wb')
csvwriter = csv.DictWriter(boston_city_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)




