import argparse
import sys
import xml.etree.ElementTree as ET

import requests

latest_release_urls = {
    "cli": "https://api.github.com/repos/linode/linode-cli/releases/latest",
    "sdk": "https://api.github.com/repos/linode/linode_api4-python/releases/latest",
    "linodego": "https://api.github.com/repos/linode/linodego/releases/latest",
    "terraform": "https://api.github.com/repos/linode/terraform-provider-linode/releases/latest",
    "packer": "https://api.github.com/repos/linode/packer-plugin-linode/releases/latest",
    "ansible": "https://api.github.com/repos/linode/ansible_linode/releases/latest",
    "py_metadata": "https://api.github.com/repos/linode/py-metadata/releases/latest",
    "go_metadata": "https://api.github.com/repos/linode/go-metadata/releases/latest",
}


def get_release_version(file_name):
    for key, url in latest_release_urls.items():
        if key in file_name:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Check for HTTP errors

                release_info = response.json()
                version = release_info["tag_name"]

                # Remove 'v' prefix if it exists
                if version.startswith("v"):
                    version = version[1:]

                return str(version)

            except requests.exceptions.RequestException as e:
                print("Error:", e)
            except KeyError:
                print("Error: Unable to fetch release information from GitHub API.")
    return "unknown log type"


def add_fields_to_xml(branch_name, gha_run_id, gha_run_number, xml_file_path):
    # Open and parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Create new elements for the information
    branch_name_element = ET.Element("branch_name")
    branch_name_element.text = branch_name

    gha_run_id_element = ET.Element("gha_run_id")
    gha_run_id_element.text = gha_run_id

    gha_run_number_element = ET.Element("gha_run_number")
    gha_run_number_element.text = gha_run_number

    gha_release_tag_element = ET.Element("release_tag")
    gha_release_tag_element.text = get_release_version(xml_file_path)

    # Add the new elements to the root of the XML
    root.append(branch_name_element)
    root.append(gha_run_id_element)
    root.append(gha_run_number_element)
    root.append(gha_release_tag_element)

    # Save the modified XML
    modified_xml_file_path = xml_file_path  # Overwrite it
    tree.write(modified_xml_file_path)

    print(f"Modified XML saved to {modified_xml_file_path}")


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print(
            "Usage: python add_gha_info_to_xml.py \
         --branch_name <branch_name> \
         --gha_run_id <gha_run_id> \
         --gha_run_number <gha_run_number> \
         --xmlfile <file_name>"
        )
        sys.exit(1)

    file_name = sys.argv[3]

    if not file_name:
        print("Error: The provided file name is empty or invalid.")
        sys.exit(1)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Modify XML with workflow information")
    parser.add_argument("--branch_name", required=True)
    parser.add_argument("--gha_run_id", required=True)
    parser.add_argument("--gha_run_number", required=True)
    parser.add_argument("--release_tag", required=False)
    parser.add_argument("--xmlfile", required=True)  # Added argument for XML file path

    args = parser.parse_args()

    add_fields_to_xml(
        args.branch_name, args.gha_run_id, args.gha_run_number, args.xmlfile
    )
