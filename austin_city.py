import requests
import bs4
import csv
from csv import DictWriter

root_url = 'https://www.austintexas.gov'
index_url = root_url + '/page/new-city-council-members'

#get page urls of all the councilors
def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)    
    return [a.attrs.get('href') for a in soup.select('h3 a[href]')][1:]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        if page_url == '/district2':
            councilor_data['official.name'] = 'Delia Garza'
            councilor_data['office.name'] = 'City Councilor ' + soup.select('title')[0].get_text().encode('utf-8').split(' |')[0]
            councilor_data['electoral.district'] = "Austin City Council "+soup.select('title')[0].get_text().encode('utf-8').split(' |')[0]
            councilor_data['address'] = soup.select('span p')[1].get_text().encode('utf-8')
            councilor_data['website'] =  root_url + page_url
            councilor_data['email'] = root_url + [a.attrs.get('href') for a in soup.select('a[href^=/email]')][0] 
            councilor_data['phone'] = '512-974-2250'
        else:    
            councilor_data['official.name'] = soup.select('div h3')[0].get_text().encode('utf-8').replace('\n\t', '')
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


for dictionary in dictList:
    dictionary['state'] = 'TX'

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

