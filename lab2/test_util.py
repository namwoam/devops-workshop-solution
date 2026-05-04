from unittest.mock import patch
from litellm import ModelResponse
from lab2.util import analyze_sentiment


def test_analyze_sentiment_positive():
    with patch(
        "litellm.completion",
        return_value=ModelResponse(
            choices=[
                {
                    "message": {
                        "content": "[[ ## reasoning ## ]]\nThe text 'I love this product!' is positive.\n"
                        "[[ ## sentiment ## ]]\npositive\n[[ ## completed ## ]]"
                    }
                }
            ],
            usage={"total_tokens": 10},
        ),
    ):
        result = analyze_sentiment("I love this product!")
        assert result == "positive"


def test_entity_extraction():
    raise NotImplementedError("This test is not implemented yet.")
