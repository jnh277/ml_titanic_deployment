from sklearn.metrics import accuracy_score

from regression_model.predict import make_prediction


#
def test_make_prediction(sample_input_data):
    # Given
    # When
    result = make_prediction(input_data=sample_input_data)

    # Then
    predictions = result.get("predictions")

    accuracy = accuracy_score(sample_input_data["survived"], predictions)
    print("train accuracy: {}".format(accuracy))
    assert accuracy > 0.6
