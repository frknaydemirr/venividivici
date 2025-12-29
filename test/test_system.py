import multiprocessing
import os
import socket
import time

import pytest
import requests

from server.common.check_schema import check_schema
from server.common.schemas.cities import get_multiple_cities_schema
from server.common.schemas.countries import get_country_schema
from server.server import create_test_app


SERVER_HOST = "127.0.0.1"
SERVER_START_TIMEOUT = 30


def _run_test_server(port: int) -> None:
	"""Start a single-process Sanic test app on the requested port."""
	app_name = os.getenv("APP_NAME", "venividivici")
	app = create_test_app(app_name)
	app.run(host=SERVER_HOST, port=port, single_process=True, access_log=False, auto_reload=False)


def _find_free_port() -> int:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.bind((SERVER_HOST, 0))
		return sock.getsockname()[1]


def _wait_until_ready(base_url: str) -> None:
	deadline = time.time() + SERVER_START_TIMEOUT
	last_error = None

	while time.time() < deadline:
		try:
			response = requests.get(f"{base_url}/countries/8", timeout=1)
			if response.status_code == 200:
				return
		except requests.RequestException as exc:
			last_error = exc
		time.sleep(0.5)

	raise RuntimeError("Timed out waiting for system server to become ready") from last_error


@pytest.fixture(scope="module")
def system_base_url():
	port = _find_free_port()
	process = multiprocessing.Process(target=_run_test_server, args=(port,), daemon=True)
	process.start()

	base_url = f"http://{SERVER_HOST}:{port}"

	try:
		_wait_until_ready(base_url)
		yield base_url
	finally:
		if process.is_alive():
			process.terminate()
		process.join(timeout=5)


def test_get_country_via_http(system_base_url):
	response = requests.get(f"{system_base_url}/countries/8", timeout=2)

	assert response.status_code == 200
	data = response.json()
	assert check_schema(data, get_country_schema)
	assert data["country-name"] == "get_country"


def test_get_cities_in_country_via_http(system_base_url):
	response = requests.get(f"{system_base_url}/cities/by-country/8", timeout=2)

	assert response.status_code == 200
	data = response.json()
	assert check_schema(data, get_multiple_cities_schema)

	city_names = [city["city-name"] for city in data]
	assert city_names == ["get_city"]
