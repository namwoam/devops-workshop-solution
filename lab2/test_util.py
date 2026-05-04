from unittest.mock import patch
from litellm import ModelResponse
from lab2.util import analyze_sentiment, extract_named_entities


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
    with patch(
        "litellm.completion",
        return_value=ModelResponse(
            choices=[
                {
                    "message": {
                        "content": "[[ ## reasoning ## ]]\nThe text mentions a company, person, and city.\n"
                        '[[ ## entities ## ]]\n["Apple", "Tim Cook", "Cupertino"]\n[[ ## completed ## ]]'
                    }
                }
            ],
            usage={"total_tokens": 10},
        ),
    ):
        result = extract_named_entities("Tim Cook announced a new Apple product in Cupertino.")
        assert result == ["Apple", "Tim Cook", "Cupertino"]


def test_entity_extraction_parses_json_string():
    with patch(
        "litellm.completion",
        return_value=ModelResponse(
            choices=[
                {
                    "message": {
                        "content": "[[ ## reasoning ## ]]\nThe text mentions a company, person, and city.\n"
                        '[[ ## entities ## ]]\n["Apple", "Tim Cook", "Cupertino"]\n[[ ## completed ## ]]'
                    }
                }
            ],
            usage={"total_tokens": 10},
        ),
    ), patch("lab2.util._named_entity_extractor.extractor") as extractor:
        extractor.return_value.entities = '["Apple", "Tim Cook", "Cupertino"]'

        result = extract_named_entities("Tim Cook announced a new Apple product in Cupertino.")
        assert result == ["Apple", "Tim Cook", "Cupertino"]
