SHELL := '/bin/bash'

.PHONY: downloads
downloads:
	@-export PYTHONPATH="${PYTHONPATH}:${pwd}/etl/" && \
		python3 -m venv ./etl/.venv && \
		./etl/.venv/bin/pip install -r etl/requirements.txt && \
		./etl/.venv/bin/python3 etl/downloader.py

.PHONY: sql_loader
sql_loader:
	@-export PYTHONPATH="${PYTHONPATH}:${pwd}/etl/" && \
		python3 -m venv ./etl/.venv && \
		./etl/.venv/bin/pip install -r etl/requirements.txt && \
		./etl/.venv/bin/python3 etl/loader.py