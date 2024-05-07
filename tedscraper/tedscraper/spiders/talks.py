import json
import scrapy


class TEDscraper(scrapy.Spider):
    """Recursively crawls ted.com/talks and extracts talk data."""
    name = 'talks'
    start_urls = ['https://www.ted.com/talks/quick-list?page=1']

    def parse(self, response):
        """Recursively follows links to all TED talks and extracts data from them."""

        # follow all the links to each talk on the page calling the parse_talk callback for each of them
        talks_page_links = response.xpath('//span[@class="l3"]/a/@href').getall()
        
        #talks_page_links = response.xpath("//a[@class=' ga-link']/@href")
        yield from response.follow_all(talks_page_links, self.parse_talk)

        pagination_links = response.css(".pagination__next")
        yield from response.follow_all(pagination_links, self.parse)
    
    def parse_talk(self, response):
        """Parses the response, extracting the scraped talk data as dicts."""

        # find xpath to the JSON with talk data
        raw = response.xpath("//script[@type='application/json']/text()").get()
        # cast the string 'raw' to a dict
        js = json.loads(raw)
        # create dict with talk data of interest
        d = js['props']['pageProps']['videoData']

        transcript = ''
        if not js['props']['pageProps']['transcriptData']['translation'] or js['props']['pageProps']['transcriptData']['translation']['language']['englishName'] == 'English':
            for paragraph in js['props']['pageProps']['transcriptData']['translation']['paragraphs'][0:2]:
                for cue in paragraph['cues']:
                    transcript += cue['text'] + ' '

        yield {
            'talk_id': d['id'],
            'title': d['title'],
            'description': d['description'],
            'speaker': d['presenterDisplayName'],
            'recorded_date': d['recordedOn'],
            'published_date': d['publishedAt'],
            'event': d['videoContext'],
            'duration': d['duration'],
            'topic_names': [topic['name'] for topic in d['topics']['nodes']],
            'transcription': transcript,
            'views': d['viewedCount']
        }
 