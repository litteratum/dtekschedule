venv:
	uv sync

.PHONY: clean
clean:
	rm -rf .venv

.PHONY: server
server:
	uv run gunicorn --daemon --bind 127.0.0.1:8000 server:app
