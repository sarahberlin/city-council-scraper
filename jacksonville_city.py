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


root_url = 'http://www.coj.net/city-council.aspx#feature01'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)
dictList = []

#runs error check on root_url
if checkURL(root_url) == 404:
    print '404 error. Check the url for {0}'.format(root_url)

def get_councilor_data1():
    for x in range (1,15):
        newDict = {}
        newDict['office.name'] = "City Council Member "+ soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[0].replace('Group', 'At-Large Group')
        newDict['official.name'] = soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[1].strip()
        newDict['electoral.district'] = "Jacksonville City Council " + soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[0].replace('Group', 'At-Large Group')
        newDict['address'] = '117 West Duval St., Suite 425 Jacksonville, FL 32202'
        newDict['website'] = root_url
        if x < 7:
            newDict['email'] = [a.attrs.get('href') for a in soup.select('div a[href*mailto:]')][x].replace('mailto:','')
        elif x > 7:
            newDict['email'] = [a.attrs.get('href') for a in soup.select('div a[href*mailto:]')][x-1].replace('mailto:','')
        if x < 4:
            newDict['phone'] = soup.find_all('div', {'align':'left'})[x-1].get_text().encode('utf-8').split('\r\n')[1].replace('          Phone: ', '')
        else:
            newDict['phone'] = soup.find_all('div', {'align':'left'})[x].get_text().encode('utf-8').split('\r\n')[1].replace('          Phone: ', '')
        dictList.append(newDict)
    return dictList

def get_councilor_data2():
    for x in range (16,21):
        newDict = {}
        newDict['office.name'] = "City Council Member "+ soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[0].replace('Group', 'At-Large Group')
        newDict['official.name'] = soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[1].strip()
        newDict['electoral.district'] = "Jacksonville City Council " + soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[0].replace('Group', 'At-Large Group')
        newDict['address'] = '117 West Duval St., Suite 425 Jacksonville, FL 32202'
        newDict['website'] = root_url
        newDict['phone'] = '(904) 630-1377'
        dictList.append(newDict)
    return dictList


get_councilor_data1()
get_councilor_data2() 

#adds states
for dictionary in dictList:
    dictionary['state'] = 'FL'

fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
jacksonville_council_file = open('jacksonville_council.csv','wb')
csvwriter = csv.DictWriter(jacksonville_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

jacksonville_council_file.close()
 
with open("jacksonville_council.csv", "r") as jacksonville_council_csv:
     jacksonville_council = jacksonville_council_csv.read()

#print jacksonville_council