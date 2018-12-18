import unittest
from nytimes_headline_scrape import *

class NytimesArticlesScrapeTest(unittest.TestCase):

    def test_create_valid_article_path(self):
        expected = "https://spiderbites.nytimes.com/1991/articles_1991_11_00000.html"
        self.assertEqual(
            create_articles_path(
                NYTIMES_BASE_URL, 1991, 11, 0), expected)

    def test_get_date_from_url(self):
        expected = "1991/04/09"

        self.assertEqual(get_date_from_url("https://www.nytimes.com/1991/04/09/obituaries/theodore-distler-92-was-college-president.html"),
            expected)

    def test_wrong_date_from_url(self):
        self.assertIsNone(get_date_from_url("https://www.nytimes.com/1991/13/09/obituaries/theodore-distler-92-was-college-president.html"))

    def test_nondate_from_url(self):
        self.assertIsNone(get_date_from_url("https://www.nytimes.com/gsp/obituaries/theodore-distler-92-was-college-president.html"))

if __name__ == "__main__":
    unittest.main()