from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from scrapy.selector import Selector
from workabroad.items import PostItem

class JobPostSpider(CrawlSpider):
    name = 'post'
    start_urls = [
        'http://www.workabroad.ph/report_job_listing.php?ajid=1155069&utm_source=WA+Jobs&utm_medium=job+details&utm_campaign=job_details',
        'http://www.workabroad.ph/report_job_listing.php?ajid=1110009&utm_source=WA+Jobs&utm_medium=job+details&utm_campaign=job_details',
        'http://www.workabroad.ph/report_job_listing.php?ajid=1110004&utm_source=WA+Jobs&utm_medium=job+details&utm_campaign=job_details',
        'http://www.workabroad.ph/report_job_listing.php?ajid=1109910&utm_source=WA+Jobs&utm_medium=job+details&utm_campaign=job_details',
    ]

    def parse(self, response):
        sel = Selector(response)
        item = PostItem()
        item['title'] = sel.xpath('//td[@class="jobtitle"]/h1/text()').extract()
        item['location'] = sel.xpath('//td[@class="jobsite"]/text()').extract()
        item['expiry'] = sel.xpath('//td[@class="jobexpiration"]/text()').extract()

        item['agency'] = {}
        item['agency']['name'] = sel.xpath('//td[@class="profile"]/a/b/text()').extract()
        item['agency']['license'] = sel.xpath('//td[preceding-sibling::td[position()=1]/b[text()="POEA License No.:"]]/text()').extract()
        item['agency']['address'] = sel.xpath('//td[preceding-sibling::td[position()=1]/b[text()="Address:"]]/text()').extract()
        item['agency']['telephone'] = sel.xpath('//td[preceding-sibling::td[position()=1]/b[text()="Tel. No.:"]]/text()').extract()

        item['qualifications'] = {}
        item['qualifications']['gender'] = sel.xpath('//td[preceding-sibling::td[position()=1]/b[text()="Gender:"]]/text()').extract()
        item['qualifications']['age'] = sel.xpath('//td[preceding-sibling::td[position()=1]/b[text()="Age:"]]/text()').extract()
        item['qualifications']['education'] = sel.xpath('//td[preceding-sibling::td[position()=1]/b[text()="Education:"]]/text()').extract()
        item['qualifications']['experience'] = sel.xpath('//td[preceding-sibling::td[position()=1]/b[text()="Experience:"]]/text()').extract()

        item['info'] = {}
        item['info']['principal'] = sel.xpath('//td[preceding-sibling::td[position()=1]/b[text()="Principal/Project:"]]/text()').extract()

        # Everything under the 'Job Description and Requirements' header
        item['requirements'] = sel.xpath('//tr[preceding-sibling::tr[position()=1]/td/b[text()="Job Description and Requirements"]]//text()').extract()
        return item
