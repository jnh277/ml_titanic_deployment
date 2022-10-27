from typing import Any, List, Optional

import pandas as pd
from pydantic import BaseModel
from regression_model.processing.validation import TitanicDataInputSchema


class PredictionResults(BaseModel):
    validation_errors: Optional[Any]
    model_version: str
    predictions: Optional[List]


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "pclass": 1,
                        "sex": "female",
                        "age": 29.0,
                        "sibsp": 0,
                        "parch": 0,
                        "fare": 211.3375,
                        "cabin": "B5",
                        "embarked": "S",
                        "title": "Miss"
                    },
                ]
            }
        }
