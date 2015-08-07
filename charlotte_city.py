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


root_url = 'http://charmeck.org'
index_url = '/city/charlotte/CityCouncil/MeettheCouncil/Pages/home.aspx'


#get page urls of all the councilors
def get_page_urls():
    if checkURL(root_url + index_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url + index_url)
    else:
        response = requests.get(root_url + index_url)
        soup = bs4.BeautifulSoup(response.text)
        return [a.attrs.get('href') for a in soup.select('p a[href^=/city/charlotte/CityCouncil/MeettheCouncil]')][1:]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(root_url+page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url+page_url)
    else:
        councilor_data = {}
        response = requests.get(root_url+page_url)
        soup = bs4.BeautifulSoup(response.text)
        try:
            councilor_data['official.name'] = soup.select('div.heading')[0].get_text().encode('utf-8').replace('\r\n\t\t\t', '').replace('\t', '').split(',')[0]
            councilor_data['office.name'] = "City Council "+soup.select('div.heading')[0].get_text().encode('utf-8').replace('\r\n\t\t\t', '').replace('\t', '').split(',')[1].strip()
            councilor_data['email'] = soup.select('a[href^=mailto]')[0].get_text().encode('utf-8').replace(' \n', '')
            councilor_data['website'] = (root_url+page_url)
            councilor_data['address'] = '600 E. 4th Street Charlotte, NC 28202'
            councilor_data['phone'] ='704-336-2241'
            if 'At-Large' in soup.select('div.heading')[0].get_text().encode('utf-8').replace('\r\n\t\t\t', '').replace('\t', '').split(',')[1].strip():
                councilor_data['electoral.district'] = "Charlotte"
            else:
                councilor_data['electoral.district'] = "Charlotte City Council "+soup.select('div.heading')[0].get_text().encode('utf-8').replace('\r\n\t\t\t', '').replace('\t', '').split(',')[1].strip().replace(' Representative','')
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
    dictionary['state'] = 'NC'

#scrape mayor page
def mayor_page():
    mayor_url = 'http://charmeck.org/city/charlotte/Mayor/Pages/MeetTheMayor.aspx'  
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text)
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Charlotte"
        mayorDict['address'] =  '600 East Fourth Street, 15th Floor Charlotte, NC 28202' 
        mayorDict['email'] = 'mayor@charlottenc.gov'
        mayorDict['phone'] = '704-336-2241'
        mayorDict['website'] = mayor_url 
        mayorDict['state'] = "NC"
        dictList.append(mayorDict)
        return dictList 

mayor_page()


#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
charlotte_council_file = open('charlotte_council.csv','wb')
csvwriter = csv.DictWriter(charlotte_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

charlotte_council_file.close()
 
with open("charlotte_council.csv", "r") as charlotte_council_csv:
     charlotte_council = charlotte_council_csv.read()

#print charlotte_council 
