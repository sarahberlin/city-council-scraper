import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://www.cityofchicago.org'
index_url = root_url + '/city/en/about/wards.html'

def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#get page urls of all the councilors
def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')    
    return [a.attrs.get('href') for a in soup.select('h4 a[href]')]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url + page_url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    try:
        if len(soup.select('tr td')[3].get_text().encode('utf-8')) == 12:
            councilor_data['phone'] = soup.select('tr td')[3].get_text().encode('utf-8')
        else:
            councilor_data['phone'] = '312.744.5000'
        councilor_data['address'] = '121 N. LaSalle Street Chicago, Illinois 60602'
        try:
            if "Chicago" in soup.select('tr td')[7].get_text().encode('utf-8'):
                councilor_data['address'] = soup.select('tr td')[7].get_text().encode('utf-8').replace('\n', '').replace('\xc2\xa0', ' ')
            else:
                councilor_data['address'] = '121 N. LaSalle Street Chicago, Illinois 60602'
        except:
            pass
        councilor_data['office.name'] = "Alderman "+soup.find_all('h1')[0].get_text().encode('utf-8')
        councilor_data['electoral.district'] = "Chicago City Council District " + soup.find_all('h1')[0].get_text().encode('utf-8').replace('Ward ', '').strip()
        councilor_data['official.name'] = soup.select('h3')[2].get_text().encode('utf-8').replace('Alderman', '').replace('\xc2\xa0',' ').strip()
        councilor_data['website'] = (root_url + page_url).encode('utf-8')
        councilor_data['email'] = [a.attrs.get('href') for a in soup.select('td a[href]')][0].encode('utf-8').replace('mailto:','')
        councilor_data['state'] = 'IL'
        councilor_data['Body Name'] = 'Chicago Council'
        councilor_data['body represents - muni'] = 'Chicago'
        councilor_data['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/ward:'.format(councilor_data['state'].lower(), councilor_data['body represents - muni'].lower()) + councilor_data['electoral.district'][-2:].strip()
    except:
        pass
    return councilor_data


#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    try:
        dictList.append(get_councilor_data(page_url))
        #print page_url
    except:
        pass

#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.cityofchicago.org/city/en/depts/mayor.html'
    mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
    mayorDict = {}
    mayorDict['official.name'] = mayor_soup.select('h2 span.small')[0].get_text().encode('utf-8').split(',')[0]
    mayorDict['office.name'] = "Mayor"
    mayorDict['electoral.district'] = "Chicago"
    mayorDict['address'] = "121 N LaSalle Street Chicago City Hall 4th Floor Chicago, IL 60602 "
    mayorDict['website'] = mayor_url 
    mayorDict['state'] = "IL"
    mayorDict['Body Name'] = 'Chicago Elected Officials'
    mayorDict['body represents - muni'] = 'Chicago'
    mayorDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(mayorDict['state'].lower(),mayorDict['body represents - muni'].lower())
    dictList.append(mayorDict)
    return dictList 
mayor_page()


#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
chicago_council_file = open('chicago_council.csv','wb')
csvwriter = csv.DictWriter(chicago_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

chicago_council_file.close()
 
with open("chicago_council.csv", "r") as chicago_council_csv:
     chicago_council = chicago_council_csv.read()

#print chicago_council 