import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://www.sfbos.org/'


#get page urls of all the councilors
def get_page_urls():
    response = requests.get(root_url)
    soup = bs4.BeautifulSoup(response.text)    
    urls = []
    for x in range(0,11):
        for ul in soup.findAll('ul', {'id': 'bos_list'}):
            a = ul.findAll('a')[x]
            urls.append(a.attrs['href'])
    return urls

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        councilor_data['electoral.district'] = 'San Francisco City Council '+ soup.select('div.sup_district')[0].get_text().encode('utf-8')
        councilor_data['office.name'] = 'Board of Supervisors ' + soup.select('div.sup_district')[0].get_text().encode('utf-8')
        councilor_data['official.name'] = soup.select('div.sup_name')[0].get_text().encode('utf-8')
        str = ' '
        seq = soup.select('p')[-1].get_text().encode('utf-8').replace('\n', '').split('\r')[0:3]
        councilor_data['address'] = str.join(seq)
        councilor_data['website'] = (root_url+page_url)
        councilor_data['phone'] = soup.select('p')[-1].get_text().encode('utf-8').replace('\n', '').split('\r')[3].replace(' - voice', '')[0:14]
        councilor_data['email'] = [a.attrs.get('href') for a in soup.select('a[href^=mailto]')][0].replace('mailto:','').replace('" target="_top', '')
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
    dictionary['state'] = 'CA'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
san_francisco_council_file = open('san_francisco_council.csv','wb')
csvwriter = csv.DictWriter(san_francisco_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

san_francisco_council_file.close()
 
with open("san_francisco_council.csv", "r") as san_francisco_council_csv:
     san_francisco_council = san_francisco_council_csv.read()

#print san_francisco_council 
