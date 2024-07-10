SHELL := '/bin/bash'

.PHONY: downloads
downloads:
	@-python3 -m venv ./etl/.venv && \
		./etl/.venv/bin/pip install -r etl/requirements.txt && \
		./etl/.venv/bin/python3 etl/downloader.py
