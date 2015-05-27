import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://www.sandiego.gov'
index_url = root_url + '/citycouncil'


page_urls = []
for x in range (1, 10):
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)
    page_url = "/cd{0}".format(x)
    page_urls.append(page_url)

dictList = []
   
for x in range(0,9):
    councilor_data = {}
    try:
        councilor_data['electoral.district'] = 'San Diego City Council '+soup.select('div.cdinfo')[x].get_text().replace('District 2 ','District 2 \r\n\t\t').replace('District 8 ','District 8 \r\n\t\t').replace('\r\n\t\r\n\t','\r\n\t').replace('\r\n\t', ',').replace('\t   ', '').replace('\t', '').replace('\r\n                ',',').replace("Email: ", "").replace('\n', '').encode('utf-8').split(',')[0]
        councilor_data['office.name'] = 'City Councilmember '+soup.select('div.cdinfo')[x].get_text().replace('District 2 ','District 2 \r\n\t\t').replace('District 8 ','District 8 \r\n\t\t').replace('\r\n\t\r\n\t','\r\n\t').replace('\r\n\t', ',').replace('\t   ', '').replace('\t', '').replace('\r\n                ',',').replace("Email: ", "").replace('\n', '').encode('utf-8').split(',')[0]
        councilor_data['official.name'] = soup.select('div.cdinfo')[x].get_text().replace('District 2 ','District 2 \r\n\t\t').replace('District 8 ','District 8 \r\n\t\t').replace('\r\n\t\r\n\t','\r\n\t').replace('\r\n\t', ',').replace('\t   ', '').replace('\t', '').replace('\r\n                ',',').replace("Email: ", "").replace('\n', '').encode('utf-8').split(',')[1].replace('Councilmember ','').replace('Council President Pro Tem ','').replace('Council President ','')
        councilor_data['email'] = soup.select('div.cdinfo')[x].get_text().replace('District 2 ','District 2 \r\n\t\t').replace('District 8 ','District 8 \r\n\t\t').replace('\r\n\t\r\n\t','\r\n\t').replace('\r\n\t', ',').replace('\t   ', '').replace('\t', '').replace('\r\n                ',',').replace("Email: ", "").replace('\n', '').encode('utf-8').split(',')[2]
        councilor_data['website'] = index_url + page_urls[x]
        councilor_data['address'] = 'City Administration Building, 202 C Street, San Diego, CA 92101.'
        councilor_data['phone'] = '619-236-5555'
    except:
        pass
    dictList.append(councilor_data)         


for dictionary in dictList:
    dictionary['state'] = 'CA'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
san_diego_council_file = open('san_diego_council.csv','wb')
csvwriter = csv.DictWriter(san_diego_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

san_diego_council_file.close()
 
with open("san_diego_council.csv", "r") as san_diego_council_csv:
     san_diego_council = san_diego_council_csv.read()

#print san_diego_council 
