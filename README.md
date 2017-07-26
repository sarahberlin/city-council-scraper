# city-council-scraper
Scripts designed to pull basic information about city councils of high population US cities

Requirements for these scripts:
Beautiful Soup 4
Requests
Selenium
Phantom JS

Instructions:
To get csv files of each city's council, run the city python files, either one at a time, or all at once using the run_cityscripts.py file
To compare csv files of scraped data to an existing file of office holders, first run all the city scripts to get most up to date info, then run city_addUID.py with 2 arguments: 1. full path to the existing csv file of office holders 2. full path to where the scraped csv files are stored on your computer. Then run city_scrapecompare.py with the same 2 arguments. This script will print out any instances where the the office holder differed between the 2 files. 
If you want run_cityscripts.py to emailed the results to you, uncomment out everything through line 200, fill in the email address you want the email to come FROM in line 180, the email address you want it emailed TO in line 181, and your log in info (from address, then password as strings) in line 195.


