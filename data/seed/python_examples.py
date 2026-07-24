"""Python Programming Examples — New-mir Seed Training Data.

Covers: algorithms, OOP, async, decorators, generators, data structures.
"""

from __future__ import annotations

import asyncio
import functools
import hashlib
import itertools
import json
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Callable, Generator, Iterator, TypeVar

T = TypeVar("T")

# ─── Sorting Algorithms ────────────────────────────────────────────────────────


def bubble_sort(arr: list[int]) -> list[int]:
    """Sort a list using bubble sort. O(n²) time complexity."""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def merge_sort(arr: list[int]) -> list[int]:
    """Sort a list using merge sort. O(n log n) time complexity."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: list[int]) -> list[int]:
    """Sort a list using quick sort. O(n log n) average."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# ─── Search Algorithms ─────────────────────────────────────────────────────────


def binary_search(arr: list[int], target: int) -> int:
    """Return index of target in sorted array, or -1 if not found."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# ─── Data Structures ───────────────────────────────────────────────────────────


class Stack:
    """LIFO stack implementation."""

    def __init__(self) -> None:
        self._data: list[Any] = []

    def push(self, item: Any) -> None:
        self._data.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)


class LinkedListNode:
    """Node in a singly linked list."""

    def __init__(self, value: Any, next_node: "LinkedListNode | None" = None) -> None:
        self.value = value
        self.next = next_node


class LinkedList:
    """Singly linked list implementation."""

    def __init__(self) -> None:
        self.head: LinkedListNode | None = None
        self._size = 0

    def append(self, value: Any) -> None:
        node = LinkedListNode(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self._size += 1

    def to_list(self) -> list[Any]:
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __len__(self) -> int:
        return self._size


# ─── Object-Oriented Programming ──────────────────────────────────────────────


@dataclass
class MemoryCell:
    """Honeycomb memory cell — stores compressed binary data."""

    cell_id: str
    capacity: int = 65_536
    _data: bytes = field(default=b"", repr=False)
    _metadata: dict[str, Any] = field(default_factory=dict, repr=False)
    created_at: float = field(default_factory=time.time)

    @classmethod
    def from_seed(cls, content: str, capacity: int = 65_536) -> "MemoryCell":
        """Create a cell seeded with given content."""
        seed_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        cell = cls(cell_id=seed_hash, capacity=capacity)
        cell.write(content.encode("utf-8"))
        return cell

    def write(self, data: bytes) -> bool:
        if len(self._data) + len(data) > self.capacity:
            return False
        self._data += data
        return True

    @property
    def fill_ratio(self) -> float:
        return len(self._data) / self.capacity

    @property
    def is_full(self) -> bool:
        return self.fill_ratio >= 0.70


class HoneycombShard:
    """A shard of the honeycomb memory pool."""

    def __init__(self, capacity: int = 65_536) -> None:
        self.capacity = capacity
        self._cells: dict[str, MemoryCell] = {}

    def create_cell(self, seed: str) -> MemoryCell:
        cell = MemoryCell.from_seed(seed, self.capacity)
        self._cells[cell.cell_id] = cell
        return cell

    def get_cell(self, cell_id: str) -> MemoryCell | None:
        return self._cells.get(cell_id)

    @property
    def size(self) -> int:
        return len(self._cells)

    @property
    def fill_percent(self) -> float:
        return self.size / self.capacity * 100


# ─── Decorators ────────────────────────────────────────────────────────────────


def timer(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator that prints execution time."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f}s")
        return result

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator that retries a function on exception."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exc: Exception = RuntimeError("No attempts made")
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exc

        return wrapper

    return decorator


# ─── Generators ────────────────────────────────────────────────────────────────


def fibonacci() -> Generator[int, None, None]:
    """Infinite Fibonacci sequence generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def chunked(iterable: Iterator[T], size: int) -> Generator[list[T], None, None]:
    """Yield successive chunks of given size from an iterable."""
    chunk: list[T] = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def token_stream(text: str, chunk_size: int = 4) -> Generator[str, None, None]:
    """Simulate token streaming by yielding text in chunks."""
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]
        time.sleep(0.01)  # simulate generation delay


# ─── Async Programming ────────────────────────────────────────────────────────


async def fetch_data(url: str) -> dict[str, Any]:
    """Simulate async HTTP fetch."""
    await asyncio.sleep(0.1)  # simulate network delay
    return {"url": url, "data": "response", "status": 200}


async def train_batch(files: list[str]) -> list[dict[str, Any]]:
    """Train on multiple files concurrently."""
    tasks = [fetch_data(f"file://{f}") for f in files]
    results = await asyncio.gather(*tasks)
    return list(results)


async def stream_response(text: str) -> None:
    """Stream response tokens with async generator."""
    for chunk in token_stream(text):
        print(chunk, end="", flush=True)
        await asyncio.sleep(0)  # yield control to event loop


# ─── Utilities ────────────────────────────────────────────────────────────────


def flatten(nested: list[Any]) -> list[Any]:
    """Flatten a nested list to a single level."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries; override values win."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def word_frequency(text: str) -> dict[str, int]:
    """Count word frequencies in text."""
    freq: dict[str, int] = defaultdict(int)
    for word in text.lower().split():
        word = word.strip(".,!?;:\"'()[]")
        if word:
            freq[word] += 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))


# ─── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    # Sorting
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Original:", arr)
    print("Bubble sort:", bubble_sort(arr))
    print("Merge sort:", merge_sort(arr))
    print("Quick sort:", quick_sort(arr))

    # Binary search
    sorted_arr = sorted(arr)
    idx = binary_search(sorted_arr, 25)
    print(f"\nBinary search for 25 in {sorted_arr}: index {idx}")

    # Data structures
    stack = Stack()
    for i in [1, 2, 3, 4, 5]:
        stack.push(i)
    print(f"\nStack size: {len(stack)}, peek: {stack.peek()}")

    # Memory cells
    cell = MemoryCell.from_seed("hello world", capacity=1024)
    print(f"\nCell ID: {cell.cell_id}, fill: {cell.fill_ratio:.2%}")

    # Fibonacci
    fib = fibonacci()
    first_10 = [next(fib) for _ in range(10)]
    print(f"\nFirst 10 Fibonacci: {first_10}")

    # Word frequency
    text = "the quick brown fox jumps over the lazy dog the fox"
    freq = word_frequency(text)
    print(f"\nWord frequencies: {dict(itertools.islice(freq.items(), 5))}")

    # JSON
    data = {"model": "new-mir", "version": "1.0", "cells": 65536}
    json_str = json.dumps(data, indent=2)
    print(f"\nJSON:\n{json_str}")


if __name__ == "__main__":
    main()
