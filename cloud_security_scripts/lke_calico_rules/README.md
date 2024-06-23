# Linode LKE Cluster Management Script

This script manages Linode Kubernetes Engine (LKE) clusters by applying Calico network policies. It includes features for retrying commands with exponential backoff and handles clusters that are not yet fully provisioned or are empty.

### For each cluster, the script:
* Downloads the cluster configuration file with retry logic.
* Exports the downloaded configuration file.
* Checks the availability of nodes using kubectl get nodes with retry logic.
* If node check fails after retries, it deletes the cluster.
* Applies Calico network policies using calicoctl.

## Prerequisites

These binaries is available:
* curl
* jq
* kubectl
* calicoctl 
* A valid Linode API token with permissions to manage LKE clusters

## Environment Variables
- LINODE_TOKEN: Your Linode API token

## Usage
- Set up the environment variable: 
```
export LINODE_TOKEN="your_linode_api_token"
```
Ensure that the LINODE_TOKEN environment variable is set with your Linode API token

Run the script:
Execute the script to apply Calico rules to your LKE clusters:

    ./lke_calico_rules_e2e.sh

## Script Details
* RETRIES: Number of retry attempts for commands (default: 3).
* DELAY: Delay between retries in seconds (default: 30).