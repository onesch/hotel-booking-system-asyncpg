import os
import subprocess
import time

import httpx
import pytest

from app.settings import TEST_REDIS_URL


def wait_for_server(
    url: str,
    process: subprocess.Popen,
    timeout: float = 5.0,
) -> None:
    """Wait until the test server is ready to accept requests."""
    deadline = time.monotonic() + timeout

    with httpx.Client() as client:
        while time.monotonic() < deadline:
            # Stop waiting if the server process has already crashed.
            if process.poll() is not None:
                raise RuntimeError(
                    f"Server exited with code {process.returncode}"
                )

            # Check whether the server is ready.
            try:
                response = client.get(url)

                if response.is_success:
                    return

            except httpx.ConnectError:
                pass

            # Avoid busy waiting between connection attempts.
            time.sleep(0.1)

    raise RuntimeError("Server did not start in time")


@pytest.fixture
def run_server():
    """Run the application in a separate process for E2E tests."""
    env = os.environ.copy()

    # Force the E2E server to use the test Redis database.
    env["REDIS_URL"] = TEST_REDIS_URL

    # Start the FastAPI application through Uvicorn.
    process = subprocess.Popen(
        [
            "uv",
            "run",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        env=env,
    )

    try:
        # Wait until the application is ready before starting the test.
        wait_for_server(
            "http://127.0.0.1:8000/health",
            process,
        )

        yield

    finally:
        # Stop the server if it is still running.
        if process.poll() is None:
            process.terminate()
            process.wait()
