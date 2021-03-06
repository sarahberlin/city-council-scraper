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

root_url = 'http://www.houstontx.gov'
index_url = root_url + '/council'

#get page urls of all the councilors
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        return [a.attrs.get('href') for a in soup.select('div a[href^=http://www.houstontx.gov/council/]')][:16]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url + page_url)
    else:
        councilor_data = {}
        response = requests.get(page_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        councilor_data['website'] = page_url
        councilor_data['address'] = "City Hall Annex 900 Bagby, First Floor Houston, TX 77002"
        councilor_data['phone'] = "832.393.1100"
        councilor_data['email'] = [a.attrs.get('href') for a in soup.select('p a[href^=mailto]')][0].replace('mailto:','')
        councilor_data['office.name'] = "City Council Member " + soup.select('h2.deptTitle')[0].get_text().encode('utf-8')
        councilor_data['official.name'] = soup.select('h3.pageTitle')[0].get_text().encode('utf-8').replace('Council Member ', '').replace('---','').replace('Mayor Pro Tem ','')
        if "At-Large" in councilor_data['office.name']:
            councilor_data['electoral.district'] = 'Houston'
        else:
            councilor_data['electoral.district'] = "Houston " +councilor_data['office.name'].replace('Member ', "")
        return councilor_data 


#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 


#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.houstontx.gov/mayor/'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('h3')[0].get_text().encode('utf-8').replace(', Mayor', '')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Houston"
        mayorDict['address'] = 'City of Houston P.O. Box 1562 Houston, TX 77251'
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = '713.837.0311'
        mayorDict['email'] = 'mayor@houstontx.gov'
        dictList.append(mayorDict)
        return dictList 

mayor_page()

def controller_scrape():
    controller_url = 'http://www.houstontx.gov/controller/index.html'
    soup = bs4.BeautifulSoup((requests.get(controller_url)).text, 'lxml')
    controllerDict = {}
    controllerDict['official.name'] = soup.select('p.content11black')[1].get_text().encode('utf-8').replace('- Houston City Controller ','')
    controllerDict['office.name'] = "Controller"
    controllerDict['electoral.district'] = "Houston"
    controllerDict['website'] = controller_url
    dictList.append(controllerDict)
    return dictList

controller_scrape()

#adds states
for dictionary in dictList:
    dictionary['state'] = 'TX'
    dictionary['body represents - muni'] = 'Houston'
    if "At-Large" in dictionary['office.name']:
        dictionary['office.name'] = dictionary['office.name'].replace('At-Large Position','At Large').strip()
    if "District" in dictionary['electoral.district']:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(dictionary['state'].lower(), dictionary['body represents - muni'].lower().replace(' ','_')) + dictionary['electoral.district'][-2:].lower().strip()
    else:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(dictionary['state'].lower(),dictionary['body represents - muni'].lower())  



#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
houston_council_file = open('houston_council.csv','wb')
csvwriter = csv.DictWriter(houston_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)
houston_council_file.close()
 
with open("houston_council.csv", "r") as houston_council_csv:
     houston_council = houston_council_csv.read()

#print houston_council 
