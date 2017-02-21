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


root_url = 'http://charlottenc.gov'
index_url = '/CityCouncil/bios/Pages/default.aspx'


#get page urls of all the councilors
def get_page_urls():
    if checkURL(root_url + index_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url + index_url)
    else:
        response = requests.get(root_url + index_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        return [a.attrs.get('href') for a in soup.select('td.ms-stylebody a[href^=/CityCouncil/bios/Pages]')]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(root_url+page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url+page_url)
    else:
        councilor_data = {}
        response = requests.get(root_url+page_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        try:
            if soup.select('span strong') != []:
                base_text = soup.select('span strong')[0].get_text().encode('utf-8')
            else:
                base_text = soup.select('span.ms-rteStyle-CharcoalHeading')[0].get_text().encode('utf-8')
            councilor_data['official.name'] = base_text.split(",")[0].replace("\xe2\x80\x8ba","a")
            councilor_data['office.name'] = "City Council "+ base_text.split(",")[1].strip()
            councilor_data['email'] = soup.select('a[href^=mailto]')[0].get_text().encode('utf-8').replace(' \n', '')
            councilor_data['website'] = (root_url+page_url)
            councilor_data['address'] = '600 E. 4th Street Charlotte, NC 28202'
            councilor_data['state'] = 'NC'
            councilor_data['Body Name'] = 'Charlotte Council'
            councilor_data['phone'] ='704-336-2241'
            if 'at-large' in base_text.split(",")[1].strip():
                councilor_data['electoral.district'] = "Charlotte"
            elif "district" in base_text.split(",")[1].strip() or "District" in base_text.split(",")[1].strip():
                councilor_data['electoral.district'] = "Charlotte City Council "+base_text.split(",")[1].strip().replace(' Representative','').replace(' representative','').strip().replace('district', "District")
            else:
                councilor_data['electoral.district'] = "Charlotte"
        except:
            pass    
        return councilor_data

#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

for x in dictList:
    if x == []:
        dictList.pop(dictList.index(pop))

#scrape mayor page
def mayor_page():
    mayor_url = 'http://charlottenc.gov/mayor/Pages/MeetTheMayor.aspx'  
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('h3')[1].get_text().encode('utf-8').replace('Mayor ', '')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Charlotte"
        mayorDict['address'] =  '600 East Fourth Street, 15th Floor Charlotte, NC 28202' 
        mayorDict['email'] = 'mayor@charlottenc.gov'
        mayorDict['phone'] = '704-336-2241'
        mayorDict['website'] = mayor_url 
        mayorDict['state'] = "NC"
        mayorDict['Body Name'] = 'Charlotte Elected Officials'
        dictList.append(mayorDict)
        return dictList 

mayor_page()

for dictionary in dictList:
    dictionary['body represents - muni'] = 'Charlotte'
    if "District" in dictionary['electoral.district'] or 'district' in dictionary['electoral.district']:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(dictionary['state'].lower(), dictionary['body represents - muni'].lower()) + dictionary['electoral.district'][-1]
    else:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(dictionary['state'].lower(),dictionary['body represents - muni'].lower())   


#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
charlotte_council_file = open('charlotte_council.csv','wb')
csvwriter = csv.DictWriter(charlotte_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

charlotte_council_file.close()
 
with open("charlotte_council.csv", "r") as charlotte_council_csv:
     charlotte_council = charlotte_council_csv.read()

#print charlotte_council 
