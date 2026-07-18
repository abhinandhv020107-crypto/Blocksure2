"""Verification helpers for the BlockSure blockchain."""

from __future__ import annotations

from typing import Any, Dict, List

from .blockchain import Blockchain
from .hash_utils import is_valid_hash


def verify_blockchain(blockchain: Blockchain) -> Dict[str, Any]:
    """Return a detailed validation result for the entire blockchain."""

    if not isinstance(blockchain, Blockchain):
        raise TypeError("blockchain must be a Blockchain object.")

    errors: List[str] = []

    if not blockchain.chain:
        errors.append("Blockchain is empty.")
        return {
            "valid": False,
            "message": "Blockchain is invalid.",
            "total_blocks": 0,
            "errors": errors,
        }

    for position, block in enumerate(blockchain.chain):
        if block.index != position:
            errors.append(
                f"Block {position}: stored index is {block.index}, expected {position}."
            )

        if not is_valid_hash(block.current_hash):
            errors.append(f"Block {position}: current hash format is invalid.")
        elif not block.is_hash_valid():
            errors.append(f"Block {position}: block data has been changed.")

        if position == 0:
            if block.previous_hash != Blockchain.GENESIS_PREVIOUS_HASH:
                errors.append("Genesis block previous hash must be '0'.")
        else:
            previous_block = blockchain.chain[position - 1]
            if block.previous_hash != previous_block.current_hash:
                errors.append(
                    f"Block {position}: previous hash does not match block {position - 1}."
                )

    valid = len(errors) == 0

    return {
        "valid": valid,
        "message": (
            "Blockchain is valid. No tampering detected."
            if valid
            else "Blockchain is invalid. Possible tampering detected."
        ),
        "total_blocks": len(blockchain),
        "errors": errors,
    }


def verify_product_history(
    blockchain: Blockchain,
    product_id: str,
) -> Dict[str, Any]:
    """Validate the blockchain and return one product's history."""

    if not isinstance(product_id, str) or not product_id.strip():
        raise ValueError("product_id must be a non-empty string.")

    chain_result = verify_blockchain(blockchain)
    history = blockchain.get_product_history(product_id)

    if not history:
        return {
            "product_id": product_id,
            "found": False,
            "valid": False,
            "status": "PRODUCT_NOT_FOUND",
            "message": "Product ID does not exist in the blockchain.",
            "history": [],
        }

    if not chain_result["valid"]:
        return {
            "product_id": product_id,
            "found": True,
            "valid": False,
            "status": "BLOCKCHAIN_INVALID",
            "message": "Product exists, but the blockchain is invalid.",
            "history": [block.to_dict() for block in history],
        }

    return {
        "product_id": product_id,
        "found": True,
        "valid": True,
        "status": "GENUINE_PRODUCT",
        "message": "Product exists and its blockchain history is valid.",
        "history": [block.to_dict() for block in history],
    }
