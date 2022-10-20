import re
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from regression_model.config.core import config


def get_title(passenger):
    line = passenger
    if re.search("Mrs", line):
        return "Mrs"
    elif re.search("Mr", line):
        return "Mr"
    elif re.search("Miss", line):
        return "Miss"
    elif re.search("Master", line):
        return "Master"
    else:
        return "Other"


def get_first_cabin(row):
    try:
        return row.split()[0]
    except:
        return np.nan


def validate_inputs(
    *, input_data: pd.DataFrame, training=False
) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # convert syntax error field names (beginning with numbers)

    # get title from name if needed
    if not ("title" in input_data):
        input_data["title"] = input_data["name"].apply(get_title)

    # do somethign with cabin
    input_data["cabin"] = input_data["cabin"].apply(get_first_cabin)

    # extract features
    if training:
        relevant_data = input_data[
            config.model_config.features + [config.model_config.target]
        ]
    else:
        relevant_data = input_data[config.model_config.features].copy()

    # in some cases we might want to check for nan's here etc
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        temp = MultipleTitanicDataInputs(
            inputs=relevant_data.replace({np.nan: None}).to_dict(orient="records")
        )
        validated_data = pd.DataFrame([model.dict() for model in temp.inputs])
    except ValidationError as error:
        errors = error.json()

    if not training:
        validated_data.drop(columns=["survived"], inplace=True)

    return validated_data, errors


# pclass,survived,sex,age,sibsp,parch,fare,cabin,embarked,title
class TitanicDataInputSchema(BaseModel):
    pclass: Union[int, None]
    sex: Union[str, None]
    age: Union[float, None]
    sibsp: Union[int, None]
    parch: Union[int, None]
    fare: Union[float, None]
    cabin: Union[str, None]
    embarked: Union[str, None]
    title: Optional[str]
    survived: Optional[int]


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]
