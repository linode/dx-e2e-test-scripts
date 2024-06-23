PYTHON ?= python3

.PHONY: lint
lint:
	$(PYTHON) -m isort .
	$(PYTHON) -m autoflake --recursive .
	$(PYTHON) -m black --verbose .
	$(PYTHON) -m pylint --disable=too-many-locals,line-too-long,missing-docstring,broad-exception-caught,parse-error .

.PHONY: merge_terraform
merge_terraform:
	$(PYTHON) ./terraform_tests/merge_terraform_results.py

.PHONY: merge_ansible
merge_ansible:
	$(PYTHON) ./ansible_tests/merge_ansible_results.py

.PHONY: add_gha_info
add_gha_info:
	$(PYTHON) ./scripts/add_gha_info_to_xml.py

.PHONY: upload
upload:
	$(PYTHON) ./scripts/xml_to_obj.py