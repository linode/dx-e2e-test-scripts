# XML to Linode Object Storage

This package is designed to be used as a Git submodule in GitHub Actions (GHA) within the DX team.

Note: These set of scripts are meant to be specifically used internally by the DX team's projects

Here is the list of quick summaries of each script:
- `scripts/add_gha_info_to_xml.py`: modifies an XML file by adding branch name, GitHub Actions run ID, run number, and the release version tag of the relevant Linode project, fetched from the GitHub API, based on the XML file name
- `scripts/xml_to_obj.py`: uploads a specified file to Linode Object storage using AWS S3 API
- `ansible-tests/merge_ansible_results.py` and `terraform-tests/merge_terraform_results.py`: merges multiple JUnit XML test result files from a specified directory into a single XML file, aggregating failure, skipped, error, and test counts


## **Pre requisite:**
- Python 3.x
- Required Python packages (listed in requirements.txt)


## **Installation and Usage:**

### Usage in GHA 

1. Define this repo as submodule in the project repo. E.g. `.gitmodules` file should look similar to below:
```
[submodule "e2e_scripts"]
	path = e2e_scripts
	url = git clone https://github.com/linode/dx-e2e-test-scripts
```

2. Add step to Install dependencies in workflow `.yaml` file
```
pip install -r requirements.txt
```

3. Add Linode object storage token values to GH Secrets
```
LINODE_CLI_OBJ_ACCESS_KEY=***
LINODE_CLI_OBJ_SECRET_KEY=***
```

4. Call the wanted script based on repository
```
python xml_to_obj_storage/scripts/add_gha_info_to_xml.py
python xml_to_obj_storage/terraform-tests/merge_terraform_results.py
```




