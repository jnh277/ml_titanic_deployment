from typing import Any, List, Optional

import pandas as pd
from pydantic import BaseModel
from regression_model.processing.validation import PVInputSchema


class PredictionResults(BaseModel):
    validation_errors: Optional[Any]
    model_version: str
    predictions: Optional[List]
    test_r_score: float
    test_mse: float


class MultiplePVDataInputs(BaseModel):
    inputs: List[PVInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "datetime": pd.Timestamp(2022, 4, 12, 1),
                    },
                    {
                        "datetime": pd.Timestamp(2020,10, 5, 3),
                    },
                    {
                        "datetime": pd.Timestamp(2020, 10, 5, 5),
                    }
                ]
            }
        }
