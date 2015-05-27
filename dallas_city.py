import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://dallascityhall.com'
index_url = root_url + '/government/Pages/city-council.aspx'

#get page urls of all the councilors
def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)    
    return [a.attrs.get('href') for a in soup.select('a[href^=/government/citycouncil/district]')][:14]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:        
        if page_url == '/government/citycouncil/district6/':
            councilor_data['electoral.district'] = "Dallas "+soup.select('h1 span')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '')
            councilor_data['official.name'] = soup.select('h1 span')[0].get_text().encode('utf-8').replace('\xe2\x80\x8b\xc2\xa0', '').replace('Deputy Mayor Pro Tem','')
            councilor_data['website'] =  root_url + page_url
            councilor_data['office.name'] = soup.select('h1 span')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '')
            councilor_data['address'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[0]
            councilor_data['phone'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[1]
        elif page_url == '/government/citycouncil/district14/':
            councilor_data['electoral.district'] = "Dallas "+soup.select('div h1')[3].get_text().encode('utf-8')
            councilor_data['official.name'] =soup.select('div h1')[2].get_text().encode('utf-8').replace('Council Member ', '')
            councilor_data['office.name'] = soup.select('div h1')[3].get_text().encode('utf-8')
            councilor_data['website'] =  root_url + page_url
            councilor_data['address'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[0]
            councilor_data['phone'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[1]
        else:
            councilor_data['address'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[0]
            councilor_data['electoral.district'] = "Dallas "+ soup.select('h1 p')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '')
            councilor_data['office.name'] = soup.select('h1 p')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '')
            councilor_data['official.name'] = soup.select('h1 p')[0].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('\xc2\xa0', '').replace('City Council Member ', '').replace('Council Member ', '')
            councilor_data['website'] =  root_url + page_url
            councilor_data['phone'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[1]
            councilor_data['email'] = soup.select('a[href^=mailto]')[0].get_text().encode('utf-8')     
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
dallas_council_file = open('dallas_council.csv','wb')
csvwriter = csv.DictWriter(dallas_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

dallas_council_file.close()
 
with open("dallas_council.csv", "r") as dallas_council_csv:
     dallas_council = dallas_council_csv.read()

#print dallas_council 

