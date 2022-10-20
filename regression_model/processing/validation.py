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


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # convert syntax error field names (beginning with numbers)

    # get title from name if needed
    if not ("title" in input_data):
        input_data["title"] = input_data["name"].apply(get_title)

    # do somethign with cabin
    input_data["cabin"] = input_data["cabin"].apply(get_first_cabin)

    # extract features
    validated_data = input_data[config.model_config.features].copy()

    # in some cases we might want to check for nan's here etc
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        test = MultipleTitanicDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


# pclass,survived,sex,age,sibsp,parch,fare,cabin,embarked,title
class TitanicDataInputSchema(BaseModel):
    passengerid: Optional[int]
    pclass: int
    name: Optional[str]
    sex: str
    age: float
    sibsp: int
    parch: int
    ticket: Optional[str]
    fare: float
    cabin: Union[str, None]
    embarked: str
    title: Optional[str]


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]
