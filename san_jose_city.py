import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2


###removed checkURL from functions because of false 404

def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

root_url = 'http://www.sanjoseca.gov/council'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text, 'lxml')
dictList = []


def get_councilor_data():
    for x in range(1,11):
        cData = {}
        cData['official.name']=soup.select('span.Subhead2')[x].get_text().encode('utf-8').replace('\xa0',', ').replace('\xc2',', ').split(", ")[0].replace('Vice Mayor ','')
        district =soup.select('span.Subhead2')[x].get_text().encode('utf-8').replace('\xa0',', ').replace('\xc2','').split(", ")[1].strip()
        cData['electoral.district']='San Jose City Council '+ district
        cData['office.name']= 'City Councilmember '+district
        cData['address']= '200 E. Santa Clara St. San Jose, CA 95113'
        cData['website']= 'http://www.sanjoseca.gov/council'
        cData['email']=  'district{0}@sanjoseca.gov'.format(x)
        dictList.append(cData)

get_councilor_data()


#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.sanjoseca.gov/mayor'
    mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
    mayorDict = {}
    mayorDict['official.name'] = mayor_soup.select('div.Headline')[0].get_text().encode('utf-8').split(',')[0].replace('Office of Mayor ','').replace('The ','')
    mayorDict['office.name'] = "Mayor"
    mayorDict['electoral.district'] = "San Jose"
    mayorDict['address'] = '200 E. Santa Clara St. San Jose, CA 95113'
    mayorDict['website'] = 'http://www.sanjoseca.gov/mayor'
    mayorDict['phone'] = '408 535-3500 Main'
    dictList.append(mayorDict)
    return dictList

mayor_page()

#adds other info
for dictionary in dictList:
    dictionary['state'] = 'CA'
    dictionary['body represents - muni'] = 'San Jose'
    if "District" in dictionary['electoral.district']:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(dictionary['state'].lower(), dictionary['body represents - muni'].lower().replace(' ','_')) + dictionary['electoral.district'][-2:].lower().strip()
    else:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(dictionary['state'].lower(),dictionary['body represents - muni'].lower().replace(' ','_')) 

#makes csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
san_jose_council_file = open('san_jose_council.csv','wb')
csvwriter = csv.DictWriter(san_jose_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

san_jose_council_file.close()
 
with open("san_jose_council.csv", "r") as san_jose_council_csv:
     san_jose_council = san_jose_council_csv.read()

#print san_jose_council 

