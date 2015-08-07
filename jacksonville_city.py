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


def get_councilor_data1():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        for x in range (1,15):
            newDict = {}
            newDict['office.name'] =  "City Council Member "+ soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[0].replace('Group', 'At-Large Group').replace('\r\n\t\t\t\t\t\t\t\t\t\t','')
            newDict['official.name'] = soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[1].strip()
            newDict['electoral.district'] = "Jacksonville City Council " + soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[0].replace('Group', 'At-Large Group').replace('\r\n\t\t\t\t\t\t\t\t\t\t','')
            newDict['address'] = '117 West Duval St., Suite 425 Jacksonville, FL 32202'
            newDict['website'] = root_url
            if x < 7:
                newDict['email'] = [a.attrs.get('href') for a in soup.select('div a[href*mailto:]')][x].replace('mailto:','')
            elif x > 7:
                newDict['email'] = [a.attrs.get('href') for a in soup.select('div a[href*mailto:]')][x-1].replace('mailto:','')
            if x < 4:
                newDict['phone'] = soup.find_all('div', {'align':'left'})[x-1].get_text().encode('utf-8').split('\r\n')[1].replace('Phone: ', '').strip()
            else:
                newDict['phone'] = soup.find_all('div', {'align':'left'})[x].get_text().encode('utf-8').split('\r\n')[1].replace('Phone: ', '').strip()
            dictList.append(newDict)
        return dictList

def get_councilor_data2():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else: 
        for x in range (16,21):
            newDict = {}
            newDict['office.name'] = "City Council Member "+ soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[0].replace('Group', 'At-Large Group').replace('\r\n\t\t\t\t\t\t\t\t\t\t','')
            newDict['official.name'] = soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n          ','').split(':')[1].strip()
            newDict['electoral.district'] = "Jacksonville" 
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

#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.coj.net/mayor.aspx'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text)
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('h1')[0].get_text().encode('utf-8').replace('Office of Mayor ','').replace('\r\n', '').strip()
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Jacksonville"
        mayorDict['address'] = 'City Hall at St. James Building 117 W. Duval St.  Suite 400 Jacksonville, FL  32202'
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = '(904) 630-1776'
        mayorDict['email'] = 'MayorLennyCurry@coj.net'
        mayorDict['state'] = "FL"
        dictList.append(mayorDict)
        return dictList 

mayor_page()



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