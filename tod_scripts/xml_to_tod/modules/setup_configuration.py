"""
This module provides functions to setup Linode configuration by loading environment variables,
checking if required environment variables are set, and verifying the installation of Linode CLI.
"""

import os
import subprocess
import sys

from dotenv import load_dotenv


def load_environment_variables():
    """Load environment variables from a .env file."""
    dotenv_path = os.path.join(
        os.path.dirname(__file__), "..", ".env"
    )  # Adjust the path as per your file location
    load_dotenv(dotenv_path=dotenv_path)


def check_required_env_vars():
    """Check if required environment variables are set."""
    required_env_vars = [
        "LINODE_CLI_TOKEN",
        "LINODE_CLI_OBJ_ACCESS_KEY",
        "LINODE_CLI_OBJ_SECRET_KEY",
        "CLUSTER",
        "BUCKET",
        "URL",
    ]
    missing_vars = [var for var in required_env_vars if var not in os.environ]

    if missing_vars:
        print("Error: The following environment variables are not set:")
        for var in missing_vars:
            print(f"- {var}")
        sys.exit(1)


def check_linode_cli_installed():
    """Check if Linode CLI is installed."""
    try:
        subprocess.run(
            ["linode-cli", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError:
        print(
            "linode-cli is not installed. Please make sure Linode CLI is installed..."
        )


def setup_linode_configuration():
    """Setup Linode configuration by checking environment variables and CLI installation."""
    load_environment_variables()
    check_required_env_vars()
    check_linode_cli_installed()
