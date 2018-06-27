import io
import os
import unittest
from pathlib import Path

from run_service import app

test_object = 'some_tiffs'
test_file = 'test.tif'


class StagingControllerTest(unittest.TestCase):

    resource_dir = os.environ['RESOURCE_DIR']
    staging_dir = os.environ['STAGING_DIR']

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        object_path = os.path.join(self.resource_dir, 'objects', test_object)
        for file_name in os.listdir(object_path):
            self._remove_file_from_staging(file_name)
        self._remove_file_from_staging(test_file)

    def test_upload_single_file(self):
        file_path = os.path.join(self.resource_dir, 'objects',
                                 test_object, test_file)
        file = False
        try:
            file = (open(file_path, 'rb'), test_file)
            response = self._upload_to_staging({'file': file})
            self.assertEqual(response.status_code, 200)
            self._assert_file_in_staging(test_file)
        finally:
            if file:
                file[0].close()

    def test_upload_multiple_files(self):
        object_path = os.path.join(self.resource_dir, 'objects', test_object)
        response = self._upload_folder_to_staging(object_path)
        self.assertEqual(response.status_code, 200)
        self._assert_file_in_staging(test_file)
        for file_name in os.listdir(object_path):
            self._assert_file_in_staging(file_name)

    def test_upload_file_extension_not_allowed(self):
        response = self._upload_to_staging(
            {'file': (io.BytesIO(b'asdf'), 'foo.asdf')})
        self.assertEqual(response.status_code, 415)

    def test_list_staging(self):
        object_path = os.path.join(self.resource_dir, 'objects', test_object)
        file_names = os.listdir(object_path)
        self._upload_folder_to_staging(object_path)

        response = self.client.get('/staging')
        response_object = response.get_json()
        self.assertGreaterEqual(len(response_object), len(file_names))
        staged_files = [e for e in response_object if e['name'] in file_names]
        self.assertEqual(len(staged_files), len(file_names))

    def _upload_folder_to_staging(self, object_path):
        file_names = os.listdir(object_path)
        files = []
        try:
            for file_name in file_names:
                file_path = os.path.join(object_path, file_name)
                file = (open(file_path, 'rb'), file_name)
                files.append(file)

            return self._upload_to_staging({'files': files})
        finally:
            for file in files:
                file[0].close()

    def _upload_to_staging(self, data):
        return self.client.post(
            '/staging',
            content_type='multipart/form-data',
            data=data
        )

    def _assert_file_in_staging(self, file_name):
        file = Path(os.path.join(self.staging_dir, file_name))
        if not file.is_file():
            raise AssertionError(f"File '{file_name}' was not present in the "
                                 f"staging folder")

    def _remove_file_from_staging(self, file_name):
        file_path = os.path.join(self.staging_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)