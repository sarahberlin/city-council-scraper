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


root_url = 'http://www.sandiego.gov'
index_url = root_url + '/citycouncil'
dictList = []

#scrapes council main page   
def scrape_table():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text)
        for x in range(0,9):
            councilor_data = {}
            try:
                councilor_data['electoral.district'] = 'San Diego City Council '+soup.select('div.cdinfo')[x].get_text().replace('District 2 ','District 2 \r\n\t\t').replace('District 8 ','District 8 \r\n\t\t').replace('\r\n\t\r\n\t','\r\n\t').replace('\r\n\t', ',').replace('\t   ', '').replace('\t', '').replace('\r\n                ',',').replace("Email: ", "").replace('\n', '').encode('utf-8').split(',')[0]
                councilor_data['office.name'] = 'City Councilmember '+soup.select('div.cdinfo')[x].get_text().replace('District 2 ','District 2 \r\n\t\t').replace('District 8 ','District 8 \r\n\t\t').replace('\r\n\t\r\n\t','\r\n\t').replace('\r\n\t', ',').replace('\t   ', '').replace('\t', '').replace('\r\n                ',',').replace("Email: ", "").replace('\n', '').encode('utf-8').split(',')[0]
                councilor_data['official.name'] = soup.select('div.cdinfo')[x].get_text().replace('District 2 ','District 2 \r\n\t\t').replace('District 8 ','District 8 \r\n\t\t').replace('\r\n\t\r\n\t','\r\n\t').replace('\r\n\t', ',').replace('\t   ', '').replace('\t', '').replace('\r\n                ',',').replace("Email: ", "").replace('\n', '').encode('utf-8').split(',')[1].replace('Councilmember ','').replace('Council President Pro Tem ','').replace('Council President ','')
                councilor_data['email'] = soup.select('div.cdinfo')[x].get_text().replace('District 2 ','District 2 \r\n\t\t').replace('District 8 ','District 8 \r\n\t\t').replace('\r\n\t\r\n\t','\r\n\t').replace('\r\n\t', ',').replace('\t   ', '').replace('\t', '').replace('\r\n                ',',').replace("Email: ", "").replace('\n', '').encode('utf-8').split(',')[2]
                councilor_data['website'] = index_url + "/cd{0}".format(x+1)
                councilor_data['address'] = 'City Administration Building, 202 C Street, San Diego, CA 92101.'
                councilor_data['phone'] = '619-236-5555'
            except:
                pass
            dictList.append(councilor_data)    

scrape_table()

#adds state
for dictionary in dictList:
    dictionary['state'] = 'CA'


#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.sandiego.gov/mayor/'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text)
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('div h2')[0].get_text().encode('utf-8')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "San Diego"
        mayorDict['address'] = "City Administration Building 202 C Street, 11th Floor San Diego, CA 92101"
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = '(619) 236-6330'
        mayorDict['state'] = "CA"
        mayorDict['email'] = 'kevinfaulconer@sandiego.gov'
        dictList.append(mayorDict)
        return dictList

mayor_page()



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
