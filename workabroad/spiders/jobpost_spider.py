import urlparse
from scrapy import log
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from scrapy.selector import Selector
from workabroad.items import PostItem

class JobPostSpider(CrawlSpider):
    name = 'post'

    allowed_domains = ['workabroad.ph']
    start_urls = [
        'http://www.workabroad.ph/list_specific_jobs.php?by_what=date',
    ]

    def get_absolute_address(relative_address):
        return 'http://www.workabroad.ph/' + relative_address

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//table/tr[4]/td/table/tr/td[3]/table[5]/tr/td/form/a'),
                               process_value=get_absolute_address),
             follow=True, callback='parse_index'),
    )

    def parse_index(self, response):
        self.log("LOG: parse_index: Parsing %s" % response.url)
        sel = Selector(response)
        post_links = sel.xpath('//table/tr[4]/td/table/tr/td[3]/table[4]/tr/td[1]//a/@href').extract()
        for link in post_links:
            link = 'http://www.workabroad.ph/' + link
            request = Request(link, callback=self.parse_job_page)
            yield request


    def parse_job_page(self, response):
        self.log("LOG: parse_job_page: Parsing %s" % response.url)
        sel = Selector(response)
        item = PostItem()

        # Job post's URL and the job post's ID
        item['href'] = response.url
        item['id'] = urlparse.parse_qs(urlparse.urlparse(response.url).query
                                       ).get('ajid', [None])[0]

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
