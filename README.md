WorkAbroad.ph Scraper
=====================

A Scrapy project for scraping
[workabroad.ph](http://www.workabroad.ph/index.php) job posts.

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
# Number of seconds to wait before fetching page
DOWNLOAD_DELAY = 10
# Wait a random time between 0.5 and 1.5 * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True
```
### To clean and export scraped data to CSV
```
./sanitize.py csv inputfile.json outputfile.json
```
