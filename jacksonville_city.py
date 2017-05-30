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


root_url = 'http://www.coj.net/city-council.aspx'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text, 'lxml')
dictList = []

def get_councilor_data():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        for x in range(0,14):
            newDict = {}
            row = soup.select('ul.secondCMSListMenuUL li')[x]
            newDict['office.name'] =  "City Council Member "+ [a.attrs.get('href') for a in row.select('a[href]')][0].split('-members/')[1].replace('.aspx', '').replace('d0', "District ").replace('al', "At-Large Group ")
            newDict['official.name'] = row.select('a')[0].get_text().encode('utf-8')
            newDict['body represents - muni'] = "Jacksonville"
            newDict['state'] = "FL"
            newDict['address'] = '117 West Duval St., Suite 425 Jacksonville, FL 32202'
            newDict['website'] = [a.attrs.get('href') for a in row.select('a[href]')][0]
            if "Large" in newDict['office.name']:
                newDict['electoral.district'] = "Jacksonville"
                newDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(newDict['state'].lower(),newDict['body represents - muni'].lower())  
            else:
                newDict['electoral.district'] = "Jacksonville City Council " + [a.attrs.get('href') for a in row.select('a[href]')][0].split('-members/')[1].replace('.aspx', '').replace('d', "District ").replace('District 0', 'District ')
                newDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(newDict['state'].lower(), newDict['body represents - muni'].lower().replace(' ','_')) + newDict['electoral.district'][-2:].lower().strip()
            dictList.append(newDict)

get_councilor_data()


#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.coj.net/mayor.aspx'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('h1')[0].get_text().encode('utf-8').replace('Office of Mayor ','').replace('\r\n', '').strip()
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Jacksonville"
        mayorDict['address'] = 'City Hall at St. James Building 117 W. Duval St.  Suite 400 Jacksonville, FL  32202'
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = '(904) 630-1776'
        mayorDict['email'] = 'MayorLennyCurry@coj.net'
        mayorDict['state'] = 'FL'
        mayorDict['body represents - muni'] = 'Jacksonville'
        mayorDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(mayorDict['state'].lower(),mayorDict['body represents - muni'].lower())  
        dictList.append(mayorDict)

mayor_page()


fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
jacksonville_council_file = open('jacksonville_council.csv','wb')
csvwriter = csv.DictWriter(jacksonville_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

jacksonville_council_file.close()
 
with open("jacksonville_council.csv", "r") as jacksonville_council_csv:
     jacksonville_council = jacksonville_council_csv.read()

#print jacksonville_council