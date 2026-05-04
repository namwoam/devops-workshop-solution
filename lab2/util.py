import ast
import json

import dspy
from dspy import ChainOfThought, Signature


class SentimentAnalysisSignature(Signature):
    """Analyze the sentiment of the given text and return one of: positive, negative, or neutral."""

    text: str = dspy.InputField(desc="The text to analyze")
    sentiment: str = dspy.OutputField(
        desc="The sentiment: 'positive', 'negative', or 'neutral'"
    )


class SentimentAnalyzer(dspy.Module):
    """A sentiment analyzer using DSPy ChainOfThought."""

    def __init__(self):
        super().__init__()
        self.analyzer = ChainOfThought(SentimentAnalysisSignature)

    def forward(self, text: str) -> str:
        """Analyze sentiment of the input text."""
        result = self.analyzer(text=text)
        sentiment = result.sentiment.strip().lower()

        # Ensure valid response
        if sentiment not in ["positive", "negative", "neutral"]:
            sentiment = "neutral"

        return sentiment


class NamedEntityExtractionSignature(Signature):
    """Extract named entities from the given text."""

    text: str = dspy.InputField(desc="The text to analyze")
    entities: list[str] = dspy.OutputField(
        desc="A list of named entities found in the text"
    )


class NamedEntityExtractor(dspy.Module):
    """A named entity extractor using DSPy ChainOfThought."""

    def __init__(self):
        super().__init__()
        self.extractor = ChainOfThought(NamedEntityExtractionSignature)

    def forward(self, text: str) -> list[str]:
        """Extract named entities from the input text."""
        result = self.extractor(text=text)
        return _normalize_entities(result.entities)


def _normalize_entities(entities) -> list[str]:
    """Normalize DSPy entity outputs across parser/model versions."""
    if isinstance(entities, str):
        parsed_entities = None
        for parser in (json.loads, ast.literal_eval):
            try:
                parsed_entities = parser(entities)
                break
            except (ValueError, SyntaxError, TypeError, json.JSONDecodeError):
                continue

        if isinstance(parsed_entities, list):
            entities = parsed_entities
        else:
            entities = entities.strip().strip("[]").split(",")

    if not isinstance(entities, list):
        return []

    return [
        str(entity).strip().strip("\"'")
        for entity in entities
        if str(entity).strip().strip("\"'")
    ]


# Initialize the analyzer module
_analyzer = SentimentAnalyzer()
_named_entity_extractor = NamedEntityExtractor()


def analyze_sentiment(text: str, model: str = "gpt-5.5") -> str:
    """
    Analyze the sentiment of the given text using DSPy.

    Args:
        text: The text to analyze
        model: The language model to use, default is "gpt-5.5"
    Returns:
        A string indicating the sentiment: "positive", "negative", or "neutral"
    """
    # Configure DSPy with the specified model
    lm = dspy.LM(model=model)
    with dspy.context(lm=lm):
        return _analyzer.forward(text)


def extract_named_entities(text: str, model: str = "gpt-5.5") -> list:
    """
    Extract named entities from the given text using DSPy.

    Args:
        text: The text to analyze
        model: The language model to use, default is "gpt-5.5"
    Returns:
        A list of named entities found in the text
    """
    # This function can be implemented similarly to analyze_sentiment,
    # but with a different signature and processing logic.
    lm = dspy.LM(model=model)
    with dspy.context(lm=lm):
        return _named_entity_extractor.forward(text)
