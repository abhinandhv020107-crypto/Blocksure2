"""Block model used by the BlockSure blockchain."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict

from .hash_utils import calculate_sha256


@dataclass
class Block:
    """Represents one transaction block in the BlockSure blockchain."""

    index: int
    product_id: str
    action: str
    previous_hash: str
    from_user: str = ""
    to_user: str = ""
    location: str = ""
    extra_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    current_hash: str = ""

    def __post_init__(self) -> None:
        """Validate block fields and create the hash when needed."""

        if self.index < 0:
            raise ValueError("Block index cannot be negative.")

        if not isinstance(self.product_id, str) or not self.product_id.strip():
            raise ValueError("product_id must be a non-empty string.")

        if not isinstance(self.action, str) or not self.action.strip():
            raise ValueError("action must be a non-empty string.")

        if not isinstance(self.previous_hash, str):
            raise ValueError("previous_hash must be a string.")

        if not isinstance(self.extra_data, dict):
            raise ValueError("extra_data must be a dictionary.")

        self.product_id = self.product_id.strip()
        self.action = self.action.strip()
        self.from_user = str(self.from_user).strip()
        self.to_user = str(self.to_user).strip()
        self.location = str(self.location).strip()

        if not self.current_hash:
            self.current_hash = self.calculate_hash()

    def hash_payload(self) -> Dict[str, Any]:
        """Return only the data that is protected by the block hash."""

        return {
            "index": self.index,
            "product_id": self.product_id,
            "action": self.action,
            "from_user": self.from_user,
            "to_user": self.to_user,
            "location": self.location,
            "extra_data": self.extra_data,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
        }

    def calculate_hash(self) -> str:
        """Calculate this block's SHA-256 hash."""

        return calculate_sha256(self.hash_payload())

    def is_hash_valid(self) -> bool:
        """Return True when the stored hash matches the block data."""

        return self.current_hash == self.calculate_hash()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the block into a dictionary for APIs or databases."""

        return {
            **self.hash_payload(),
            "current_hash": self.current_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Block":
        """Create a Block object from dictionary data."""

        required_fields = {
            "index",
            "product_id",
            "action",
            "previous_hash",
            "timestamp",
            "current_hash",
        }

        missing_fields = required_fields.difference(data.keys())
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Missing block fields: {missing}")

        return cls(
            index=int(data["index"]),
            product_id=str(data["product_id"]),
            action=str(data["action"]),
            previous_hash=str(data["previous_hash"]),
            from_user=str(data.get("from_user", "")),
            to_user=str(data.get("to_user", "")),
            location=str(data.get("location", "")),
            extra_data=dict(data.get("extra_data", {})),
            timestamp=str(data["timestamp"]),
            current_hash=str(data["current_hash"]),
        )
