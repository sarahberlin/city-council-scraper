import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://www.indy.gov'
index_url = root_url + '/eGov/Council/Councillors/Biography/Pages/home.aspx'
   
#get page urls of all the councilors
def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)    
    page_urls = []
    for item in ([a.attrs.get('href') for a in soup.select('li a[href*at-large_]')]):
        page_urls.append(item)
    for item in ([a.attrs.get('href') for a in soup.select('li a[href*district]')]):
        page_urls.append(item)
    return page_urls

#root_url = 'http://www.indy.gov'
#page_url = '/eGov/Council/Councillors/Biography/Pages/at-large_1.aspx'
#response = requests.get(root_url+page_url)
#soup = bs4.BeautifulSoup(response.text)

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        if 'at-large' in page_url:
            councilor_data['official.name'] = (soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').split(",")[0]).strip()
            councilor_data['office.name'] = "City Council "+(soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').split(",")[1]).strip()
            councilor_data['electoral.district'] = 'Indianapolis'
            councilor_data['website'] =  root_url + page_url
            councilor_data['address'] = 'City-County Building, 200 E. Washington St., Indianapolis, IN 46204'
            councilor_data['email'] = soup.select('a[href^=mailto]')[0].get_text().encode('utf-8').replace('mailto:','')
            councilor_data['phone'] = soup.select('td p')[1].get_text().encode('utf-8').replace('\xc2\xa0', '').split("Phone: ")[1].replace('(317)', '317-')[:12]
        else:
            councilor_data['official.name'] = (soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').split(",")[1]).strip()
            councilor_data['office.name'] = "City Councillor "+(soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').split(",")[0]).strip()
            councilor_data['electoral.district'] = "Indianapolis City Council "+(soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').split(",")[0]).strip()
            councilor_data['website'] =  root_url + page_url
            councilor_data['address'] = 'City-County Building, 200 E. Washington St., Indianapolis, IN 46204'
            councilor_data['email'] = soup.select('a[href^=mailto]')[0].get_text().encode('utf-8').replace('mailto:','')
            councilor_data['phone'] = soup.select('td p')[1].get_text().encode('utf-8').replace('\xc2\xa0', '').split("Phone: ")[1].replace('(317)', '317-')[:12]
    except:
        pass
    return councilor_data

#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

for dictionary in dictList:
    dictionary['state'] = 'IN'

#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.indy.gov/eGov/mayor/Pages/home.aspx'
    mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text)
    mayorDict = {}
    mayorDict['official.name'] = mayor_soup.select('h6')[0].get_text().encode('utf-8').replace('Office of the Mayor', '')
    mayorDict['office.name'] = "Mayor"
    mayorDict['electoral.district'] = "Indianapolis"
    mayorDict['address'] = '200 East Washington Street Indianapolis, Indiana 46204'
    mayorDict['website'] = mayor_url
    mayorDict['phone'] = '(317) 327-3601'
    mayorDict['state'] = "IN"
    dictList.append(mayorDict)
    return dictList 

mayor_page()


#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
indianapolis_council_file = open('indianapolis_council.csv','wb')
csvwriter = csv.DictWriter(indianapolis_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

indianapolis_council_file.close()
 
with open("indianapolis_council.csv", "r") as indianapolis_council_csv:
     indianapolis_council = indianapolis_council_csv.read()

#print indianapolis_council 

