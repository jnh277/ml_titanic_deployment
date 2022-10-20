from regression_model.config.core import config
from regression_model.processing.features import ExtractLetterTransformer


def test_extract_letter_transformer(sample_input_data):
    # given
    transformer = ExtractLetterTransformer(variables=config.model_config.cabin)

    # when
    transformer.fit(sample_input_data)
    subject = transformer.transform(sample_input_data)
    cabins = subject["cabin"].tolist()

    for cabin in cabins:
        if isinstance(cabin, str):
            assert len(cabin) <= 1
