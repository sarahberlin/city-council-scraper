import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://columbus.gov/council/members/'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)
dictList = []

def get_councilor_data():
	for x in range(1,9):
		newDict = {}
		try:
			newDict['official.name'] = soup.find('div', {'id': 'inner-right-single'}).select('div p')[x].get_text().encode('utf-8').replace('\xc2\xa0', '').replace('Chair', '').replace(', Council President', '').replace(', President Pro-Tem', '').split(':')[0]
			newDict['office.name'] = 'City Council Member '+'At-Large'
			newDict['electoral.district'] = 'Columbus'
			newDict['email'] = soup.find('div', {'id': 'inner-right-single'}).select('div p')[x].get_text().encode('utf-8').replace('\xc2\xa0', '').replace('Chair', '').replace(', Council President', '').replace(', President Pro-Tem', '').split(':')[3].replace('Legislative Assistant', '').replace('Legislative Aide', '').split('(')[0].replace(') ', ' ').strip()
			newDict['phone']= soup.find('div', {'id': 'inner-right-single'}).select('div p')[x].get_text().encode('utf-8').replace('\xc2\xa0', '').replace('Chair', '').replace(', Council President', '').replace(', President Pro-Tem', '').split(':')[3].replace('Legislative Assistant', '').replace('Legislative Aide', '').split('(')[1].replace(') ', ' ').strip()
			newDict['address'] = '90 West Broad St. Columbus, OH 43215'
			newDict['website'] = root_url
			dictList.append(newDict)
			return dictList
		except:
			pass

get_councilor_data()


for dictionary in dictList:
    dictionary['state'] = 'OH'

fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
columbus_council_file = open('columbus_council.csv','wb')
csvwriter = csv.DictWriter(columbus_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

columbus_council_file.close()
 
with open("columbus_council.csv", "r") as columbus_council_csv:
     columbus_council = columbus_council_csv.read()

#print columbus_council		
