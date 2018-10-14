
import json
import unittest
import petit_poucet_scraper
from lxml import html


class TestPetitPoucet(unittest.TestCase):

    def setUp(self):
        try:
            f_data = open('data/petit_poucet_input.json', 'r')
            self.data = json.load(f_data)
            f_data.close()
        except Exception as e:
            print('Couldn\'t read input json file : ' + str(e))
            exit(1)
        self.petit_poucet = petit_poucet_scraper.PetitPoucet('data/petit_poucet_input.json',
                                                             'https://yolaw-tokeep-hiring-env.herokuapp.com/')

    def test_constructor(self):
        with self.assertRaises(Exception):
            petit_poucet_scraper.PetitPoucet('data/test/petit_poucet_input.json',
                                             'https://yolaw-tokeep-hiring-env.herokuapp.com/')
        with self.assertRaises(Exception):
            petit_poucet_scraper.PetitPoucet('data/petit_poucet_input.json',
                                             'yolaw-tokeep-hiring-env.herokuapp.com/')
        with self.assertRaises(ValueError):
            petit_poucet_scraper.PetitPoucet('data/petit_poucet_input.json',
                                             'https://yolaw-tokeep-hiring-env.herokuapp.com/',
                                             'index')
        petit_poucet_scraper.PetitPoucet('data/petit_poucet_input.json',
                                         'https://yolaw-tokeep-hiring-env.herokuapp.com/')

    def test_get_current_web_page(self):
        self.petit_poucet.BASIC_AUTH_USERNAME = 'Test'
        with self.assertRaises(Exception):
            self.petit_poucet.get_current_web_page()
        self.petit_poucet.BASIC_AUTH_USERNAME = 'Thumb'
        self.petit_poucet.current_link = 'test url'
        with self.assertRaises(Exception):
            self.petit_poucet.get_current_web_page()
        self.petit_poucet.current_link = 'https://yolaw-tokeep-hiring-env.herokuapp.com/'
        self.petit_poucet.get_current_web_page()

    def test_check_current_web_page(self):
        self.petit_poucet.current_web_page = html.document_fromstring('<html><body>ThumbScraper</body></html>')
        self.assertFalse(self.petit_poucet.check_current_web_page())
        self.petit_poucet.get_current_web_page()
        self.assertTrue(self.petit_poucet.check_current_web_page())

