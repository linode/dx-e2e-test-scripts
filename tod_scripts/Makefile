PYTHON ?= python3

.PHONY: lint
lint:
	$(PYTHON) -m isort xml_to_tod
	$(PYTHON) -m autoflake --recursive xml_to_tod
	$(PYTHON) -m black --verbose xml_to_tod
	$(PYTHON) -m pylint --disable=too-many-locals,line-too-long,missing-docstring,broad-exception-caught xml_to_tod
