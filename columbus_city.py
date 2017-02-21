import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2


root_url = 'http://columbus.gov/council/members/'
dictList = []


def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

def get_councilor_data():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        response = requests.get(root_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        for x in range(1,9):
            if soup.find('div', {'id': 'inner-right-single'}).select('div p')[x].get_text().encode('utf-8').replace('\xc2\xa0', '').replace('Chair', '').replace(', Council President', '').replace(', President Pro-Tem', '').split(':')[0].strip() != '':
                newDict = {}
                newDict['official.name'] = soup.find('div', {'id': 'inner-right-single'}).select('div p')[x].get_text().encode('utf-8').replace('\xc2\xa0', '').replace('Chair', '').replace(', Council President', '').replace(', President Pro-Tem', '').replace(' Pro Tempore','').split(':')[0].strip()
                newDict['office.name'] = 'City Council Member '+'At-Large'
                newDict['electoral.district'] = 'Columbus'
                newDict['address'] = '90 West Broad St. Columbus, OH 43215'
                newDict['website'] = root_url
                newDict['Body Name'] = "Columbus Board Of Directors"
                try:
                    newDict['email'] = soup.find('div', {'id': 'inner-right-single'}).select('div p')[x].get_text().encode('utf-8').replace('\xc2\xa0', '').replace('Chair', '').replace(', Council President', '').replace(', President Pro-Tem', '').split(':')[3].replace('Legislative Assistant', '').replace('Legislative Aide', '').split('(')[0].replace(') ', ' ').strip()
                    newDict['phone']= soup.find('div', {'id': 'inner-right-single'}).select('div p')[x].get_text().encode('utf-8').replace('\xc2\xa0', '').replace('Chair', '').replace(', Council President', '').replace(', President Pro-Tem', '').split(':')[3].replace('Legislative Assistant', '').replace('Legislative Aide', '').split('(')[1].replace(') ', ' ').strip()
                except:
                    pass
                dictList.append(newDict)
        return dictList

get_councilor_data()

#adds state
for dictionary in dictList:
    dictionary['state'] = 'OH'

#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.columbus.gov/Templates/Detail.aspx?id=66058'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('p strong')[2].get_text().encode('utf-8').replace('Mayor ','')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Columbus"
        mayorDict['address'] = 'City Hall 2nd Floor 90 West Broad Street Columbus, OH 43215'
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = '614-645-7671'
        mayorDict['email'] = '311@columbus.gov'
        mayorDict['state'] = "OH"
        mayorDict['Body Name'] = 'Columbus Elected Officials'
        dictList.append(mayorDict)
        return dictList 

mayor_page()


for dictionary in dictList:
    dictionary['body represents - muni'] = 'Columbus'
    dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(dictionary['state'].lower(),dictionary['body represents - muni'].lower())   


#makes csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
columbus_council_file = open('columbus_council.csv','wb')
csvwriter = csv.DictWriter(columbus_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

columbus_council_file.close()
 
with open("columbus_council.csv", "r") as columbus_council_csv:
     columbus_council = columbus_council_csv.read()

#print columbus_council		
