from functools import lru_cache
import math
from pathlib import Path

from django.conf import settings


DEFAULT_MODEL_NAME = "BAAI/bge-small-en-v1.5"


def get_model_name():
    return getattr(settings, "EMBEDDING_MODEL_NAME", DEFAULT_MODEL_NAME)


def get_cache_folder():
    cache_folder = getattr(settings, "EMBEDDING_MODEL_CACHE", Path.cwd() / ".hf_cache")
    return str(cache_folder)


@lru_cache(maxsize=1)
def get_model():
    from fastembed import TextEmbedding

    return TextEmbedding(model_name=get_model_name(), cache_dir=get_cache_folder())


def embed_text(text):
    """Return a normalized embedding from the configured Hugging Face model."""
    text = text.strip()
    if not text:
        return []

    vector = next(get_model().embed([text]))
    return [round(float(value), 6) for value in vector.tolist()]


def cosine_similarity(left, right):
    left_magnitude = math.sqrt(sum(value * value for value in left))
    right_magnitude = math.sqrt(sum(value * value for value in right))

    if left_magnitude == 0 or right_magnitude == 0:
        return 0.0

    dot_product = sum(a * b for a, b in zip(left, right))
    return dot_product / (left_magnitude * right_magnitude)
