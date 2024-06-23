# DX E2E Test Scripts

This repository contains various end-to-end (E2E) test scripts designed for different purposes, including XML transformations and cloud security validations.

## Project structure:

### tod_scripts
This directory includes scripts for XML transformations and uploading XML results to object storage and Test Ooutcome Database (TOD).
* **xml_to_obj_storage:** Contains scripts and configurations to transform XML data and upload it to object storage.
* **xml_to_tod:** Contains script to download all test reports from Linode Object storage and process them to TOD.

### cloud_security_scripts
This directory includes scripts related to cloud security validations, specifically for LKE Calico rules.
**lke_calico_rules:** Contains scripts and templates for LKE Calico rules E2E testing.

## Getting Started
To set up and run these scripts, follow the instructions in each subdirectory's README.md file. Generally, you'll need to install dependencies listed in requirements.txt and follow any specific setup instructions provided.

## Contribution Guidelines

Want to improve DX E2E Test scripts? Please start [here](CONTRIBUTING.md).