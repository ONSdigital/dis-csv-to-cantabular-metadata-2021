Release Notes
=============

1.5
-----

- Update to metadata schema version 1.5.
  - Expose new `Dataset.Origin_Variable_Mnemonic`, `Dataset.Destination_Variable_Mnemonic`  and
    `Dataset.OD_Flag` fields.

1.3.4
-----

- Update to metadata schema version 1.4.
  - Expose new `Classification.Not_Applicable_Category_Description` and
    `Classification.Not_Applicable_Category_Description_Welsh` fields.
  - Removed references to `Database.IAR_Asset_Id`.
  - `Dataset_Variable.Minimum_Threshold_Person` and `Dataset_Variable.Minimum_Threshold_HH`
    are not exposed.
  - Expose new `Statistical_Unit.Statistical_Unit_Label` and
    `Statistical_Unit.Statistical_Unit_Label_Welsh` fields.
  - Expose new `Variable.Variable_Short_Description` and
    `Variable.Variable_Short_Description_Welsh` fields.
  - Support new `Variable.Quality_Statement_Text_Welsh` field.
  - Expose dataset and variable keywords from `Dataset_Keyword` and `Variable_Keyword`.
- Cantabular version 10.2.3 is now the default version. The file format for version 10.2.3 is
  the same for all currently supported versions of Cantabular.

1.3.3
-----

- Support multiple geography lookup files. Files can be supplied using the `-g` option, with
  one `-g` option per file. Alternatively a geography folder can be specifed using the new `-d` option.
- Expose `Cantabular_Public_Flag` for each variable on a per-dataset basis.

1.3.2
-----

- Include English category labels in variable metadata.
  These labels will be used in placed of labels in the codebook when variable category labels
  are obtained from the extended API.
- Add build and version information to service metadata.
- Dropped support for Cantabular version 9.2.0.

1.3.1
-----
- Expose `Variable.Geography_Hierarchy_Order` in variable metadata.
- Base dataset name is now configurable.
- Cantabular version 10.2.2 is now the default version. The file format for version 10.2.2 is
  identical to all other supported versions except 9.2.0.

1.3.alpha
---------
- Updated code to work with metadata schema version 1.3.
- Removed preprocessing scripts that are no longer necessary.
- Cantabular version 10.2.0 is now the default version. The file format for version 10.2.0 is
  identical to all other supported versions except 9.2.0.

1.2.epsilon
-----------
- The code to process the geography lookup file expects lowercase file suffixes `cd`, `nm` and `nmw`.
  Previously it expected uppercase suffixes.

1.2.delta
-----------
- Added a new `--dataset-filter` option that is used to filter the datasets which are processed
  and included in the output JSON.

1.2.gamma
-----------
- Ensure input files to `remove_empty_rows_and_columns.py` are processed in a repeatable
  order. This fixes an issue where unit tests might incorrectly fail on some systems.

1.2.1-alpha
-----------
- Added utility `remove_empty_rows_and_columns.py` to remove any empty rows and
  columns from all CSV files in a given directory and write the modified files
  to a specified output directory.

1.2.alpha
---------
- Updated code to work with metadata schema version 1.2.
- Cantabular version 10.1.0 is now the default version. The file format for version 10.1.0 and
  10.0.0 are identical.

1.1.delta
---------
- Cantabular version 10.0.0 is now the default version. The file format for version 10.0.0 and
  9.3.0 are identical.
- Use the Codebook_Mnemonic from Category_Mapping.csv as the variable name.
- Drop the Parent_Classification_Mnemonic from VariableMetadata in the GraphQL schema. This
  information can be obtained from the codebook and its contents are ambiguous since a variable
  name can now be either the Classification_Mnemonic or Codebook_Mnemonic.

1.1.gamma
---------
- In `--best-effort` mode don't drop tables (ONS datasets) which use variables (ONS classifications) that
  are not listed as belonging to the table dataset (ONS database).

1.1.beta
--------
- Added `--best-effort` flag to discard invalid data and make a best effort
  attempt to generate output files.
  - This replaces the `fixup.py` script.
- Formatted and customizable output filenames.
- Support for Cantabular version 9.2.0 formatting.
- Rework on mandatory fields.
- Added 2011 1% sample metadata.

1.1.alpha
---------
- Updated code to work with metadata schema version 1.1.
- Updated fixup.py script to work with latest drop of CSV source files.

1.0.gamma
---------
- Categories for geographic variables are read from a separate lookup file which is specified
  using the `-g` flag.
  - No categories for geographic variables will be loaded if a geography lookup file is not
    specified.
  - Categories for geographic variables must not be specified in the main set of CSV files.
- Classifications are automatically created for geographic variables.
  - The classification will have the same name as the variable.
  - The main set of CSV files must not contain classifications for geographic variables.
- Added logging to fixup.py
- The built-in descriptions fields for variables and datasets are now populated.

1.0.beta
--------
- Supports Cantabular version 9.3.0
  - Tables are now a built-in concept in `cantabular-metadata` and are written to their own JSON file
  - The generated JSON files must now be supplied to `cantabular-metadata` via environment variables
  - Every table must have at least one variable (geographic or non-geographic)
- Clearer error message if invalid directories supplied to ons_csv_to_ctb_json_main.py

1.0.alpha
---------
- Supports metadata schema version 1.0
- Supports Cantabular version 9.2.0
