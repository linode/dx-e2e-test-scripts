"""
Module containing the LinodeCommands class for interacting with Linode object storage.

This class provides methods to generate Linode CLI commands for listing, downloading,
and removing objects in a Linode cluster.
"""


class LinodeCommands:
    """
    Set of Linode CLI commands to interact with obj storage.
    """

    def __init__(self, cli_path="/usr/local/bin/linode-cli"):
        """
        Initialize LinodeCommands with the path to the Linode CLI.
        """
        self.cli_path = cli_path

    def get_list_command(self, cluster):
        """
        Generate Linode CLI command for listing objects in a cluster.
        """
        return [
            self.cli_path,
            "obj",
            "la",
            "--cluster",
            cluster,
        ]

    def get_download_command(self, cluster, bucket, file_name, destination):
        """
        Generate Linode CLI command for downloading an object from a bucket.
        """
        return [
            self.cli_path,
            "obj",
            "get",
            "--cluster",
            cluster,
            bucket,
            file_name,
            destination,
        ]

    def get_remove_command(self, cluster, bucket, file_name):
        """
        Generate Linode CLI command for removing an object from a bucket.
        """
        return [
            self.cli_path,
            "obj",
            "rm",
            "--cluster",
            cluster,
            bucket,
            file_name,
        ]
