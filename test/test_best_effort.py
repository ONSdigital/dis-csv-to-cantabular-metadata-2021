import json
import unittest.mock
import unittest
import pathlib
import os
import logging
from io import StringIO
from datetime import date
import ons_csv_to_ctb_json_main

FILENAME_TABLES = 'cantabm_v9-3-0_best-effort_tables-md_19700101-1.json'
FILENAME_DATASET = 'cantabm_v9-3-0_best-effort_dataset-md_19700101-1.json'
FILENAME_SERVICE = 'cantabm_v9-3-0_best-effort_service-md_19700101-1.json'

class TestBestEffort(unittest.TestCase):
    @unittest.mock.patch('ons_csv_to_ctb_json_main.date')
    def test_generated_json_best_effort(self, mock_date):
        """Generate JSON from source CSV and compare it with expected values."""
        mock_date.today.return_value = date(1970, 1, 1)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        file_dir = pathlib.Path(__file__).parent.resolve()
        input_dir = os.path.join(file_dir, 'testdata/best_effort')
        output_dir = os.path.join(file_dir, 'out')

        with self.assertLogs(level='WARNING') as cm:
            with unittest.mock.patch('sys.argv', ['test', '-i', input_dir, '-o', output_dir, '-m', 'best-effort', '--best-effort']):
                ons_csv_to_ctb_json_main.main()
                with open(os.path.join(output_dir, FILENAME_SERVICE)) as f:
                    service_metadata = json.load(f)
                with open(os.path.join(file_dir, 'expected/service-metadata.json')) as f:
                    expected_service_metadata = json.load(f)
                self.assertEqual(service_metadata, expected_service_metadata)

                with open(os.path.join(output_dir, FILENAME_DATASET)) as f:
                    dataset_metadata = json.load(f)
                with open(os.path.join(file_dir, 'expected/dataset-metadata-best-effort.json')) as f:
                    expected_dataset_metadata = json.load(f)
                self.assertEqual(dataset_metadata, expected_dataset_metadata)

                with open(os.path.join(output_dir, FILENAME_TABLES)) as f:
                    table_metadata = json.load(f)
                with open(os.path.join(file_dir, 'expected/table-metadata-best-effort.json')) as f:
                    expected_table_metadata = json.load(f)
                self.assertEqual(table_metadata, expected_table_metadata)

        warnings = [
            r'Classification.csv:3 no value supplied for required field Variable_Mnemonic',
            r'Classification.csv:3 dropping record',
            r'Classification.csv:4 duplicate value CLASS1 for Classification_Mnemonic',
            r'Classification.csv:4 dropping record',
            r'Classification.csv:5 invalid value x for Number_Of_Category_Items',
            r'Category.csv Unexpected number of categories for CLASS1: expected 4 but found 1',
            r'Database_Variable.csv Lowest_Geog_Variable_Flag set on GEO3 and GEO1 for database DB1',
            r'Dataset_Variable.csv:4 duplicate value combo DS1/VAR1 for Dataset_Mnemonic/Variable_Mnemonic',
            r'Dataset_Variable.csv:4 dropping record',
            r'Dataset_Variable.csv:2 Lowest_Geog_Variable_Flag set on non-geographic variable VAR1 for dataset DS1',
            r'Dataset_Variable.csv:2 Processing_Priority not specified for classification CLASS1 in dataset DS1',
            r'Dataset_Variable.csv:3 Classification_Mnemonic must not be specified for geographic variable GEO1 in dataset DS1',
            r'Dataset_Variable.csv:3 Processing_Priority must not be specified for geographic variable GEO1 in dataset DS1',
            r'Dataset_Variable.csv:5 Lowest_Geog_Variable_Flag set on variable GEO2 and GEO1 for dataset DS1',
            r'Dataset_Variable.csv:7 Classification must be specified for non-geographic VAR2 in dataset DS1',
            r'Dataset_Variable.csv:7 dropping record',
            r'Dataset_Variable.csv:8 Invalid classification CLASS1 specified for variable VAR3 in dataset DS1',
            r'Dataset_Variable.csv:8 dropping record',
            r'Dataset_Variable.csv Invalid processing_priorities \[0\] for dataset DS1',
            r'Dataset.csv:3 DS2 has classification CLASS3 that is not in database DB1',
            r'Dataset.csv:3 dropping record',
            r'Dataset.csv:4 DS3 has no associated classifications or geographic variable',
            r'Dataset.csv:4 dropping record',
            r'16 errors were encountered during processing',
        ]

        self.assertEqual(len(warnings), len(cm.output))
        for i, warning in enumerate(cm.output):
            self.assertRegex(warning, warnings[i])

