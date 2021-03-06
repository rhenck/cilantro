import unittest
from urllib.error import HTTPError

from workers.default.ojs.ojs_api import publish, generate_frontmatter


class GenerateFrontmatterTest(unittest.TestCase):
    """Test the usage of the OJS frontmatter plugin."""

    published_articles = []

    @classmethod
    def setUpClass(cls):
        """
        Prepare some test data for the frontmatter generation.

        As a class method this runs once before all the tests are done.
        It uses the 'publish_to_ojs' worker which in turn uses
        OJS frontmatter plugin to generate 4 articles in OJS. It is done
        in 2 calls as the test import XML only contains 2 articles
        and the test is supposed to take a list with multiple articles.
        One article is a basic text though which is supposed to fail.
        Therefore the normal test uses the even number IDs and the test
        expecting failure the odd numbers refenrecing txt instead of PDF.
        """
        ojs_import_file = 'test/resources/files/ojs_import.xml'
        _, response = publish(ojs_import_file, 'test')
        cls.published_articles.extend(response['published_articles'])
        _, response = publish(ojs_import_file, 'test')
        cls.published_articles.extend(response['published_articles'])

    def test_generate_frontmatter(self):
        """
        Test valid PDF documents in OJS to generate frontmatter for.

        Takes the first ID from the published articles in the setup
        method, which are supposed to be a valid PDF file.
        """
        response_status_code, response = \
            generate_frontmatter(self.published_articles[0])

        self.assertEqual(200, response_status_code)
        self.assertTrue(response['success'])

    def test_generate_frontmatter_txt(self):
        """
        Test invalid text documents in OJS to generate frontmatter for.

        Takes the second ID from the published articles in the setup
        method, which are supposed to fail becasue it is simple text.
        The expected result of the call is to return a 500 HTTP error.
        """
        self.assertRaises(HTTPError, generate_frontmatter,
                          self.published_articles[1])
