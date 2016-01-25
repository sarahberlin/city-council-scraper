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

dictList = []
page_urls = []

def get_page_urls():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        response = requests.get(root_url)
        soup = bs4.BeautifulSoup(response.text)
        for page in [a.attrs.get('href') for a in soup.select('li#menu-item-655 ul li a[href^=http://phlcouncil.com/]')]:
            page_urls.append(page)
        for page in [a.attrs.get('href') for a in soup.select('li#menu-item-656 ul li a[href^=http://phlcouncil.com/]')]:
            page_urls.append(page)
        return page_urls


def get_councilor_data(page_url):
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        councilor_data = {}
        response = requests.get(page_url)
        soup = bs4.BeautifulSoup(response.text)
        try:
            if 'At-Large' not in soup.select('title')[0].get_text().encode('utf-8'):
                councilor_data['official.name']= soup.select('title')[0].get_text().encode('utf-8').split('District')[0].replace("\xe2\x80\x99","'").replace('\xc3\xb1', 'n').replace('\xc3\xa1','a')
                councilor_data['office.name'] = "City Council Member District" + soup.select('title')[0].get_text().encode('utf-8').split('District')[1].split('|')[0]
                councilor_data['electoral.district'] = "Philadelphia City Council District"+ soup.select('title')[0].get_text().encode('utf-8').split('District')[1].split('|')[0]
            else:
                councilor_data['official.name']= soup.select('title')[0].get_text().encode('utf-8').split('|')[0].replace('Councilwoman At-Large','').replace('Councilman At-Large','').replace("\xe2\x80\x99","'").replace('\xc3\xb1', 'n').replace('\xc3\xa1','a')
                councilor_data['office.name'] = "City Council Member At-Large"
                councilor_data['electoral.district'] = "Philadelphia"
            councilor_data['address'] = soup.select('div.textwidget p strong')[0].get_text().encode('utf-8')+ " Philadelphia, PA 19107-3290"
            councilor_data['website'] = page_url
            councilor_data['state'] = 'PA'
            if "FAX" in soup.select('div.textwidget p')[0].get_text().encode('utf-8').split('\r\n')[3]:
                councilor_data['phone'] = soup.select('div.textwidget p')[0].get_text().encode('utf-8').split('\r\n')[2]
            else:
                councilor_data['phone'] = soup.select('div.textwidget p')[0].get_text().encode('utf-8').split('\r\n')[3]
        except:
            pass
    return councilor_data


#run the functions together
get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url))


#scrape mayor page
def mayor_page():
    mayor_url = 'https://alpha.phila.gov/departments/mayor/'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text)
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('p span.email a')[0].get_text().encode('utf-8').split('@')[0].replace('.', ' ')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Philadelphia"
        mayorDict['address'] = mayor_soup.select('p span.adr span')[0].get_text().encode('utf-8') + ' Philadelphia, PA 19107'
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = mayor_soup.select('p span.tel a')[0].get_text().encode('utf-8')
        mayorDict['state'] = "PA"
        mayorDict['email'] = mayor_soup.select('p span.email a')[0].get_text().encode('utf-8')
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
