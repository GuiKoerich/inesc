venv:
	virtualenv venv && source $(shell pwd)/venv/bin/activate && pip install -r requirements.txt && deactivate;

install: venv