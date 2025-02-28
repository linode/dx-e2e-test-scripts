#!/bin/bash

RETRIES=3
DELAY=30
# Path to the binary installation script
INSTALL_SCRIPT_PATH="./install_requirements.sh"

# Function to retry a command with exponential backoff
retry_command() {
    local retries=$1
    local wait_time=60
    shift
    until "$@"; do
        if ((retries == 0)); then
            echo "Command failed after multiple retries. Exiting."
            exit 1
        fi
        echo "Command failed. Retrying in $wait_time seconds..."
        sleep $wait_time
        ((retries--))
        wait_time=$((wait_time * 2))
    done
}

check_linode_token() {
    if [ -z "$LINODE_TOKEN" ]; then
        echo "Error: LINODE_TOKEN is not set. Please export it and try again."
        exit 1
    fi
}

# Function to check if binaries are available, if not, call the installation script
check_and_install_binaries() {
    if ! command -v kubectl &> /dev/null || ! command -v calicoctl &> /dev/null; then
        echo "kubectl or calicoctl not found. Running the installation script..."
        if [ -x "$INSTALL_SCRIPT_PATH" ]; then
            $INSTALL_SCRIPT_PATH
        else
            echo "Error: Installation script $INSTALL_SCRIPT_PATH not found or not executable."
            exit 1
        fi
    else
        echo "kubectl and calicoctl are already installed."
    fi
}

# Check if LINODE_TOKEN is set before proceeding
check_linode_token

# Check and install required binaries before proceeding
check_and_install_binaries

# Fetch the list of LKE cluster IDs
CLUSTER_IDS=$(curl -s -H "Authorization: Bearer $LINODE_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.linode.com/v4/lke/clusters" | jq -r '.data[].id')

# Check if CLUSTER_IDS is empty
if [ -z "$CLUSTER_IDS" ]; then
    echo "All clusters have been cleaned and properly destroyed. No need to apply inbound or outbound rules"
    exit 0
fi

for ID in $CLUSTER_IDS; do
    echo "Applying Calico rules to nodes in Cluster ID: $ID"

    # Download cluster configuration file with retry
    for ((i=1; i<=RETRIES; i++)); do
        config_response=$(curl -sH "Authorization: Bearer $LINODE_TOKEN" "https://api.linode.com/v4/lke/clusters/$ID/kubeconfig")
        if [[ $config_response != *"kubeconfig is not yet available"* ]]; then
            echo $config_response | jq -r '.[] | @base64d' > "/tmp/${ID}_config.yaml"
            break
        fi
        echo "Attempt $i to download kubeconfig for cluster $ID failed. Retrying in $DELAY seconds..."
        sleep $DELAY
    done

    if [[ $config_response == *"kubeconfig is not yet available"* ]]; then
        echo "kubeconfig for cluster id:$ID not available after $RETRIES attempts, mostly likely it is an empty cluster. Skipping..."
    else
        # Export downloaded config file
        export KUBECONFIG="/tmp/${ID}_config.yaml"

        retry_command $RETRIES kubectl get nodes

        # check exit status of previous command is not zero then proceed to delete the cluster
        if [ $? -ne 0 ]; then
            echo "kubectl get nodes failed after retries. Deleting cluster ID: $ID"

            # Add Linode API call to delete the cluster
            curl -X DELETE -H "Authorization: Bearer $LINODE_TOKEN" \
                 "https://api.linode.com/v4/lke/clusters/$ID"

            continue  # Move to the next cluster in the loop
        fi

        retry_command $RETRIES calicoctl patch kubecontrollersconfiguration default --allow-version-mismatch --patch='{"spec": {"controllers": {"node": {"hostEndpoint": {"autoCreate": "Enabled"}}}}}'

        retry_command $RETRIES calicoctl apply --allow-version-mismatch -f "$(pwd)/template/lke-policy.yaml"
    fi
done
