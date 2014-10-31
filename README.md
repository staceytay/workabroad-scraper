WorkAbroad.ph Scraper
=====================

A Scrapy project for scraping
[workabroad.ph](http://www.workabroad.ph/index.php) job posts. This was my
project as a research assistant for
Dr. [Emily Beam](https://sites.google.com/site/eabeam/) for her research on
employment trends.

# Installing Scrapy
```
pip install scrapy
```

# Usage
### To scrape data from [workabroad.ph](http://www.workabroad.ph/index.php)
```
scrapy crawl post -t json -o outputfile.json
```
#### Scrapy settings
To change scraping settings, open `workabroad/settings.py`.
```
# Scrape job posts from the top n most recent pages
DEPTH_LIMIT = n
# Number of seconds to wait before fetching page
DOWNLOAD_DELAY = 10
# Wait a random time between 0.5 and 1.5 * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True
```
### To clean and export scraped data to CSV
```
./sanitize.py csv inputfile.json outputfile.csv
```
### To clean and export scraped data to JSON
```
./sanitize.py json inputfile.json outputfile.json
```
