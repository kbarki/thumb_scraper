
import json
import os
import requests
import validators
from lxml import html
from requests.auth import HTTPBasicAuth


class PetitPoucet:

    BASIC_AUTH_USERNAME = 'Thumb'
    BASIC_AUTH_PASSWORD = 'Scraper'

    def __init__(self, jsonDataPath, initialLink, initialIndex='0'):
        """
        :param jsonDataPath: The path of the json file -> data/petit_poucet_input.json
        :param initialLink: Url of the entry point -> https://yolaw-tokeep-hiring-env.herokuapp.com/
        :param initialIndex: Index of the first page -> 0
        """
        if not os.path.exists(jsonDataPath):
            raise Exception(jsonDataPath + ' is not a valid path')
        if not validators.url(initialLink):
            raise Exception(initialLink + ' is not a valid Url')

        try:
            f_data = open(jsonDataPath, 'r')
            self.data = json.load(f_data)
            f_data.close()
        except Exception as e:
            print('Couldn\'t read input json file : ' + str(e))

        self.initial_link = initialLink
        self.current_link = initialLink
        self.current_index = initialIndex
        if self.current_index not in self.data:
            raise ValueError('The initial index \'initialIndex\' = ' + self.current_index + ', is not in data')
        self.current_web_page = html.document_fromstring('<html>')
        self.web_page_counter = 0

    def run_web_scraper(self):

        while True:
            self.get_current_web_page()
            if self.check_current_web_page():
                self.web_page_counter += 1
                print('Move to page ' + str(self.web_page_counter))
                link = self.current_web_page.xpath(
                    self.data[self.current_index]['xpath_button_to_click']
                )
                self.current_link = link[0].attrib['href']
                self.current_index = self.data[self.current_index]['next_page_expected']
            else:
                print('ALERT - Can\'t move to page ' + str(self.web_page_counter + 1) + ': page '
                      + str(self.web_page_counter) + ' link has been malevolently tampered with!!')
                return

    def get_current_web_page(self):
        """Fetches the html document at self.current_link
        """
        web_page = requests.get(self.current_link,
                                auth=HTTPBasicAuth(self.BASIC_AUTH_USERNAME, self.BASIC_AUTH_PASSWORD))
        if web_page.status_code != 200:
            raise Exception('Couldn\'t fetch page ' + self.current_link)
        self.current_web_page = html.document_fromstring(web_page.text)
        self.current_web_page.make_links_absolute(self.initial_link)

    def check_current_web_page(self):
        """Check if xpath_test_query matches xpath_test_result
        """
        return self.current_web_page.xpath(self.data[self.current_index]['xpath_test_query']
                                           ) == self.data[self.current_index]['xpath_test_result']


if __name__ == '__main__':
    def main():
        """Start PetitPoucet scraper
        """
        mon_petit_poucet = PetitPoucet('data/petit_poucet_input.json', 'https://yolaw-tokeep-hiring-env.herokuapp.com/')
        mon_petit_poucet.run_web_scraper()

    main()

