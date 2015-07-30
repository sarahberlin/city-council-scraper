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

root_url = 'http://www.sanjoseca.gov/council'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)
dictList = []

#runs error check on root_url
if checkURL(root_url) == 404:
    print '404 error. Check the url for {0}'.format(root_url)

def get_councilor_data():
    for x in range(1,11):
        cData = {}
        cData['official.name']=soup.select('span.Subhead2')[x].get_text().encode('utf-8').split(", ")[0]
        cData['electoral.district']='San Jose City Council '+soup.select('span.Subhead2')[x].get_text().encode('utf-8').split(", ")[1]
        cData['office.name']= 'City Councilmember '+soup.select('span.Subhead2')[x].get_text().encode('utf-8').split(", ")[1]
        cData['phone']= soup.select('tbody tr td')[x].get_text().split('\n')[1].encode('utf-8').replace('            Ph: ', '')
        cData['address']= '200 E. Santa Clara St. San Jose, CA 95113'
        cData['website']= 'http://www.sanjoseca.gov/council'
        cData['email']=  'district{0}@sanjoseca.gov'.format(x)
        dictList.append(cData)

get_councilor_data()

for dictionary in dictList:
    dictionary['state'] = 'CA'


#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.sanjoseca.gov/mayor'
    mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text)
    mayorDict = {}
    mayorDict['official.name'] = mayor_soup.select('div.Headline')[0].get_text().encode('utf-8').split(',')[0].replace('Office of Mayor ','')
    mayorDict['office.name'] = "Mayor"
    mayorDict['electoral.district'] = "San Jose"
    mayorDict['address'] = '200 E. Santa Clara St. San Jose, CA 95113'
    mayorDict['website'] = 'http://www.sfmayor.org/'
    mayorDict['phone'] = '408 535-3500 Main'
    mayorDict['state'] = "CA"
    dictList.append(mayorDict)
    return dictList 

mayor_page()



#makes csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
san_jose_council_file = open('san_jose_council.csv','wb')
csvwriter = csv.DictWriter(san_jose_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

san_jose_council_file.close()
 
with open("san_jose_council.csv", "r") as san_jose_council_csv:
     san_jose_council = san_jose_council_csv.read()

#print san_jose_council 

