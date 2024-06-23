PYTHON ?= python3

.PHONY: lint
lint:
	$(PYTHON) -m isort .
	$(PYTHON) -m autoflake --recursive .
	$(PYTHON) -m black --verbose .
	$(PYTHON) -m pylint --disable=too-many-locals,line-too-long,missing-docstring,broad-exception-caught,parse-error .

.PHONY: run
run:
	$(PYTHON) tod_report_uploader.py