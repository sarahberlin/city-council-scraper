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


root_url = 'http://phlcouncil.com/council-members/'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)
dictList = []


def get_councilor_data():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        for x in range (0, 17):
    		newDict = {}
    		newDict['official.name']=  soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n','').replace('Johnson\n', 'Johnson').replace('\n\n','').replace('\xc2\xa0','').replace('\nMaria', 'Maria').replace("\xe2\x80\x99", "'").replace('\n\xc2\xa0\n', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').replace('\nVacant\n\n','Vacant').split('\n')[0].strip()
    		newDict['website']= root_url
    		if x == 16:
    			newDict['office.name']= 'City Council Member '+'At-Large'
    			newDict['electoral.district'] = 'Philadelphia'
    		elif 10 >  x >=  0:
    			newDict['office.name']="City Council Member "+ soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n','').replace('Johnson\n', 'Johnson').replace('\n\n','').replace('\nMaria', 'Maria').replace("\xe2\x80\x99", "'").replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n')[1]
    			newDict['electoral.district'] = 'Philadelphia City Council ' + soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n','').replace('Johnson\n', 'Johnson').replace('\n\n','').replace('\nMaria', 'Maria').replace("\xe2\x80\x99", "'").replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n')[1]
    			newDict['address'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n','').replace('Johnson\n', 'Johnson').replace('\n\n','').replace('\nMaria', 'Maria').replace("\xe2\x80\x99", "'").replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n')[2]+ ' ' + soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n','').replace('Johnson\n', 'Johnson').replace('\n\n','').replace('\nMaria', 'Maria').replace("\xe2\x80\x99", "'").replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n')[3]
    			newDict['phone'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n','').replace('Johnson\n', 'Johnson').replace('\n\n','').replace('\nMaria', 'Maria').replace("\xe2\x80\x99", "'").replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n')[4].split(',')[0]
    		else:
    			newDict['office.name']= "City Council Member At-Large"
    			newDict['electoral.district'] = 'Philadelphia'
    			newDict['address'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n','').replace('Johnson\n', 'Johnson').replace('\n\n','').replace('\nMaria', 'Maria').replace("\xe2\x80\x99", "'").replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n')[1]+ ' '+soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n','').replace('Johnson\n', 'Johnson').replace('\n\n','').replace('\nMaria', 'Maria').replace("\xe2\x80\x99", "'").replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n')[2]
    			newDict['phone'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n','').replace('Johnson\n', 'Johnson').replace('\n\n','').replace('\nMaria', 'Maria').replace("\xe2\x80\x99", "'").replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n')[3].split(',')[0]
                if newDict['official.name']== 'Vacant':
                    newDict['address'] = ''
    		dictList.append(newDict)


get_councilor_data()

#adds state
for dictionary in dictList:
    dictionary['state'] = 'PA'

#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.phila.gov/Pages/default.aspx'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text)
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('title')[0].get_text().encode('utf-8').replace('\r\n\t','').replace('\r\n', '').split(':')[1].strip()
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Philadelphia"
        mayorDict['address'] = 'Office of the Mayor Room 215 City Hall Philadelphia, PA 19107'
        mayorDict['website'] = 'http://www.phila.gov/mayor/index.html'
        mayorDict['phone'] = '(215) 686-2181'
        mayorDict['state'] = "PA"
        mayorDict['email'] = 'michael.nutter@phila.gov'
        dictList.append(mayorDict)
        return dictList 

mayor_page()



#make csv
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
