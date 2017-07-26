import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2
from selenium import webdriver
import lxml.html as lh
import os

root_url = "https://www.okc.gov/"
index_url = root_url + '/government/city-council'

browser = webdriver.PhantomJS()
browser.get(index_url)
soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
dictList = []

def council_scrape():
    for row in soup.select('tr td')[:-1]:
        newDict = {}
        newDict['state'] = 'OK'
        newDict['body represents - muni'] = 'Oklahoma City'
        try:
            newDict['office.name'] = "City Council Member " + row.select('a')[0].contents[0].get_text().encode('utf-8')
            newDict['electoral.district'] = "Oklahoma City Council " + row.select('a')[0].contents[0].get_text().encode('utf-8')
            newDict['official.name'] = row.select('a')[0].contents[1].get_text().encode('utf-8').strip()
            newDict['website'] = root_url + [a.attrs.get('href') for a in row.select('a[href]')][0].encode('utf-8')
        except:
            newDict['office.name'] = "City Council Member " + row.select('a')[0].get_text().encode('utf-8').strip()
            newDict['electoral.district'] = "Oklahoma City Council " + row.select('a')[0].get_text().encode('utf-8').strip()
            newDict['official.name'] = row.select('a')[1].get_text().encode('utf-8').strip()
            newDict['website'] = root_url + "/government/city-council/ward-4"
        newDict['OCDID'] = 'ocd-division/country:us/state:ok/place:oklahoma_city/ward:' + newDict['electoral.district'][-1]
        try:
            os.system('taskkill /f /im phantomjs.exe')
        except:
            pass
        dictList.append(newDict)

def mayor_scrape():
    mayor_url = 'https://www.okc.gov/government/mayor'
    browser = webdriver.PhantomJS()
    browser.get(mayor_url)
    mayor_soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
    mayorDict = {}
    mayorDict['official.name'] = mayor_soup.select('h1')[1].get_text().encode('utf-8').replace('Mayor ','')
    mayorDict['office.name'] = "Mayor"
    mayorDict['electoral.district'] = "Oklahoma City"
    mayorDict['website'] = mayor_url
    mayorDict['state'] = "OK"
    mayorDict['body represents - muni'] = 'Oklahoma City'
    mayorDict['OCDID'] = 'ocd-division/country:us/state:ok/place:oklahoma_city'
    try:
        os.system('taskkill /f /im phantomjs.exe')
    except:
        pass
    dictList.append(mayorDict)

council_scrape()
mayor_scrape()

#creates csv
fieldnames = ['UID','state','body represents - muni','Body Name','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter', "OCDID"]
okc_council_file = open('okc_council.csv','wb')
csvwriter = csv.DictWriter(okc_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

okc_council_file.close()
