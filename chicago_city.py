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
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text)    
        return [a.attrs.get('href') for a in soup.select('h4 a[href]')][1:]

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
    try:
        if len(soup.select('tr td')[3].get_text().encode('utf-8')) == 12:
            councilor_data['phone'] = soup.select('tr td')[3].get_text().encode('utf-8')
        else:
            councilor_data['phone'] = '312.744.5000'
        councilor_data['address'] = '121 N. LaSalle Street Chicago, Illinois 60602'
        try:
            if "Chicago" in soup.select('tr td')[7].get_text().encode('utf-8'):
                councilor_data['address'] = soup.select('tr td')[7].get_text().encode('utf-8').replace('\n', '')
            else:
                councilor_data['address'] = '121 N. LaSalle Street Chicago, Illinois 60602'
        except:
            pass
        councilor_data['office.name'] = "Alderman "+soup.find_all('h1')[0].get_text().encode('utf-8')
        councilor_data['electoral.district'] = "Chicago City Council District " + soup.find_all('h1')[0].get_text().encode('utf-8').replace('Ward ', '')
        councilor_data['official.name'] = soup.select('h3')[2].get_text().encode('utf-8').replace('Alderman', '').strip()
        councilor_data['website'] = (root_url + page_url).encode('utf-8')
        councilor_data['email'] = [a.attrs.get('href') for a in soup.select('td a[href]')][0].encode('utf-8').replace('mailto:','')
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
    dictionary['state'] = 'IL'


#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
chicago_council_file = open('chicago_council.csv','wb')
csvwriter = csv.DictWriter(chicago_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

chicago_council_file.close()
 
with open("chicago_council.csv", "r") as chicago_council_csv:
     chicago_council = chicago_council_csv.read()

#print chicago_council 