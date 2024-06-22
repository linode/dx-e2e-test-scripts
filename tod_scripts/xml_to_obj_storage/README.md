# XML to Linode Object Storage

This package is designed to be used as a Git submodule for GitHub Actions (GHA) test executions within the DX team. It comprises two essential scripts:

1. GitHub Fields Addition Script (`add_to_xml_test_report.py`)
- The first script enhances the generated XML test report by adding GitHub-specific fields. This helps in providing additional information relevant to GitHub Actions.

2. External Object Storage Upload Script (`test_report_upload_script.py`)
- The second script is responsible for uploading the modified XML test report to an external linode object storage. This ensures that the enhanced test report is stored and accessible externally.

Usage
To incorporate this package into your GHA workflows, add it as a submodule and integrate the provided scripts into your testing pipeline.

e.g. `git submodule add https://github.com/linode/TOD-test-report-uploader.git <intended_path>`

Make sure to check for the latest updates and releases in the repository for any improvements or new features.

Feel free to contribute, report issues, or provide feedback to help enhance the functionality of this package for the DX team's testing processes.


