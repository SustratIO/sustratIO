from typing import TYPE_CHECKING

from fastapi.testclient import TestClient

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

    from fastapi import FastAPI


@pytest.fixture
def offline_app(
    monkeypatch,
) -> Generator[FastAPI]:
    """
    By offline it refers merely to an app which executes all the logic
    in-memory.
    """

    from infrastructure.config import settings

    # Ensures we use in-memory adapters for the app
    monkeypatch.setattr(settings, 'AUTH_ENGINE', 'in_memory')
    monkeypatch.setattr(settings, 'DATABASE_ENGINE', 'in_memory')

    from infrastructure.entrypoints.api.main import app

    yield app

    # We call this manually in case any test needs to modify dependencies
    app.dependency_overrides.clear()


@pytest.fixture
def offline_client(offline_app) -> Generator[TestClient]:
    """
    By offline it refers merely to a client whose app executes all the logic
    in-memory.
    """

    with TestClient(app=offline_app) as test_client:
        yield test_client
