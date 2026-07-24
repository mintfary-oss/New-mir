"""New-mir core package — honeycomb neural architecture."""
from .cell_memory import HoneycombMemory, MemoryCell
from .qr_encoder import QRBinaryEncoder
from .binary_engine import BinaryCompressionEngine
from .neural_core import NeuralCodeGen

__all__ = [
    "HoneycombMemory",
    "MemoryCell",
    "QRBinaryEncoder",
    "BinaryCompressionEngine",
    "NeuralCodeGen",
]
