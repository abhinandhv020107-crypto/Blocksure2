"""Hashing utilities for the BlockSure blockchain module."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def serialize_data(data: Any) -> str:
    """Convert Python data into a stable JSON string.

    Sorting keys ensures that the same data always produces the same hash.
    """

    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    )


def calculate_sha256(data: Any) -> str:
    """Return the SHA-256 hash of the supplied data."""

    serialized_data = serialize_data(data)
    return hashlib.sha256(serialized_data.encode("utf-8")).hexdigest()


def is_valid_hash(hash_value: str) -> bool:
    """Check whether a value looks like a SHA-256 hexadecimal hash."""

    if not isinstance(hash_value, str) or len(hash_value) != 64:
        return False

    try:
        int(hash_value, 16)
    except ValueError:
        return False

    return True
