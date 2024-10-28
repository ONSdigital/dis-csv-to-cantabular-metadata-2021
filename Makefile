## ----------------------------------------------------------------------------------------------------
## This script is to remove as much manual steps as possible when generating the Json from the CSV
##
## Required params:
## csv_zip_file  - Should be the location of the zip file containing the CSV files
## geography_dir - Should be the loction of the directory containing the geography files
## Optional params:
## best_effort - If added and set to 'true' the underyling python script will run in best effort mode
##
## Example usage:
##
## make run csv_zip_file=/path/to/csv_zip_file.zip geography_dir=/path/to/geography best_effort=true
##
## ----------------------------------------------------------------------------------------------------

.PHONY: help
help:
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

.PHONY: run

CSV_ZIP_FILE := $(csv_zip_file)
GEOGRAPHY_DIR := $(geography_dir)
BEST_EFFORT := $(best_effort)

TODAYS_DATE := $(shell date +%Y-%m-%d)
CENSUS_CSV_DIR := census_csv_$(TODAYS_DATE)
METADATA_DIR := ctb_metadata_files
METADATA_VERSION_FILE := $(CENSUS_CSV_DIR)/Metadata_Version.csv
STOCK_METADATA_FILE := metadata.graphql

run: pre_flight_checks unpack clean_workspace run_script

pre_flight_checks:
	@if [ -z "$(CSV_ZIP_FILE)" ]; then \
		echo "Error: 'csv_zip_file' file argument is required. Provide as csv_zip_file=/path/to/csv_zip_file.zip"; \
		exit 1; \
	fi
	@if [ -z "$(GEOGRAPHY_DIR)" ]; then \
		echo "Error: 'geography_dir' directory argument is required. Provide as geography_dir=/path/to/geography"; \
		exit 1; \
	fi
	@if [ ! -f $(CSV_ZIP_FILE) ]; then \
		echo "Error: ZIP file '$(CSV_ZIP_FILE)' does not exist."; \
		exit 1; \
	fi
	@if [ ! -d $(GEOGRAPHY_DIR) ]; then \
		echo "Error: Geography directory '$(GEOGRAPHY_DIR)' does not exist."; \
		exit 1; \
	fi
	@if [ ! -d $(METADATA_DIR) ]; then \
		echo "Error: Metadata directory '$(METADATA_DIR)' does not exist."; \
		exit 1; \
	fi

clean_workspace:
	@echo "Cleaning out old files from directory $(METADATA_DIR)"; \
	rm -f $(METADATA_DIR)/cantabm*;

unpack:
	@echo "Unzipping $(CSV_ZIP_FILE) to $(CENSUS_CSV_DIR)..."
	@unzip -q $(CSV_ZIP_FILE) -d $(CENSUS_CSV_DIR)
	@echo "Unzipping complete."

run_script:

	@if [ ! -f $(METADATA_VERSION_FILE) ]; then \
		echo "Error: Metadata_Version.csv file '$(METADATA_VERSION_FILE)' does not exist."; \
		exit 1; \
	fi

	@echo "Running the Python script with the parameters..."
	@if [ "$(BEST_EFFORT)" = "true" ]; then \
		python bin/ons_csv_to_ctb_json_main.py -i $(CENSUS_CSV_DIR) -d $(GEOGRAPHY_DIR) -o $(METADATA_DIR) -m $(basename $(notdir $(CSV_ZIP_FILE))) \
			-b $(shell awk -F, 'NR==1 {for (i=1; i<=NF; i++) if ($$i=="Metadata_Version_Number") col=i} NR>1 {val=$$col} END {print (val ? val : 1)}' $(METADATA_VERSION_FILE)) \--best-effort; \
	else \
		python bin/ons_csv_to_ctb_json_main.py -i $(CENSUS_CSV_DIR) -d $(GEOGRAPHY_DIR) -o $(METADATA_DIR) -m $(basename $(notdir $(CSV_ZIP_FILE))) \
			-b $(shell awk -F, 'NR==1 {for (i=1; i<=NF; i++) if ($$i=="Metadata_Version_Number") col=i} NR>1 {val=$$col} END {print (val ? val : 1)}' $(METADATA_VERSION_FILE)) ; \
	fi; \
	$(MAKE) remove_unpacked_csvs || true

	@echo "Making a copy of the metadata.graphql template..."
	@cd $(METADATA_DIR) && \
	NEW_GRAPH_QL_NAME=$$(ls cantabm_*_tables-md_*.json | head -n 1 | sed 's/_tables-md_/_metadata_/; s/.json/.graphql/'); \
	echo "calling file $$NEW_GRAPH_QL_NAME"; \
	cp $(STOCK_METADATA_FILE) $$NEW_GRAPH_QL_NAME; \
	echo "Done."

	@echo "Creating zip of generated files..."
	@cd $(METADATA_DIR) && \
	ZIP_NAME=$$(ls cantabm_*_tables-md_*.json | sed 's/_tables-md//; s/.json//').zip; \
	echo "calling zip $$ZIP_NAME"; \
	zip -r $$ZIP_NAME cantabm*; \
	echo "Done."

remove_unpacked_csvs:
	@echo "Cleaning up upacked csvs..."
	@rm -rf $(CENSUS_CSV_DIR)
	@echo "Done."
