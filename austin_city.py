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
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text)
        for x in range(1, 21):
            if x%2 == 1:
                tempDict = {}
                tempDict['name'] = soup.select('h3')[x].get_text().encode('utf-8')
                tempDict['district'] = "Austin City Council "+ soup.select('div.tooltip p')[((x-1)/2)*3].get_text().encode('utf-8')
                name_and_district_list.append(tempDict)
        return name_and_district_list

#get office name, district, address, and email from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(root_url+page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url+page_url)
    else:
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
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#adds state
for dictionary in dictList:
    dictionary['state'] = 'TX'

#adds official names to dictionaries
get_names()
for tempDict in name_and_district_list:
    for dictionary in dictList:
        if tempDict['district'] == dictionary['electoral.district']:
            dictionary['official.name'] = tempDict['name']

#scrape mayor page
def mayor_page():
    mayor_url = 'https://www.austintexas.gov/department/mayor'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:  
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text)
        mayorDict = {}
        mayorDict['official.name'] =  [img.attrs.get('alt') for img in mayor_soup.select('p img[alt]')][0].replace("Mayor ", "")
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Austin"
        mayorDict['address'] =  '301 W 2nd St Austin, 78701' 
        mayorDict['phone'] = '512-978-2100'
        mayorDict['website'] = mayor_url 
        mayorDict['state'] = "TX"
        dictList.append(mayorDict)
        return dictList 

mayor_page()

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

