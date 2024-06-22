"""
Helper functions for various operations including HTTP requests, command execution, and others.
"""

import subprocess

import requests

# Dictionary mapping file keywords to GitHub API URLs
latest_release_urls = {
    "cli": "https://api.github.com/repos/linode/linode-cli/releases/latest",
    "sdk": "https://api.github.com/repos/linode/linode_api4-python/releases/latest",
    "linodego": "https://api.github.com/repos/linode/linodego/releases/latest",
    "terraform": "https://api.github.com/repos/linode/terraform-provider-linode/releases/latest",
    "packer": "https://api.github.com/repos/linode/packer-plugin-linode/releases/latest",
    "ansible": "https://api.github.com/repos/linode/ansible_linode/releases/latest",
    "py-metadata": "https://api.github.com/repos/linode/py-metadata/releases/latest",
    "go-metadata": "https://api.github.com/repos/linode/go-metadata/releases/latest",
}


def get_release_version(file_name):
    """
    Get the latest release version from GitHub API based on the file name.
    """
    url = latest_release_urls.get(file_name, "")
    if not url:
        print(f"Error: Unknown file type for '{file_name}'.")
        return None

    try:
        response = requests.get(
            url, timeout=10
        )  # Add timeout to prevent indefinite hang
        response.raise_for_status()  # Check for HTTP errors

        release_info = response.json()
        version = release_info["tag_name"]

        # Remove 'v' prefix if it exists
        if version.startswith("v"):
            version = version[1:]

        return version

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {file_name} release information:", e)
    except KeyError:
        print(
            f"Error: Unable to fetch release information from GitHub API for {file_name}."
        )

    return None


def upload_encoded_xml_file(url, payload, headers):
    """
    Upload encoded XML file to a specified URL using HTTP POST.
    """
    try:
        response = requests.post(
            url, data=payload, headers=headers, timeout=10
        )  # Add timeout to prevent indefinite hang
        response.raise_for_status()  # Check for HTTP errors
        return response
    except requests.exceptions.RequestException as e:
        print("Error uploading XML file:", e)
        return None


def execute_command(args):
    """
    Execute a command with subprocess.run and capture stdout and stderr.
    """
    try:
        process = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        return process
    except subprocess.CalledProcessError as e:
        print(f"Error executing command with args: {args}, with error: {e}")
        raise  # Re-raise the exception to indicate failure
