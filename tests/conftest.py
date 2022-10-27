from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from regression_model.config.core import config
from regression_model.processing.data_manager import load_dataset


@pytest.fixture()
def sample_input_data():
    data = load_dataset(
        file_name=config.app_config.training_data_file
    )  # this should probably not be train data
    # file but need to know the survival to do my test_predictions
    return data


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}
