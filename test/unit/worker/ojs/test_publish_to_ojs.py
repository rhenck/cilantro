import unittest
from urllib.error import HTTPError

from workers.default.ojs.ojs_api import publish


class PublishToOJSTest(unittest.TestCase):
    """Test import to OJS via XML-Plugin."""

    def test_publish_to_ojs(self):
        """
        Publish via prebuilt Import-XML.

        Tested are the return code and part of the returned text for a string
        indicating a successful operation.
        """
        ojs_import_file = 'test/resources/files/ojs_import.xml'

        response_status_code, response = publish(ojs_import_file, 'test')

        self.assertEqual(200, response_status_code)
        self.assertTrue(response['success'])

    def test_publish_to_ojs_faulty_xml(self):
        """
        Publish via prebuilt Import-XML which has syntax errors and is to fail.

        Expected is a 500er HTTP error.
        """
        ojs_import_file = 'test/resources/files/ojs_import_faulty.xml'

        self.assertRaises(HTTPError, publish, ojs_import_file, 'test')
