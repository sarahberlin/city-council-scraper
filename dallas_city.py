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

root_url = 'http://dallascityhall.com'
index_url = root_url + '/government/Pages/city-council.aspx'

#get page urls of all the councilors
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')    
        return [a.attrs.get('href') for a in soup.select('a[href^=/government/citycouncil/district]')][:14]


#get data from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(root_url + page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url + page_url)
    else:
        councilor_data = {}
        response = requests.get(root_url+page_url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        try:        
            if page_url == '/government/citycouncil/district6/':
                councilor_data['electoral.district'] = "Dallas "+soup.select('h1 span')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('\n', " ")
                councilor_data['official.name'] = soup.select('h1 span')[0].get_text().encode('utf-8').replace('\xe2\x80\x8b\xc2\xa0', '').replace('\xe2\x80\x8b', '').replace('Mayor Pro Tem', '').replace('Deputy Mayor Pro Tem ','').replace('\n', " ").strip()
                councilor_data['website'] =  root_url + page_url
                councilor_data['office.name'] = soup.select('h1 span')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('\n', " ")
                councilor_data['address'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[0]
                councilor_data['phone'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[1]
                councilor_data['Body Name'] = 'Dallas Council'
            elif page_url == '/government/citycouncil/district14/':
                councilor_data['electoral.district'] = "Dallas City Council "+soup.select('div h1')[0].get_text().encode('utf-8').replace('\n', " ")
                councilor_data['official.name'] =soup.select('h1 span')[0].get_text().encode('utf-8').replace('Council Member ', '').replace('Deputy Mayor Pro Tem ','').replace('\n', " ").strip()
                councilor_data['office.name'] = "City Council "+soup.select('div h1')[0].get_text().encode('utf-8').replace('\n', " ")
                councilor_data['website'] =  root_url + page_url
                councilor_data['address'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[0]
                councilor_data['phone'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[1]
                councilor_data['Body Name'] = 'Dallas Council'
            else:
                councilor_data['address'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[0]
                councilor_data['electoral.district'] = "Dallas "+ soup.select('h1 p')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('\xc2\xa0', '').replace('\n', " ")
                councilor_data['office.name'] = soup.select('h1 p')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('\xc2\xa0', '').replace('\n', " ")
                councilor_data['official.name'] = soup.select('h1 p')[0].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('\xc2\xa0', '').replace('City Council Member ', '').replace('Council Member ', '').replace('Deputy Mayor Pro Tem ','').replace('\n', " ").strip()
                councilor_data['website'] =  root_url + page_url
                councilor_data['phone'] = soup.select('li.deptAddress')[0].get_text().encode('utf-8').replace('Dallas', ' Dallas').replace(' Dallas City', 'Dallas City').replace('Hall', 'Hall ').replace("Phone: ", "*").replace(" Fax: ", "*").split("*")[1]
                councilor_data['email'] = soup.select('a[href^=mailto]')[0].get_text().encode('utf-8')
                councilor_data['Body Name'] = 'Dallas Council'
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
    mayor_url = 'http://dallascityhall.com/government/citymayor/Pages/default.aspx'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').replace('City of Dallas ', '')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "Dallas"
        mayorDict['address'] = "1500 Marilla St. Dallas, TX 75201"
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = '214-670-3111'
        mayorDict['Body Name'] = 'Dallas Elected Officials'
        dictList.append(mayorDict)
        return dictList 

mayor_page()


#adds states
for dictionary in dictList:
    dictionary['state'] = 'TX'
    dictionary['body represents - muni'] = 'Dallas'
    if "District" in dictionary['electoral.district']:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(dictionary['state'].lower(), dictionary['body represents - muni'].lower()) + dictionary['electoral.district'][-2:].strip()
    else:
        dictionary['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(dictionary['state'].lower(),dictionary['body represents - muni'].lower())  


#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
dallas_council_file = open('dallas_council.csv','wb')
csvwriter = csv.DictWriter(dallas_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

dallas_council_file.close()
 
with open("dallas_council.csv", "r") as dallas_council_csv:
     dallas_council = dallas_council_csv.read()

#print dallas_council 

