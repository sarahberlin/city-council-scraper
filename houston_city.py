import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://www.houstontx.gov'
index_url = root_url + '/council'

#get page urls of all the councilors
def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)    
    return [a.attrs.get('href') for a in soup.select('div.content a[href^=/council]')][1:17]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        if page_url == '/council/b':
            councilor_data['official.name'] = soup.select('li.leaf')[1].get_text().encode('utf-8').replace("About ", "")
        else:
            councilor_data['official.name'] = soup.select('p span.contBold')[0].get_text().replace('Council Member ', '')
        councilor_data['electoral.district'] = 'Houston City '+soup.select('h1')[0].get_text().encode('utf-8').replace('City', "").strip() 
        councilor_data['office.name'] = soup.select('h1')[0].get_text().encode('utf-8').replace('Council', 'Council Member').replace('City', "").strip()  
        councilor_data['address'] = "City Hall Annex 900 Bagby, First Floor Houston, TX 77002"
        councilor_data['website'] = (root_url+page_url)     
        if len(soup.select('div.content p')[4].get_text().encode('utf-8').split("FAX")[0].replace("Phone: ", "")) >12:
                councilor_data['phone'] = "832.393.1100"
        else:
          councilor_data['phone'] =   soup.select('div.content')[3].get_text().encode('utf-8').split('\xc2\xa0')[2].replace('\n', '').replace('E-Mail:', '').replace('Phone: ', '')[:12]       
        councilor_data['email'] = soup.select('div.content a[href^=mailto:]')[0].get_text()
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
houston_council_file = open('houston_council.csv','wb')
csvwriter = csv.DictWriter(houston_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)
houston_council_file.close()
 
with open("houston_council.csv", "r") as houston_council_csv:
     houston_council = houston_council_csv.read()

#print houston_council 
