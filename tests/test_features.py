from regression_model.config.core import config
from regression_model.processing.features import ExtractLetterTransformer


def test_extract_letter_transformer(sample_input_data):
    # given
    transformer = ExtractLetterTransformer(variables=config.model_config.cabin)

    # when
    subject = transformer.fit(sample_input_data)

    for row in subject.iterrows():
        if (row is not None) and (row != ""):
            assert len(row) <= 1
