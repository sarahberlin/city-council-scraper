import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://phlcouncil.com/council-members/'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)
dictList = []

def get_councilor_data():
	for x in range(0,17):
		newDict = {}
		try:
			if 4 < x < 7:
				newDict['official.name']=(soup.select('div.one_half')[x].get_text().encode('utf-8').replace("\xe2\x80\x99", "'").replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n'))[1]
				newDict['office.name']="City Council Member "+(soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[2]
				str = ' '
				seq = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[3], soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[4]
				newDict['address'] = str.join(seq)
				newDict['phone'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[5].split(', ')[0]
				newDict['website'] = 'http://phlcouncil.com/council-members/'
				newDict['electoral.district'] = 'Philadelphia City Council ' + (soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[2]
			elif x < 10 and x != 3 and x != 5 and x != 6:
				newDict['official.name']=(soup.select('div.one_half')[x].get_text().encode('utf-8').replace("\xe2\x80\x99", "'").replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[0]
				newDict['office.name']="City Council Member "+(soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[1]
				str = ' '
				seq = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[2], soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[3]
				newDict['address'] = str.join(seq)
				newDict['phone'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[4].split(', ')[0]
				newDict['website'] = 'http://phlcouncil.com/council-members/'
				newDict['electoral.district'] = 'Philadelphia City Council ' + (soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[1]
			elif x == 3:
				newDict['official.name'] = soup.select('div.one_half span')[1].get_text().encode('utf-8')
				newDict['office.name'] = 'City Council Member '+'District 4'
				newDict['website'] = 'http://phlcouncil.com/council-members/'
				newDict['electoral.district'] = "Philadelphia City Council District 4"
			elif  16 > x >9 :
				newDict['official.name']=(soup.select('div.one_half')[x].get_text().encode('utf-8').replace("\xe2\x80\x99", "'").replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[0]
				newDict['office.name']= 'City Council Member '+'At-Large'
				str = ' '
				seq = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '').replace('\xc2\xa0', '').split('\n')[1], soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '').replace('\xc2\xa0', '').split('\n')[2]
				newDict['address'] = str.join(seq)
				newDict['phone'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[3].split(', ')[0]
				newDict['website'] = 'http://phlcouncil.com/council-members/'
				newDict['electoral.district'] = 'Philadelphia'
			else:
				newDict['official.name'] = "Vacant"
				newDict['office.name']= 'City Council Member '+'At-Large'
				newDict['electoral.district'] = 'Philadelphia'
		except:
			pass	
		dictList.append(newDict)
		return dictList

get_councilor_data()

for dictionary in dictList:
    dictionary['state'] = 'PA'


fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'party']
philadelphia_council_file = open('philadelphia_council.csv','wb')
csvwriter = csv.DictWriter(philadelphia_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

philadelphia_council_file.close()
 
with open("philadelphia_council.csv", "r") as philadelphia_council_csv:
     philadelphia_council = philadelphia_council_csv.read()

#print philadelphia_council
