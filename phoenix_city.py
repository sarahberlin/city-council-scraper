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

dictList = []

root_url = 'https://www.phoenix.gov'
index_url = root_url + '/mayorcouncil'
response = requests.get(index_url)
soup = bs4.BeautifulSoup(response.text, 'lxml')
def council_scrape():
    for row in soup.select('td.cop-rteTableOddCol-COPTABLE'):
        councilor_data = {}
        councilor_data['state'] = 'AZ'
        councilor_data['body represents - muni'] = 'Phoenix'
        linkp = row.select('p')[1]
        if ":" in row.select('p')[0].get_text().encode('utf-8'):
            councilor_data['electoral.district'] = "Phoenix City Council " + row.select('p')[0].get_text().encode('utf-8').split(':')[0].strip()
            councilor_data['office.name'] = 'City Council ' + row.select('p')[0].get_text().encode('utf-8').split(':')[0].strip()
            councilor_data['official.name'] = row.select('p')[0].get_text().encode('utf-8').split(':')[1].replace('Councilwoman','').replace('Councilman','').replace('Vice Mayor','').strip()
            councilor_data['website']= root_url + [a.attrs.get('href') for a in linkp.select('a[href^=/district]')][0]
            councilor_data['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(councilor_data['state'].lower(), councilor_data['body represents - muni'].lower().replace(' ','_')) + councilor_data['electoral.district'][-2:].lower().strip()
        else:
            councilor_data['electoral.district'] = "Phoenix"
            councilor_data['office.name'] = "Mayor"
            councilor_data['official.name'] = row.select('p')[0].get_text().encode('utf-8').split('Mayor')[1].strip()
            councilor_data['website']= root_url + [a.attrs.get('href') for a in linkp.select('a[href]')][0]
            councilor_data['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(councilor_data['state'].lower(),councilor_data['body represents - muni'].lower())
        dictList.append(councilor_data)

council_scrape()

#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]

phoenix_council_file = open('phoenix_council.csv','wb')
csvwriter = csv.DictWriter(phoenix_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

phoenix_council_file.close()

with open("phoenix_council.csv", "r") as phoenix_council_csv:
     phoenix_council = phoenix_council_csv.read()
