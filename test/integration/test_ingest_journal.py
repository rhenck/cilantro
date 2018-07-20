from test.integration.job_type_test import JobTypeTest


class IngestJournalTest(JobTypeTest):

    def test_success(self):
        self.stage_resource('objects', 'pdf')
        params = self.load_params_from_file('params', 'a_journal.json')

        data, status_code = self.post_job('ingest_journal', params)
        self.assertEquals(status_code, 202)
        job_id = data['job_id']
        self.assertEqual('Accepted', data['status'])
        self.assert_status(job_id, 'SUCCESS')

        files_generated = [
            'parts/part_0001/data/pdf/merged.pdf',
            'parts/part_0001/meta.json',
            'parts/part_0001/marc.xml',
            'parts/part_0002/data/pdf/merged.pdf',
            'parts/part_0002/meta.json',
            'parts/part_0002/marc.xml',
            'parts/part_0002/data/nlp/page.1.json',
            'meta.json',
            'ojs_import.xml'
        ]
        for file in files_generated:
            self.assert_file_in_repository(job_id, file)
        self.unstage_resource('pdf')
