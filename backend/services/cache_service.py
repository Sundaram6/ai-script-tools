import hashlib
from typing import Optional

_cache = {}

def get_cached_response(prompt: str) -> Optional[dict]:
    """Retrieve a cached response if it exists."""
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    return _cache.get(prompt_hash)

def set_cached_response(prompt: str, response: dict) -> None:
    """Store a response in the cache."""
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    _cache[prompt_hash] = response
