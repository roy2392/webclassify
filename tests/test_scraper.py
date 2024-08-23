import unittest
from app.scraper import scrape_website
import asyncio

class TestScraper(unittest.TestCase):
    def test_scrape_website(self):
        url = "https://example.com"
        content = asyncio.run(scrape_website(url))
        self.assertIsNotNone(content)
        self.assertIn("Example Domain", content)

if __name__ == '__main__':
    unittest.main()