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


root_url = 'http://www.memphistn.gov'
index_url = root_url + '/Government/CityCouncil/CouncilMembers.aspx'
soup = bs4.BeautifulSoup(requests.get(index_url).text, 'lxml')

dictList = []

def council_scrape():
    for x in range(0,13):
        cData = {}
        cData['office.name'] = 'City Council Member ' + [a.attrs.get('href') for a in soup.select('tr td a[href^=/Government/CityCouncil/]')][x].replace('/Government/CityCouncil/', '').replace('.aspx','').replace('District', 'District ').replace('/Position',' Position ').replace('Super', 'Super ')
        cData['official.name'] = [img.attrs.get('alt') for img in soup.select('tr td img[alt]')][x]
        cData['website'] = root_url + [a.attrs.get('href') for a in soup.select('tr td a[href^=/Government/CityCouncil/]')][x]
        cData['body represents - muni'] = 'Memphis'
        cData['state'] = 'TN'
        cData['electoral.district'] = 'Memphis City Council District '+ [a.attrs.get('href') for a in soup.select('tr td a[href^=/Government/CityCouncil/]')][x].replace('/Government/CityCouncil/', '').replace('.aspx','').replace('District', 'District ').replace('/Position',' Position ').replace('Super', '').split(' ')[1]
        cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(cData['state'].lower(), cData['body represents - muni'].lower().replace(' ','_')) + cData['electoral.district'][-2:].lower().strip().replace(' ', '_')
        dictList.append(cData)


council_scrape()

#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.memphistn.gov/Government/ExecutiveDivision/MayorsOffice.aspx'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select("div#dnn_ctr738_HtmlModule_lblContent strong")[0].get_text().encode('utf-8').replace('Mayor ','')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Memphis"
        mayorDict['state'] = "TN"
        mayorDict['website'] = mayor_url
        mayorDict['body represents - muni'] = 'Memphis'
        mayorDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(mayorDict['state'].lower(),mayorDict['body represents - muni'].lower().replace(' ','_'))  
        dictList.append(mayorDict)

mayor_page()


#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
memphis_city_council_file = open('memphis_city_council.csv','wb')
csvwriter = csv.DictWriter(memphis_city_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)










