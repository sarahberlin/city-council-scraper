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


root_url = 'https://www.austintexas.gov'
index_url = root_url + '/government'

#get page urls of all the councilors
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text)
        return list(set([a.attrs.get('href') for a in soup.select('p a[href^=/district]')]))

#creates list of names and districts which will be added later
name_and_district_list = []
def get_names():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)
    for x in range(1, 21):
        if x%2 == 1:
            tempDict = {}
            tempDict['name'] = soup.select('h3')[x].get_text().encode('utf-8')
            tempDict['district'] = "Austin City Council "+ soup.select('div.tooltip p')[((x-1)/2)*3].get_text().encode('utf-8')
            name_and_district_list.append(tempDict)
    return name_and_district_list

#creates a list of all the urls and does an error check on each of them
page_urls = get_page_urls()
for page_url in page_urls:
    if checkURL(root_url+page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url+page_url)

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        councilor_data['office.name'] = 'City Councilor ' + soup.select('title')[0].get_text().encode('utf-8').split(' |')[0]
        councilor_data['electoral.district'] = "Austin City Council "+soup.select('title')[0].get_text().encode('utf-8').split(' |')[0]
        councilor_data['address'] = soup.select('span p')[1].get_text().encode('utf-8')
        councilor_data['website'] =  root_url + page_url
        councilor_data['email'] = root_url + [a.attrs.get('href') for a in soup.select('a[href^=/email]')][0] 
        councilor_data['phone'] = '512-974-2250'
    except:
        pass
    return councilor_data

#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#adds state
for dictionary in dictList:
    dictionary['state'] = 'TX'

#adds official names
get_names()
for tempDict in name_and_district_list:
    for dictionary in dictList:
        if tempDict['district'] == dictionary['electoral.district']:
            dictionary['official.name'] = tempDict['name']


#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
austin_council_file = open('austin_council.csv','wb')
csvwriter = csv.DictWriter(austin_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

austin_council_file.close()
 
with open("austin_council.csv", "r") as austin_council_csv:
     austin_council = austin_council_csv.read()

#print austin_council 
