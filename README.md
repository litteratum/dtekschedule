# DTEK Shutdown schedule
A tool that simplifies checking power shutdown schedules for DTEK customers.

Consists of two parts:
1. `main.py` script that uses Selenium to open shutdown schedule for a specific address and make screenshots
2. `server.py` app that serves the screenshots via a web interface

## Usage
1. Prepare an environment: `make venv`
2. Prepare a configuration file under configs/{user}.json. See [configuration example](#configuration-example)
3. Run `main.py -c configs/{user}.json`
4. Start the server: `python server.py`
5. Open `http://localhost:6789/{user}` in your browser

It is recommended to run the server behind a reverse proxy like Nginx.

## Configuration example
```json
{
  "city": "М. Місто",
  "street": "Вул. Вулиця",
  "house": "17/B"
}
```
