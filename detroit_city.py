#!/usr/bin/python
# -*- coding: latin-1 -*-
import os

from selenium import webdriver
import lxml.html as lh

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


dictList = []


root_url = 'http://www.detroitmi.gov'
index_url = root_url + '/Government/City-Council'

#response = requests.get(root_url)
#soup = bs4.BeautifulSoup(response.text, 'lxml')

def council_scrape():
	driver = webdriver.PhantomJS()
	driver.get(index_url)
	content = driver.page_source
	doc = lh.fromstring(content)
	driver.close()
	os.system('taskkill /f /im phantomjs.exe')
	for x in range(0,9):
		cData = {}
		cData['official.name'] = doc.xpath('//div[@class="ico"]/h3/text()')[x].encode('utf-8').replace('\xc3\xa9','e')#.replace('├⌐','e')
		cData['office.name'] = "City Council " + doc.xpath('//div[@class="ico"]/p/text()')[x].encode('utf-8').replace('\xe9','e')
		cData['website'] = root_url + doc.xpath('//div[@class="ico"]/a/@href')[x + 1 + (x*1)]
		cData['body represents - muni'] = 'Detroit'
		cData['state'] = 'MI'
		if doc.xpath('//div[@class="ico"]/p/text()')[x].encode('utf-8').replace('\xe9','e') == 'At-Large':
			cData['electoral.district'] = 'Detroit'
			cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(cData['state'].lower(),cData['body represents - muni'].lower().replace(' ', '_'))
		else:
			cData['electoral.district'] = "Detroit City Council " + doc.xpath('//div[@class="ico"]/p/text()')[x].encode('utf-8').replace('\xe9','e')
			cData['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}/council_district:'.format(cData['state'].lower(), cData['body represents - muni'].lower().replace(' ', '_')) + cData['electoral.district'][-2:].strip()
		dictList.append(cData)

council_scrape()

def mayor_scrape():
	mayor_url = 'http://www.detroitmi.gov/Government/Mayors-Office'
	driver = webdriver.PhantomJS()
	driver.get(mayor_url)
	content = driver.page_source
	doc = lh.fromstring(content)
	driver.close()
	os.system('taskkill /f /im phantomjs.exe')
	mayorDict = {}
	mayorDict['office.name'] = 'Mayor'
	mayorDict['electoral.district'] = 'Detroit'
	mayorDict['body represents - muni'] = 'Detroit'
	mayorDict['state'] = "MI"
	mayorDict['website'] = mayor_url
	mayorDict['OCDID'] = 'ocd-division/country:us/state:{0}/place:{1}'.format(mayorDict['state'].lower(),mayorDict['body represents - muni'].lower().replace(' ', '_'))
	mayorDict['official.name'] = doc.xpath('//h3[@class="carousel_title"]/a/text()')[0].encode('utf-8')
	dictList.append(mayorDict)

mayor_scrape()

#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
detroit_council_file = open('detroit_council.csv','wb')
csvwriter = csv.DictWriter(detroit_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

detroit_council_file.close()
 
with open("detroit_council.csv", "r") as detroit_council_csv:
     detroit_council = detroit_council_csv.read()