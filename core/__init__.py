"""New-mir core package — honeycomb neural architecture."""

from .binary_engine import BinaryCompressionEngine
from .cell_memory import HoneycombMemory, MemoryCell
from .neural_core import NeuralCodeGen
from .qr_encoder import QRBinaryEncoder
from .trainer import HoneycombTrainer

__all__ = [
    "BinaryCompressionEngine",
    "HoneycombMemory",
    "HoneycombTrainer",
    "MemoryCell",
    "NeuralCodeGen",
    "QRBinaryEncoder",
]
