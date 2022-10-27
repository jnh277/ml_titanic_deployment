import numpy as np
import pandas as pd
from fastapi.testclient import TestClient


def test_make_prediction(client: TestClient, sample_input_data: pd.DataFrame) -> None:
    # Given
    payload = {
        # ensure pydantic plays well with np.nan
        "inputs": sample_input_data.replace({np.nan: None}).to_dict(orient="records")
    }

    # When
    response = client.post(
        "http://localhost:8001/api/v1/predict",
        json=payload,
    )

    # Then
    assert response.status_code == 200
    prediction_data = response.json()
    assert prediction_data["predictions"]
    assert prediction_data["validation_errors"] is None
    assert prediction_data["predictions"][0] == 0  # should do more of these
    # assert math.isclose(prediction_data["predictions"][0], 113422, rel_tol=100)
