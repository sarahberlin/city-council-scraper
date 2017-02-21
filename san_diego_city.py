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
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    for x in range(0,9):
        councilor_data = {}
        row = soup.select('div.l-margin-bm')[x]
        try:
            councilor_data['electoral.district'] = 'San Diego City Council '+ row.get_text().encode('utf-8').replace('\xc2\xa0','').replace('\xc3\xb3','o').strip().split('\n')[0]
            councilor_data['office.name'] = 'City Councilmember '+row.get_text().encode('utf-8').replace('\xc2\xa0','').replace('\xc3\xb3','o').strip().split('\n')[0]
            councilor_data['website'] = index_url + "/cd{0}".format(councilor_data['electoral.district'][-2].strip())
            councilor_data['address'] = 'City Administration Building, 202 C Street, San Diego, CA 92101.'
            councilor_data['phone'] = '619-236-5555'
            if "@" in row.get_text().encode('utf-8').replace('Council President', 'Council').replace('\xc2\xa0','').replace('\xc3\xb3','o').strip().split('\n')[1].split(' ')[-1]:
                first_name = row.get_text().encode('utf-8').replace('Council President', 'Council').replace('\xc2\xa0','').replace('\xc3\xb3','o').strip().split('\n')[1].split(' ')[1]
                last_and_email = row.get_text().encode('utf-8').replace('Council President', 'Council').replace('\xc2\xa0','').replace('\xc3\xb3','o').strip().split('\n')[1].split(' ')[2]
                repeat_index = last_and_email.lower().find(first_name.lower())
                councilor_data['official.name'] =first_name + " " +last_and_email[:repeat_index]
                #print councilor_data['official.name']
            else:
                councilor_data['official.name'] = row.get_text().encode('utf-8').replace('\xc2\xa0','').replace('\xc3\xb3','o').strip().split('\n')[1].replace('Councilmember ','').replace('Council President Pro Tem','')
            #print councilor_data['official.name']
        except:
            pass
        dictList.append(councilor_data)    

scrape_table()


#scrape mayor page
def mayor_page():
    mayor_url = 'http://www.sandiego.gov/mayor/'
    #if checkURL(mayor_url) == 404:
    #    print '404 error. Check the url for {0}'.format(mayor_url)
    #else:
    mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
    mayorDict = {}
    mayorDict['official.name'] = mayor_soup.select('h1')[0].get_text().encode('utf-8').replace('Mayor','')
    mayorDict['office.name'] = "Mayor"
    mayorDict['electoral.district'] = "San Diego"
    mayorDict['address'] = "City Administration Building 202 C Street, 11th Floor San Diego, CA 92101"
    mayorDict['website'] = mayor_url
    mayorDict['phone'] = '(619) 236-6330'
    mayorDict['email'] = 'kevinfaulconer@sandiego.gov'
    dictList.append(mayorDict)
    return dictList

mayor_page()

#adds other info
for dictionary in dictList:
    dictionary['state'] = 'CA'
    dictionary['body represents - muni'] = 'San Diego'
    if "District" in dictionary['electoral.district']:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(dictionary['state'].lower(), dictionary['body represents - muni'].lower().replace(' ','_')) + dictionary['electoral.district'][-2:].lower().strip()
    else:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(dictionary['state'].lower(),dictionary['body represents - muni'].lower().replace(' ','_')) 

#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
san_diego_council_file = open('san_diego_council.csv','wb')
csvwriter = csv.DictWriter(san_diego_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

san_diego_council_file.close()
 
with open("san_diego_council.csv", "r") as san_diego_council_csv:
     san_diego_council = san_diego_council_csv.read()

#print san_diego_council 
