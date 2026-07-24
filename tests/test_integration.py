"""
Integration tests for all four layers of New-mir.

Run with:  python -m pytest tests/ -v
"""

import pytest

from api.converters import convert_to_binary
from core.binary_engine import (
    BinaryCompressionEngine,
    bits_to_bytes,
    bytes_to_bits,
    bytes_to_numpy_bits,
    numpy_bits_to_bytes,
)
from core.cell_memory import HoneycombMemory
from core.neural_core import NeuralCodeGen
from core.qr_encoder import (
    QRBinaryEncoder,
    binary_string_to_bytes,
    bytes_to_binary_string,
)

# ---------------------------------------------------------------------------
# Layer 1 — HoneycombMemory
# ---------------------------------------------------------------------------


class TestHoneycombMemory:
    def test_create_and_read(self) -> None:
        mem = HoneycombMemory(capacity=10)
        cell = mem.create_cell("test-seed", data=b"hello")
        assert cell.read() == b"hello"
        assert cell.write_count == 1

    def test_lru_eviction(self) -> None:
        mem = HoneycombMemory(capacity=3)
        ids = [mem.create_cell(f"seed-{i}", data=bytes([i])).cell_id for i in range(4)]
        # First cell should be evicted
        assert mem.get_cell(ids[0]) is None
        assert mem.get_cell(ids[-1]) is not None

    def test_export_import(self) -> None:
        mem = HoneycombMemory(capacity=100)
        mem.create_cell("a", data=b"payload-a")
        json_str = mem.export_json()
        mem2 = HoneycombMemory(capacity=100)
        count = mem2.import_json(json_str)
        assert count == 1

    def test_stats(self) -> None:
        mem = HoneycombMemory()
        mem.create_cell("s1", data=b"x" * 100)
        s = mem.stats()
        assert s["cells_in_memory"] == 1
        assert s["total_payload_bytes"] == 100


# ---------------------------------------------------------------------------
# Layer 2 — QRBinaryEncoder
# ---------------------------------------------------------------------------


class TestQRBinaryEncoder:
    def test_round_trip_small(self) -> None:
        enc = QRBinaryEncoder()
        data = b"Hello New-mir!"
        ids = enc.encode(data)
        assert enc.decode(ids) == data

    def test_round_trip_large(self) -> None:
        enc = QRBinaryEncoder()
        data = b"A" * 5000
        ids = enc.encode(data)
        assert enc.decode(ids) == data
        assert len(ids) >= 1

    def test_binary_string_helpers(self) -> None:
        original = b"Hi"
        bits = bytes_to_binary_string(original)
        assert bits == "01001000 01101001"
        assert binary_string_to_bytes(bits) == original

    def test_qr_image_png(self) -> None:
        enc = QRBinaryEncoder()
        ids = enc.encode(b"test QR image")
        slot = enc.get_slot(ids[0])
        assert slot is not None
        png = slot.to_png_bytes()
        assert png[:4] == b"\x89PNG"


# ---------------------------------------------------------------------------
# Layer 3 — BinaryCompressionEngine
# ---------------------------------------------------------------------------


class TestBinaryCompressionEngine:
    def setup_method(self) -> None:
        self.engine = BinaryCompressionEngine()

    def test_round_trip_bytes(self) -> None:
        data = b"def hello():\n    return 'world'\n" * 100
        block = self.engine.compress(data)
        assert self.engine.decompress(block) == data

    def test_round_trip_text_hint(self) -> None:
        data = b"function greet(name) { return `Hello, ${name}!`; }\n" * 50
        block = self.engine.compress(data, hint="text")
        assert self.engine.decompress(block) == data

    def test_bit_string_round_trip(self) -> None:
        data = b"New-mir binary engine test"
        bits = self.engine.compress_to_bits(data)
        assert self.engine.decompress_from_bits(bits) == data

    def test_numpy_round_trip(self) -> None:
        data = b"numpy bits test"
        bits = bytes_to_bits(data)
        recovered = bits_to_bytes(bits)
        assert recovered[: len(data)] == data

    def test_numpy_array_round_trip(self) -> None:
        data = b"\x00\xff\xab\xcd"
        arr = bytes_to_numpy_bits(data)
        assert arr.dtype == bool
        back = numpy_bits_to_bytes(arr)
        assert back == data

    def test_sha256_integrity(self) -> None:
        data = b"integrity check"
        block = self.engine.compress(data)
        # Corrupt the data
        import dataclasses

        bad_block = dataclasses.replace(block, sha256=b"\x00" * 32)
        with pytest.raises(ValueError, match="SHA-256"):
            self.engine.decompress(bad_block)

    def test_wire_format(self) -> None:
        data = b"wire format test"
        block = self.engine.compress(data)
        raw = block.to_bytes()
        restored = type(block).from_bytes(raw)
        assert self.engine.decompress(restored) == data


# ---------------------------------------------------------------------------
# Layer 4 — Converters
# ---------------------------------------------------------------------------


class TestConverters:
    def test_text_conversion(self) -> None:
        code = b"print('hello world')\n"
        result = convert_to_binary(code, filename="hello.py")
        assert result.bit_count > 0
        assert result.text_content is not None
        assert "hello" in result.text_content

    def test_binary_conversion(self) -> None:
        raw = bytes(range(256))
        result = convert_to_binary(raw, filename="data.bin")
        assert result.bit_count == len(raw) * 8
        assert result.mime_type == "application/octet-stream"

    def test_to_dict(self) -> None:
        result = convert_to_binary(b"test", filename="test.txt")
        d = result.to_dict()
        assert "bit_count" in d
        assert "compression_ratio" in d
        assert "binary_preview" in d


# ---------------------------------------------------------------------------
# Neural code gen
# ---------------------------------------------------------------------------


class TestNeuralCodeGen:
    def setup_method(self) -> None:
        self.gen = NeuralCodeGen(embed_dim=32, num_heads=2, num_layers=1, ff_dim=64)
        self.gen.load_demo_weights()

    def test_generate_returns_string(self) -> None:
        result = self.gen.generate("def f():", max_new_tokens=16, throttle_ms=0)
        assert isinstance(result, str)
        assert "def f():" in result

    def test_parameter_count(self) -> None:
        assert self.gen.parameter_count > 0

    def test_memory_persistence(self) -> None:
        mem = HoneycombMemory(capacity=500)
        cell_id = self.gen.save_to_memory(mem)
        gen2 = NeuralCodeGen.load_from_memory(mem, cell_id)
        assert gen2.parameter_count == self.gen.parameter_count

    def test_generate_from_description(self) -> None:
        result = self.gen.generate_from_description(
            "a function that adds two numbers",
            language="python",
            max_new_tokens=32,
        )
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# HoneycombTrainer
# ---------------------------------------------------------------------------


class TestHoneycombTrainer:
    def setup_method(self) -> None:
        from core.trainer import HoneycombTrainer

        self.mem = HoneycombMemory(capacity=200)
        self.enc = QRBinaryEncoder()
        self.engine = BinaryCompressionEngine()
        self.gen = NeuralCodeGen(embed_dim=32, num_heads=2, num_layers=1, ff_dim=64)
        self.gen.load_demo_weights()
        self.trainer = HoneycombTrainer(
            memory_shards=[self.mem],
            qr_encoder=self.enc,
            compression_engine=self.engine,
            neural_gen=self.gen,
        )

    def test_train_text_file(self) -> None:
        code = b"def add(a, b):\n    return a + b\n"
        session = self.trainer.train_files([("add.py", code)])
        d = session.to_dict()
        assert d["files_trained"] == 1
        assert d["cells_written"] == 1
        assert len(session.accepted_files) == 1
        f = session.accepted_files[0]
        assert f["filename"] == "add.py"
        assert int(f["qr_slots"]) >= 1  # type: ignore[arg-type]

    def test_train_binary_file(self) -> None:
        raw = bytes(range(256)) * 10
        session = self.trainer.train_files([("data.bin", raw)])
        assert len(session.accepted_files) == 1

    def test_train_multiple_files(self) -> None:
        files = [
            ("a.py", b"x = 1\n"),
            ("b.js", b"const x = 1;\n"),
            ("c.go", b"package main\nfunc main() {}\n"),
        ]
        session = self.trainer.train_files(files)
        d = session.to_dict()
        assert d["files_trained"] == 3
        assert d["cells_written"] == 3

    def test_auto_shard_expansion(self) -> None:
        """Fill shard past 70% threshold and verify new shard is created."""
        tiny_mem = HoneycombMemory(capacity=3)
        from core.trainer import HoneycombTrainer

        trainer = HoneycombTrainer(
            memory_shards=[tiny_mem],
            qr_encoder=self.enc,
            compression_engine=self.engine,
            neural_gen=self.gen,
        )
        files = [(f"f{i}.txt", f"content {i}".encode()) for i in range(4)]
        session = trainer.train_files(files)
        assert session.shards_created >= 1

    def test_global_stats(self) -> None:
        self.trainer.train_files([("test.txt", b"hello world")])
        stats = self.trainer.global_stats()
        assert int(stats["total_cells"]) >= 1  # type: ignore[arg-type]
        assert int(stats["shards"]) >= 1  # type: ignore[arg-type]
        assert float(stats["fill_percent"]) >= 0  # type: ignore[arg-type]
