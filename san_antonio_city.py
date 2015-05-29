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

root_url = 'https://www.sanantonio.gov'
index_url = root_url + '/council'


#get page urls of all the councilors
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text)
        return [a.attrs.get('href') for a in soup.select('ul.side-sub-menu a[href^=/council]')]

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
        if ', I' in soup.select('title')[0].get_text().encode('utf-8').replace('\r\n','').replace('\t', '').replace('\xc3\x91', 'N'):
            str = " "
            seq = soup.select('title')[0].get_text().encode('utf-8').replace('\r\n','').replace('\t', '').replace('\xc3\x91', 'N').split(', ')[0], soup.select('title')[0].get_text().encode('utf-8').replace('\r\n','').replace('\t', '').replace('\xc3\x91', 'N').split(', ')[1]
            councilor_data['official.name'] = str.join(seq)
            councilor_data['electoral.district'] = "San Antonio "+soup.select('title')[0].get_text().encode('utf-8').replace('\r\n','').replace('\t', '').replace('\xc3\x91', 'N').split(', ')[2].title()
            councilor_data['office.name'] = soup.select('title')[0].get_text().encode('utf-8').replace('\r\n','').replace('\t', '').replace('\xc3\x91', 'N').split(', ')[2].title().replace('Council', 'Council Member')
        else:
            councilor_data['electoral.district'] = 'San Antonio '+soup.select('title')[0].get_text().encode('utf-8').replace('\r\n','').replace('\t', '').replace('\xc3\x91', 'N').split(', ')[1].title()
            
            councilor_data['official.name'] = soup.select('title')[0].get_text().encode('utf-8').replace('\r\n','').replace('\t', '').replace('\xc3\x91', 'N').split(', ')[0].title()
            councilor_data['office.name'] = soup.select('title')[0].get_text().encode('utf-8').replace('\r\n','').replace('\t', '').replace('\xc3\x91', 'N').split(', ')[1].title().replace('Council', 'Council Member')
        councilor_data['website'] = (root_url+page_url) 
        councilor_data['address'] = soup.select('div p')[0].get_text().encode('utf-8').replace('\r\n', ' ').replace(' \n\n', '').replace('\n', ' ').split('Office Line: ')[0]
        councilor_data['phone'] = soup.select('div p')[0].get_text().encode('utf-8').replace('\r\n', ' ').replace(' \n\n', '').replace('\n', ' ').split('Office Line: ')[1][:13]
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

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
san_antonio_council_file = open('san_antonio_council.csv','wb')
csvwriter = csv.DictWriter(san_antonio_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

san_antonio_council_file.close()
 
with open("san_antonio_council.csv", "r") as san_antonio_council_csv:
     san_antonio_council = san_antonio_council_csv.read()

#print san_antonio_council 

