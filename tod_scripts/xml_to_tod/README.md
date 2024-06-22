# XML to TOD (Test Outcome Database)

This repository contains scripts to process XML test report files and upload them to the Test Outcome Database (TOD). These scripts handle downloading XML files from Linode Object Storage, processing them to ensure they meet TOD's requirements, and then uploading the processed reports to TOD.

Note: This script is meant to be specifically used internally by the DX team's projects

## **Pre requisite:**
- Python 3.x
- Linode CLI
- Required Python packages (listed in requirements.txt)


## **Installation and Usage:**

- Clone the repo in Test VM or any unix machine
```
git clone https://github.com/linode/dx-e2e-test-scripts
```
- Install dependencies
```
cd xml_to_linode
pip install -r requirements.txt
```
- Set up environment (.env) variable in script's root directory
```
# TOKENS
LINODE_CLI_TOKEN=***
LINODE_CLI_OBJ_ACCESS_KEY=***
LINODE_CLI_OBJ_SECRET_KEY=***

# Linode Object Storage env variables
CLUSTER='us-southeast-1'
BUCKET='dx-test-results'

# TOD URL
URL="http://198.19.5.79:7272/builds/"

# Test Report Variables
TEAM_NAME='DX Team'
```

- Run the script
```
python scripts/upload_xml_to_tod.py
```

This script performs the following tasks:

- Downloads all XML test report files from the specified Linode Object Storage bucket.
- Processes each XML file to ensure it meets TOD's requirements.
- Uploads the processed XML files to TOD.
- Logs the upload status and any errors encountered.


Setting it as cronjob in ECP machine:
1. SSH to ECP machine, `ssh root@198.19.5.95`
2. Edit cront job, `crontab -e`
3. Add line to the file, `0 */2 * * * cd /root/DX-Tests/test_report_uploader && python3 main.py >> logs.txt 2>&1`
