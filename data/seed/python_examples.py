"""Python examples — New-mir seed training data."""
from __future__ import annotations
import time, json, hashlib
from dataclasses import dataclass, field
from typing import Any, Generator

# Sorting algorithms
def bubble_sort(arr: list[int]) -> list[int]:
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result

def binary_search(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1

# Data structures
class Stack:
    def __init__(self) -> None:
        self._data: list[Any] = []
    def push(self, item: Any) -> None: self._data.append(item)
    def pop(self) -> Any:
        if not self._data: raise IndexError("empty")
        return self._data.pop()
    def peek(self) -> Any: return self._data[-1]
    def __len__(self) -> int: return len(self._data)

# Memory cell (mirrors honeycomb architecture)
@dataclass
class MemoryCell:
    cell_id: str
    capacity: int = 65_536
    _data: bytes = field(default=b"", repr=False)
    created_at: float = field(default_factory=time.time)

    @classmethod
    def from_seed(cls, content: str) -> "MemoryCell":
        cid = hashlib.sha256(content.encode()).hexdigest()[:16]
        cell = cls(cell_id=cid)
        cell._data = content.encode("utf-8")
        return cell

    @property
    def fill_ratio(self) -> float:
        return len(self._data) / self.capacity

# Decorators
import functools
def timer(func):  # type: ignore[no-untyped-def]
    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        t = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter()-t:.4f}s")
        return result
    return wrapper

# Generators
def fibonacci() -> Generator[int, None, None]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def chunked(lst: list[Any], n: int) -> Generator[list[Any], None, None]:
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

# Utilities
def flatten(nested: list[Any]) -> list[Any]:
    result = []
    for item in nested:
        result.extend(flatten(item)) if isinstance(item, list) else result.append(item)
    return result

def word_freq(text: str) -> dict[str, int]:
    freq: dict[str, int] = {}
    for word in text.lower().split():
        word = word.strip(".,!?;:'\"")
        if word:
            freq[word] = freq.get(word, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

# Demo
if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("bubble:", bubble_sort(arr))
    print("merge:", merge_sort(arr))
    fib = fibonacci()
    print("fib:", [next(fib) for _ in range(10)])
    cell = MemoryCell.from_seed("hello world")
    print(f"cell {cell.cell_id}: fill={cell.fill_ratio:.4f}")
    data = {"model": "new-mir", "version": "1.2", "cells": 65536}
    print(json.dumps(data, indent=2))
