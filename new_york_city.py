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

root_url = 'http://council.nyc.gov'
index_url = root_url + '/html/members/members.shtml'

#get page urls of all the councilors
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text)    
        return [a.attrs.get('href') for a in soup.select('tr a[href^=/d]')]

#creates a list of all the urls and does an error check on each of them
page_urls = get_page_urls()
for page_url in page_urls:
    if checkURL(root_url + page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url + page_url)

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url + page_url)
    soup = bs4.BeautifulSoup(response.text)
    #office name and electoral district
    councilor_data['office.name'] = "City Council Member "+((soup.select('title')[0].get_text()).split(" - ")[0]).encode('utf-8').replace(' Rosie Mendez','')
    councilor_data['electoral.district'] = "New York City Council "+((soup.select('title')[0].get_text()).split(" - ")[0]).encode('utf-8').replace(' Rosie Mendez','')
    #name
    try:
        if page_url == '/d6/html/members/home.shtml':
            councilor_data['official.name'] = soup.select('tr td em')[0].get_text().encode('utf-8').split(' - ')[0]
        else:    
            councilor_data['official.name'] = soup.select('h1')[0].get_text().encode('utf-8').replace("\n", "").replace('"', '')
    except:
        pass
    #party
    try:
        if len(soup.select('title')[0].get_text().split(" - "))==2:
            councilor_data['party'] = "Unknown"
        else:
            councilor_data['party'] = ((soup.select('title')[0].get_text()).split(" - ")[2]).encode('utf-8')
    except:
        pass  
    #phone
    try:      
        if len(soup.select('td.nav_text')[0].get_text().encode('utf-8').split('District')[2].replace("\n", "").replace("            ", "").replace('Office Phone', '').strip()) > 15:
            councilor_data['phone'] = '212-NEW-YORK'
        else:
            councilor_data['phone'] = soup.select('td.nav_text')[0].get_text().encode('utf-8').split('District')[2].replace("\n", "").replace("            ", "").replace('Office Phone', '').strip()
    except:
        pass
    #email
    try:
        councilor_data['email'] = ([a.attrs.get('href') for a in soup.select('tr td a[href^=mailto]')][0]).replace('mailto:', '')
    except:
        pass              
    #website
    councilor_data['website'] = (root_url + page_url).encode('utf-8')
    #address
    str = ' '
    seq = soup.find('td', {'class': 'nav_text'}).get_text().encode('utf-8').split('\n')[1].replace('            ',''),soup.find('td', {'class': 'nav_text'}).get_text().encode('utf-8').split('\n')[2], soup.find('td', {'class': 'nav_text'}).get_text().encode('utf-8').replace('District Office Phone', '').replace('(Entrance on Hoffman Street)', '').split('\n')[3]
    councilor_data['address'] = str.join(seq).strip()
    return councilor_data 


#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#adds states
for dictionary in dictList:
    dictionary['state'] = 'NY'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
new_york_city_council_file = open('new_york_city_council.csv','wb')
csvwriter = csv.DictWriter(new_york_city_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

new_york_city_council_file.close()
 
with open("new_york_city_council.csv", "r") as new_york_city_council_csv:
     new_york_city_council = new_york_city_council_csv.read()

#print new_york_city_council

