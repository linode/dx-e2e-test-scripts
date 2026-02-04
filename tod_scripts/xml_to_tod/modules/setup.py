"""
This module provides functions to setup Linode configuration by loading environment variables,
checking if required environment variables are set, and verifying the installation of Linode CLI.
"""

import os
import subprocess
import sys
import hvac

from dotenv import load_dotenv


def load_environment_variables():
    """Load environment variables from a .env file."""
    dotenv_path = os.path.join(
        os.path.dirname(__file__), "..", ".env"
    )  # Adjust the path as per your file location
    load_dotenv(dotenv_path=dotenv_path)


def get_secret_from_vault(secret_path):
    """Retrieve secret from Vault."""
    vault_client = hvac.Client(
        url=os.getenv("VAULT_ADDR", "http://127.0.0.1:8200"),
        token=os.getenv("VAULT_TOKEN")
    )

    try:
        response = vault_client.secrets.kv.read_secret_version(path=secret_path)
        return response['data']['data']
    except hvac.exceptions.InvalidPath as e:
        print(f"Error: {e}")
        sys.exit(1)


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

    # Retrieve secrets from Vault if not set
    if not os.getenv("LINODE_CLI_TOKEN"):
        vault_secret_path = "dx"

        print("Fetching secrets from Vault...")
        secrets = get_secret_from_vault(secret_path=vault_secret_path)
        os.environ["LINODE_CLI_TOKEN"] = secrets["LINODE_CLI_TOKEN"]
        os.environ["LINODE_CLI_OBJ_ACCESS_KEY"] = secrets["LINODE_CLI_OBJ_ACCESS_KEY"]
        os.environ["LINODE_CLI_OBJ_SECRET_KEY"] = secrets["LINODE_CLI_OBJ_SECRET_KEY"]

    # Check if the environment variables are set
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
