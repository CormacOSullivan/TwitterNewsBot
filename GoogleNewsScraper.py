import googlesearch
import urllib.request as urllib2
from bs4 import BeautifulSoup
import json
import lxml.html

class GoogleNewsScraper:

    def __init__(self, json_path, logger=None):
        self.json_path = json_path
        self.logger = logger

    def get_search_results(self, location, num_results=3, extra_params=None):
        results = googlesearch.search(location, tld='com', lang='en', tbs='0', safe='off', num=10, start=0,
                                      stop=10,
                                      pause=2.0,
                                      country=location.replace(" ", "+"), extra_params=extra_params, user_agent='Mozilla/5.0',
                                      verify_ssl=True)
        links = []
        titles = []
        for x in results:
            try:
                req = urllib2.Request(x, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(urllib2.urlopen(req), features="html.parser")
                if soup.title:
                    links.append(x)
                    titles.append(soup.title.string.strip()[:40] + "...")
            except Exception as e:
                self.logger.error(e)
            if len(links) == num_results:
                break
        return links, titles

    def create_tweet(self, location, links, titles):
        tweet = f"Here are some headlines for {location.title()}:\n"
        for x in range(0, len(links)):
            tweet += f"\n{titles[x]}\n{links[x]}\n"
        tweet += f"\n- NewsInternationalBot"
        return tweet

    def read_json(self):
        """
        Reads the information found in the countries.json file for checking the users requested weather location
        and returns the data after decoding
        :return: data -> A dictionary contain all the information for locations compatible with openweatherapi
                 -1 -> If an error occurred
        """
        try:
            with open(self.json_path, encoding='utf-8') as f:
                data = json.load(f)
        except (IOError, ValueError, EOFError) as e:
            self.logger.error(e)
            return -1
        except Exception as f:
            self.logger.error("An Unexpected error has occurred: ", f)
            return -1
        return data
