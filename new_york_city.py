#!/usr/bin/python
# -*- coding: latin-1 -*-
import csv
from csv import DictWriter
import urllib, urllib2
import os

from selenium import webdriver
import lxml.html as lh

import requests
import bs4

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#empty list that all the dictionaries will be appended to
dictList = []

root_url = 'http://council.nyc.gov'
index_url = root_url + '/districts/'


page_urls = []
driver = webdriver.PhantomJS()
driver.get(index_url)
content = driver.page_source
doc = lh.fromstring(content)
driver.close()
try:
    os.system('taskkill /f /im phantomjs.exe')
except:
    pass
#for x in doc.xpath('//td/a/strong/text()'):
#	print x
for url in doc.xpath('//td/a/@href'):
    if url not in page_urls:
        page_urls.append(url)

def council_scrape(page_url):
    driver = webdriver.PhantomJS()
    driver.get(page_url)
    content = driver.page_source
    doc = lh.fromstring(content)
    cData = {}
    cData['official.name'] = doc.xpath('//h4/a/text()')[0].encode('utf-8')
    cData['website'] = page_url
    cData['office.name'] = 'Council Member '+ doc.xpath("//h1/a/text()")[0].encode('utf-8').replace('\xc2\xa0',' ')
    cData['electoral.district'] = 'New York City Council '+ doc.xpath("//h1/a/text()")[0].encode('utf-8').replace('\xc2\xa0',' ')
    cData['state'] = 'NY'
    cData['body represents - muni'] = 'New York'
    cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(cData['state'].lower(), cData['body represents - muni'].lower().replace(' ','_')) + cData['electoral.district'][-2:].lower().strip()
    driver.close()
    try:
        os.system('taskkill /f /im phantomjs.exe')
    except:
        pass
    return cData
	#print cData['electoral.district']

for page_url in page_urls:
	try:
		dictList.append(council_scrape(page_url))
	except:
		print page_url + " error"
        #cData = {}
        #cData['official.name'] = ''
        #cData['website'] = page_url
        #cData['office.name'] = 'Council Member District '+ page_url.replace('http://council.nyc.gov/district-','').replace('/','')
        #cData['electoral.district'] = 'New York City Council District '+ page_url.replace('http://council.nyc.gov/district-','').replace('/','')
        #cData['state'] = 'NY'
        #cData['body represents - muni'] = 'New York'
        #cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(cData['state'].lower(), cData['body represents - muni'].lower().replace(' ','_')) + cData['electoral.district'][-2:].lower().strip()
        #dictList.append(cData)
        pass


#scrape mayor page
def mayor_page():
    mayor_url = 'http://www1.nyc.gov/office-of-the-mayor/index.page'
    if checkURL(mayor_url) == 404:
        print '404 error. Check the url for {0}'.format(mayor_url)
    else:
        mayor_soup = bs4.BeautifulSoup((requests.get(mayor_url)).text, 'lxml')
        mayorDict = {}
        mayorDict['official.name'] = mayor_soup.select('h3')[0].get_text().encode('utf-8')
        mayorDict['office.name'] = "Mayor"
        mayorDict['electoral.district'] = "New York City"
        mayorDict['address'] = 'City Hall New York, NY 10007'
        mayorDict['website'] = mayor_url
        mayorDict['phone'] = '212-NEW-YORK'
        mayorDict['state'] = "NY"
        mayorDict['body represents - muni'] = 'New York'
        mayorDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(mayorDict['state'].lower(),mayorDict['body represents - muni'].lower().replace(' ','_'))  
        dictList.append(mayorDict)
        return dictList 

mayor_page()



#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
new_york_city_council_file = open('new_york_city_council.csv','wb')
csvwriter = csv.DictWriter(new_york_city_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

new_york_city_council_file.close()
 
with open("new_york_city_council.csv", "r") as new_york_city_council_csv:
     new_york_city_council = new_york_city_council_csv.read()
