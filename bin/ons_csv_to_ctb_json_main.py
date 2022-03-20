"""Load metadata from CSV files and export in JSON format."""
import json
import os
import logging
from argparse import ArgumentParser
from ons_csv_to_ctb_json_load import Loader, PUBLIC_SECURITY_MNEMONIC
from ons_csv_to_ctb_json_bilingual import BilingualDict, Bilingual

VERSION = '1.0.alpha'


def main():
    """
    Load metadata in CSV format and export in JSON format.

    The exported JSON files can be loaded by cantabular-metadata.
    """
    parser = ArgumentParser(description='Program for converting metadata files in CSV format to '
                                        'JSON format that can be loaded into cantabular-metadata.',
                            epilog=f'Version: {VERSION}')

    parser.add_argument('-i', '--input-dir',
                        type=str,
                        required=True,
                        help='Input directory containing CSV files to convert to JSON')

    parser.add_argument('-o', '--output-dir',
                        type=str,
                        required=True,
                        help='Output directory to write JSON files')

    parser.add_argument('-l', '--log_level',
                        type=str,
                        default='INFO',
                        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                        help='Log level (default: %(default)s)')

    args = parser.parse_args()

    logging.basicConfig(format='t=%(asctime)s lvl=%(levelname)s msg=%(message)s',
                        level=args.log_level)

    # loader is used to load the metadata from CSV files and convert it to JSON.
    loader = Loader(args.input_dir)

    # Build Cantabular variable and dataset objects and write them to a JSON file.
    # A Cantabular variable is equivalent to an ONS classification.
    # A Cantabular dataset is equivalent to an ONS database.
    ctb_variables = build_ctb_variables(loader.classifications, loader.categories)
    ctb_datasets = build_ctb_datasets(loader.databases, ctb_variables)
    filename = os.path.join(args.output_dir, 'dataset-metadata.json')
    with open(filename, 'w') as jsonfile:
        json.dump(ctb_datasets, jsonfile, indent=4)
    logging.info(f'Written dataset metadata file to: {filename}')

    # Build Cantabular table objects, embed them within the service metadata and write to JSON.
    ctb_tables = build_ctb_tables(loader.datasets)
    service_metadata = build_ctb_service_metadata(ctb_tables)
    filename = os.path.join(args.output_dir, 'service-metadata.json')
    with open(filename, 'w') as jsonfile:
        json.dump(service_metadata, jsonfile, indent=4)
    logging.info(f'Written service metadata file to: {filename}')


def build_ctb_variables(classifications, cat_labels):
    """
    Build Cantabular variable objects.

    A variable is a built-in concept in cantabular-metadata, and is equivalent to an ONS
    classification.
    """
    ctb_variables = []
    for mnemonic, classification in classifications.items():
        # Only export public variables.
        if classification.private['Security_Mnemonic'] != PUBLIC_SECURITY_MNEMONIC:
            logging.info(f'Dropped non public classification: {mnemonic}')
            continue

        ctb_class = {
            'name': mnemonic,
            'label': classification.private['Classification_Label'],
            'meta': classification,
            'catLabels': cat_labels.get(mnemonic, None)
        }
        ctb_variables.append(BilingualDict(ctb_class))
        logging.debug(f'Loaded metadata for Cantabular variable: {mnemonic}')

    logging.info(f'Loaded metadata for {len(ctb_variables)} Cantabular variables')

    return ctb_variables


def build_ctb_datasets(databases, ctb_variables):
    """
    Build Cantabular dataset objects.

    A dataset is a built-in concept in cantabular-metadata, and is equivalent to an ONS
    database.
    """
    ctb_datasets = []

    # Add all the variables to a base dataset. Other datasets include this to avoid duplicating
    # metadata.
    ctb_dataset = BilingualDict({
        'name': 'base',
        'label': Bilingual(
            'Base dataset with metadata for all variables',
            'Base dataset with metadata for all variables in Welsh',
        ),
        'lang': Bilingual('en', 'cy'),
        'meta': {
            'Database_Description': Bilingual(
                'This is a base dataset containing metadata for all variables used across all '
                'other datasets. Other datasets include it to avoid duplicating metadata.',
                'This is the Welsh version of the base dataset containing metadata for all '
                'variables.'),
            'Source': {
                'Source_Mnemonic': 'Census2021',
                'Source_Description': 'The 2021 England and Wales Census',
            },
            'Version': '1'
        },
        'vars': ctb_variables,
    })
    ctb_datasets.extend([ctb_dataset.english(), ctb_dataset.welsh()])

    for database_mnemonic, database in databases.items():
        ctb_dataset = BilingualDict({
            'name': database_mnemonic,
            'incl': [{'name': 'base', 'lang': Bilingual('en', 'cy')}],
            'label': database.private['Database_Title'],
            'lang': Bilingual('en', 'cy'),
            'meta': database,
            'vars': None,
        })
        ctb_datasets.extend([ctb_dataset.english(), ctb_dataset.welsh()])
        logging.debug(f'Loaded metadata for Cantabular dataset: {database_mnemonic}')

    logging.info(f'Loaded metadata for {len(databases)} Cantabular datasets')

    return ctb_datasets


def build_ctb_tables(datasets):
    """
    Build the metadata for each predefined table.

    A Cantabular table is equivalent to an ONS dataset.
    """
    ctb_tables = []
    for mnemonic, dataset in datasets.items():
        # Only export public tables.
        if datasets[mnemonic].private['Security_Mnemonic'] != PUBLIC_SECURITY_MNEMONIC:
            logging.info(f'Dropped non public ONS Dataset: {mnemonic}')
            continue

        table = BilingualDict({
            'name': mnemonic,
            'label': dataset.private['Dataset_Title'],
            'description': dataset.private['Dataset_Description'],
            'datasetName': dataset.private['Database_Mnemonic'],
            'vars': dataset.private['Classifications'],
            'meta': dataset,
        })
        ctb_tables.append(table)
        logging.debug(f'Loaded metadata for Cantabular table: {mnemonic}')

    logging.info(f'Loaded metadata for {len(ctb_tables)} Cantabular tables')

    return ctb_tables


def build_ctb_service_metadata(ctb_tables):
    """Build the service metadata which embeds the tables."""
    service_metadata = BilingualDict({
        'lang': Bilingual('en', 'cy'),
        'meta': {
            'tables': ctb_tables,
        },
    })
    logging.info(f'Loaded service metadata')

    return [service_metadata.english(), service_metadata.welsh()]


if __name__ == '__main__':
    main()
