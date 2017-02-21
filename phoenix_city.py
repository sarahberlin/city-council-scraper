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


root_url = 'https://www.phoenix.gov'
index_url = root_url + '/mayorcouncil'

#get page urls of all the councilors
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')    
        urls = []
        for x in [a.attrs.get('href') for a in soup.select('a[href^=/district]')]:
            if len(x) == 10:
                urls.append(x)
        urls = set(urls)
        return urls


#get data from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(root_url + page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url + page_url)
    else:
        councilor_data = {}
        response = requests.get(root_url+page_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        try:
            councilor_data['address'] = "200 W. Washington St., 11th Floor Phoenix, AZ 85003"
            councilor_data['website'] = (root_url+page_url)
            councilor_data['phone'] = '602-262-6011'     
            councilor_data['email'] = root_url + '/district{0}/contact-district-{0}'.format(page_url[-1])
            if page_url != '/district6' and page_url != '/district3':
                councilor_data['office.name'] = 'City ' + soup.select('h3.title')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('\xc2\xa0', '').replace('Vice', 'Council').strip().split(' ')[0] + " " + soup.select('h3.title')[0].get_text().encode('utf-8').replace('\r\n','').replace('Vice', 'Council').strip()
                councilor_data['official.name'] = soup.select('h3.title')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('\xc2\xa0', '').replace('Councilman ','').replace('Councilwoman ','').replace('Vice Mayor','').strip()
                councilor_data['electoral.district'] = "Phoenix City Council " + soup.select('h3.title')[0].get_text().encode('utf-8').replace('\r\n','').strip()
            else:
                councilor_data['electoral.district'] = "Phoenix City Council "+ soup.select('span#ctl00_breadcrumbNav_spnCurrentTerm')[0].get_text().encode('utf-8')
                councilor_data['official.name'] = soup.select('h3.title')[0].get_text().encode('utf-8').replace('Councilman ','').replace('Councilwoman ','').replace('Vice Mayor ','').replace("\xe2\x80\x8b", "").strip()
                councilor_data['office.name'] =  "City " + soup.select('h3.title')[0].get_text().encode('utf-8').split(' ')[0]+ " " +soup.select('span#ctl00_breadcrumbNav_spnCurrentTerm')[0].get_text().encode('utf-8')
        except:
            pass
        return councilor_data 

#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 




#scrape mayor page
def mayor_page():
    mayor_url = 'https://www.phoenix.gov/mayor'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('title')[0].get_text().encode('utf-8').replace('\r\n\t','').replace('\r\n', '').replace('Office of ', '').replace('Mayor ','')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Phoenix"
        mayorDict['address'] = "200 W. Washington St., 11th Floor Phoenix, AZ 85003"
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = '602-262-6011'   
        mayorDict['state'] = "AZ"
        dictList.append(mayorDict)
        return dictList

mayor_page()


#adds other info
for dictionary in dictList:
    dictionary['state'] = 'AZ'
    dictionary['body represents - muni'] = 'Phoenix'
    if "District" in dictionary['electoral.district']:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(dictionary['state'].lower(), dictionary['body represents - muni'].lower().replace(' ','_')) + dictionary['electoral.district'][-2:].lower().strip()
    else:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(dictionary['state'].lower(),dictionary['body represents - muni'].lower())  



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

#print phoenix_council 
