"""
Script to upload XML test reports to TOD (Test Outcome Database).

This script downloads XML files from Linode Object Storage, processes them,
and uploads them to TOD.
"""

import base64
import datetime
import json
import logging
import os
import xml.etree.ElementTree as ET

from modules.helpers import (
    execute_command,
    get_release_version,
    upload_encoded_xml_file,
)
from modules.linode_cli_cmds import LinodeCommands
from modules.setup import setup_linode_configuration

# Configure logging
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
log_file_path = f"logs/{timestamp}_log.txt"
logging.basicConfig(
    filename=log_file_path,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


def log_and_print(message, level=logging.INFO):
    """
    Log a message and also print it to console.
    """
    logging.log(level, message)
    print(message)


def get_software_name(file_name):
    """
    Determine the software name based on the XML file name.
    """
    software_mapping = {
        "cli": "linode-cli",
        "sdk": "linode_api4",
        "linodego": "linodego",
        "terraform": "linode-terraform",
        "packer": "packer",
        "ansible": "ansible_linode",
        "py_metadata": "py-metadata",
        "go_metadata": "go-metadata",
    }

    for key, software_name in software_mapping.items():
        if key in file_name:
            return software_name

    return "unknown software type"


def change_xml_report_to_tod_acceptable_version(file_path):
    """
    Modify XML report to be acceptable by TOD (Test Outcome Database).
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    if len(root.findall("testsuite")) > 1:
        testsuites_element = root

        # Aggregate total values
        total_tests = int(testsuites_element.get("tests", 0))
        total_failures = int(testsuites_element.get("failures", 0))
        total_errors = int(testsuites_element.get("errors", 0))
        total_skipped = int(testsuites_element.get("skipped", 0))

        # Create a new <testsuites> element with aggregated values
        new_testsuites = ET.Element("testsuites")
        new_testsuites.set("tests", str(total_tests))
        new_testsuites.set("failures", str(total_failures))
        new_testsuites.set("errors", str(total_errors))
        new_testsuites.set("skipped", str(total_skipped))

        # Create a new <testsuite> element under <testsuites>
        new_testsuite = ET.SubElement(
            new_testsuites, "testsuite", attrib=testsuites_element.attrib
        )

        # Move <testcase> elements under the new <testsuite>
        for testcase in root.findall(".//testcase"):
            new_testcase = ET.SubElement(
                new_testsuite, "testcase", attrib=testcase.attrib
            )
            for child in testcase:
                new_testcase.append(child)

        # Copy essential metadata
        for key in ["branch_name", "gha_run_id", "gha_run_number", "release_tag"]:
            element = ET.SubElement(new_testsuites, key)
            element.text = root.find(key).text if root.find(key) is not None else ""

        # Save the modified XML back to the file
        try:
            new_tree = ET.ElementTree(new_testsuites)
            new_tree.write(file_path, encoding="UTF-8", xml_declaration=True)
            log_and_print(
                f"{timestamp}: XML content successfully overwritten to {file_path}"
            )
        except Exception as e:
            log_and_print(
                f"{timestamp}: Error writing XML content: {str(e)}", level=logging.ERROR
            )


def download_and_upload_xml_files(cluster, bucket, url):
    """
    Download XML test reports from Linode object storage, modify and upload them to TOD.
    """
    linode_commands = LinodeCommands()
    list_process = execute_command(linode_commands.get_list_command(cluster=cluster))
    lines_of_all_files = list_process.stdout.decode().split("\n")

    xml_files = [
        line.split("/")[-1]
        for line in lines_of_all_files
        if bucket in line and line.endswith(".xml")
    ]

    team_name = os.environ.get("TEAM_NAME", "default_team_name")
    current_dir = os.getcwd()
    report_dir = os.path.join(current_dir, "reports")

    for file in xml_files:
        file_path = os.path.join(report_dir, file)
        result = execute_command(
            linode_commands.get_download_command(
                cluster=cluster, bucket=bucket, file_name=file, destination=file_path
            )
        )

        if result.returncode == 0:
            change_xml_report_to_tod_acceptable_version(file_path)

            with open(file_path, "r", encoding="utf-8") as f:
                encoded_file = str(
                    base64.b64encode(f.read().encode("utf-8")).decode("utf-8")
                )

            software_name = get_software_name(file_name=file)

            tree = ET.parse(file_path)
            root = tree.getroot()

            release_version_value = (
                root.find("release_tag").text
                if root.find("release_tag") is not None
                else get_release_version(file)
            )

            testsuite_failures = (
                root.find("testsuite").get("failures")
                if root.find("testsuite") is not None
                else 0
            )
            failures = (
                root.find("failures").text if root.find("failures") is not None else 0
            )
            pass_value = int(testsuite_failures or failures) == 0

            tag_value = (
                f"GHA ID: {root.find('gha_run_id').text} Run ID: {root.find('gha_run_number').text}"
                if root.find("gha_run_id").text and root.find("gha_run_number").text
                else ""
            )

            data = {
                "team": team_name,
                "softwareName": software_name,
                "semanticVersion": release_version_value,
                "buildName": software_name,
                "pass": pass_value,
                "xunitResults": [encoded_file],
                "tag": tag_value,
                "branchName": (
                    root.find("branch_name").text
                    if root.find("branch_name") is not None
                    else "N/A"
                ),
            }

            headers = {"Content-Type": "application/json"}
            data_json = json.dumps(data)

            response = upload_encoded_xml_file(url, data_json, headers)

            if response.status_code == 201:
                log_and_print(f"{timestamp}: {file} uploaded to TOD successfully.")
                result = execute_command(
                    linode_commands.get_remove_command(
                        cluster=cluster, bucket=bucket, file_name=file
                    )
                )

                if result.returncode == 0:
                    log_and_print(f"{timestamp}: {file} deleted from object storage.")
                else:
                    log_and_print(
                        f"{timestamp}: Error deleting {file} from object storage. "
                        f"Command returned non-zero exit code: {result.returncode}",
                        level=logging.ERROR,
                    )
            else:
                log_and_print(
                    f"{timestamp}: POST request for file {file} failed with status code: {response.status_code}",
                    level=logging.ERROR,
                )
        else:
            log_and_print(
                f"{timestamp}: Error downloading {file} from object storage. "
                f"Command returned non-zero exit code: {result.returncode}",
                level=logging.ERROR,
            )


def main():
    """
    Main function to orchestrate the download, modification, and upload of XML test reports.
    """
    try:
        setup_linode_configuration()

        cluster = os.environ.get("CLUSTER")
        bucket = os.environ.get("BUCKET")
        url = os.environ.get("URL")

        download_and_upload_xml_files(cluster, bucket, url)

    except Exception as e:
        log_and_print(
            f"An error occurred in the main function: {str(e)}", level=logging.ERROR
        )


if __name__ == "__main__":
    main()
