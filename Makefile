.PHONY: server
server:
	gunicorn --daemon --bind 127.0.0.1:8000 server:app

venv:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
