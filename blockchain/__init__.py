"""BlockSure blockchain package.

This package exposes the main blockchain classes and validation helpers
used by the backend, database, and product-verification modules.
"""

from .block import Block
from .blockchain import Blockchain
from .verify_chain import verify_blockchain, verify_product_history

__all__ = [
    "Block",
    "Blockchain",
    "verify_blockchain",
    "verify_product_history",
]
