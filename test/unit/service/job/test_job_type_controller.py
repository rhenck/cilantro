import unittest
import os
import yaml
import json
import glob

from service.run_service import app

config_dir = os.environ['CONFIG_DIR']
job_types_dir = os.path.join(config_dir, 'job_types')


class JobTypeControllerTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_job_types_list_length(self):
        """
        Test the length of the job type list.

        Checks if the length of the element list of what the API returns is
        the same than the number of files in the directory on disk.

        :return: None
        """
        job_types_from_files = []
        for job_type in glob.glob(job_types_dir + '/*.yml'):
            job_types_from_files.append(job_type.rsplit('.', 1)[0])

        response = self.client.get('/job_types')

        self.assertEqual(len(job_types_from_files), len(response.get_json()))

    def test_first_job_types_exists(self):
        """
        Test if the first job type exists.

        Checks if the first filename from the job type directory is present
        in the JSON returned by the API.

        :return: None
        """
        first_job_type_name = _get_first_job_type_file().rsplit('.', 1)[0]
        response_text = self.client.get('/job_types').get_data(as_text=True)
        response_json = json.loads(response_text)

        type_found = False
        for job_type in response_json:
            type_found = (job_type['name'] == first_job_type_name) or type_found

        self.assertTrue(type_found)

    def test_job_type_detail(self):
        """
        Compare job file content with API return value as YAML.

        Checks if the file contents of the first file found in the job type
        directory is the same as what is served by the API when called with
        that name. Contents are both converted to YAML for comparison.

        :return: None
        """
        first_job_type_file = _get_first_job_type_file()
        with open(os.path.join(job_types_dir, first_job_type_file), 'r') as f:
            first_job_type_file_content = f.read()
        url = '/job_types/' + first_job_type_file.rsplit('.', 1)[0]
        response_text = self.client.get(url).get_data(as_text=True)

        self.assertEqual(yaml.safe_load(first_job_type_file_content),
                         yaml.safe_load(str(response_text)))

    def test_job_type_detail_with(self):
        """Test if a schema is returned when any job type is requested."""
        first_job_type_file = _get_first_job_type_file()
        url = '/job_types/' + first_job_type_file.rsplit('.', 1)[0] + '?schema=true'
        response_text = self.client.get(url).get_data(as_text=True)

        self.assertTrue("\"schema\":{\"$schema\"" in response_text)

    def test_invalid_job_type(self):
        response = self.client.get('/job_types/foobarbaz')
        self.assertEqual(404, response.status_code)

        response_json = response.get_json()
        self.assertFalse(response_json['success'])
        self.assertEqual(response_json['error']['code'], "job_type_not_found")


def _get_first_job_type_file():
    return os.path.basename(glob.glob(f"{job_types_dir}/*.yml")[0])
