#!/bin/bash

set -e  # Exit on error

# Function to download binaries if they don't exist
install_requirements() {
    if ! command -v kubectl &> /dev/null; then
        echo "Downloading kubectl..."
        curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl
        mv kubectl /usr/local/bin/kubectl
    else
        echo "kubectl is already installed."
    fi

    if ! command -v calicoctl &> /dev/null; then
        echo "Downloading calicoctl..."
        curl -LO "https://github.com/projectcalico/calico/releases/download/v3.25.0/calicoctl-linux-amd64"
        chmod +x calicoctl-linux-amd64
        mv calicoctl-linux-amd64 /usr/local/bin/calicoctl
    else
        echo "calicoctl is already installed."
    fi
}

# Run the installation function
install_requirements