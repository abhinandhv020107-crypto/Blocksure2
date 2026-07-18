"""Blockchain management for the BlockSure project."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from .block import Block


class Blockchain:
    """Creates, stores, searches, and validates BlockSure blocks."""

    GENESIS_PRODUCT_ID = "GENESIS"
    GENESIS_ACTION = "Blockchain Created"
    GENESIS_PREVIOUS_HASH = "0"

    def __init__(self, blocks: Optional[Iterable[Block]] = None) -> None:
        """Create a new blockchain or load an existing block collection."""

        if blocks is None:
            self.chain: List[Block] = [self._create_genesis_block()]
        else:
            self.chain = list(blocks)
            if not self.chain:
                self.chain.append(self._create_genesis_block())

    def _create_genesis_block(self) -> Block:
        """Create the first block in the blockchain."""

        return Block(
            index=0,
            product_id=self.GENESIS_PRODUCT_ID,
            action=self.GENESIS_ACTION,
            previous_hash=self.GENESIS_PREVIOUS_HASH,
            from_user="SYSTEM",
            to_user="SYSTEM",
            location="",
            extra_data={"description": "BlockSure genesis block"},
        )

    @property
    def latest_block(self) -> Block:
        """Return the newest block in the chain."""

        return self.chain[-1]

    def add_block(
        self,
        product_id: str,
        action: str,
        from_user: str = "",
        to_user: str = "",
        location: str = "",
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> Block:
        """Create a new block, link it, append it, and return it."""

        if not self.is_valid():
            raise ValueError(
                "Cannot add a block because the existing blockchain is invalid."
            )

        new_block = Block(
            index=len(self.chain),
            product_id=product_id,
            action=action,
            previous_hash=self.latest_block.current_hash,
            from_user=from_user,
            to_user=to_user,
            location=location,
            extra_data=extra_data or {},
        )

        self.chain.append(new_block)
        return new_block

    def is_valid(self) -> bool:
        """Check hashes, indexes, links, and the genesis block."""

        if not self.chain:
            return False

        genesis = self.chain[0]

        if genesis.index != 0:
            return False

        if genesis.product_id != self.GENESIS_PRODUCT_ID:
            return False

        if genesis.previous_hash != self.GENESIS_PREVIOUS_HASH:
            return False

        if not genesis.is_hash_valid():
            return False

        for position in range(1, len(self.chain)):
            current_block = self.chain[position]
            previous_block = self.chain[position - 1]

            if current_block.index != position:
                return False

            if not current_block.is_hash_valid():
                return False

            if current_block.previous_hash != previous_block.current_hash:
                return False

        return True

    def get_block(self, index: int) -> Optional[Block]:
        """Return a block by index, or None when it does not exist."""

        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def get_product_history(self, product_id: str) -> List[Block]:
        """Return every block belonging to one product."""

        normalized_product_id = product_id.strip().lower()

        return [
            block
            for block in self.chain
            if block.product_id.strip().lower() == normalized_product_id
        ]

    def product_exists(self, product_id: str) -> bool:
        """Return True when at least one block exists for the product."""

        return bool(self.get_product_history(product_id))

    def to_list(self) -> List[Dict[str, Any]]:
        """Convert the complete blockchain into dictionaries."""

        return [block.to_dict() for block in self.chain]

    @classmethod
    def from_list(cls, block_data: Iterable[Dict[str, Any]]) -> "Blockchain":
        """Rebuild a blockchain from database or JSON dictionaries."""

        blocks = [Block.from_dict(item) for item in block_data]
        return cls(blocks=blocks)

    def __len__(self) -> int:
        """Return the number of blocks."""

        return len(self.chain)

    def __iter__(self):
        """Allow iteration over blockchain blocks."""

        return iter(self.chain)
