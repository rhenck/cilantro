import unittest
import os
import json
import logging

from worker.xml.xml_generator import generate_xml
from worker.xml.marc_xml_generator import generate_marc_xml

log = logging.getLogger(__name__)


class GenerateXMLTest(unittest.TestCase):

        resource_dir = os.environ['RESOURCE_DIR']
        working_dir = os.environ['WORKING_DIR']

        generated_filename1 = f'{working_dir}/Ein_kleines_Musterdokument_mit_zweizeiligem_Titel.xml'
        generated_filename2 = f'{working_dir}/Titel_2.xml'
        generated_filename3 = f'{working_dir}/ojs_import.xml'

        def test_generate_marcxml(self):
            data_path = f'{self.resource_dir}/objects/pdf/data_json/data.json'
            with open(data_path) as json_object:
                data = json.load(json_object)

            template_file = open('resources/marc_template.xml', 'r')
            template_string = template_file.read()
            template_file.close()

            generate_marc_xml(self.working_dir, data, template_string)

            self.assertTrue(os.path.isfile(self.generated_filename1))
            self.assertTrue(os.path.isfile(self.generated_filename2))

        def test_generate_ojsxml(self):
            data_path = f'{self.resource_dir}/objects/pdf/data_json/data.json'
            with open(data_path) as json_object:
                data = json.load(json_object)

            template_file = open('resources/ojs_template.xml', 'r')
            template_string = template_file.read()
            template_file.close()

            generate_xml(self.working_dir, data, template_string)

            self.assertTrue(os.path.isfile(self.generated_filename3))

        @classmethod
        def tearDownClass(cls):
            try:
                os.remove(cls.generated_filename1)
                log.debug("Deleted file: " + cls.generated_filename1)
            except FileNotFoundError as e:
                log.error("File not found: " + e.filename)
            try:
                os.remove(cls.generated_filename2)
                log.debug("Deleted file: " + cls.generated_filename2)
            except FileNotFoundError as e:
                log.error("File not found: " + e.filename)
            try:
                os.remove(cls.generated_filename3)
                log.debug("Deleted file: " + cls.generated_filename3)
            except FileNotFoundError as e:
                log.error("File not found: " + e.filename)