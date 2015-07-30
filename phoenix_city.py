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


root_url = 'https://www.phoenix.gov'
index_url = root_url + '/mayorcouncil'

#get page urls of all the councilors
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text)    
        urls = []
        for x in [a.attrs.get('href') for a in soup.select('a[href^=/district]')]:
            if len(x) == 10:
                urls.append(x)
        urls = set(urls)
        return urls

#creates a list of all the urls and does an error check on each of them
page_urls = get_page_urls()
for page_url in page_urls:
    if checkURL(root_url + page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url + page_url)

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        councilor_data['address'] = "200 W. Washington St., 11th Floor Phoenix, AZ 85003"
        councilor_data['website'] = (root_url+page_url)
        councilor_data['phone'] = '602-262-6011'     
        councilor_data['email'] = root_url + '/district{0}/contact-district-{0}'.format(page_url[-1])
        if page_url != '/district6':
            councilor_data['office.name'] = 'City ' + soup.select('h3.title')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('Vice', 'Council').strip().split(' ')[0] + " " + soup.select('h3.title')[0].get_text().encode('utf-8').replace('\r\n','').replace('Vice', 'Council').strip()
            councilor_data['official.name'] = soup.select('h3.title')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('Councilman ','').replace('Councilwoman ','').replace('Vice Mayor ','').strip()
            councilor_data['electoral.district'] = "Phoenix City Council " + soup.select('h3.title')[0].get_text().encode('utf-8').replace('\r\n','').strip()
        else:
            councilor_data['electoral.district'] = "Phoenix City Council District 6"
            councilor_data['official.name'] = soup.select('h3.title')[0].get_text().encode('utf-8')
            councilor_data['office.name'] = 'City Councilman District 6'
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
    dictionary['state'] = 'AZ'


#scrape mayor page
def mayor_page():
    mayor_url = 'https://www.phoenix.gov/mayor'
    mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text)
    mayorDict = {}
    mayorDict['official.name'] = mayor_soup.select('title')[0].get_text().encode('utf-8').replace('\r\n\t','').replace('\r\n', '').replace('Office of ', '')
    mayorDict['office.name'] = "Mayor"
    mayorDict['electoral.district'] = "Phoenix"
    mayorDict['address'] = "200 W. Washington St., 11th Floor Phoenix, AZ 85003"
    mayorDict['website'] = mayor_url
    mayorDict['phone'] = '602-262-6011'   
    mayorDict['state'] = "AZ"
    dictList.append(mayorDict)
    return dictList 

mayor_page()



#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
phoenix_council_file = open('phoenix_council.csv','wb')
csvwriter = csv.DictWriter(phoenix_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

phoenix_council_file.close()
 
with open("phoenix_council.csv", "r") as phoenix_council_csv:
     phoenix_council = phoenix_council_csv.read()

#print phoenix_council 
