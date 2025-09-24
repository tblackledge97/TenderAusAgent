import scrapy
import xml.etree.ElementTree as ET


class TendersSpider(scrapy.Spider):
    name = "tenders"
    allowed_domains = ["tenders.gov.au"]
    # start_urls = ["https://www.tenders.gov.au/public_data/rss/rss.xml"]

    def parse(self, response):
        """
        Parses the RSS feed XML to find links to full pages.
        """
        root = ET.fromstring(response.text)

        # Loop through each tender in the feed
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text

            # Check for new tenders
            # simple, make this better later
            if "tender" in title.lower():
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_tender_details,
                    meta={'tender_title': title}
                )

    def parse_tender_details(self, response):
        """
        Parses the full tender page to extract details.
        """

        main_container = response.css('div.box.boxW.listInner')

        atm_id = main_container.css('label[for="AtmId"] + .list-desc-inner::text').get()
        agency = main_container.css('label[for="Agency"] + .list-desc-inner::text').get()
        category = main_container.css('label[for="Category"] + .list-desc-inner::text').get()
        close_date = main_container.css('label[for="CloseDate"] + .list-desc-inner::text').get().strip()
        publish_date = main_container.css('label[for="PublishDate"] + .list-desc-inner::text').get().strip()
        tender_type = main_container.css('label[for="Type"] + .list-desc-inner::text').get()
        description = main_container.css('label[for="Description"] + .list-desc-inner p::text').get()

        yield {
            'title': response.meta['tender_title'],
            'url': response.url,
            'description': description,
            'close_date_time': close_date,
            'ATM_ID': atm_id,
            'agency': agency,
            'category': category,
            'publish_date': publish_date,
            'tender_type': tender_type
        }