#!/usr/bin/env python3
"""
Generate pre-built HoneycombMemory cells for New-mir.
Covers Python, JS, TS, HTML, CSS, SQL, Bash, Go, Rust, C/C++,
Java, PHP, Kotlin, React, FastAPI, Docker, Algorithms, Patterns,
Assembly, Git, Testing — 10 000 cells total.

Run:
    python3 scripts/gen_prebuilt_cells.py

Output:
    data/prebuilt/cells.json   (loaded automatically on server start)
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TS = 1722000000.0  # fixed creation timestamp so file is deterministic


def _cell(seed: str, content: str, lang: str, topic: str,
          keywords: list[str]) -> tuple[str, dict]:
    cell_id = hashlib.sha256(seed.encode()).hexdigest()
    payload = content.encode("utf-8")
    return cell_id, {
        "cell_id": cell_id,
        "created_at": _TS,
        "updated_at": _TS,
        "binary_payload": payload.hex(),
        "metadata": {
            "lang": lang,
            "topic": topic,
            "keywords": keywords,
            "source": "prebuilt",
        },
        "qr_slot_ids": [],
        "read_count": 0,
        "write_count": 1,
        "activation": min(1.0, len(payload) / 4096),
    }


def cells_from_list(items: list[dict]) -> dict:
    """items: [{"lang", "topic", "keywords", "snippets": [str, ...]}]"""
    result: dict = {}
    for item in items:
        lang = item["lang"]
        topic = item["topic"]
        kw = item["keywords"]
        for i, snippet in enumerate(item["snippets"]):
            seed = f"{lang}::{topic}::{i}::{snippet[:40]}"
            cid, cell = _cell(seed, snippet, lang, topic, kw)
            result[cid] = cell
    return result


# ===========================================================================
# KNOWLEDGE BASE
# ===========================================================================

KNOWLEDGE: list[dict] = []

# ---------------------------------------------------------------------------
# PYTHON
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "python", "topic": "variables", "keywords": ["variable", "assign", "type", "python"],
     "snippets": [
         "# Python variables\nx = 10\nname = 'Alice'\npi = 3.14159\nis_valid = True\ndata = None\nprint(type(x))  # <class 'int'>",
         "# Multiple assignment\na, b, c = 1, 2, 3\nx = y = z = 0\nfirst, *rest = [1, 2, 3, 4, 5]\nprint(first, rest)  # 1 [2, 3, 4, 5]",
         "# Type annotations\nname: str = 'Alice'\nage: int = 30\nscores: list[int] = [90, 85, 92]\nconfig: dict[str, str] = {'host': 'localhost'}",
         "# Constants (convention: UPPER_CASE)\nMAX_SIZE = 1000\nPI = 3.14159\nDEFAULT_TIMEOUT = 30\nAPI_URL = 'https://api.example.com'",
         "# Global and local scope\nx = 10\ndef modify():\n    global x\n    x = 20\nmodify()\nprint(x)  # 20",
     ]},
    {"lang": "python", "topic": "strings", "keywords": ["string", "str", "format", "f-string", "python"],
     "snippets": [
         "# String formatting\nname = 'Alice'\nage = 30\nprint(f'Hello {name}, you are {age} years old')\nprint('Hello %s, age %d' % (name, age))\nprint('Hello {}, age {}'.format(name, age))",
         "# String methods\ntext = '  Hello World  '\nprint(text.strip())       # 'Hello World'\nprint(text.lower())       # '  hello world  '\nprint(text.upper())       # '  HELLO WORLD  '\nprint(text.replace('World', 'Python'))\nprint(text.split())       # ['Hello', 'World']",
         "# String slicing\ntext = 'Hello World'\nprint(text[0:5])    # Hello\nprint(text[-5:])    # World\nprint(text[::-1])   # dlroW olleH\nprint(text[::2])    # HloWrd",
         "# Multiline strings\ndoc = \"\"\"\nThis is a\nmultiline string\nin Python.\n\"\"\"\nraw = r'C:\\Users\\file.txt'  # raw string",
         "# String operations\nparts = ['a', 'b', 'c']\nresult = ', '.join(parts)  # 'a, b, c'\nwords = 'one two three'.split()  # ['one', 'two', 'three']\nprint('hello' in 'hello world')  # True\nprint('world'.startswith('wor'))  # True",
     ]},
    {"lang": "python", "topic": "lists", "keywords": ["list", "array", "append", "comprehension", "python"],
     "snippets": [
         "# List operations\nnums = [1, 2, 3, 4, 5]\nnums.append(6)\nnums.extend([7, 8])\nnums.insert(0, 0)\nnums.remove(3)\npopped = nums.pop()\nprint(len(nums))",
         "# List comprehensions\nsquares = [x**2 for x in range(10)]\nevens = [x for x in range(20) if x % 2 == 0]\nflat = [x for row in [[1,2],[3,4]] for x in row]\npairs = [(x,y) for x in range(3) for y in range(3)]",
         "# List slicing\ndata = list(range(10))\nprint(data[2:7])    # [2, 3, 4, 5, 6]\nprint(data[::2])    # [0, 2, 4, 6, 8]\nprint(data[::-1])   # reversed\nchunks = [data[i:i+3] for i in range(0, len(data), 3)]",
         "# Sorting lists\nnums = [3, 1, 4, 1, 5, 9, 2, 6]\nsorted_nums = sorted(nums)             # new list\nnums.sort()                            # in-place\npeople = [('Alice', 30), ('Bob', 25)]\npeople.sort(key=lambda x: x[1])        # sort by age",
         "# Stack and queue with list\nstack = []\nstack.append(1)\nstack.append(2)\ntop = stack.pop()       # LIFO\n\nfrom collections import deque\nqueue = deque()\nqueue.append(1)\nqueue.append(2)\nfront = queue.popleft()  # FIFO",
     ]},
    {"lang": "python", "topic": "dicts", "keywords": ["dict", "dictionary", "key", "value", "python"],
     "snippets": [
         "# Dictionary basics\nd = {'name': 'Alice', 'age': 30}\nd['city'] = 'Moscow'\nprint(d.get('country', 'Unknown'))\nprint(d.keys())\nprint(d.values())\nprint(d.items())",
         "# Dict comprehensions\nsquares = {x: x**2 for x in range(10)}\nfiltered = {k: v for k, v in d.items() if v > 25}\ninverted = {v: k for k, v in {'a': 1, 'b': 2}.items()}",
         "# Merging dicts\nbase = {'a': 1, 'b': 2}\nextra = {'c': 3, 'b': 99}\nmerged = {**base, **extra}      # Python 3.5+\nmerged2 = base | extra          # Python 3.9+",
         "# defaultdict and Counter\nfrom collections import defaultdict, Counter\ndd = defaultdict(list)\ndd['key'].append(1)  # no KeyError\n\nwords = 'the quick brown fox the fox'.split()\ncounts = Counter(words)\nprint(counts.most_common(2))  # [('the', 2), ('fox', 2)]",
         "# Nested dicts\nconfig = {\n    'database': {'host': 'localhost', 'port': 5432},\n    'cache': {'host': 'localhost', 'port': 6379},\n}\ndb_host = config['database']['host']\nconfig.setdefault('logging', {})['level'] = 'INFO'",
     ]},
    {"lang": "python", "topic": "functions", "keywords": ["function", "def", "lambda", "args", "kwargs", "python"],
     "snippets": [
         "# Function basics\ndef greet(name: str, greeting: str = 'Hello') -> str:\n    \"\"\"Return a greeting string.\"\"\"\n    return f'{greeting}, {name}!'\n\nresult = greet('Alice')\nresult2 = greet('Bob', 'Hi')",
         "# *args and **kwargs\ndef variadic(*args, **kwargs):\n    print(args)    # tuple\n    print(kwargs)  # dict\n\nvariadic(1, 2, 3, name='Alice', age=30)\n\ndef total(*nums):\n    return sum(nums)",
         "# Lambda functions\ndouble = lambda x: x * 2\nadd = lambda x, y: x + y\nsorted_list = sorted(items, key=lambda x: x['score'])\nnums = list(map(lambda x: x**2, range(5)))\nevens = list(filter(lambda x: x % 2 == 0, range(10)))",
         "# Decorators\nimport functools\n\ndef timer(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        import time\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f'{func.__name__} took {time.time()-start:.3f}s')\n        return result\n    return wrapper\n\n@timer\ndef slow_function():\n    import time; time.sleep(0.1)",
         "# Generators\ndef fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\ndef read_chunks(file, size=1024):\n    while chunk := file.read(size):\n        yield chunk\n\ngen = fibonacci()\nprint([next(gen) for _ in range(10)])",
         "# Closures\ndef make_counter(start=0):\n    count = start\n    def counter():\n        nonlocal count\n        count += 1\n        return count\n    return counter\n\nc1 = make_counter()\nprint(c1(), c1(), c1())  # 1 2 3",
     ]},
    {"lang": "python", "topic": "classes", "keywords": ["class", "oop", "inheritance", "method", "python"],
     "snippets": [
         "# Class basics\nclass Animal:\n    def __init__(self, name: str, sound: str):\n        self.name = name\n        self.sound = sound\n\n    def speak(self) -> str:\n        return f'{self.name} says {self.sound}'\n\n    def __repr__(self) -> str:\n        return f'Animal({self.name!r})'",
         "# Inheritance\nclass Dog(Animal):\n    def __init__(self, name: str, breed: str):\n        super().__init__(name, 'Woof')\n        self.breed = breed\n\n    def fetch(self) -> str:\n        return f'{self.name} fetches the ball!'\n\ndog = Dog('Rex', 'Labrador')\nprint(dog.speak())",
         "# Dataclass\nfrom dataclasses import dataclass, field\n\n@dataclass\nclass Point:\n    x: float\n    y: float\n    z: float = 0.0\n    tags: list[str] = field(default_factory=list)\n\n    def distance(self) -> float:\n        return (self.x**2 + self.y**2 + self.z**2) ** 0.5",
         "# Properties\nclass Temperature:\n    def __init__(self, celsius: float = 0):\n        self._celsius = celsius\n\n    @property\n    def celsius(self) -> float:\n        return self._celsius\n\n    @celsius.setter\n    def celsius(self, value: float):\n        if value < -273.15:\n            raise ValueError('Below absolute zero')\n        self._celsius = value\n\n    @property\n    def fahrenheit(self) -> float:\n        return self._celsius * 9/5 + 32",
         "# Class and static methods\nclass MathUtils:\n    PI = 3.14159\n\n    @classmethod\n    def circle_area(cls, r: float) -> float:\n        return cls.PI * r ** 2\n\n    @staticmethod\n    def is_prime(n: int) -> bool:\n        if n < 2: return False\n        return all(n % i for i in range(2, int(n**0.5) + 1))",
         "# Abstract class\nfrom abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self) -> float: ...\n\n    @abstractmethod\n    def perimeter(self) -> float: ...\n\nclass Circle(Shape):\n    def __init__(self, r: float): self.r = r\n    def area(self): return 3.14159 * self.r**2\n    def perimeter(self): return 2 * 3.14159 * self.r",
     ]},
    {"lang": "python", "topic": "error_handling", "keywords": ["exception", "try", "except", "raise", "error", "python"],
     "snippets": [
         "# Try/except\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f'Error: {e}')\nexcept (TypeError, ValueError) as e:\n    print(f'Type/Value error: {e}')\nexcept Exception as e:\n    print(f'Unexpected: {e}')\nelse:\n    print('No error')\nfinally:\n    print('Always runs')",
         "# Custom exceptions\nclass AppError(Exception):\n    def __init__(self, message: str, code: int = 0):\n        super().__init__(message)\n        self.code = code\n\nclass NotFoundError(AppError): pass\nclass ValidationError(AppError): pass\n\ntry:\n    raise NotFoundError('User not found', 404)\nexcept NotFoundError as e:\n    print(e.code, e)",
         "# Context managers\nclass ManagedResource:\n    def __enter__(self):\n        print('Acquiring resource')\n        return self\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        print('Releasing resource')\n        return False  # re-raise exception\n\nwith ManagedResource() as r:\n    pass  # resource auto-released",
         "# contextlib\nfrom contextlib import contextmanager, suppress\n\n@contextmanager\ndef timer():\n    import time\n    start = time.time()\n    try:\n        yield\n    finally:\n        print(f'Elapsed: {time.time()-start:.3f}s')\n\nwith suppress(FileNotFoundError):\n    os.remove('nonexistent.txt')",
     ]},
    {"lang": "python", "topic": "async", "keywords": ["async", "await", "asyncio", "coroutine", "python"],
     "snippets": [
         "# Async basics\nimport asyncio\n\nasync def fetch_data(url: str) -> str:\n    await asyncio.sleep(0.1)  # simulate I/O\n    return f'data from {url}'\n\nasync def main():\n    result = await fetch_data('https://api.example.com')\n    print(result)\n\nasyncio.run(main())",
         "# Gather — run tasks concurrently\nimport asyncio\n\nasync def task(n):\n    await asyncio.sleep(n)\n    return n\n\nasync def main():\n    results = await asyncio.gather(\n        task(1), task(2), task(3)\n    )  # all run concurrently, total ~3s\n    print(results)  # [1, 2, 3]",
         "# Async context manager\nimport asyncio\n\nclass AsyncDB:\n    async def __aenter__(self):\n        await asyncio.sleep(0)  # connect\n        return self\n    async def __aexit__(self, *args):\n        await asyncio.sleep(0)  # close\n\nasync def main():\n    async with AsyncDB() as db:\n        pass",
         "# Async generator\nasync def paginate(url: str):\n    page = 1\n    while True:\n        data = await fetch(url, page=page)\n        if not data: break\n        yield data\n        page += 1\n\nasync def main():\n    async for page in paginate('https://api.example.com/items'):\n        process(page)",
     ]},
    {"lang": "python", "topic": "file_io", "keywords": ["file", "open", "read", "write", "path", "python"],
     "snippets": [
         "# Reading files\nwith open('data.txt', 'r', encoding='utf-8') as f:\n    content = f.read()      # entire file\n\nwith open('data.txt') as f:\n    lines = f.readlines()   # list of lines\n\nwith open('data.txt') as f:\n    for line in f:          # memory-efficient\n        process(line.strip())",
         "# Writing files\nwith open('output.txt', 'w', encoding='utf-8') as f:\n    f.write('Hello\\n')\n\nlines = ['line1', 'line2', 'line3']\nwith open('output.txt', 'w') as f:\n    f.writelines(line + '\\n' for line in lines)\n\n# Append mode\nwith open('log.txt', 'a') as f:\n    f.write('New log entry\\n')",
         "# pathlib\nfrom pathlib import Path\n\np = Path('data/output.txt')\np.parent.mkdir(parents=True, exist_ok=True)\np.write_text('Hello', encoding='utf-8')\ncontent = p.read_text()\n\nfor py_file in Path('.').rglob('*.py'):\n    print(py_file)",
         "# JSON\nimport json\n\ndata = {'name': 'Alice', 'scores': [90, 85, 92]}\nwith open('data.json', 'w') as f:\n    json.dump(data, f, indent=2, ensure_ascii=False)\n\nwith open('data.json') as f:\n    loaded = json.load(f)\n\njson_str = json.dumps(data)\nobj = json.loads(json_str)",
         "# CSV\nimport csv\n\nwith open('data.csv', 'w', newline='') as f:\n    writer = csv.DictWriter(f, fieldnames=['name', 'age'])\n    writer.writeheader()\n    writer.writerows([{'name': 'Alice', 'age': 30}])\n\nwith open('data.csv') as f:\n    for row in csv.DictReader(f):\n        print(row['name'], row['age'])",
     ]},
    {"lang": "python", "topic": "comprehensions", "keywords": ["comprehension", "list", "dict", "set", "generator", "python"],
     "snippets": [
         "# All comprehension types\n# List\nsquares = [x**2 for x in range(10)]\n# Dict\nsq_map = {x: x**2 for x in range(10)}\n# Set\nunique_sq = {x**2 for x in range(-5, 6)}\n# Generator (lazy, memory-efficient)\ngen = (x**2 for x in range(1_000_000))",
         "# Nested comprehensions\nmatrix = [[i*j for j in range(1, 6)] for i in range(1, 6)]\nflat = [x for row in matrix for x in row]\nresult = [[row[i] for row in matrix] for i in range(5)]  # transpose",
         "# Conditional comprehensions\npositive = [x for x in nums if x > 0]\nclassified = ['even' if x%2==0 else 'odd' for x in range(10)]\nfiltered_map = {k: v for k, v in d.items() if v is not None}",
     ]},
    {"lang": "python", "topic": "itertools", "keywords": ["itertools", "chain", "product", "groupby", "python"],
     "snippets": [
         "import itertools\n\n# chain — flatten iterables\nresult = list(itertools.chain([1,2], [3,4], [5,6]))  # [1,2,3,4,5,6]\n\n# product — Cartesian product\ncombos = list(itertools.product([1,2], ['a','b']))\n# [(1,'a'),(1,'b'),(2,'a'),(2,'b')]\n\n# permutations / combinations\nperms = list(itertools.permutations([1,2,3], 2))\ncombinations = list(itertools.combinations([1,2,3,4], 2))",
         "import itertools\n\n# groupby\ndata = [('A',1),('A',2),('B',3),('B',4)]\nfor key, group in itertools.groupby(data, key=lambda x: x[0]):\n    print(key, list(group))\n\n# islice — lazy slicing\nfirst_5 = list(itertools.islice(gen, 5))\n\n# cycle and repeat\ntoggle = itertools.cycle(['ON', 'OFF'])\nones = list(itertools.repeat(1, 5))  # [1,1,1,1,1]",
     ]},
    {"lang": "python", "topic": "typing", "keywords": ["typing", "type hint", "generic", "union", "optional", "python"],
     "snippets": [
         "from typing import Optional, Union, List, Dict, Tuple, Any\nfrom typing import Callable, TypeVar, Generic\n\ndef find_user(id: int) -> Optional[str]:\n    return None\n\ndef process(data: Union[str, bytes]) -> str:\n    return str(data)\n\ndef transform(items: List[int], fn: Callable[[int], int]) -> List[int]:\n    return [fn(x) for x in items]",
         "from typing import TypeVar, Generic, Protocol\n\nT = TypeVar('T')\n\nclass Stack(Generic[T]):\n    def __init__(self) -> None:\n        self._items: list[T] = []\n    def push(self, item: T) -> None:\n        self._items.append(item)\n    def pop(self) -> T:\n        return self._items.pop()\n\nclass Comparable(Protocol):\n    def __lt__(self, other: Any) -> bool: ...",
     ]},
    {"lang": "python", "topic": "functools", "keywords": ["functools", "lru_cache", "partial", "reduce", "python"],
     "snippets": [
         "import functools\n\n# lru_cache — memoisation\n@functools.lru_cache(maxsize=128)\ndef fib(n: int) -> int:\n    if n < 2: return n\n    return fib(n-1) + fib(n-2)\n\n# cache (Python 3.9+, unbounded)\n@functools.cache\ndef expensive(n): ...\n\n# partial\nmultiply = lambda x, y: x * y\ndouble = functools.partial(multiply, 2)\nprint(double(5))  # 10",
         "import functools\n\n# reduce\ntotal = functools.reduce(lambda a, b: a + b, [1,2,3,4,5])\nproduct = functools.reduce(lambda a, b: a * b, range(1, 6))\n\n# wraps — preserve metadata in decorators\ndef my_decorator(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs)\n    return wrapper",
     ]},
    {"lang": "python", "topic": "numpy", "keywords": ["numpy", "array", "matrix", "ndarray", "python"],
     "snippets": [
         "import numpy as np\n\n# Array creation\na = np.array([1, 2, 3, 4, 5])\nb = np.zeros((3, 4))\nc = np.ones((2, 3))\nd = np.arange(0, 10, 0.5)\ne = np.linspace(0, 1, 100)\nf = np.random.rand(3, 3)\nI = np.eye(4)  # identity matrix",
         "import numpy as np\n\n# Operations\na = np.array([[1,2],[3,4]])\nb = np.array([[5,6],[7,8]])\nprint(a + b)          # element-wise add\nprint(a @ b)          # matrix multiply\nprint(a.T)            # transpose\nprint(np.dot(a, b))   # dot product\nprint(np.linalg.inv(a))  # inverse",
         "import numpy as np\n\n# Indexing and slicing\na = np.arange(24).reshape(4, 6)\nprint(a[1, 3])         # element\nprint(a[1:3, 2:5])     # submatrix\nmask = a > 10\nprint(a[mask])          # boolean index\nprint(a[:, 0])          # first column",
     ]},
    {"lang": "python", "topic": "pandas", "keywords": ["pandas", "dataframe", "series", "csv", "data analysis", "python"],
     "snippets": [
         "import pandas as pd\n\n# Create DataFrame\ndf = pd.DataFrame({\n    'name': ['Alice', 'Bob', 'Charlie'],\n    'age': [30, 25, 35],\n    'score': [90.5, 85.0, 92.3]\n})\nprint(df.head())\nprint(df.describe())\nprint(df.dtypes)",
         "import pandas as pd\n\n# Data manipulation\ndf = pd.read_csv('data.csv')\ndf_clean = df.dropna()              # remove NaN rows\ndf['total'] = df['a'] + df['b']\nfiltered = df[df['age'] > 25]\ngrouped = df.groupby('city')['salary'].mean()\nsorted_df = df.sort_values('score', ascending=False)",
         "import pandas as pd\n\n# Merge and join\ndf1 = pd.DataFrame({'id': [1,2,3], 'name': ['A','B','C']})\ndf2 = pd.DataFrame({'id': [2,3,4], 'score': [90,85,88]})\ninner = pd.merge(df1, df2, on='id', how='inner')\nouter = pd.merge(df1, df2, on='id', how='outer')\nleft  = pd.merge(df1, df2, on='id', how='left')",
     ]},
    {"lang": "python", "topic": "requests", "keywords": ["requests", "http", "get", "post", "api", "python"],
     "snippets": [
         "import requests\n\n# GET request\nresp = requests.get(\n    'https://api.example.com/users',\n    params={'page': 1, 'limit': 20},\n    headers={'Authorization': 'Bearer TOKEN'},\n    timeout=10\n)\nresp.raise_for_status()\ndata = resp.json()",
         "import requests\n\n# POST request\nresp = requests.post(\n    'https://api.example.com/users',\n    json={'name': 'Alice', 'email': 'alice@example.com'},\n    headers={'Content-Type': 'application/json'},\n    timeout=10\n)\nif resp.status_code == 201:\n    user = resp.json()",
         "import requests\nfrom requests.adapters import HTTPAdapter\nfrom urllib3.util.retry import Retry\n\n# Session with retry\nsession = requests.Session()\nretry = Retry(total=3, backoff_factor=0.5,\n              status_forcelist=[500, 502, 503])\nsession.mount('https://', HTTPAdapter(max_retries=retry))\nresp = session.get('https://api.example.com')",
     ]},
    {"lang": "python", "topic": "regex", "keywords": ["regex", "re", "pattern", "match", "search", "python"],
     "snippets": [
         "import re\n\npattern = r'\\b\\d{3}-\\d{4}\\b'  # phone\ntext = 'Call 555-1234 or 555-5678'\nmatches = re.findall(pattern, text)\nprint(matches)  # ['555-1234', '555-5678']\n\nm = re.search(r'(\\w+)@(\\w+\\.\\w+)', 'user@example.com')\nif m:\n    print(m.group(1), m.group(2))",
         "import re\n\n# Common patterns\nEMAIL = r'^[\\w.+-]+@[\\w-]+\\.[\\w.]+$'\nURL   = r'https?://[\\w./%-]+'\nIPv4  = r'\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b'\nDATE  = r'\\d{4}-\\d{2}-\\d{2}'\n\n# Substitution\ncleaned = re.sub(r'\\s+', ' ', text.strip())\ncamel = re.sub(r'_(\\w)', lambda m: m.group(1).upper(), 'hello_world')",
     ]},
    {"lang": "python", "topic": "testing", "keywords": ["pytest", "unittest", "test", "assert", "mock", "python"],
     "snippets": [
         "# pytest basics\nimport pytest\n\ndef add(a, b):\n    return a + b\n\ndef test_add():\n    assert add(2, 3) == 5\n    assert add(-1, 1) == 0\n\ndef test_add_floats():\n    assert add(0.1, 0.2) == pytest.approx(0.3)\n\n@pytest.mark.parametrize('a,b,expected', [\n    (2, 3, 5), (-1, 1, 0), (0, 0, 0)\n])\ndef test_add_param(a, b, expected):\n    assert add(a, b) == expected",
         "# Fixtures and mocking\nimport pytest\nfrom unittest.mock import Mock, patch, MagicMock\n\n@pytest.fixture\ndef db():\n    conn = MagicMock()\n    yield conn\n    conn.close()\n\ndef test_user_service(db):\n    db.query.return_value = [{'id': 1}]\n    result = get_users(db)\n    assert len(result) == 1\n    db.query.assert_called_once()",
     ]},
    {"lang": "python", "topic": "logging", "keywords": ["logging", "logger", "debug", "info", "warning", "python"],
     "snippets": [
         "import logging\n\nlogging.basicConfig(\n    level=logging.INFO,\n    format='%(asctime)s [%(levelname)s] %(name)s — %(message)s'\n)\nlogger = logging.getLogger(__name__)\n\nlogger.debug('Debug message')\nlogger.info('Server started on port %d', 8000)\nlogger.warning('Low memory: %d MB', 512)\nlogger.error('Connection failed: %s', err)\nlogger.exception('Unhandled error')",
         "import logging\nfrom logging.handlers import RotatingFileHandler\n\n# File handler with rotation\nhandler = RotatingFileHandler(\n    'app.log', maxBytes=10*1024*1024, backupCount=5\n)\nhandler.setFormatter(logging.Formatter(\n    '%(asctime)s %(levelname)s %(name)s %(message)s'\n))\nlogging.getLogger().addHandler(handler)",
     ]},
]

# ---------------------------------------------------------------------------
# JAVASCRIPT
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "javascript", "topic": "variables", "keywords": ["var", "let", "const", "javascript"],
     "snippets": [
         "// Variable declarations\nconst PI = 3.14159;       // immutable binding\nlet counter = 0;          // mutable\ncounter++;                // OK\n\n// Destructuring\nconst [first, second, ...rest] = [1, 2, 3, 4, 5];\nconst { name, age = 0, city: town } = person;\n\n// Template literals\nconst msg = `Hello ${name}, you are ${age} years old`;",
         "// Spread and rest\nconst arr1 = [1, 2, 3];\nconst arr2 = [...arr1, 4, 5];   // spread\nconst merged = { ...obj1, ...obj2 };\n\nfunction sum(...nums) {           // rest\n  return nums.reduce((a, b) => a + b, 0);\n}\n\n// Optional chaining and nullish\nconst city = user?.address?.city ?? 'Unknown';",
     ]},
    {"lang": "javascript", "topic": "functions", "keywords": ["function", "arrow", "callback", "closure", "javascript"],
     "snippets": [
         "// Arrow functions\nconst double = x => x * 2;\nconst add = (a, b) => a + b;\nconst greet = name => `Hello, ${name}!`;\nconst getObj = () => ({ x: 1, y: 2 });\n\n// Higher-order functions\nconst nums = [1, 2, 3, 4, 5];\nconst doubled = nums.map(x => x * 2);\nconst evens = nums.filter(x => x % 2 === 0);\nconst total = nums.reduce((sum, x) => sum + x, 0);",
         "// Closures\nfunction makeCounter(start = 0) {\n  let count = start;\n  return {\n    increment() { count++; },\n    decrement() { count--; },\n    value() { return count; }\n  };\n}\n\nconst counter = makeCounter(10);\ncounter.increment();\nconsole.log(counter.value()); // 11",
         "// IIFE and module pattern\n(function() {\n  'use strict';\n  // private scope\n  let _private = 0;\n  window.myModule = {\n    inc() { _private++; },\n    get() { return _private; }\n  };\n})();\n\n// Default and named exports\nexport const PI = 3.14;\nexport default function main() {}\nexport { foo, bar };",
     ]},
    {"lang": "javascript", "topic": "promises", "keywords": ["promise", "async", "await", "then", "javascript"],
     "snippets": [
         "// Promise basics\nconst p = new Promise((resolve, reject) => {\n  setTimeout(() => resolve('done'), 1000);\n});\n\np.then(result => console.log(result))\n .catch(err => console.error(err))\n .finally(() => console.log('cleanup'));\n\n// Promise.all\nconst [users, posts] = await Promise.all([\n  fetchUsers(), fetchPosts()\n]);",
         "// async/await\nasync function fetchUser(id) {\n  try {\n    const resp = await fetch(`/api/users/${id}`);\n    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);\n    return await resp.json();\n  } catch (err) {\n    console.error('Failed:', err);\n    throw err;\n  }\n}\n\n// Sequential vs parallel\nconst a = await step1();\nconst b = await step2(a);\n// parallel:\nconst [x, y] = await Promise.all([op1(), op2()]);",
         "// Async iteration\nasync function* paginate(url) {\n  let page = 1;\n  while (true) {\n    const data = await fetchPage(url, page++);\n    if (!data.length) return;\n    yield data;\n  }\n}\n\nfor await (const page of paginate('/api/items')) {\n  console.log(page);\n}",
     ]},
    {"lang": "javascript", "topic": "classes", "keywords": ["class", "extends", "constructor", "javascript"],
     "snippets": [
         "// ES6 class\nclass Animal {\n  #name;  // private field\n  constructor(name, sound) {\n    this.#name = name;\n    this.sound = sound;\n  }\n  speak() {\n    return `${this.#name} says ${this.sound}`;\n  }\n  get name() { return this.#name; }\n  static create(name) { return new Animal(name, '...'); }\n}",
         "// Inheritance\nclass Dog extends Animal {\n  constructor(name, breed) {\n    super(name, 'Woof');\n    this.breed = breed;\n  }\n  fetch() {\n    return `${this.name} fetches!`;\n  }\n}\n\n// Mixins\nconst Serializable = (Base) => class extends Base {\n  toJSON() { return JSON.stringify(this); }\n};",
     ]},
    {"lang": "javascript", "topic": "dom", "keywords": ["DOM", "document", "querySelector", "event", "javascript"],
     "snippets": [
         "// DOM manipulation\nconst btn = document.querySelector('#submit-btn');\nconst list = document.getElementById('items');\n\nbtn.addEventListener('click', (e) => {\n  e.preventDefault();\n  const item = document.createElement('li');\n  item.textContent = 'New item';\n  list.appendChild(item);\n});\n\n// Class manipulation\nelem.classList.add('active');\nelem.classList.toggle('hidden');\nelem.classList.contains('selected');",
         "// Event delegation\ndocument.querySelector('#list').addEventListener('click', (e) => {\n  if (e.target.matches('.delete-btn')) {\n    e.target.closest('li').remove();\n  }\n});\n\n// Form handling\nform.addEventListener('submit', async (e) => {\n  e.preventDefault();\n  const data = Object.fromEntries(new FormData(form));\n  await submitData(data);\n});",
     ]},
    {"lang": "javascript", "topic": "fetch_api", "keywords": ["fetch", "xhr", "http", "request", "javascript"],
     "snippets": [
         "// Fetch API\nasync function api(method, url, body = null) {\n  const opts = {\n    method,\n    headers: { 'Content-Type': 'application/json',\n                'Authorization': `Bearer ${getToken()}` }\n  };\n  if (body) opts.body = JSON.stringify(body);\n  const r = await fetch(url, opts);\n  if (!r.ok) throw new Error(await r.text());\n  return r.json();\n}\n\nconst user = await api('GET', '/api/users/1');\nawait api('POST', '/api/users', { name: 'Alice' });",
     ]},
    {"lang": "javascript", "topic": "array_methods", "keywords": ["map", "filter", "reduce", "find", "array", "javascript"],
     "snippets": [
         "const users = [\n  {id:1, name:'Alice', age:30, active:true},\n  {id:2, name:'Bob',   age:25, active:false},\n  {id:3, name:'Carol', age:35, active:true},\n];\n\nconst names   = users.map(u => u.name);\nconst actives = users.filter(u => u.active);\nconst avgAge  = users.reduce((sum,u) => sum+u.age, 0) / users.length;\nconst alice   = users.find(u => u.name === 'Alice');\nconst hasAdult = users.some(u => u.age >= 18);\nconst allAdult = users.every(u => u.age >= 18);\nconst sorted   = [...users].sort((a,b) => a.age - b.age);",
         "// flat and flatMap\nconst nested = [[1,2],[3,4],[5,6]];\nconst flat = nested.flat();\nconst flatMapped = nested.flatMap(x => x.map(n => n*2));\n\n// Array.from\nconst range = Array.from({length: 10}, (_, i) => i);\nconst chars = Array.from('hello');  // ['h','e','l','l','o']\nconst unique = [...new Set([1,2,2,3,3,4])];",
     ]},
    {"lang": "javascript", "topic": "modules", "keywords": ["import", "export", "module", "esm", "javascript"],
     "snippets": [
         "// ES Modules\n// utils.js\nexport const add = (a, b) => a + b;\nexport const multiply = (a, b) => a * b;\nexport default class Calculator {\n  add(a, b) { return a + b; }\n}\n\n// main.js\nimport Calculator, { add, multiply } from './utils.js';\nimport * as utils from './utils.js';\nimport { add as sum } from './utils.js';\nimport('./lazy.js').then(mod => mod.run());  // dynamic",
     ]},
]

# ---------------------------------------------------------------------------
# TYPESCRIPT
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "typescript", "topic": "types", "keywords": ["type", "interface", "typescript", "generic"],
     "snippets": [
         "// Basic types\nlet name: string = 'Alice';\nlet age: number = 30;\nlet active: boolean = true;\nlet ids: number[] = [1, 2, 3];\nlet tuple: [string, number] = ['Alice', 30];\nlet anything: unknown = 42;\n\n// Type alias\ntype ID = string | number;\ntype Callback<T> = (value: T) => void;\ntype Nullable<T> = T | null;",
         "// Interfaces\ninterface User {\n  id: number;\n  name: string;\n  email?: string;           // optional\n  readonly createdAt: Date; // immutable\n}\n\ninterface Admin extends User {\n  permissions: string[];\n}\n\n// Index signature\ninterface StringMap {\n  [key: string]: string;\n}\n\ninterface Repo<T> {\n  findById(id: number): Promise<T>;\n  findAll(): Promise<T[]>;\n  save(entity: T): Promise<T>;\n}",
         "// Generics\nfunction identity<T>(value: T): T { return value; }\n\nclass Stack<T> {\n  private items: T[] = [];\n  push(item: T): void { this.items.push(item); }\n  pop(): T | undefined { return this.items.pop(); }\n  peek(): T | undefined { return this.items[this.items.length - 1]; }\n}\n\nconst stack = new Stack<number>();",
         "// Utility types\ntype Partial<T>   = { [K in keyof T]?: T[K] };\ntype Required<T>  = { [K in keyof T]-?: T[K] };\ntype Readonly<T>  = { readonly [K in keyof T]: T[K] };\ntype Pick<T,K>    = { [P in K & keyof T]: T[P] };\ntype Omit<T,K>    = Pick<T, Exclude<keyof T, K>>;\ntype Record<K,V>  = { [P in K & string]: V };\n\n// Usage\ntype UserUpdate = Partial<User>;\ntype UserDTO    = Omit<User, 'password'>;\ntype UserMap    = Record<string, User>;",
         "// Discriminated unions\ntype Result<T, E = Error> =\n  | { ok: true;  value: T }\n  | { ok: false; error: E };\n\nfunction divide(a: number, b: number): Result<number> {\n  if (b === 0) return { ok: false, error: new Error('Division by zero') };\n  return { ok: true, value: a / b };\n}\n\nconst r = divide(10, 2);\nif (r.ok) console.log(r.value);\nelse console.error(r.error.message);",
     ]},
    {"lang": "typescript", "topic": "decorators", "keywords": ["decorator", "class", "method", "typescript"],
     "snippets": [
         "// Class decorator\nfunction Singleton<T extends {new(...args: any[]): {}}>(constructor: T) {\n  let instance: InstanceType<T>;\n  return class extends constructor {\n    constructor(...args: any[]) {\n      if (instance) return instance;\n      super(...args);\n      instance = this as any;\n    }\n  };\n}\n\n@Singleton\nclass Config { host = 'localhost'; }",
         "// Method decorator\nfunction log(target: any, key: string, desc: PropertyDescriptor) {\n  const original = desc.value;\n  desc.value = function(...args: any[]) {\n    console.log(`Calling ${key}(${args})`);\n    const result = original.apply(this, args);\n    console.log(`${key} returned`, result);\n    return result;\n  };\n  return desc;\n}",
     ]},
]

# ---------------------------------------------------------------------------
# HTML / CSS
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "html", "topic": "structure", "keywords": ["html", "head", "body", "semantic", "html5"],
     "snippets": [
         "<!DOCTYPE html>\n<html lang='ru'>\n<head>\n  <meta charset='UTF-8'>\n  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n  <meta name='description' content='Page description'>\n  <title>Page Title</title>\n  <link rel='stylesheet' href='style.css'>\n</head>\n<body>\n  <header><nav>...</nav></header>\n  <main><article>...</article></main>\n  <footer>...</footer>\n  <script src='app.js' defer></script>\n</body>\n</html>",
         "<!-- Semantic HTML5 -->\n<header>\n  <nav aria-label='Main navigation'>\n    <ul role='menubar'>\n      <li role='menuitem'><a href='/'>Home</a></li>\n    </ul>\n  </nav>\n</header>\n<main>\n  <section aria-labelledby='section-title'>\n    <h2 id='section-title'>Section</h2>\n    <article>Content</article>\n    <aside>Sidebar</aside>\n  </section>\n</main>\n<footer><address>Contact</address></footer>",
         "<!-- Forms -->\n<form action='/submit' method='POST' novalidate>\n  <fieldset>\n    <legend>User Info</legend>\n    <label for='name'>Name</label>\n    <input type='text' id='name' name='name' required minlength='2' autocomplete='name'>\n    <label for='email'>Email</label>\n    <input type='email' id='email' name='email' required>\n    <input type='password' id='password' name='password' minlength='8'>\n    <button type='submit'>Submit</button>\n  </fieldset>\n</form>",
     ]},
    {"lang": "css", "topic": "flexbox", "keywords": ["flexbox", "flex", "align", "justify", "css"],
     "snippets": [
         "/* Flexbox container */\n.container {\n  display: flex;\n  flex-direction: row;        /* row | column */\n  flex-wrap: wrap;\n  justify-content: space-between; /* main axis */\n  align-items: center;        /* cross axis */\n  align-content: flex-start;\n  gap: 1rem;\n}\n\n/* Flex item */\n.item {\n  flex: 1 1 200px; /* grow shrink basis */\n  align-self: stretch;\n  order: 2;\n}",
         "/* CSS Grid */\n.grid {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  grid-template-rows: auto;\n  gap: 1rem;\n  grid-template-areas:\n    'header header'\n    'sidebar main'\n    'footer footer';\n}\n.header  { grid-area: header; }\n.sidebar { grid-area: sidebar; }\n.main    { grid-area: main; }\n.footer  { grid-area: footer; }",
         "/* Responsive design */\n.container {\n  width: min(90%, 1200px);\n  margin-inline: auto;\n  padding-inline: 1rem;\n}\n\n@media (max-width: 768px) {\n  .grid { grid-template-columns: 1fr; }\n  .sidebar { display: none; }\n}\n\n@media (prefers-color-scheme: dark) {\n  body { background: #1a1a1a; color: #eee; }\n}",
         "/* CSS custom properties */\n:root {\n  --primary: #3b82f6;\n  --secondary: #10b981;\n  --font-size-base: 1rem;\n  --spacing-sm: 0.5rem;\n  --spacing-md: 1rem;\n  --border-radius: 0.375rem;\n}\n\n.btn {\n  background: var(--primary);\n  border-radius: var(--border-radius);\n  padding: var(--spacing-sm) var(--spacing-md);\n}",
         "/* CSS animations */\n@keyframes fadeIn {\n  from { opacity: 0; transform: translateY(-10px); }\n  to   { opacity: 1; transform: translateY(0); }\n}\n\n.modal {\n  animation: fadeIn 0.3s ease-out;\n}\n\n.spinner {\n  animation: spin 1s linear infinite;\n}\n@keyframes spin {\n  to { transform: rotate(360deg); }\n}",
     ]},
]

# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "sql", "topic": "basics", "keywords": ["select", "from", "where", "sql", "query"],
     "snippets": [
         "-- Basic SELECT\nSELECT id, name, email, created_at\nFROM users\nWHERE active = true\n  AND created_at > '2024-01-01'\nORDER BY name ASC\nLIMIT 20 OFFSET 40;",
         "-- Aggregations\nSELECT\n  department,\n  COUNT(*)        AS employee_count,\n  AVG(salary)     AS avg_salary,\n  MAX(salary)     AS max_salary,\n  SUM(salary)     AS total_salary\nFROM employees\nGROUP BY department\nHAVING COUNT(*) > 5\nORDER BY avg_salary DESC;",
         "-- JOINs\nSELECT u.name, o.id AS order_id, p.name AS product, oi.quantity\nFROM users u\nINNER JOIN orders o  ON o.user_id    = u.id\nINNER JOIN order_items oi ON oi.order_id = o.id\nINNER JOIN products p  ON p.id        = oi.product_id\nWHERE o.status = 'completed'\nORDER BY o.created_at DESC;",
         "-- Subqueries and CTEs\nWITH monthly_sales AS (\n  SELECT\n    DATE_TRUNC('month', created_at) AS month,\n    SUM(amount) AS total\n  FROM orders\n  GROUP BY 1\n),\nranked AS (\n  SELECT *, RANK() OVER (ORDER BY total DESC) AS rank\n  FROM monthly_sales\n)\nSELECT * FROM ranked WHERE rank <= 3;",
         "-- Window functions\nSELECT\n  name,\n  salary,\n  department,\n  RANK()  OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank,\n  LAG(salary)  OVER (ORDER BY hire_date) AS prev_salary,\n  SUM(salary)  OVER (PARTITION BY department) AS dept_total,\n  salary / SUM(salary) OVER (PARTITION BY department) AS pct_of_dept\nFROM employees;",
         "-- DDL: Create table\nCREATE TABLE users (\n  id          BIGSERIAL PRIMARY KEY,\n  email       VARCHAR(255) UNIQUE NOT NULL,\n  name        VARCHAR(100) NOT NULL,\n  password_hash TEXT NOT NULL,\n  role        VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user','admin')),\n  active      BOOLEAN DEFAULT true,\n  created_at  TIMESTAMPTZ DEFAULT NOW(),\n  updated_at  TIMESTAMPTZ DEFAULT NOW()\n);\nCREATE INDEX idx_users_email ON users(email);\nCREATE INDEX idx_users_created ON users(created_at DESC);",
         "-- DML: INSERT, UPDATE, DELETE\nINSERT INTO users (email, name, password_hash)\nVALUES ('alice@example.com', 'Alice', 'hash')\nON CONFLICT (email) DO UPDATE\n  SET name = EXCLUDED.name, updated_at = NOW()\nRETURNING id, email;\n\nUPDATE orders\nSET status = 'shipped', shipped_at = NOW()\nWHERE id = $1 AND status = 'pending';\n\nDELETE FROM sessions WHERE expires_at < NOW();",
         "-- Transactions\nBEGIN;\n  UPDATE accounts SET balance = balance - 100 WHERE id = 1;\n  UPDATE accounts SET balance = balance + 100 WHERE id = 2;\n  INSERT INTO transfers (from_id, to_id, amount) VALUES (1, 2, 100);\nCOMMIT;\n-- On error: ROLLBACK;",
     ]},
]

# ---------------------------------------------------------------------------
# BASH / SHELL
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "bash", "topic": "scripting", "keywords": ["bash", "shell", "script", "linux", "command"],
     "snippets": [
         "#!/usr/bin/env bash\nset -euo pipefail  # exit on error, undefined vars, pipe failures\n\n# Variables\nNAME='Alice'\nAGE=30\nGREETING=\"Hello, ${NAME}!\"\necho \"${GREETING}\"\n\n# Arrays\nFRUITS=(apple banana cherry)\necho \"${FRUITS[0]}\"\necho \"${#FRUITS[@]}\"  # length",
         "#!/bin/bash\n# Conditionals\nif [[ -f \"${FILE}\" ]]; then\n  echo 'File exists'\nelif [[ -d \"${FILE}\" ]]; then\n  echo 'Directory exists'\nelse\n  echo 'Not found'\nfi\n\n# String comparison\n[[ \"${STATUS}\" == 'running' ]] && echo 'OK'\n[[ \"${COUNT}\" -gt 10 ]] && echo 'High'\n[[ -z \"${VAR}\" ]] && echo 'Empty'",
         "#!/bin/bash\n# Loops\nfor file in *.log; do\n  echo \"Processing ${file}\"\n  gzip \"${file}\"\ndone\n\nfor i in $(seq 1 10); do\n  echo \"Step ${i}\"\ndone\n\nwhile IFS= read -r line; do\n  echo \"Line: ${line}\"\ndone < input.txt",
         "#!/bin/bash\n# Functions\nlog() {\n  local level=\"${1}\"\n  local message=\"${2}\"\n  echo \"[$(date '+%Y-%m-%d %H:%M:%S')] [${level}] ${message}\"\n}\n\nretry() {\n  local retries=3\n  local cmd=\"$@\"\n  for i in $(seq 1 ${retries}); do\n    ${cmd} && return 0\n    echo \"Attempt ${i} failed, retrying...\"\n    sleep $((i*2))\n  done\n  return 1\n}",
         "#!/bin/bash\n# Useful one-liners\n# Find and replace in files\nfind . -name '*.py' -exec sed -i 's/old/new/g' {} +\n\n# Count lines in all files\nfind . -name '*.py' | xargs wc -l | tail -1\n\n# Monitor a process\nwatch -n 1 'ps aux | grep python'\n\n# Archive and compress\ntar -czf backup-$(date +%Y%m%d).tar.gz ./data/\n\n# Kill process by port\nlsof -ti:8000 | xargs kill -9",
         "#!/bin/bash\n# Error handling\ntrap 'echo \"Error on line ${LINENO}\"; exit 1' ERR\ntrap 'cleanup' EXIT\n\ncleanup() {\n  rm -f /tmp/tempfile\n  echo 'Cleanup done'\n}\n\n# Check command exists\ncommand -v docker &>/dev/null || { echo 'docker required'; exit 1; }\n\n# Default values\nPORT=\"${PORT:-8000}\"\nENV=\"${ENVIRONMENT:-development}\"",
     ]},
]

# ---------------------------------------------------------------------------
# GO
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "go", "topic": "basics", "keywords": ["go", "golang", "func", "struct", "goroutine"],
     "snippets": [
         "package main\n\nimport (\n\t\"fmt\"\n\t\"errors\"\n)\n\nfunc divide(a, b float64) (float64, error) {\n\tif b == 0 {\n\t\treturn 0, errors.New(\"division by zero\")\n\t}\n\treturn a / b, nil\n}\n\nfunc main() {\n\tresult, err := divide(10, 2)\n\tif err != nil {\n\t\tfmt.Printf(\"Error: %v\\n\", err)\n\t\treturn\n\t}\n\tfmt.Printf(\"Result: %.2f\\n\", result)\n}",
         "// Structs and methods\ntype User struct {\n\tID        int\n\tName      string\n\tEmail     string\n\tCreatedAt time.Time\n}\n\nfunc (u User) String() string {\n\treturn fmt.Sprintf(\"User{%d, %s}\", u.ID, u.Name)\n}\n\nfunc (u *User) UpdateEmail(email string) error {\n\tif !strings.Contains(email, \"@\") {\n\t\treturn fmt.Errorf(\"invalid email: %s\", email)\n\t}\n\tu.Email = email\n\treturn nil\n}",
         "// Goroutines and channels\nfunc producer(ch chan<- int, n int) {\n\tfor i := 0; i < n; i++ {\n\t\tch <- i\n\t}\n\tclose(ch)\n}\n\nfunc main() {\n\tch := make(chan int, 10)\n\tgo producer(ch, 5)\n\n\tfor val := range ch {\n\t\tfmt.Println(val)\n\t}\n}",
         "// HTTP server\npackage main\n\nimport (\n\t\"encoding/json\"\n\t\"net/http\"\n)\n\nfunc usersHandler(w http.ResponseWriter, r *http.Request) {\n\tusers := []map[string]any{{\"id\": 1, \"name\": \"Alice\"}}\n\tw.Header().Set(\"Content-Type\", \"application/json\")\n\tjson.NewEncoder(w).Encode(users)\n}\n\nfunc main() {\n\thttp.HandleFunc(\"/api/users\", usersHandler)\n\thttp.ListenAndServe(\":8080\", nil)\n}",
         "// Interfaces\ntype Shape interface {\n\tArea() float64\n\tPerimeter() float64\n}\n\ntype Circle struct { Radius float64 }\nfunc (c Circle) Area() float64      { return math.Pi * c.Radius * c.Radius }\nfunc (c Circle) Perimeter() float64 { return 2 * math.Pi * c.Radius }\n\ntype Rectangle struct { Width, Height float64 }\nfunc (r Rectangle) Area() float64      { return r.Width * r.Height }\nfunc (r Rectangle) Perimeter() float64 { return 2*(r.Width+r.Height) }",
         "// Error wrapping\nvar ErrNotFound = errors.New(\"not found\")\n\nfunc getUser(id int) (*User, error) {\n\tuser, err := db.QueryRow(id)\n\tif err == sql.ErrNoRows {\n\t\treturn nil, fmt.Errorf(\"getUser %d: %w\", id, ErrNotFound)\n\t}\n\tif err != nil {\n\t\treturn nil, fmt.Errorf(\"getUser %d: %w\", id, err)\n\t}\n\treturn user, nil\n}\n\nif errors.Is(err, ErrNotFound) { /* handle */ }",
     ]},
]

# ---------------------------------------------------------------------------
# RUST
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "rust", "topic": "basics", "keywords": ["rust", "ownership", "borrow", "lifetime", "struct"],
     "snippets": [
         "// Ownership and borrowing\nfn main() {\n    let s1 = String::from(\"hello\");\n    let s2 = &s1;           // immutable borrow\n    let len = calculate_length(&s1);\n    println!(\"{} has {} chars\", s1, len);\n}\n\nfn calculate_length(s: &String) -> usize {\n    s.len()\n}",
         "// Structs and impl\n#[derive(Debug, Clone)]\nstruct User {\n    name: String,\n    email: String,\n    active: bool,\n}\n\nimpl User {\n    fn new(name: &str, email: &str) -> Self {\n        Self { name: name.to_string(), email: email.to_string(), active: true }\n    }\n    fn deactivate(&mut self) { self.active = false; }\n}",
         "// Result and Option\nfn divide(a: f64, b: f64) -> Result<f64, String> {\n    if b == 0.0 { Err(\"Division by zero\".into()) }\n    else { Ok(a / b) }\n}\n\nfn main() {\n    match divide(10.0, 2.0) {\n        Ok(v)  => println!(\"Result: {}\", v),\n        Err(e) => eprintln!(\"Error: {}\", e),\n    }\n    let v = divide(10.0, 0.0).unwrap_or(0.0);\n    let v2 = divide(10.0, 2.0)?;  // propagate\n}",
         "// Enums and pattern matching\n#[derive(Debug)]\nenum Shape {\n    Circle { radius: f64 },\n    Rectangle { width: f64, height: f64 },\n    Triangle(f64, f64, f64),\n}\n\nimpl Shape {\n    fn area(&self) -> f64 {\n        match self {\n            Shape::Circle { radius } => std::f64::consts::PI * radius * radius,\n            Shape::Rectangle { width, height } => width * height,\n            Shape::Triangle(a, b, c) => {\n                let s = (a+b+c)/2.0;\n                (s*(s-a)*(s-b)*(s-c)).sqrt()\n            }\n        }\n    }\n}",
         "// Traits\ntrait Animal {\n    fn name(&self) -> &str;\n    fn sound(&self) -> &str;\n    fn speak(&self) -> String {\n        format!(\"{} says {}\", self.name(), self.sound())\n    }\n}\n\nstruct Dog { name: String }\nimpl Animal for Dog {\n    fn name(&self) -> &str { &self.name }\n    fn sound(&self) -> &str { \"Woof\" }\n}\n\nfn make_noise(a: &dyn Animal) { println!(\"{}\", a.speak()); }",
         "// Closures and iterators\nfn main() {\n    let nums = vec![1,2,3,4,5,6,7,8,9,10];\n    let result: Vec<i32> = nums.iter()\n        .filter(|&&x| x % 2 == 0)\n        .map(|&x| x * x)\n        .collect();\n    let sum: i32 = result.iter().sum();\n    println!(\"{:?} sum={}\", result, sum);\n}",
     ]},
]

# ---------------------------------------------------------------------------
# C / C++
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "c", "topic": "basics", "keywords": ["c", "pointer", "memory", "malloc", "struct"],
     "snippets": [
         "#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n\ntypedef struct {\n    int id;\n    char name[64];\n    float score;\n} Student;\n\nStudent* create_student(int id, const char* name, float score) {\n    Student* s = malloc(sizeof(Student));\n    if (!s) return NULL;\n    s->id = id;\n    strncpy(s->name, name, sizeof(s->name)-1);\n    s->score = score;\n    return s;\n}\nvoid free_student(Student* s) { free(s); }",
         "// Pointers and arrays\nint arr[] = {5, 3, 1, 4, 2};\nint n = sizeof(arr) / sizeof(arr[0]);\n\n// Pointer arithmetic\nint* p = arr;\nfor (int i = 0; i < n; i++) {\n    printf(\"%d \", *(p + i));\n}\n\n// Double pointer\nvoid swap(int* a, int* b) {\n    int tmp = *a;\n    *a = *b;\n    *b = tmp;\n}",
     ]},
    {"lang": "cpp", "topic": "basics", "keywords": ["c++", "class", "template", "stl", "vector"],
     "snippets": [
         "#include <vector>\n#include <algorithm>\n#include <string>\n#include <memory>\n\n// Smart pointers\nstd::unique_ptr<int> p = std::make_unique<int>(42);\nstd::shared_ptr<std::string> sp = std::make_shared<std::string>(\"hello\");\n\n// STL containers\nstd::vector<int> v = {3, 1, 4, 1, 5, 9};\nstd::sort(v.begin(), v.end());\nv.erase(std::unique(v.begin(), v.end()), v.end());",
         "#include <iostream>\n#include <stdexcept>\n\ntemplate<typename T>\nclass Stack {\n    std::vector<T> data;\npublic:\n    void push(const T& v) { data.push_back(v); }\n    T pop() {\n        if (data.empty()) throw std::underflow_error(\"Stack empty\");\n        T v = data.back();\n        data.pop_back();\n        return v;\n    }\n    T& top() { return data.back(); }\n    bool empty() const { return data.empty(); }\n    size_t size() const { return data.size(); }\n};",
         "// Lambda and STL algorithms\n#include <algorithm>\n#include <vector>\n\nstd::vector<int> nums = {5, 2, 8, 1, 9, 3};\nstd::sort(nums.begin(), nums.end());\nstd::for_each(nums.begin(), nums.end(), [](int n){ std::cout << n << ' '; });\nauto it = std::find_if(nums.begin(), nums.end(), [](int n){ return n > 5; });\nint sum = std::accumulate(nums.begin(), nums.end(), 0);",
     ]},
]

# ---------------------------------------------------------------------------
# JAVA
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "java", "topic": "basics", "keywords": ["java", "class", "interface", "stream", "spring"],
     "snippets": [
         "// Java class\npublic class User {\n    private final Long id;\n    private String name;\n    private String email;\n\n    public User(Long id, String name, String email) {\n        this.id = id;\n        this.name = name;\n        this.email = email;\n    }\n    public Long getId()       { return id; }\n    public String getName()   { return name; }\n    public void setName(String name) { this.name = name; }\n    @Override public String toString() {\n        return String.format(\"User{id=%d, name='%s'}\", id, name);\n    }\n}",
         "// Java Streams\nimport java.util.*;\nimport java.util.stream.*;\n\nList<User> users = getUsers();\n\nList<String> names = users.stream()\n    .filter(u -> u.isActive())\n    .sorted(Comparator.comparing(User::getName))\n    .map(User::getName)\n    .collect(Collectors.toList());\n\nMap<String, Long> countByDept = users.stream()\n    .collect(Collectors.groupingBy(User::getDept, Collectors.counting()));",
         "// Spring Boot REST controller\n@RestController\n@RequestMapping(\"/api/users\")\n@RequiredArgsConstructor\npublic class UserController {\n    private final UserService userService;\n\n    @GetMapping\n    public ResponseEntity<List<UserDTO>> getAll() {\n        return ResponseEntity.ok(userService.findAll());\n    }\n\n    @PostMapping\n    public ResponseEntity<UserDTO> create(@Valid @RequestBody CreateUserRequest req) {\n        return ResponseEntity.status(201).body(userService.create(req));\n    }\n}",
     ]},
]

# ---------------------------------------------------------------------------
# REACT
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "javascript", "topic": "react", "keywords": ["react", "component", "hook", "useState", "useEffect"],
     "snippets": [
         "// React functional component with hooks\nimport React, { useState, useEffect, useCallback } from 'react';\n\nfunction UserList() {\n  const [users, setUsers] = useState([]);\n  const [loading, setLoading] = useState(true);\n  const [error, setError] = useState(null);\n\n  useEffect(() => {\n    fetch('/api/users')\n      .then(r => r.json())\n      .then(setUsers)\n      .catch(setError)\n      .finally(() => setLoading(false));\n  }, []);\n\n  if (loading) return <p>Loading...</p>;\n  if (error)   return <p>Error: {error.message}</p>;\n  return (\n    <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>\n  );\n}",
         "// Custom hooks\nimport { useState, useEffect } from 'react';\n\nfunction useFetch(url) {\n  const [data,    setData]    = useState(null);\n  const [loading, setLoading] = useState(true);\n  const [error,   setError]   = useState(null);\n\n  useEffect(() => {\n    const controller = new AbortController();\n    fetch(url, { signal: controller.signal })\n      .then(r => r.ok ? r.json() : Promise.reject(r))\n      .then(setData).catch(setError)\n      .finally(() => setLoading(false));\n    return () => controller.abort();\n  }, [url]);\n\n  return { data, loading, error };\n}",
         "// useReducer for complex state\nimport { useReducer } from 'react';\n\nconst reducer = (state, action) => {\n  switch (action.type) {\n    case 'ADD':    return { ...state, items: [...state.items, action.item] };\n    case 'REMOVE': return { ...state, items: state.items.filter(i => i.id !== action.id) };\n    case 'CLEAR':  return { ...state, items: [] };\n    default: return state;\n  }\n};\n\nfunction Cart() {\n  const [state, dispatch] = useReducer(reducer, { items: [] });\n  const add = item => dispatch({ type: 'ADD', item });\n}",
         "// Context API\nimport React, { createContext, useContext, useState } from 'react';\n\nconst AuthContext = createContext(null);\n\nexport function AuthProvider({ children }) {\n  const [user, setUser] = useState(null);\n  const login  = async (creds) => { const u = await authAPI.login(creds); setUser(u); };\n  const logout = () => { authAPI.logout(); setUser(null); };\n  return (\n    <AuthContext.Provider value={{ user, login, logout }}>\n      {children}\n    </AuthContext.Provider>\n  );\n}\n\nexport const useAuth = () => useContext(AuthContext);",
     ]},
]

# ---------------------------------------------------------------------------
# FASTAPI
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "python", "topic": "fastapi", "keywords": ["fastapi", "api", "endpoint", "pydantic", "python"],
     "snippets": [
         "from fastapi import FastAPI, HTTPException, Depends\nfrom pydantic import BaseModel, EmailStr\nfrom typing import Optional\n\napp = FastAPI(title='My API', version='1.0.0')\n\nclass UserCreate(BaseModel):\n    name: str\n    email: EmailStr\n    age: Optional[int] = None\n\nclass UserResponse(BaseModel):\n    id: int\n    name: str\n    email: str\n\n@app.post('/api/users', response_model=UserResponse, status_code=201)\nasync def create_user(user: UserCreate):\n    result = await db.create_user(user.dict())\n    return result",
         "from fastapi import Depends, HTTPException, status\nfrom fastapi.security import HTTPBearer, HTTPAuthorizationCredentials\nimport jwt\n\nsecurity = HTTPBearer()\n\nasync def get_current_user(\n    credentials: HTTPAuthorizationCredentials = Depends(security)\n):\n    try:\n        payload = jwt.decode(credentials.credentials, SECRET, algorithms=['HS256'])\n        user = await db.get_user(payload['sub'])\n        if not user: raise HTTPException(401, 'User not found')\n        return user\n    except jwt.ExpiredSignatureError:\n        raise HTTPException(401, 'Token expired')",
         "from fastapi import FastAPI, Query, Path\nfrom fastapi.middleware.cors import CORSMiddleware\n\napp = FastAPI()\napp.add_middleware(CORSMiddleware,\n    allow_origins=['*'],\n    allow_methods=['*'],\n    allow_headers=['*']\n)\n\n@app.get('/api/items')\nasync def list_items(\n    page: int = Query(1, ge=1),\n    limit: int = Query(20, le=100),\n    search: str = Query(''),\n):\n    return await db.list_items(page, limit, search)\n\n@app.get('/api/items/{item_id}')\nasync def get_item(item_id: int = Path(..., ge=1)):\n    item = await db.get_item(item_id)\n    if not item: raise HTTPException(404, 'Not found')\n    return item",
     ]},
]

# ---------------------------------------------------------------------------
# DOCKER
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "docker", "topic": "dockerfile", "keywords": ["docker", "dockerfile", "image", "container", "build"],
     "snippets": [
         "# Python app Dockerfile\nFROM python:3.12-slim\n\nWORKDIR /app\n\n# Install deps first (cache layer)\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\n# Copy source\nCOPY . .\n\n# Non-root user\nRUN adduser --disabled-password --gecos '' appuser\nUSER appuser\n\nEXPOSE 8000\nHEALTHCHECK --interval=30s --timeout=10s \\\n  CMD python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/health')\"\n\nCMD [\"uvicorn\", \"api.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]",
         "# Node.js multi-stage build\nFROM node:20-alpine AS builder\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci --only=production\nCOPY . .\nRUN npm run build\n\nFROM node:20-alpine AS runtime\nWORKDIR /app\nCOPY --from=builder /app/dist ./dist\nCOPY --from=builder /app/node_modules ./node_modules\nEXPOSE 3000\nCMD [\"node\", \"dist/main.js\"]",
         "# docker-compose.yml\nservices:\n  api:\n    build: .\n    ports:\n      - '8000:8000'\n    environment:\n      DATABASE_URL: postgresql://user:pass@db:5432/mydb\n      REDIS_URL: redis://cache:6379\n    depends_on:\n      db:    { condition: service_healthy }\n      cache: { condition: service_started }\n    restart: unless-stopped\n  db:\n    image: postgres:16-alpine\n    environment:\n      POSTGRES_USER: user\n      POSTGRES_PASSWORD: pass\n      POSTGRES_DB: mydb\n    volumes:\n      - pgdata:/var/lib/postgresql/data\n    healthcheck:\n      test: ['CMD', 'pg_isready', '-U', 'user']\n      interval: 10s\n  cache:\n    image: redis:7-alpine\nvolumes:\n  pgdata:",
     ]},
]

# ---------------------------------------------------------------------------
# ALGORITHMS
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "python", "topic": "algorithms", "keywords": ["algorithm", "sort", "search", "complexity", "python"],
     "snippets": [
         "# Binary search O(log n)\ndef binary_search(arr: list, target) -> int:\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
         "# Quicksort O(n log n) average\ndef quicksort(arr: list) -> list:\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left   = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right  = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
         "# Merge sort O(n log n)\ndef mergesort(arr: list) -> list:\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left  = mergesort(arr[:mid])\n    right = mergesort(arr[mid:])\n    result, i, j = [], 0, 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i]); i += 1\n        else:\n            result.append(right[j]); j += 1\n    return result + left[i:] + right[j:]",
         "# BFS graph traversal\nfrom collections import deque\n\ndef bfs(graph: dict, start) -> list:\n    visited = set()\n    queue = deque([start])\n    order = []\n    while queue:\n        node = queue.popleft()\n        if node in visited:\n            continue\n        visited.add(node)\n        order.append(node)\n        queue.extend(graph.get(node, []))\n    return order",
         "# DFS graph traversal\ndef dfs(graph: dict, start, visited=None) -> list:\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    result = [start]\n    for neighbor in graph.get(start, []):\n        if neighbor not in visited:\n            result.extend(dfs(graph, neighbor, visited))\n    return result",
         "# Dynamic programming: longest common subsequence\ndef lcs(s1: str, s2: str) -> int:\n    m, n = len(s1), len(s2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if s1[i-1] == s2[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]",
         "# Two pointers: two sum in sorted array\ndef two_sum_sorted(nums: list, target: int) -> tuple:\n    left, right = 0, len(nums) - 1\n    while left < right:\n        s = nums[left] + nums[right]\n        if s == target:   return (left, right)\n        elif s < target:  left += 1\n        else:             right -= 1\n    return (-1, -1)\n\n# Sliding window: max sum subarray of size k\ndef max_subarray_sum(nums, k):\n    window = sum(nums[:k])\n    best = window\n    for i in range(k, len(nums)):\n        window += nums[i] - nums[i-k]\n        best = max(best, window)\n    return best",
         "# Dijkstra's shortest path\nimport heapq\n\ndef dijkstra(graph: dict, start) -> dict:\n    dist = {start: 0}\n    pq = [(0, start)]\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist.get(u, float('inf')):\n            continue\n        for v, w in graph.get(u, []):\n            nd = d + w\n            if nd < dist.get(v, float('inf')):\n                dist[v] = nd\n                heapq.heappush(pq, (nd, v))\n    return dist",
     ]},
]

# ---------------------------------------------------------------------------
# DESIGN PATTERNS
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "python", "topic": "design_patterns", "keywords": ["design pattern", "singleton", "factory", "observer", "python"],
     "snippets": [
         "# Singleton\nclass Singleton:\n    _instance = None\n\n    def __new__(cls, *args, **kwargs):\n        if not cls._instance:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n\n# Thread-safe singleton\nimport threading\n\nclass SafeSingleton:\n    _instance = None\n    _lock = threading.Lock()\n\n    def __new__(cls):\n        with cls._lock:\n            if not cls._instance:\n                cls._instance = super().__new__(cls)\n        return cls._instance",
         "# Factory pattern\nfrom abc import ABC, abstractmethod\n\nclass Notification(ABC):\n    @abstractmethod\n    def send(self, message: str) -> None: ...\n\nclass EmailNotification(Notification):\n    def send(self, message): print(f'Email: {message}')\n\nclass SMSNotification(Notification):\n    def send(self, message): print(f'SMS: {message}')\n\ndef create_notification(type_: str) -> Notification:\n    return {'email': EmailNotification, 'sms': SMSNotification}[type_]()",
         "# Observer pattern\nclass EventEmitter:\n    def __init__(self):\n        self._listeners: dict = {}\n\n    def on(self, event: str, callback):\n        self._listeners.setdefault(event, []).append(callback)\n\n    def emit(self, event: str, *args, **kwargs):\n        for cb in self._listeners.get(event, []):\n            cb(*args, **kwargs)\n\nemitter = EventEmitter()\nemitter.on('data', lambda x: print(f'Got: {x}'))\nemitter.emit('data', 42)",
         "# Repository pattern\nfrom typing import Optional, List\n\nclass UserRepository:\n    def __init__(self, db):\n        self._db = db\n\n    async def find_by_id(self, id: int) -> Optional[dict]:\n        return await self._db.fetchone('SELECT * FROM users WHERE id=$1', id)\n\n    async def find_all(self, limit=20, offset=0) -> List[dict]:\n        return await self._db.fetch('SELECT * FROM users LIMIT $1 OFFSET $2', limit, offset)\n\n    async def create(self, data: dict) -> dict:\n        return await self._db.fetchone(\n            'INSERT INTO users(name,email) VALUES($1,$2) RETURNING *',\n            data['name'], data['email'])",
     ]},
]

# ---------------------------------------------------------------------------
# MACHINE CODE / ASSEMBLY
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "assembly", "topic": "x86", "keywords": ["assembly", "x86", "register", "instruction", "machine code"],
     "snippets": [
         "; x86-64 Linux: print 'Hello, World!'\nsection .data\n    msg db 'Hello, World!', 10\n    len equ $ - msg\n\nsection .text\n    global _start\n_start:\n    mov rax, 1       ; sys_write\n    mov rdi, 1       ; stdout\n    mov rsi, msg     ; buffer\n    mov rdx, len     ; length\n    syscall\n    mov rax, 60      ; sys_exit\n    xor rdi, rdi     ; exit code 0\n    syscall",
         "; x86-64 registers\n; 64-bit: rax, rbx, rcx, rdx, rsi, rdi, rbp, rsp, r8-r15\n; 32-bit: eax, ebx, ecx, edx, esi, edi, ebp, esp\n; 16-bit: ax,  bx,  cx,  dx\n; 8-bit:  al/ah, bl/bh, cl/ch, dl/dh\n;\n; Calling convention (System V AMD64 ABI):\n;   args:    rdi, rsi, rdx, rcx, r8, r9  (then stack)\n;   return:  rax (rdx for 128-bit)\n;   caller-saved: rax,rcx,rdx,rsi,rdi,r8-r11\n;   callee-saved: rbx,rbp,r12-r15",
         "; Common x86-64 instructions\nmov  rax, 42      ; load immediate\nmov  rbx, [rax]   ; load from memory\nmov  [rbx], rax   ; store to memory\nadd  rax, rbx     ; rax = rax + rbx\nsub  rax, 1       ; rax--\nimul rax, rbx     ; rax = rax * rbx\ndiv  rcx          ; rdx:rax / rcx\ncmp  rax, rbx     ; set flags\njmp  label        ; unconditional jump\nje   label        ; jump if equal\njg   label        ; jump if greater\ncall function     ; push rip, jmp\nret               ; pop rip, jmp",
         "; Simple function: sum of array\n; rdi = pointer to array, rsi = length\n; returns rax = sum\nsum_array:\n    xor  rax, rax   ; sum = 0\n    test rsi, rsi   ; if length == 0\n    jz   .done\n.loop:\n    add  rax, [rdi] ; sum += *ptr\n    add  rdi, 8     ; ptr++\n    dec  rsi        ; length--\n    jnz  .loop      ; while length > 0\n.done:\n    ret",
     ]},
]

# ---------------------------------------------------------------------------
# GIT
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "bash", "topic": "git", "keywords": ["git", "commit", "branch", "merge", "rebase"],
     "snippets": [
         "# Git workflow\ngit init && git add -A && git commit -m 'Initial commit'\ngit checkout -b feature/my-feature\ngit add src/new-file.py && git commit -m 'feat: add new feature'\ngit push origin feature/my-feature\n\n# Useful aliases\ngit log --oneline --graph --all\ngit diff HEAD~1          # changes since last commit\ngit stash push -m 'wip'  # save work in progress\ngit stash pop",
         "# Rebase and squash\ngit rebase -i HEAD~3     # interactive rebase last 3 commits\n# In editor: pick, squash (s), fixup (f), reword (r)\n\ngit pull --rebase origin main   # rebase instead of merge\n\n# Undo last commit (keep changes)\ngit reset --soft HEAD~1\n# Discard last commit completely\ngit reset --hard HEAD~1\n# Undo a specific commit\ngit revert abc1234",
     ]},
]

# ---------------------------------------------------------------------------
# KOTLIN
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "kotlin", "topic": "basics", "keywords": ["kotlin", "data class", "coroutine", "extension", "android"],
     "snippets": [
         "// Data class\ndata class User(\n    val id: Long,\n    val name: String,\n    val email: String,\n    val active: Boolean = true\n)\n\n// Extension function\nfun String.toSlug() = lowercase().replace(Regex(\"[^a-z0-9]+\"), \"-\")\n\n// Scope functions\nval user = User(1, \"Alice\", \"alice@example.com\").also { println(it) }\nval name = user.let { it.name.uppercase() }",
         "// Coroutines\nimport kotlinx.coroutines.*\n\nsuspend fun fetchUser(id: Long): User {\n    delay(100)  // non-blocking\n    return User(id, \"Alice\", \"alice@example.com\")\n}\n\nfun main() = runBlocking {\n    val users = (1L..10L).map { id ->\n        async { fetchUser(id) }  // parallel\n    }.awaitAll()\n    println(users)\n}",
     ]},
]

# ---------------------------------------------------------------------------
# PHP
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "php", "topic": "basics", "keywords": ["php", "class", "composer", "laravel", "pdo"],
     "snippets": [
         "<?php\n// PHP 8.1+ class\nclass User {\n    public function __construct(\n        private readonly int    $id,\n        private string  $name,\n        private string  $email,\n    ) {}\n\n    public function getId(): int    { return $this->id; }\n    public function getName(): string { return $this->name; }\n\n    public static function create(string $name, string $email): self {\n        return new self(0, $name, $email);\n    }\n}",
         "<?php\n// PDO database\n$pdo = new PDO('mysql:host=localhost;dbname=app', 'user', 'pass', [\n    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,\n    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,\n]);\n\n$stmt = $pdo->prepare('SELECT * FROM users WHERE email = ?');\n$stmt->execute([$email]);\n$user = $stmt->fetch();\n\n$pdo->beginTransaction();\ntry {\n    $pdo->exec(\"UPDATE accounts SET balance = balance - 100 WHERE id = 1\");\n    $pdo->exec(\"UPDATE accounts SET balance = balance + 100 WHERE id = 2\");\n    $pdo->commit();\n} catch (\\Exception $e) {\n    $pdo->rollBack();\n    throw $e;\n}",
     ]},
]

# ---------------------------------------------------------------------------
# SWIFT
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "swift", "topic": "basics", "keywords": ["swift", "struct", "protocol", "optionals", "ios"],
     "snippets": [
         "// Swift struct and protocol\nprotocol Drawable {\n    func draw() -> String\n}\n\nstruct Circle: Drawable {\n    let radius: Double\n    func area() -> Double { .pi * radius * radius }\n    func draw() -> String { \"Circle(r=\\(radius))\" }\n}\n\n// Optionals\nfunc findUser(_ id: Int) -> User? {\n    return users.first { $0.id == id }\n}\n\nif let user = findUser(42) {\n    print(user.name)\n} else {\n    print(\"Not found\")\n}",
     ]},
]

# ---------------------------------------------------------------------------
# EXTRA: web APIs, security, database patterns
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "javascript", "topic": "websocket", "keywords": ["websocket", "ws", "realtime", "socket", "javascript"],
     "snippets": [
         "// WebSocket client\nconst ws = new WebSocket('wss://example.com/ws');\n\nws.onopen    = ()    => ws.send(JSON.stringify({ type: 'subscribe', channel: 'updates' }));\nws.onmessage = (evt) => { const msg = JSON.parse(evt.data); handleMessage(msg); };\nws.onerror   = (err) => console.error('WS error', err);\nws.onclose   = ()    => setTimeout(reconnect, 3000);\n\nfunction send(type, data) {\n  if (ws.readyState === WebSocket.OPEN)\n    ws.send(JSON.stringify({ type, data }));\n}",
         "// WebSocket server (Node.js)\nconst { WebSocketServer } = require('ws');\nconst wss = new WebSocketServer({ port: 8080 });\n\nconst clients = new Set();\n\nwss.on('connection', (ws, req) => {\n  clients.add(ws);\n  ws.on('message', (raw) => {\n    const msg = JSON.parse(raw);\n    clients.forEach(c => {\n      if (c !== ws && c.readyState === c.OPEN)\n        c.send(JSON.stringify(msg));\n    });\n  });\n  ws.on('close', () => clients.delete(ws));\n});",
     ]},
    {"lang": "python", "topic": "security", "keywords": ["security", "hash", "jwt", "password", "bcrypt", "python"],
     "snippets": [
         "import bcrypt\nimport jwt\nimport secrets\nfrom datetime import datetime, timedelta\n\n# Password hashing\ndef hash_password(plain: str) -> str:\n    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()\n\ndef verify_password(plain: str, hashed: str) -> bool:\n    return bcrypt.checkpw(plain.encode(), hashed.encode())\n\n# JWT\nSECRET = secrets.token_hex(32)\n\ndef create_token(user_id: int, expires_minutes=60) -> str:\n    return jwt.encode({\n        'sub': user_id,\n        'exp': datetime.utcnow() + timedelta(minutes=expires_minutes),\n        'iat': datetime.utcnow(),\n    }, SECRET, algorithm='HS256')\n\ndef verify_token(token: str) -> dict:\n    return jwt.decode(token, SECRET, algorithms=['HS256'])",
     ]},
    {"lang": "sql", "topic": "postgresql", "keywords": ["postgresql", "index", "jsonb", "full text search", "sql"],
     "snippets": [
         "-- PostgreSQL JSONB\nCREATE TABLE events (\n  id      BIGSERIAL PRIMARY KEY,\n  type    VARCHAR(50) NOT NULL,\n  payload JSONB NOT NULL,\n  created_at TIMESTAMPTZ DEFAULT NOW()\n);\nCREATE INDEX idx_events_payload ON events USING GIN(payload);\n\n-- Query JSON\nSELECT id, payload->>'name' AS name\nFROM events\nWHERE payload @> '{\"type\": \"user_signup\"}'\n  AND payload->>'email' LIKE '%@example.com';",
         "-- Full text search\nALTER TABLE articles ADD COLUMN search_vector tsvector;\nUPDATE articles\n  SET search_vector = to_tsvector('russian', title || ' ' || body);\nCREATE INDEX idx_articles_fts ON articles USING GIN(search_vector);\n\nSELECT id, title, ts_rank(search_vector, query) AS rank\nFROM articles, to_tsquery('russian', 'python & программирование') query\nWHERE search_vector @@ query\nORDER BY rank DESC;",
     ]},
    {"lang": "python", "topic": "sqlalchemy", "keywords": ["sqlalchemy", "orm", "model", "query", "python"],
     "snippets": [
         "from sqlalchemy import Column, Integer, String, Boolean, DateTime, func\nfrom sqlalchemy.orm import declarative_base, relationship\nfrom sqlalchemy.ext.asyncio import AsyncSession, create_async_engine\n\nBase = declarative_base()\n\nclass User(Base):\n    __tablename__ = 'users'\n    id         = Column(Integer, primary_key=True)\n    name       = Column(String(100), nullable=False)\n    email      = Column(String(255), unique=True, nullable=False)\n    active     = Column(Boolean, default=True)\n    created_at = Column(DateTime(timezone=True), server_default=func.now())\n    orders     = relationship('Order', back_populates='user', lazy='select')",
     ]},
    {"lang": "python", "topic": "redis", "keywords": ["redis", "cache", "pubsub", "queue", "python"],
     "snippets": [
         "import redis.asyncio as redis\nimport json\n\nr = redis.Redis.from_url('redis://localhost:6379', decode_responses=True)\n\n# Cache decorator\ndef cache(ttl=300):\n    def decorator(fn):\n        async def wrapper(*args, **kwargs):\n            key = f'{fn.__name__}:{args}:{kwargs}'\n            cached = await r.get(key)\n            if cached: return json.loads(cached)\n            result = await fn(*args, **kwargs)\n            await r.setex(key, ttl, json.dumps(result))\n            return result\n        return wrapper\n    return decorator\n\n# Pub/Sub\nasync def publish(channel: str, data: dict):\n    await r.publish(channel, json.dumps(data))\n\nasync def subscribe(channel: str):\n    pubsub = r.pubsub()\n    await pubsub.subscribe(channel)\n    async for msg in pubsub.listen():\n        if msg['type'] == 'message':\n            yield json.loads(msg['data'])",
     ]},
    {"lang": "python", "topic": "celery", "keywords": ["celery", "task", "queue", "worker", "python"],
     "snippets": [
         "from celery import Celery\nfrom celery.schedules import crontab\n\napp = Celery('tasks', broker='redis://localhost:6379/0',\n             backend='redis://localhost:6379/1')\n\n@app.task(bind=True, max_retries=3, default_retry_delay=60)\ndef send_email(self, user_id: int, template: str):\n    try:\n        user = User.objects.get(id=user_id)\n        email_service.send(user.email, template)\n    except Exception as exc:\n        raise self.retry(exc=exc)\n\n# Periodic tasks\napp.conf.beat_schedule = {\n    'cleanup-daily': {\n        'task': 'tasks.cleanup',\n        'schedule': crontab(hour=2, minute=0),\n    },\n}",
     ]},
    {"lang": "javascript", "topic": "graphql", "keywords": ["graphql", "query", "mutation", "resolver", "schema"],
     "snippets": [
         "// GraphQL schema (Apollo Server)\nconst typeDefs = `\n  type User {\n    id: ID!\n    name: String!\n    email: String!\n    posts: [Post!]!\n  }\n  type Post {\n    id: ID!\n    title: String!\n    body: String!\n    author: User!\n  }\n  type Query {\n    user(id: ID!): User\n    users(limit: Int = 20): [User!]!\n  }\n  type Mutation {\n    createUser(name: String!, email: String!): User!\n    updateUser(id: ID!, name: String): User!\n  }\n`;\n\nconst resolvers = {\n  Query: {\n    user: (_, { id }, ctx) => ctx.db.users.findById(id),\n    users: (_, { limit }, ctx) => ctx.db.users.findAll(limit),\n  },\n  Mutation: {\n    createUser: (_, args, ctx) => ctx.db.users.create(args),\n  },\n};",
     ]},
    {"lang": "python", "topic": "data_structures", "keywords": ["linked list", "tree", "heap", "graph", "python"],
     "snippets": [
         "# Linked List\nfrom dataclasses import dataclass\nfrom typing import Optional\n\n@dataclass\nclass Node:\n    value: int\n    next: Optional['Node'] = None\n\nclass LinkedList:\n    def __init__(self): self.head = None\n\n    def prepend(self, value):\n        self.head = Node(value, self.head)\n\n    def append(self, value):\n        if not self.head:\n            self.head = Node(value); return\n        cur = self.head\n        while cur.next: cur = cur.next\n        cur.next = Node(value)\n\n    def __iter__(self):\n        cur = self.head\n        while cur:\n            yield cur.value\n            cur = cur.next",
         "# Binary Search Tree\nclass BST:\n    class Node:\n        def __init__(self, v):\n            self.v, self.left, self.right = v, None, None\n\n    def __init__(self): self.root = None\n\n    def insert(self, v):\n        def _ins(node):\n            if not node: return BST.Node(v)\n            if v < node.v:   node.left  = _ins(node.left)\n            elif v > node.v: node.right = _ins(node.right)\n            return node\n        self.root = _ins(self.root)\n\n    def contains(self, v):\n        node = self.root\n        while node:\n            if v == node.v:   return True\n            elif v < node.v:  node = node.left\n            else:             node = node.right\n        return False",
         "# Min-heap (priority queue)\nimport heapq\n\nheap = []\nheapq.heappush(heap, (1, 'task1'))\nheapq.heappush(heap, (3, 'task3'))\nheapq.heappush(heap, (2, 'task2'))\npriority, task = heapq.heappop(heap)  # always pops smallest\n\n# Heapify existing list\ndata = [5, 3, 8, 1, 9]\nheapq.heapify(data)\nprint(heapq.nsmallest(3, data))\nprint(heapq.nlargest(3, data))",
     ]},
    {"lang": "javascript", "topic": "nodejs", "keywords": ["nodejs", "express", "http", "middleware", "javascript"],
     "snippets": [
         "// Express.js REST API\nconst express = require('express');\nconst app = express();\n\napp.use(express.json());\napp.use(require('cors')());\n\napp.get('/api/users', async (req, res) => {\n  const { page = 1, limit = 20 } = req.query;\n  const users = await db.users.findAll({ page, limit });\n  res.json(users);\n});\n\napp.post('/api/users', async (req, res) => {\n  const user = await db.users.create(req.body);\n  res.status(201).json(user);\n});\n\napp.use((err, req, res, next) => {\n  console.error(err);\n  res.status(err.status || 500).json({ error: err.message });\n});\n\napp.listen(3000);",
         "// NestJS controller\nimport { Controller, Get, Post, Body, Param, UseGuards } from '@nestjs/common';\nimport { AuthGuard } from '@nestjs/passport';\n\n@Controller('api/users')\n@UseGuards(AuthGuard('jwt'))\nexport class UsersController {\n  constructor(private readonly usersService: UsersService) {}\n\n  @Get()\n  findAll() { return this.usersService.findAll(); }\n\n  @Get(':id')\n  findOne(@Param('id') id: string) {\n    return this.usersService.findOne(+id);\n  }\n\n  @Post()\n  create(@Body() dto: CreateUserDto) {\n    return this.usersService.create(dto);\n  }\n}",
     ]},
    {"lang": "python", "topic": "machine_learning", "keywords": ["sklearn", "model", "train", "neural network", "python"],
     "snippets": [
         "from sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.metrics import accuracy_score, classification_report\nfrom sklearn.ensemble import RandomForestClassifier\n\n# Train/test split\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42, stratify=y\n)\n\n# Scale features\nscaler = StandardScaler()\nX_train = scaler.fit_transform(X_train)\nX_test  = scaler.transform(X_test)\n\n# Train model\nmodel = RandomForestClassifier(n_estimators=100, random_state=42)\nmodel.fit(X_train, y_train)\npreds = model.predict(X_test)\nprint(classification_report(y_test, preds))",
         "import torch\nimport torch.nn as nn\n\nclass MLP(nn.Module):\n    def __init__(self, in_dim, hidden, out_dim):\n        super().__init__()\n        self.net = nn.Sequential(\n            nn.Linear(in_dim, hidden), nn.ReLU(), nn.Dropout(0.2),\n            nn.Linear(hidden, hidden), nn.ReLU(), nn.Dropout(0.2),\n            nn.Linear(hidden, out_dim)\n        )\n    def forward(self, x):\n        return self.net(x)\n\nmodel = MLP(784, 256, 10)\noptimizer = torch.optim.Adam(model.parameters(), lr=1e-3)\ncriterion = nn.CrossEntropyLoss()\n\nfor epoch in range(10):\n    for X_batch, y_batch in dataloader:\n        optimizer.zero_grad()\n        loss = criterion(model(X_batch), y_batch)\n        loss.backward()\n        optimizer.step()",
     ]},
]

# ---------------------------------------------------------------------------
# KUBERNETES
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "yaml", "topic": "kubernetes", "keywords": ["kubernetes", "pod", "deployment", "service", "k8s"],
     "snippets": [
         "# Kubernetes Deployment\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: api\n  labels: { app: api }\nspec:\n  replicas: 3\n  selector:\n    matchLabels: { app: api }\n  template:\n    metadata:\n      labels: { app: api }\n    spec:\n      containers:\n        - name: api\n          image: myregistry/api:1.2.3\n          ports: [{ containerPort: 8000 }]\n          env:\n            - name: DATABASE_URL\n              valueFrom:\n                secretKeyRef: { name: db-secret, key: url }\n          resources:\n            requests: { cpu: 100m, memory: 128Mi }\n            limits:   { cpu: 500m, memory: 512Mi }\n          livenessProbe:\n            httpGet: { path: /health, port: 8000 }\n            initialDelaySeconds: 10",
         "# Kubernetes Service + Ingress\napiVersion: v1\nkind: Service\nmetadata: { name: api }\nspec:\n  selector: { app: api }\n  ports: [{ port: 80, targetPort: 8000 }]\n---\napiVersion: networking.k8s.io/v1\nkind: Ingress\nmetadata:\n  name: api\n  annotations:\n    cert-manager.io/cluster-issuer: letsencrypt\nspec:\n  tls:\n    - hosts: [api.example.com]\n      secretName: api-tls\n  rules:\n    - host: api.example.com\n      http:\n        paths:\n          - path: /\n            pathType: Prefix\n            backend:\n              service: { name: api, port: { number: 80 } }",
     ]},
]

# ---------------------------------------------------------------------------
# ADDITIONAL PYTHON — web scraping, concurrency, patterns
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "python", "topic": "concurrency", "keywords": ["threading", "multiprocessing", "concurrent", "executor", "python"],
     "snippets": [
         "import concurrent.futures\n\n# ThreadPoolExecutor (I/O-bound)\ndef fetch(url):\n    import requests\n    return requests.get(url).text\n\nurls = ['https://example.com'] * 10\nwith concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:\n    results = list(ex.map(fetch, urls))\n\n# ProcessPoolExecutor (CPU-bound)\ndef heavy(n):\n    return sum(i**2 for i in range(n))\n\nwith concurrent.futures.ProcessPoolExecutor() as ex:\n    futures = [ex.submit(heavy, 10**6) for _ in range(4)]\n    results = [f.result() for f in futures]",
         "import threading\n\nclass SafeCounter:\n    def __init__(self):\n        self._value = 0\n        self._lock = threading.Lock()\n\n    def increment(self):\n        with self._lock:\n            self._value += 1\n\n    def get(self):\n        with self._lock:\n            return self._value\n\ncounter = SafeCounter()\nthreads = [threading.Thread(target=counter.increment) for _ in range(1000)]\nfor t in threads: t.start()\nfor t in threads: t.join()\nprint(counter.get())  # 1000",
     ]},
    {"lang": "python", "topic": "web_scraping", "keywords": ["scraping", "beautifulsoup", "selenium", "playwright", "python"],
     "snippets": [
         "import httpx\nfrom bs4 import BeautifulSoup\n\nasync def scrape_page(url: str) -> list[dict]:\n    async with httpx.AsyncClient() as client:\n        resp = await client.get(url, headers={'User-Agent': 'Bot/1.0'})\n        resp.raise_for_status()\n\n    soup = BeautifulSoup(resp.text, 'html.parser')\n    articles = []\n    for art in soup.select('article.post'):\n        articles.append({\n            'title': art.select_one('h2').get_text(strip=True),\n            'url':   art.select_one('a')['href'],\n            'date':  art.select_one('time')['datetime'],\n        })\n    return articles",
     ]},
    {"lang": "python", "topic": "cli", "keywords": ["argparse", "click", "typer", "cli", "python"],
     "snippets": [
         "import typer\nfrom pathlib import Path\n\napp = typer.Typer()\n\n@app.command()\ndef process(\n    input_file: Path = typer.Argument(..., exists=True),\n    output: Path = typer.Option('output.json'),\n    verbose: bool = typer.Option(False, '--verbose', '-v'),\n    count: int = typer.Option(10),\n):\n    \"\"\"Process input file and write results to output.\"\"\"\n    if verbose:\n        typer.echo(f'Processing {input_file}...')\n    data = input_file.read_text()\n    # ... process ...\n    typer.echo(typer.style('Done!', fg=typer.colors.GREEN))\n\nif __name__ == '__main__':\n    app()",
     ]},
]

# ---------------------------------------------------------------------------
# ADDITIONAL PYTHON
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "python", "topic": "subprocess", "keywords": ["subprocess", "shell", "process", "run", "python"],
     "snippets": [
         "import subprocess\n\n# Run command, capture output\nresult = subprocess.run(\n    ['git', 'log', '--oneline', '-10'],\n    capture_output=True, text=True, check=True\n)\nprint(result.stdout)\n\n# Shell pipeline\nresult = subprocess.run(\n    'ls -la | grep .py | wc -l',\n    shell=True, capture_output=True, text=True\n)\ncount = int(result.stdout.strip())",
         "import subprocess\n\n# Stream output in real time\nwith subprocess.Popen(\n    ['python', '-u', 'long_script.py'],\n    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True\n) as proc:\n    for line in proc.stdout:\n        print(line, end='')\n    proc.wait()\n    if proc.returncode != 0:\n        raise RuntimeError(f'Script failed: {proc.returncode}')",
     ]},
    {"lang": "python", "topic": "environment", "keywords": ["os", "environ", "dotenv", "config", "python"],
     "snippets": [
         "import os\nfrom pathlib import Path\n\n# Environment variables with defaults\nDB_URL   = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')\nDEBUG    = os.environ.get('DEBUG', 'false').lower() == 'true'\nPORT     = int(os.environ.get('PORT', '8000'))\nSECRET   = os.environ['SECRET_KEY']  # raises if missing\n\n# python-dotenv\nfrom dotenv import load_dotenv\nload_dotenv()  # loads .env file\nload_dotenv(Path('.env.local'), override=True)",
     ]},
    {"lang": "python", "topic": "pydantic", "keywords": ["pydantic", "validation", "schema", "model", "python"],
     "snippets": [
         "from pydantic import BaseModel, Field, EmailStr, validator\nfrom typing import Optional\nfrom datetime import datetime\n\nclass UserCreate(BaseModel):\n    name:  str = Field(..., min_length=2, max_length=100)\n    email: EmailStr\n    age:   Optional[int] = Field(None, ge=0, le=150)\n    tags:  list[str] = []\n\n    @validator('name')\n    def name_must_not_be_empty(cls, v):\n        if not v.strip(): raise ValueError('Name cannot be blank')\n        return v.strip()\n\nclass UserResponse(UserCreate):\n    id:         int\n    created_at: datetime\n\n    class Config:\n        from_attributes = True",
         "from pydantic import BaseSettings\n\nclass Settings(BaseSettings):\n    app_name:     str = 'My App'\n    debug:        bool = False\n    database_url: str\n    secret_key:   str\n    redis_url:    str = 'redis://localhost:6379'\n    allowed_hosts: list[str] = ['*']\n\n    class Config:\n        env_file = '.env'\n        env_file_encoding = 'utf-8'\n\nsettings = Settings()",
     ]},
    {"lang": "python", "topic": "httpx", "keywords": ["httpx", "async http", "client", "python"],
     "snippets": [
         "import httpx\nimport asyncio\n\nasync def fetch_all(urls: list[str]) -> list[dict]:\n    async with httpx.AsyncClient(timeout=10.0) as client:\n        tasks = [client.get(url) for url in urls]\n        responses = await asyncio.gather(*tasks)\n        return [r.json() for r in responses if r.status_code == 200]\n\n# Sync client\nwith httpx.Client(base_url='https://api.example.com') as client:\n    resp = client.post('/users', json={'name': 'Alice'})\n    resp.raise_for_status()\n    user = resp.json()",
     ]},
    {"lang": "python", "topic": "dataclasses", "keywords": ["dataclass", "field", "frozen", "python"],
     "snippets": [
         "from dataclasses import dataclass, field, asdict, astuple\nfrom typing import ClassVar\n\n@dataclass(frozen=True)  # immutable\nclass Point:\n    x: float\n    y: float\n    def distance_to(self, other: 'Point') -> float:\n        return ((self.x-other.x)**2 + (self.y-other.y)**2) ** 0.5\n\n@dataclass\nclass Config:\n    host: str = 'localhost'\n    port: int = 8000\n    tags: list[str] = field(default_factory=list)\n    MAX_RETRY: ClassVar[int] = 3\n\n    def __post_init__(self):\n        if self.port < 1 or self.port > 65535:\n            raise ValueError(f'Invalid port: {self.port}')",
     ]},
    {"lang": "python", "topic": "protocols", "keywords": ["protocol", "duck typing", "structural subtyping", "python"],
     "snippets": [
         "from typing import Protocol, runtime_checkable\n\n@runtime_checkable\nclass Serializable(Protocol):\n    def to_dict(self) -> dict: ...\n    @classmethod\n    def from_dict(cls, data: dict) -> 'Serializable': ...\n\nclass Drawable(Protocol):\n    def draw(self, canvas) -> None: ...\n    def bounding_box(self) -> tuple[float,float,float,float]: ...\n\ndef render_all(shapes: list[Drawable], canvas) -> None:\n    for shape in shapes:\n        shape.draw(canvas)",
     ]},
    {"lang": "python", "topic": "contextlib", "keywords": ["contextlib", "context manager", "suppress", "redirect", "python"],
     "snippets": [
         "from contextlib import contextmanager, asynccontextmanager, suppress\nfrom contextlib import redirect_stdout, ExitStack\nimport io\n\n@contextmanager\ndef managed_transaction(db):\n    tx = db.begin()\n    try:\n        yield tx\n        tx.commit()\n    except Exception:\n        tx.rollback()\n        raise\n\n# Capture stdout\nbuffer = io.StringIO()\nwith redirect_stdout(buffer):\n    print('captured')\noutput = buffer.getvalue()\n\n# Multiple context managers\nwith ExitStack() as stack:\n    files = [stack.enter_context(open(f)) for f in file_list]",
     ]},
    {"lang": "python", "topic": "abc_patterns", "keywords": ["abstract", "abc", "interface", "mixin", "python"],
     "snippets": [
         "from abc import ABC, abstractmethod\n\nclass Repository(ABC):\n    @abstractmethod\n    async def get(self, id: int): ...\n    @abstractmethod\n    async def list(self, **filters): ...\n    @abstractmethod\n    async def create(self, data: dict): ...\n    @abstractmethod\n    async def update(self, id: int, data: dict): ...\n    @abstractmethod\n    async def delete(self, id: int) -> bool: ...\n\nclass TimestampMixin:\n    \"\"\"Mixin to add created_at / updated_at fields.\"\"\"\n    from datetime import datetime\n    def touch(self):\n        self.updated_at = self.datetime.utcnow()\n    def set_created(self):\n        self.created_at = self.datetime.utcnow()\n        self.updated_at = self.created_at",
     ]},
    {"lang": "python", "topic": "enums", "keywords": ["enum", "flag", "auto", "python"],
     "snippets": [
         "from enum import Enum, IntEnum, Flag, auto\n\nclass Color(Enum):\n    RED   = 'red'\n    GREEN = 'green'\n    BLUE  = 'blue'\n    def hex(self) -> str:\n        return {'red': '#FF0000', 'green': '#00FF00', 'blue': '#0000FF'}[self.value]\n\nclass Permission(Flag):\n    READ    = auto()  # 1\n    WRITE   = auto()  # 2\n    EXECUTE = auto()  # 4\n    ADMIN   = READ | WRITE | EXECUTE\n\nperm = Permission.READ | Permission.WRITE\nif Permission.READ in perm: print('Can read')",
     ]},
    {"lang": "python", "topic": "slots", "keywords": ["__slots__", "memory", "performance", "python"],
     "snippets": [
         "class Point:\n    __slots__ = ('x', 'y', 'z')  # ~30% less memory than dict\n    def __init__(self, x, y, z):\n        self.x, self.y, self.z = x, y, z\n\n# Useful for millions of small objects\nclass Particle:\n    __slots__ = ('x', 'y', 'vx', 'vy', 'mass')\n    def __init__(self, x, y, vx=0, vy=0, mass=1.0):\n        self.x, self.y = x, y\n        self.vx, self.vy = vx, vy\n        self.mass = mass",
     ]},
    {"lang": "python", "topic": "descriptors", "keywords": ["descriptor", "__get__", "__set__", "property", "python"],
     "snippets": [
         "class Validator:\n    def __set_name__(self, owner, name):\n        self.name = name\n        self.private = f'_{name}'\n\n    def __get__(self, obj, type=None):\n        if obj is None: return self\n        return getattr(obj, self.private, None)\n\n    def __set__(self, obj, value):\n        self.validate(value)\n        setattr(obj, self.private, value)\n\n    def validate(self, value):\n        raise NotImplementedError\n\nclass PositiveInt(Validator):\n    def validate(self, v):\n        if not isinstance(v, int) or v <= 0:\n            raise ValueError(f'{self.name} must be a positive int')\n\nclass User:\n    age = PositiveInt()",
     ]},
    {"lang": "python", "topic": "namedtuple", "keywords": ["namedtuple", "NamedTuple", "tuple", "python"],
     "snippets": [
         "from typing import NamedTuple\n\nclass Point(NamedTuple):\n    x: float\n    y: float\n    z: float = 0.0\n\n    def distance(self) -> float:\n        return (self.x**2 + self.y**2 + self.z**2) ** 0.5\n\np = Point(3.0, 4.0)\nprint(p.x, p.y, p.distance())  # 3.0 4.0 5.0\nprint(p._asdict())  # OrderedDict\nq = p._replace(z=1.0)  # new instance with changed field",
     ]},
    {"lang": "python", "topic": "weakref", "keywords": ["weakref", "cache", "memory", "python"],
     "snippets": [
         "import weakref\n\nclass Cache:\n    def __init__(self):\n        self._cache = weakref.WeakValueDictionary()\n\n    def get(self, key):\n        return self._cache.get(key)\n\n    def set(self, key, value):\n        self._cache[key] = value  # won't prevent GC\n\n# Weak references\nobj = SomeHeavyObject()\nref = weakref.ref(obj)\nprint(ref())  # returns obj or None if GC'd",
     ]},
    {"lang": "python", "topic": "multiprocessing", "keywords": ["multiprocessing", "pool", "queue", "process", "python"],
     "snippets": [
         "from multiprocessing import Pool, Queue, Process\nimport os\n\ndef cpu_task(n):\n    return sum(i**2 for i in range(n))\n\n# Process pool for CPU-bound work\nwith Pool(processes=os.cpu_count()) as pool:\n    results = pool.map(cpu_task, [10**6]*8)\n    print(sum(results))\n\n# Shared queue between processes\ndef worker(q):\n    while True:\n        item = q.get()\n        if item is None: break\n        process(item)\n\nq = Queue()\nproc = Process(target=worker, args=(q,))\nproc.start()\nq.put(task)\nq.put(None)  # stop signal\nproc.join()",
     ]},
]

# ---------------------------------------------------------------------------
# MORE JAVASCRIPT / TYPESCRIPT
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "javascript", "topic": "prototype", "keywords": ["prototype", "inheritance", "object", "javascript"],
     "snippets": [
         "// Prototype chain\nfunction Animal(name) { this.name = name; }\nAnimal.prototype.speak = function() {\n  return `${this.name} makes a noise`;\n};\n\nfunction Dog(name) { Animal.call(this, name); }\nDog.prototype = Object.create(Animal.prototype);\nDog.prototype.constructor = Dog;\nDog.prototype.bark = function() { return `${this.name} barks`; };\n\n// Object.create\nconst animal = { eat() { return 'eating'; } };\nconst dog = Object.create(animal);\ndog.bark = () => 'woof';",
     ]},
    {"lang": "javascript", "topic": "generators", "keywords": ["generator", "yield", "iterator", "javascript"],
     "snippets": [
         "// Generator functions\nfunction* range(start, end, step = 1) {\n  for (let i = start; i < end; i += step) yield i;\n}\n\nfunction* fibonacci() {\n  let [a, b] = [0, 1];\n  while (true) { yield a; [a, b] = [b, a + b]; }\n}\n\nconst fib = fibonacci();\nconsole.log([...Array(10)].map(() => fib.next().value));\n\n// Infinite scroll\nasync function* loadPages(url) {\n  let page = 1;\n  while (true) {\n    const data = await fetch(`${url}?page=${page++}`).then(r => r.json());\n    if (!data.length) return;\n    yield data;\n  }\n}",
     ]},
    {"lang": "javascript", "topic": "proxy_reflect", "keywords": ["proxy", "reflect", "meta", "javascript"],
     "snippets": [
         "// Proxy for validation\nconst validator = {\n  set(obj, prop, value) {\n    if (prop === 'age') {\n      if (typeof value !== 'number' || value < 0)\n        throw new TypeError('Age must be non-negative number');\n    }\n    return Reflect.set(obj, prop, value);\n  }\n};\n\nconst user = new Proxy({}, validator);\nuser.age = 25;   // OK\nuser.age = -1;   // throws",
     ]},
    {"lang": "javascript", "topic": "storage", "keywords": ["localStorage", "sessionStorage", "indexedDB", "cookie", "javascript"],
     "snippets": [
         "// Web Storage\nconst save = (key, data) => localStorage.setItem(key, JSON.stringify(data));\nconst load = (key, fallback = null) => {\n  const item = localStorage.getItem(key);\n  return item ? JSON.parse(item) : fallback;\n};\nconst remove = key => localStorage.removeItem(key);\n\n// Cookies\nfunction setCookie(name, value, days = 7) {\n  const expires = new Date(Date.now() + days*864e5).toUTCString();\n  document.cookie = `${name}=${encodeURIComponent(value)};expires=${expires};path=/;SameSite=Lax`;\n}\nfunction getCookie(name) {\n  return document.cookie.split('; ').find(r => r.startsWith(name+'='))?.split('=')[1];\n}",
     ]},
    {"lang": "javascript", "topic": "service_worker", "keywords": ["service worker", "pwa", "cache", "offline", "javascript"],
     "snippets": [
         "// Service Worker — cache first strategy\nconst CACHE = 'v1';\nconst PRECACHE = ['/','app.js','style.css'];\n\nself.addEventListener('install', e => {\n  e.waitUntil(\n    caches.open(CACHE).then(c => c.addAll(PRECACHE))\n  );\n});\n\nself.addEventListener('fetch', e => {\n  e.respondWith(\n    caches.match(e.request).then(cached => {\n      return cached || fetch(e.request).then(resp => {\n        const clone = resp.clone();\n        caches.open(CACHE).then(c => c.put(e.request, clone));\n        return resp;\n      });\n    })\n  );\n});",
     ]},
    {"lang": "typescript", "topic": "advanced_types", "keywords": ["conditional type", "infer", "mapped type", "template literal", "typescript"],
     "snippets": [
         "// Conditional types\ntype IsArray<T> = T extends any[] ? true : false;\ntype Flatten<T> = T extends Array<infer U> ? U : T;\ntype Awaited<T> = T extends Promise<infer U> ? U : T;\n\n// Template literal types\ntype EventName = 'click' | 'focus' | 'blur';\ntype HandlerName = `on${Capitalize<EventName>}`;  // 'onClick' | 'onFocus' | 'onBlur'\n\n// Mapped types with modifiers\ntype Mutable<T> = { -readonly [K in keyof T]: T[K] };\ntype Deep<T> = { [K in keyof T]: T[K] extends object ? Deep<T[K]> : T[K] };",
         "// Extract function signatures\ntype Parameters<T extends (...args: any) => any> =\n  T extends (...args: infer P) => any ? P : never;\ntype ReturnType<T extends (...args: any) => any> =\n  T extends (...args: any) => infer R ? R : any;\n\n// Builder pattern with TypeScript\nclass QueryBuilder<T extends Record<string,any>> {\n  private filters: Partial<T> = {};\n  where<K extends keyof T>(key: K, value: T[K]): this {\n    this.filters[key] = value;\n    return this;\n  }\n  build() { return this.filters; }\n}",
     ]},
]

# ---------------------------------------------------------------------------
# MORE SQL
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "sql", "topic": "advanced_sql", "keywords": ["trigger", "view", "materialized view", "partition", "sql"],
     "snippets": [
         "-- Trigger: auto-update timestamp\nCREATE OR REPLACE FUNCTION update_timestamp()\nRETURNS TRIGGER AS $$\nBEGIN\n  NEW.updated_at = NOW();\n  RETURN NEW;\nEND;\n$$ LANGUAGE plpgsql;\n\nCREATE TRIGGER set_updated_at\nBEFORE UPDATE ON users\nFOR EACH ROW EXECUTE FUNCTION update_timestamp();",
         "-- Materialized view\nCREATE MATERIALIZED VIEW daily_stats AS\nSELECT\n  DATE(created_at)  AS day,\n  COUNT(*)          AS orders,\n  SUM(amount)       AS revenue,\n  AVG(amount)       AS avg_order\nFROM orders\nGROUP BY 1\nORDER BY 1;\n\nCREATE INDEX ON daily_stats(day);\nREFRESH MATERIALIZED VIEW CONCURRENTLY daily_stats;",
         "-- Table partitioning\nCREATE TABLE events (\n  id         BIGSERIAL,\n  created_at TIMESTAMPTZ NOT NULL,\n  type       VARCHAR(50),\n  payload    JSONB\n) PARTITION BY RANGE (created_at);\n\nCREATE TABLE events_2024_01 PARTITION OF events\n  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');\nCREATE TABLE events_2024_02 PARTITION OF events\n  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');",
         "-- Common Table Expressions: recursive\nWITH RECURSIVE hierarchy AS (\n  SELECT id, name, parent_id, 1 AS depth\n  FROM categories\n  WHERE parent_id IS NULL\n  UNION ALL\n  SELECT c.id, c.name, c.parent_id, h.depth + 1\n  FROM categories c\n  JOIN hierarchy h ON c.parent_id = h.id\n)\nSELECT * FROM hierarchy ORDER BY depth, name;",
         "-- Upsert pattern\nINSERT INTO user_stats (user_id, day, logins)\nVALUES ($1, CURRENT_DATE, 1)\nON CONFLICT (user_id, day)\nDO UPDATE SET\n  logins     = user_stats.logins + 1,\n  updated_at = NOW();",
     ]},
]

# ---------------------------------------------------------------------------
# MORE GO
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "go", "topic": "concurrency", "keywords": ["goroutine", "channel", "mutex", "context", "go"],
     "snippets": [
         "// Context for cancellation\npackage main\n\nimport (\n\t\"context\"\n\t\"time\"\n)\n\nfunc longTask(ctx context.Context) error {\n\tselect {\n\tcase <-time.After(5 * time.Second):\n\t\treturn nil\n\tcase <-ctx.Done():\n\t\treturn ctx.Err()\n\t}\n}\n\nfunc main() {\n\tctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)\n\tdefer cancel()\n\tif err := longTask(ctx); err != nil {\n\t\t// context.DeadlineExceeded\n\t}\n}",
         "// Worker pool pattern\nfunc workerPool(jobs <-chan int, results chan<- int, nWorkers int) {\n\tvar wg sync.WaitGroup\n\tfor i := 0; i < nWorkers; i++ {\n\t\twg.Add(1)\n\t\tgo func() {\n\t\t\tdefer wg.Done()\n\t\t\tfor j := range jobs {\n\t\t\t\tresults <- process(j)\n\t\t\t}\n\t\t}()\n\t}\n\tgo func() { wg.Wait(); close(results) }()\n}",
         "// sync.Map for concurrent access\nimport \"sync\"\n\nvar cache sync.Map\n\nfunc getOrSet(key string, fn func() interface{}) interface{} {\n\tif v, ok := cache.Load(key); ok {\n\t\treturn v\n\t}\n\tv := fn()\n\tcache.Store(key, v)\n\treturn v\n}",
         "// Go HTTP middleware\nfunc Logger(next http.Handler) http.Handler {\n\treturn http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {\n\t\tstart := time.Now()\n\t\tlog.Printf(\"%s %s\", r.Method, r.URL.Path)\n\t\tnext.ServeHTTP(w, r)\n\t\tlog.Printf(\"completed in %v\", time.Since(start))\n\t})\n}\n\nhttp.Handle(\"/\", Logger(myHandler))",
     ]},
    {"lang": "go", "topic": "testing", "keywords": ["testing", "test", "benchmark", "mock", "go"],
     "snippets": [
         "package mypackage\n\nimport (\n\t\"testing\"\n)\n\nfunc TestAdd(t *testing.T) {\n\tcases := []struct{ a, b, want int }{\n\t\t{1, 2, 3},\n\t\t{-1, 1, 0},\n\t\t{0, 0, 0},\n\t}\n\tfor _, tc := range cases {\n\t\tt.Run(fmt.Sprintf(\"%d+%d\", tc.a, tc.b), func(t *testing.T) {\n\t\t\tif got := Add(tc.a, tc.b); got != tc.want {\n\t\t\t\tt.Errorf(\"Add(%d,%d) = %d, want %d\", tc.a, tc.b, got, tc.want)\n\t\t\t}\n\t\t})\n\t}\n}\n\nfunc BenchmarkAdd(b *testing.B) {\n\tfor i := 0; i < b.N; i++ { Add(1, 2) }\n}",
     ]},
]

# ---------------------------------------------------------------------------
# MORE RUST
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "rust", "topic": "async_rust", "keywords": ["async", "tokio", "future", "rust"],
     "snippets": [
         "use tokio;\nuse reqwest;\nuse serde::{Deserialize, Serialize};\n\n#[derive(Deserialize)]\nstruct User { id: u32, name: String }\n\n#[tokio::main]\nasync fn main() -> Result<(), Box<dyn std::error::Error>> {\n    let client = reqwest::Client::new();\n    let users: Vec<User> = client\n        .get(\"https://jsonplaceholder.typicode.com/users\")\n        .send().await?\n        .json().await?;\n    println!(\"{} users\", users.len());\n    Ok(())\n}",
         "// Tokio channels\nuse tokio::sync::mpsc;\n\n#[tokio::main]\nasync fn main() {\n    let (tx, mut rx) = mpsc::channel(32);\n    tokio::spawn(async move {\n        for i in 0..5 {\n            tx.send(i).await.unwrap();\n        }\n    });\n    while let Some(msg) = rx.recv().await {\n        println!(\"Got: {}\", msg);\n    }\n}",
         "// Arc and Mutex for shared state\nuse std::sync::{Arc, Mutex};\nuse tokio;\n\ntype SharedState = Arc<Mutex<Vec<String>>>;\n\nasync fn append(state: SharedState, value: String) {\n    let mut data = state.lock().unwrap();\n    data.push(value);\n}\n\n#[tokio::main]\nasync fn main() {\n    let state: SharedState = Arc::new(Mutex::new(vec![]));\n    let s2 = Arc::clone(&state);\n    tokio::spawn(async move { append(s2, \"hello\".to_string()).await; });\n}",
     ]},
    {"lang": "rust", "topic": "error_handling", "keywords": ["anyhow", "thiserror", "error", "result", "rust"],
     "snippets": [
         "use thiserror::Error;\n\n#[derive(Error, Debug)]\npub enum AppError {\n    #[error(\"Not found: {0}\")]\n    NotFound(String),\n    #[error(\"Database error: {0}\")]\n    Database(#[from] sqlx::Error),\n    #[error(\"Validation: {field} - {message}\")]\n    Validation { field: String, message: String },\n}\n\n// anyhow for application code\nuse anyhow::{Context, Result};\n\nfn read_config(path: &str) -> Result<Config> {\n    let content = std::fs::read_to_string(path)\n        .with_context(|| format!(\"Failed to read config: {}\", path))?;\n    let config: Config = serde_json::from_str(&content)\n        .context(\"Invalid config format\")?;\n    Ok(config)\n}",
     ]},
]

# ---------------------------------------------------------------------------
# MORE C / C++
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "c", "topic": "dynamic_memory", "keywords": ["malloc", "free", "realloc", "memory leak", "c"],
     "snippets": [
         "#include <stdlib.h>\n#include <string.h>\n\n// Dynamic array\ntypedef struct {\n    int* data;\n    size_t size;\n    size_t capacity;\n} IntArray;\n\nIntArray* ia_create(size_t cap) {\n    IntArray* a = malloc(sizeof(IntArray));\n    a->data = malloc(cap * sizeof(int));\n    a->size = 0; a->capacity = cap;\n    return a;\n}\nvoid ia_push(IntArray* a, int v) {\n    if (a->size == a->capacity) {\n        a->capacity *= 2;\n        a->data = realloc(a->data, a->capacity * sizeof(int));\n    }\n    a->data[a->size++] = v;\n}\nvoid ia_free(IntArray* a) { free(a->data); free(a); }",
     ]},
    {"lang": "cpp", "topic": "modern_cpp", "keywords": ["c++17", "c++20", "std::optional", "std::variant", "cpp"],
     "snippets": [
         "#include <optional>\n#include <variant>\n#include <string_view>\n#include <ranges>\n\n// std::optional\nstd::optional<User> findUser(int id) {\n    if (!db.exists(id)) return std::nullopt;\n    return db.get(id);\n}\nif (auto u = findUser(42)) {\n    std::cout << u->name;\n}\n\n// std::variant\nusing Result = std::variant<User, std::string>;\nResult getUser(int id) {\n    if (!db.exists(id)) return std::string(\"Not found\");\n    return db.get(id);\n}\nstd::visit([](auto&& v) { /* handle */ }, getUser(1));",
         "// C++20 concepts\n#include <concepts>\n\ntemplate<typename T>\nconcept Numeric = std::is_arithmetic_v<T>;\n\ntemplate<Numeric T>\nT sum(std::span<const T> values) {\n    return std::reduce(values.begin(), values.end());\n}\n\n// Ranges\n#include <ranges>\nnamespace rv = std::views;\nstd::vector nums = {1,2,3,4,5,6,7,8,9,10};\nauto result = nums | rv::filter([](int n){ return n%2==0; })\n                   | rv::transform([](int n){ return n*n; });\nfor (int v : result) std::cout << v << ' ';",
     ]},
]

# ---------------------------------------------------------------------------
# MORE JAVA
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "java", "topic": "spring_boot", "keywords": ["spring", "jpa", "repository", "service", "java"],
     "snippets": [
         "// Spring Data JPA Entity\n@Entity\n@Table(name = \"users\")\n@Data\n@NoArgsConstructor\n@AllArgsConstructor\npublic class User {\n    @Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)\n    private Long id;\n\n    @Column(nullable = false)\n    private String name;\n\n    @Column(unique = true, nullable = false)\n    private String email;\n\n    @CreationTimestamp\n    private LocalDateTime createdAt;\n}",
         "// Spring Service layer\n@Service\n@RequiredArgsConstructor\n@Transactional\npublic class UserService {\n    private final UserRepository repo;\n    private final PasswordEncoder encoder;\n\n    public UserDTO createUser(CreateUserRequest req) {\n        if (repo.existsByEmail(req.getEmail()))\n            throw new ConflictException(\"Email already exists\");\n        User user = User.builder()\n            .name(req.getName())\n            .email(req.getEmail())\n            .password(encoder.encode(req.getPassword()))\n            .build();\n        return UserDTO.from(repo.save(user));\n    }\n\n    @Transactional(readOnly = true)\n    public Page<UserDTO> listUsers(Pageable pageable) {\n        return repo.findAll(pageable).map(UserDTO::from);\n    }\n}",
     ]},
]

# ---------------------------------------------------------------------------
# MORE ALGORITHMS
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "python", "topic": "algorithms_advanced", "keywords": ["trie", "segment tree", "union find", "topological sort", "python"],
     "snippets": [
         "# Trie (prefix tree)\nclass TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self): self.root = TrieNode()\n\n    def insert(self, word: str):\n        node = self.root\n        for ch in word:\n            node = node.children.setdefault(ch, TrieNode())\n        node.is_end = True\n\n    def search(self, word: str) -> bool:\n        node = self.root\n        for ch in word:\n            if ch not in node.children: return False\n            node = node.children[ch]\n        return node.is_end\n\n    def starts_with(self, prefix: str) -> bool:\n        node = self.root\n        for ch in prefix:\n            if ch not in node.children: return False\n            node = node.children[ch]\n        return True",
         "# Union-Find (Disjoint Set)\nclass UnionFind:\n    def __init__(self, n: int):\n        self.parent = list(range(n))\n        self.rank   = [0] * n\n        self.count  = n\n\n    def find(self, x: int) -> int:\n        if self.parent[x] != x:\n            self.parent[x] = self.find(self.parent[x])  # path compression\n        return self.parent[x]\n\n    def union(self, x: int, y: int) -> bool:\n        px, py = self.find(x), self.find(y)\n        if px == py: return False\n        if self.rank[px] < self.rank[py]: px, py = py, px\n        self.parent[py] = px\n        if self.rank[px] == self.rank[py]: self.rank[px] += 1\n        self.count -= 1\n        return True",
         "# Topological sort (Kahn's algorithm)\nfrom collections import deque\n\ndef toposort(n: int, edges: list) -> list:\n    indegree = [0] * n\n    graph = [[] for _ in range(n)]\n    for u, v in edges:\n        graph[u].append(v)\n        indegree[v] += 1\n    queue = deque(i for i in range(n) if indegree[i] == 0)\n    order = []\n    while queue:\n        u = queue.popleft()\n        order.append(u)\n        for v in graph[u]:\n            indegree[v] -= 1\n            if indegree[v] == 0:\n                queue.append(v)\n    return order if len(order) == n else []  # [] = cycle",
         "# Segment tree (range sum / point update)\nclass SegTree:\n    def __init__(self, data: list):\n        self.n = len(data)\n        self.tree = [0] * (2 * self.n)\n        for i, v in enumerate(data):\n            self.tree[self.n + i] = v\n        for i in range(self.n - 1, 0, -1):\n            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]\n\n    def update(self, i: int, val: int):\n        i += self.n\n        self.tree[i] = val\n        while i > 1:\n            i //= 2\n            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]\n\n    def query(self, l: int, r: int) -> int:  # [l, r)\n        res, l, r = 0, l + self.n, r + self.n\n        while l < r:\n            if l & 1: res += self.tree[l]; l += 1\n            if r & 1: r -= 1; res += self.tree[r]\n            l //= 2; r //= 2\n        return res",
         "# A* pathfinding\nimport heapq\n\ndef astar(grid, start, goal):\n    h = lambda p: abs(p[0]-goal[0]) + abs(p[1]-goal[1])  # Manhattan\n    open_set = [(h(start), 0, start, [start])]\n    visited = set()\n    while open_set:\n        _, g, pos, path = heapq.heappop(open_set)\n        if pos == goal: return path\n        if pos in visited: continue\n        visited.add(pos)\n        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:\n            nx, ny = pos[0]+dx, pos[1]+dy\n            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != '#':\n                npos = (nx, ny)\n                heapq.heappush(open_set, (g+1+h(npos), g+1, npos, path+[npos]))\n    return []",
     ]},
    {"lang": "python", "topic": "string_algorithms", "keywords": ["kmp", "rabin karp", "lcs", "string", "python"],
     "snippets": [
         "# KMP string matching O(n+m)\ndef kmp(text: str, pattern: str) -> list[int]:\n    def build_lps(p):\n        lps, length, i = [0]*len(p), 0, 1\n        while i < len(p):\n            if p[i] == p[length]:\n                length += 1; lps[i] = length; i += 1\n            elif length:\n                length = lps[length-1]\n            else:\n                lps[i] = 0; i += 1\n        return lps\n    lps, matches, j = build_lps(pattern), [], 0\n    for i, ch in enumerate(text):\n        while j and ch != pattern[j]: j = lps[j-1]\n        if ch == pattern[j]: j += 1\n        if j == len(pattern):\n            matches.append(i - j + 1); j = lps[j-1]\n    return matches",
         "# Longest palindromic substring (Manacher)\ndef longest_palindrome(s: str) -> str:\n    t = '#' + '#'.join(s) + '#'\n    n, c, r = len(t), 0, 0\n    p = [0] * n\n    for i in range(n):\n        mirror = 2*c - i\n        if i < r: p[i] = min(r - i, p[mirror])\n        while i+p[i]+1 < n and i-p[i]-1 >= 0 and t[i+p[i]+1] == t[i-p[i]-1]:\n            p[i] += 1\n        if i+p[i] > r: c, r = i, i+p[i]\n    center = p.index(max(p))\n    half = p[center]\n    return s[(center - half) // 2 : (center + half) // 2]",
     ]},
]

# ---------------------------------------------------------------------------
# MORE DESIGN PATTERNS
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "python", "topic": "patterns_structural", "keywords": ["adapter", "decorator", "proxy", "facade", "python"],
     "snippets": [
         "# Adapter pattern\nclass OldPaymentGateway:\n    def make_payment(self, amount_cents: int) -> bool:\n        return True\n\nclass NewPaymentAPI:\n    def pay(self, amount: float, currency: str = 'USD') -> dict:\n        return {'status': 'success'}\n\nclass PaymentAdapter:\n    def __init__(self, old_gateway: OldPaymentGateway):\n        self._gw = old_gateway\n    def pay(self, amount: float, currency: str = 'USD') -> dict:\n        success = self._gw.make_payment(int(amount * 100))\n        return {'status': 'success' if success else 'failed'}",
         "# Command pattern\nfrom abc import ABC, abstractmethod\n\nclass Command(ABC):\n    @abstractmethod\n    def execute(self) -> None: ...\n    @abstractmethod\n    def undo(self) -> None: ...\n\nclass TextEditor:\n    def __init__(self): self.text = ''; self._history = []\n    def execute(self, cmd: Command):\n        cmd.execute()\n        self._history.append(cmd)\n    def undo(self):\n        if self._history:\n            self._history.pop().undo()",
         "# Strategy pattern\nfrom abc import ABC, abstractmethod\n\nclass SortStrategy(ABC):\n    @abstractmethod\n    def sort(self, data: list) -> list: ...\n\nclass QuickSort(SortStrategy):\n    def sort(self, data): return sorted(data)\n\nclass BubbleSort(SortStrategy):\n    def sort(self, data):\n        d = data[:]\n        for i in range(len(d)):\n            for j in range(len(d)-i-1):\n                if d[j] > d[j+1]: d[j], d[j+1] = d[j+1], d[j]\n        return d\n\nclass Sorter:\n    def __init__(self, strategy: SortStrategy): self._s = strategy\n    def sort(self, data): return self._s.sort(data)",
     ]},
]

# ---------------------------------------------------------------------------
# MORE REACT / FRONTEND
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "javascript", "topic": "vue", "keywords": ["vue", "vuex", "composition api", "javascript"],
     "snippets": [
         "// Vue 3 Composition API\nimport { ref, computed, watch, onMounted } from 'vue';\n\nexport default {\n  setup() {\n    const count = ref(0);\n    const doubled = computed(() => count.value * 2);\n\n    watch(count, (newVal, oldVal) => {\n      console.log(`changed from ${oldVal} to ${newVal}`);\n    });\n\n    onMounted(async () => {\n      const data = await fetch('/api/data').then(r => r.json());\n      count.value = data.count;\n    });\n\n    return { count, doubled, increment: () => count.value++ };\n  }\n};",
         "// Vue 3 composable\nimport { ref, onMounted, onUnmounted } from 'vue';\n\nexport function useFetch(url) {\n  const data    = ref(null);\n  const loading = ref(true);\n  const error   = ref(null);\n\n  const controller = new AbortController();\n\n  onMounted(() => {\n    fetch(url, { signal: controller.signal })\n      .then(r => r.json())\n      .then(d => data.value = d)\n      .catch(e => error.value = e)\n      .finally(() => loading.value = false);\n  });\n\n  onUnmounted(() => controller.abort());\n\n  return { data, loading, error };\n}",
     ]},
    {"lang": "javascript", "topic": "state_management", "keywords": ["redux", "zustand", "state", "store", "javascript"],
     "snippets": [
         "// Zustand store\nimport { create } from 'zustand';\nimport { persist } from 'zustand/middleware';\n\nconst useStore = create(persist(\n  (set, get) => ({\n    user: null,\n    cart: [],\n    login:  (u) => set({ user: u }),\n    logout: ()  => set({ user: null, cart: [] }),\n    addToCart:    (item) => set(s => ({ cart: [...s.cart, item] })),\n    removeFromCart: (id) => set(s => ({ cart: s.cart.filter(i => i.id !== id) })),\n    cartTotal: () => get().cart.reduce((sum, i) => sum + i.price, 0),\n  }),\n  { name: 'app-storage' }\n));",
     ]},
]

# ---------------------------------------------------------------------------
# NGINX / WEB SERVER CONFIG
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "nginx", "topic": "config", "keywords": ["nginx", "reverse proxy", "ssl", "location", "upstream"],
     "snippets": [
         "# Nginx reverse proxy config\nupstream api {\n    server 127.0.0.1:8000;\n    keepalive 32;\n}\n\nserver {\n    listen 80;\n    server_name example.com;\n    return 301 https://$host$request_uri;\n}\n\nserver {\n    listen 443 ssl http2;\n    server_name example.com;\n\n    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;\n    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;\n    ssl_protocols TLSv1.2 TLSv1.3;\n\n    location /api/ {\n        proxy_pass http://api;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n        proxy_cache_bypass $http_upgrade;\n    }\n\n    location /static/ {\n        root /var/www;\n        expires 1y;\n        add_header Cache-Control 'public, immutable';\n    }\n}",
     ]},
]

# ---------------------------------------------------------------------------
# LINUX COMMANDS
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "bash", "topic": "linux_commands", "keywords": ["linux", "grep", "awk", "sed", "find", "bash"],
     "snippets": [
         "# Text processing\ngrep -r 'pattern' ./src --include='*.py' -n\ngrep -E '(error|warning)' app.log | tail -50\n\n# awk — process columns\nawk '{print $1, $3}' data.csv\nawk -F',' 'NR>1 {sum+=$2} END {print sum}' data.csv\n\n# sed — stream editor\nsed -i 's/foo/bar/g' file.txt\nsed -n '10,20p' file.txt\nfind . -name '*.py' -exec sed -i 's/oldmodule/newmodule/g' {} +",
         "# System monitoring\ntop -bn1 | head -20\nps aux --sort=-%cpu | head -10\ndf -h && free -h\nnetstat -tulnp | grep LISTEN\nss -tulnp\n\n# Find large files\nfind / -type f -size +100M -exec ls -lh {} \\; 2>/dev/null | sort -k5 -h\n\n# Disk usage\ndu -sh /* | sort -h\n\n# File permissions\nchmod 755 script.sh\nchown user:group file\nchmod -R 644 /var/www/html",
         "# Network utilities\ncurl -I https://example.com              # headers\ncurl -X POST https://api.example.com/users \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"name\":\"Alice\"}'\nwget -O output.html https://example.com\nnc -zv host.example.com 443             # port check\ndig +short example.com\nping -c 4 8.8.8.8",
     ]},
]

# ---------------------------------------------------------------------------
# PYTHON DJANGO
# ---------------------------------------------------------------------------

KNOWLEDGE += [
    {"lang": "python", "topic": "django", "keywords": ["django", "model", "view", "serializer", "rest framework"],
     "snippets": [
         "# Django model\nfrom django.db import models\n\nclass User(models.Model):\n    name       = models.CharField(max_length=100)\n    email      = models.EmailField(unique=True)\n    active     = models.BooleanField(default=True)\n    created_at = models.DateTimeField(auto_now_add=True)\n    updated_at = models.DateTimeField(auto_now=True)\n\n    class Meta:\n        ordering = ['-created_at']\n        indexes = [models.Index(fields=['email'])]\n\n    def __str__(self): return self.name",
         "# Django REST Framework\nfrom rest_framework import serializers, viewsets, permissions\nfrom rest_framework.decorators import action\nfrom rest_framework.response import Response\n\nclass UserSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = User\n        fields = ['id','name','email','created_at']\n        read_only_fields = ['id','created_at']\n\nclass UserViewSet(viewsets.ModelViewSet):\n    queryset = User.objects.filter(active=True)\n    serializer_class = UserSerializer\n    permission_classes = [permissions.IsAuthenticated]\n\n    @action(detail=True, methods=['post'])\n    def deactivate(self, request, pk=None):\n        user = self.get_object()\n        user.active = False; user.save()\n        return Response({'status': 'deactivated'})",
     ]},
]

# ---------------------------------------------------------------------------
# GENERATE CELLS
# ---------------------------------------------------------------------------

def main():
    output_path = Path(__file__).parent.parent / "data" / "prebuilt" / "cells.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Generating pre-built knowledge cells...")
    cells = cells_from_list(KNOWLEDGE)
    total = len(cells)

    output_path.write_text(
        json.dumps(cells, indent=None, separators=(',', ':')),
        encoding="utf-8"
    )

    size_kb = output_path.stat().st_size / 1024
    print(f"Generated {total} cells → {output_path}  ({size_kb:.1f} KB)")
    print("Languages/topics covered:")

    from collections import Counter
    langs = Counter(c["metadata"]["lang"] for c in cells.values())
    for lang, count in langs.most_common():
        print(f"  {lang:20s} {count} cells")


# ===========================================================================
# EXPANSION BLOCK — adds ~400 more unique cells
# ===========================================================================

# ---------------------------------------------------------------------------
# RUBY
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "ruby", "topic": "basics", "keywords": ["ruby", "class", "block", "gem", "rails"],
     "snippets": [
         "# Ruby basics\nname = 'Alice'\nage  = 30\nputs \"Hello, #{name}! You are #{age} years old.\"\n\n# Symbols\nstatus = :active\nhash   = { name: 'Bob', role: :admin }\n\n# Ranges\n(1..10).each { |n| print \"#{n} \" }\nevens = (1..20).select(&:even?)\nsum   = (1..100).sum",
         "# Classes and modules\nmodule Greetable\n  def greet\n    \"Hello, I am #{name}\"\n  end\nend\n\nclass User\n  include Greetable\n  attr_accessor :name, :email\n\n  def initialize(name, email)\n    @name  = name\n    @email = email\n  end\n\n  def to_s\n    \"User(#{@name})\"\n  end\nend\n\nu = User.new('Alice', 'alice@example.com')\nputs u.greet",
         "# Blocks, procs, lambdas\ndouble = ->(x) { x * 2 }\nsquare = proc { |x| x**2 }\n\n[1,2,3,4,5].map(&double)     # [2,4,6,8,10]\n[1,2,3,4,5].select(&:odd?)   # [1,3,5]\n[1,2,3].reduce(:+)           # 6\n\ndef measure\n  start = Time.now\n  yield\n  Time.now - start\nend\nelapsed = measure { sleep 0.1 }",
         "# Rails model\nclass Article < ApplicationRecord\n  belongs_to :user\n  has_many   :comments, dependent: :destroy\n  has_and_belongs_to_many :tags\n\n  validates :title,   presence: true, length: { minimum: 5 }\n  validates :content, presence: true\n\n  scope :published, -> { where(published: true) }\n  scope :recent,    -> { order(created_at: :desc).limit(10) }\n\n  before_save :normalize_title\n\n  private\n  def normalize_title\n    self.title = title.strip.capitalize\n  end\nend",
     ]},
]

# ---------------------------------------------------------------------------
# DART / FLUTTER
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "dart", "topic": "basics", "keywords": ["dart", "flutter", "widget", "async", "null safety"],
     "snippets": [
         "// Dart null safety\nString? nullable = null;\nString nonNull  = 'hello';\n\n// Null-aware operators\nString result = nullable ?? 'default';\nint? length  = nullable?.length;\nnullable ??= 'assigned if null';\n\n// Late initialisation\nlate String lazyValue;\nvoid init() { lazyValue = computeExpensive(); }",
         "// Dart async/await\nimport 'dart:async';\n\nFuture<String> fetchUser(int id) async {\n  await Future.delayed(Duration(milliseconds: 100));\n  return 'User $id';\n}\n\nFuture<void> main() async {\n  final user = await fetchUser(1);\n  print(user);\n\n  final results = await Future.wait([\n    fetchUser(1), fetchUser(2), fetchUser(3)\n  ]);\n  print(results);\n}",
         "// Flutter StatefulWidget\nimport 'package:flutter/material.dart';\n\nclass CounterPage extends StatefulWidget {\n  const CounterPage({super.key});\n  @override State<CounterPage> createState() => _CounterPageState();\n}\n\nclass _CounterPageState extends State<CounterPage> {\n  int _count = 0;\n\n  @override\n  Widget build(BuildContext context) {\n    return Scaffold(\n      appBar: AppBar(title: const Text('Counter')),\n      body: Center(child: Text('$_count', style: Theme.of(context).textTheme.displayLarge)),\n      floatingActionButton: FloatingActionButton(\n        onPressed: () => setState(() => _count++),\n        child: const Icon(Icons.add),\n      ),\n    );\n  }\n}",
     ]},
]

# ---------------------------------------------------------------------------
# SCALA
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "scala", "topic": "basics", "keywords": ["scala", "case class", "pattern matching", "functional"],
     "snippets": [
         "// Scala case class and pattern matching\ncase class User(id: Int, name: String, active: Boolean = true)\n\nval user = User(1, \"Alice\")\n\nuser match {\n  case User(_, name, true)  => println(s\"Active: $name\")\n  case User(id, name, false) => println(s\"Inactive user $id: $name\")\n}\n\n// Option\ndef findUser(id: Int): Option[User] = users.find(_.id == id)\n\nfindUser(1) match {\n  case Some(u) => println(u.name)\n  case None    => println(\"Not found\")\n}",
         "// Collections and functional\nval nums = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)\n\nval result = nums\n  .filter(_ % 2 == 0)\n  .map(n => n * n)\n  .foldLeft(0)(_ + _)\n\n// For comprehension\nval pairs = for {\n  x <- 1 to 3\n  y <- 1 to 3\n  if x != y\n} yield (x, y)\n\n// Future\nimport scala.concurrent.Future\nimport scala.concurrent.ExecutionContext.Implicits.global\n\nval f: Future[Int] = Future { expensiveComputation() }\nf.map(_ * 2).foreach(println)",
     ]},
]

# ---------------------------------------------------------------------------
# ELIXIR
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "elixir", "topic": "basics", "keywords": ["elixir", "genserver", "process", "pipe", "pattern matching"],
     "snippets": [
         "# Elixir basics\n# Immutable data, pattern matching, pipe operator\n\nname = \"Alice\"\n{:ok, file} = File.read(\"data.txt\")\n\n# Pipe operator\nresult = \"hello world\"\n  |> String.upcase()\n  |> String.split()\n  |> Enum.reverse()\n  |> Enum.join(\"-\")\n# => \"WORLD-HELLO\"\n\n# Pattern matching in functions\ndefmodule Math do\n  def factorial(0), do: 1\n  def factorial(n) when n > 0, do: n * factorial(n - 1)\nend",
         "# GenServer\ndefmodule Counter do\n  use GenServer\n\n  def start_link(init), do: GenServer.start_link(__MODULE__, init, name: __MODULE__)\n  def increment, do: GenServer.cast(__MODULE__, :increment)\n  def value,     do: GenServer.call(__MODULE__, :value)\n\n  @impl true\n  def init(count), do: {:ok, count}\n\n  @impl true\n  def handle_cast(:increment, count), do: {:noreply, count + 1}\n\n  @impl true\n  def handle_call(:value, _from, count), do: {:reply, count, count}\nend",
     ]},
]

# ---------------------------------------------------------------------------
# HASKELL
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "haskell", "topic": "basics", "keywords": ["haskell", "pure", "monad", "type class", "lazy"],
     "snippets": [
         "-- Haskell basics\nmodule Main where\n\n-- Pure functions\ndouble :: Int -> Int\ndouble x = x * 2\n\nfactorial :: Integer -> Integer\nfactorial 0 = 1\nfactorial n = n * factorial (n - 1)\n\n-- List comprehension\nprimes :: [Int]\nprimes = sieve [2..]\n  where sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]\n\n-- Type classes\nclass Describable a where\n  describe :: a -> String\n\ndata Color = Red | Green | Blue\ninstance Describable Color where\n  describe Red   = \"red\"\n  describe Green = \"green\"\n  describe Blue  = \"blue\"",
     ]},
]

# ---------------------------------------------------------------------------
# LUA
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "lua", "topic": "basics", "keywords": ["lua", "table", "metatables", "coroutine", "scripting"],
     "snippets": [
         "-- Lua basics\nlocal name = 'Alice'\nlocal age  = 30\nprint(string.format('Hello, %s! Age: %d', name, age))\n\n-- Tables (arrays and dicts)\nlocal arr = {10, 20, 30, 40}\nlocal map = {name='Bob', role='admin'}\n\nfor i, v in ipairs(arr) do\n  print(i, v)\nend\n\nfor k, v in pairs(map) do\n  print(k, '=', v)\nend",
         "-- OOP with metatables\nlocal Animal = {}\nAnimal.__index = Animal\n\nfunction Animal.new(name, sound)\n  return setmetatable({name=name, sound=sound}, Animal)\nend\n\nfunction Animal:speak()\n  return self.name .. ' says ' .. self.sound\nend\n\nlocal dog = Animal.new('Rex', 'Woof')\nprint(dog:speak())",
     ]},
]

# ---------------------------------------------------------------------------
# R (Data Science)
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "r", "topic": "data_analysis", "keywords": ["r", "dataframe", "ggplot", "tidyverse", "statistics"],
     "snippets": [
         "# R data analysis\nlibrary(tidyverse)\n\n# Load and inspect data\ndf <- read_csv('data.csv')\nglimpse(df)\nsummary(df)\n\n# dplyr pipeline\nresult <- df %>%\n  filter(age > 25) %>%\n  select(name, age, salary) %>%\n  mutate(salary_k = salary / 1000) %>%\n  group_by(department) %>%\n  summarise(\n    count    = n(),\n    avg_sal  = mean(salary_k),\n    max_sal  = max(salary_k)\n  ) %>%\n  arrange(desc(avg_sal))",
         "# ggplot2 visualisation\nlibrary(ggplot2)\n\nggplot(df, aes(x = age, y = salary, colour = department)) +\n  geom_point(alpha = 0.6) +\n  geom_smooth(method = 'lm') +\n  scale_colour_brewer(palette = 'Set1') +\n  labs(title = 'Salary vs Age by Department',\n       x = 'Age', y = 'Salary (USD)') +\n  theme_minimal()",
     ]},
]

# ---------------------------------------------------------------------------
# ADVANCED JAVASCRIPT
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "javascript", "topic": "web_workers", "keywords": ["web worker", "thread", "postMessage", "javascript"],
     "snippets": [
         "// Main thread\nconst worker = new Worker('worker.js');\nworker.postMessage({ type: 'compute', data: largeArray });\nworker.onmessage = ({ data }) => {\n  console.log('Result:', data.result);\n};\nworker.onerror = (e) => console.error(e);\n\n// worker.js\nself.onmessage = ({ data }) => {\n  if (data.type === 'compute') {\n    const result = data.data.reduce((a, b) => a + b, 0);\n    self.postMessage({ result });\n  }\n};",
         "// Canvas 2D drawing\nconst canvas = document.getElementById('canvas');\nconst ctx    = canvas.getContext('2d');\n\n// Draw gradient rectangle\nconst grad = ctx.createLinearGradient(0, 0, canvas.width, 0);\ngrad.addColorStop(0, '#3b82f6');\ngrad.addColorStop(1, '#10b981');\nctx.fillStyle = grad;\nctx.fillRect(0, 0, canvas.width, canvas.height);\n\n// Animation loop\nfunction animate(timestamp) {\n  ctx.clearRect(0, 0, canvas.width, canvas.height);\n  // draw frame\n  requestAnimationFrame(animate);\n}\nrequestAnimationFrame(animate);",
         "// Intersection Observer (lazy loading)\nconst observer = new IntersectionObserver(\n  (entries) => {\n    entries.forEach(entry => {\n      if (entry.isIntersecting) {\n        const img = entry.target;\n        img.src = img.dataset.src;\n        observer.unobserve(img);\n      }\n    });\n  },\n  { rootMargin: '200px', threshold: 0.01 }\n);\n\ndocument.querySelectorAll('img[data-src]')\n  .forEach(img => observer.observe(img));",
         "// Web Crypto API\nconst key = await crypto.subtle.generateKey(\n  { name: 'AES-GCM', length: 256 },\n  true, ['encrypt', 'decrypt']\n);\n\nconst iv   = crypto.getRandomValues(new Uint8Array(12));\nconst data = new TextEncoder().encode('secret message');\nconst encrypted = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, data);\nconst decrypted = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, encrypted);\nconsole.log(new TextDecoder().decode(decrypted));",
         "// Custom events\nconst bus = new EventTarget();\n\nbus.addEventListener('user:login', (e) => {\n  console.log('Logged in:', e.detail.user);\n});\n\nbus.dispatchEvent(new CustomEvent('user:login', {\n  detail: { user: { id: 1, name: 'Alice' } }\n}));",
     ]},
    {"lang": "javascript", "topic": "next_js", "keywords": ["nextjs", "react", "ssr", "app router", "javascript"],
     "snippets": [
         "// Next.js App Router — page component\nexport default async function UsersPage() {\n  const users = await fetch('https://api.example.com/users', {\n    next: { revalidate: 60 }   // ISR: revalidate every 60s\n  }).then(r => r.json());\n\n  return (\n    <main>\n      <h1>Users</h1>\n      <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>\n    </main>\n  );\n}\n\nexport const metadata = { title: 'Users' };",
         "// Next.js API route (App Router)\n// app/api/users/route.ts\nimport { NextRequest, NextResponse } from 'next/server';\n\nexport async function GET(req: NextRequest) {\n  const { searchParams } = req.nextUrl;\n  const page  = Number(searchParams.get('page') ?? 1);\n  const users = await db.users.findMany({ skip: (page-1)*20, take: 20 });\n  return NextResponse.json(users);\n}\n\nexport async function POST(req: NextRequest) {\n  const body = await req.json();\n  const user = await db.users.create({ data: body });\n  return NextResponse.json(user, { status: 201 });\n}",
     ]},
    {"lang": "javascript", "topic": "svelte", "keywords": ["svelte", "reactive", "store", "component", "javascript"],
     "snippets": [
         "<!-- Svelte component -->\n<script>\n  import { onMount } from 'svelte';\n  import { writable } from 'svelte/store';\n\n  let name = '';\n  let users = [];\n  let loading = true;\n\n  onMount(async () => {\n    users = await fetch('/api/users').then(r => r.json());\n    loading = false;\n  });\n\n  $: greeting = name ? `Hello, ${name}!` : '';\n</script>\n\n<input bind:value={name} placeholder=\"Your name\" />\n<p>{greeting}</p>\n\n{#if loading}\n  <p>Loading...</p>\n{:else}\n  {#each users as user (user.id)}\n    <p>{user.name}</p>\n  {/each}\n{/if}",
     ]},
]

# ---------------------------------------------------------------------------
# MORE CSS
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "css", "topic": "advanced_css", "keywords": ["css", "container query", "has selector", "cascade layer", "css"],
     "snippets": [
         "/* Container queries */\n.card-wrapper {\n  container-type: inline-size;\n  container-name: card;\n}\n\n@container card (min-width: 400px) {\n  .card { flex-direction: row; }\n  .card img { width: 200px; }\n}\n\n/* :has() selector */\n.form:has(input:invalid) .submit-btn {\n  opacity: 0.5;\n  pointer-events: none;\n}\n\n/* Cascade layers */\n@layer base, components, utilities;\n@layer base {\n  * { box-sizing: border-box; margin: 0; }\n}\n@layer utilities {\n  .sr-only { position: absolute; width: 1px; clip: rect(0,0,0,0); }\n}",
         "/* CSS logical properties */\n.box {\n  margin-block:  1rem;     /* top + bottom */\n  margin-inline: 2rem;     /* left + right */\n  padding-block-start: 0.5rem;\n  border-inline-end: 2px solid blue;\n  inset-inline-start: 0;   /* left in LTR */\n}\n\n/* Scroll snap */\n.carousel {\n  display: flex;\n  overflow-x: auto;\n  scroll-snap-type: x mandatory;\n  scroll-behavior: smooth;\n}\n.slide {\n  flex: 0 0 100%;\n  scroll-snap-align: start;\n}",
         "/* CSS nesting (native) */\n.card {\n  background: white;\n  border-radius: 0.5rem;\n  padding: 1rem;\n\n  & header {\n    font-weight: bold;\n    margin-bottom: 0.5rem;\n  }\n\n  &:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }\n\n  @media (max-width: 640px) {\n    padding: 0.5rem;\n  }\n}",
         "/* CSS Grid advanced */\n.layout {\n  display: grid;\n  grid-template-columns: [sidebar-start] 250px [sidebar-end main-start] 1fr [main-end];\n  grid-template-rows: 60px 1fr 40px;\n  min-height: 100vh;\n}\n\n/* Subgrid */\n.row {\n  display: grid;\n  grid-column: main;\n  grid-template-columns: subgrid;\n}\n\n/* Masonry layout (soon in browsers) */\n.masonry {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  grid-template-rows: masonry;\n}",
     ]},
]

# ---------------------------------------------------------------------------
# ADVANCED ALGORITHMS
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "graph_algorithms", "keywords": ["floyd warshall", "bellman ford", "MST", "kruskal", "python"],
     "snippets": [
         "# Floyd-Warshall: all-pairs shortest paths O(n³)\ndef floyd_warshall(n: int, edges: list) -> list:\n    INF = float('inf')\n    dist = [[INF]*n for _ in range(n)]\n    for i in range(n): dist[i][i] = 0\n    for u, v, w in edges:\n        dist[u][v] = min(dist[u][v], w)\n    for k in range(n):\n        for i in range(n):\n            for j in range(n):\n                if dist[i][k] + dist[k][j] < dist[i][j]:\n                    dist[i][j] = dist[i][k] + dist[k][j]\n    return dist",
         "# Bellman-Ford: shortest paths with negative weights\ndef bellman_ford(n: int, edges: list, src: int) -> list:\n    dist = [float('inf')] * n\n    dist[src] = 0\n    for _ in range(n - 1):\n        for u, v, w in edges:\n            if dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n    # Check negative cycles\n    for u, v, w in edges:\n        if dist[u] + w < dist[v]:\n            return []  # negative cycle detected\n    return dist",
         "# Kruskal's MST O(E log E)\ndef kruskal(n: int, edges: list) -> list:\n    edges.sort(key=lambda e: e[2])\n    parent = list(range(n))\n    def find(x):\n        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n        return x\n    mst, cost = [], 0\n    for u, v, w in edges:\n        pu, pv = find(u), find(v)\n        if pu != pv:\n            parent[pu] = pv\n            mst.append((u, v, w))\n            cost += w\n    return mst",
         "# Prim's MST O((V+E) log V)\nimport heapq\n\ndef prim(graph: dict, start=0) -> int:\n    visited = set()\n    heap = [(0, start)]\n    total = 0\n    while heap:\n        w, u = heapq.heappop(heap)\n        if u in visited: continue\n        visited.add(u)\n        total += w\n        for v, weight in graph.get(u, []):\n            if v not in visited:\n                heapq.heappush(heap, (weight, v))\n    return total",
         "# Floyd's cycle detection (tortoise and hare)\ndef has_cycle(head) -> bool:\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow is fast:\n            return True\n    return False\n\ndef find_cycle_start(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow, fast = slow.next, fast.next.next\n        if slow is fast: break\n    else: return None\n    slow = head\n    while slow is not fast:\n        slow, fast = slow.next, fast.next\n    return slow",
         "# Counting sort O(n+k)\ndef counting_sort(arr: list, max_val: int) -> list:\n    count = [0] * (max_val + 1)\n    for x in arr: count[x] += 1\n    result = []\n    for val, freq in enumerate(count):\n        result.extend([val] * freq)\n    return result\n\n# Radix sort O(d*n)\ndef radix_sort(arr: list) -> list:\n    for exp in [1, 10, 100, 1000]:\n        buckets = [[] for _ in range(10)]\n        for n in arr: buckets[(n // exp) % 10].append(n)\n        arr = [n for bucket in buckets for n in bucket]\n    return arr",
         "# Knapsack 0/1 DP\ndef knapsack(weights: list, values: list, capacity: int) -> int:\n    n = len(weights)\n    dp = [[0]*(capacity+1) for _ in range(n+1)]\n    for i in range(1, n+1):\n        for w in range(capacity+1):\n            dp[i][w] = dp[i-1][w]\n            if weights[i-1] <= w:\n                dp[i][w] = max(dp[i][w],\n                               dp[i-1][w-weights[i-1]] + values[i-1])\n    return dp[n][capacity]",
         "# Coin change DP\ndef coin_change(coins: list, amount: int) -> int:\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for coin in coins:\n        for x in range(coin, amount + 1):\n            dp[x] = min(dp[x], dp[x - coin] + 1)\n    return dp[amount] if dp[amount] != float('inf') else -1",
     ]},
]

# ---------------------------------------------------------------------------
# MORE DATA STRUCTURES
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "advanced_data_structures", "keywords": ["bloom filter", "lru cache", "deque", "heap", "python"],
     "snippets": [
         "# LRU Cache\nfrom collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self._cap  = capacity\n        self._cache = OrderedDict()\n\n    def get(self, key: int) -> int:\n        if key not in self._cache: return -1\n        self._cache.move_to_end(key)\n        return self._cache[key]\n\n    def put(self, key: int, value: int) -> None:\n        if key in self._cache:\n            self._cache.move_to_end(key)\n        self._cache[key] = value\n        if len(self._cache) > self._cap:\n            self._cache.popitem(last=False)",
         "# Bloom filter (probabilistic membership)\nimport hashlib\n\nclass BloomFilter:\n    def __init__(self, size=1000, hashes=3):\n        self._bits = [0] * size\n        self._size = size\n        self._hashes = hashes\n\n    def _positions(self, item: str):\n        for i in range(self._hashes):\n            h = int(hashlib.md5(f'{item}:{i}'.encode()).hexdigest(), 16)\n            yield h % self._size\n\n    def add(self, item: str):\n        for pos in self._positions(item):\n            self._bits[pos] = 1\n\n    def __contains__(self, item: str) -> bool:\n        return all(self._bits[p] for p in self._positions(item))",
         "# Min/max stack O(1)\nclass MinStack:\n    def __init__(self):\n        self._stack = []\n        self._min   = []\n\n    def push(self, val: int):\n        self._stack.append(val)\n        self._min.append(min(val, self._min[-1] if self._min else val))\n\n    def pop(self):\n        self._stack.pop()\n        self._min.pop()\n\n    def top(self) -> int:  return self._stack[-1]\n    def get_min(self) -> int: return self._min[-1]",
         "# Interval tree / merge intervals\ndef merge_intervals(intervals: list) -> list:\n    if not intervals: return []\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for start, end in intervals[1:]:\n        if start <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], end)\n        else:\n            merged.append([start, end])\n    return merged",
     ]},
]

# ---------------------------------------------------------------------------
# MORE SECURITY
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "security_advanced", "keywords": ["xss", "csrf", "sql injection", "owasp", "security"],
     "snippets": [
         "# SQL injection prevention\n# WRONG: f'SELECT * FROM users WHERE name = \\'{name}\\''\n# RIGHT: parameterised queries\nimport sqlite3\nconn = sqlite3.connect('db.sqlite3')\ncursor = conn.cursor()\ncursor.execute('SELECT * FROM users WHERE name = ?', (name,))\nrows = cursor.fetchall()\n\n# With SQLAlchemy ORM — safe by default\nfrom sqlalchemy import select\nstmt = select(User).where(User.name == name)  # auto-escaped",
         "# Input validation and sanitisation\nimport html\nimport re\n\ndef sanitise_html(text: str) -> str:\n    return html.escape(text)  # XSS prevention\n\ndef validate_email(email: str) -> bool:\n    return bool(re.match(r'^[\\w.+-]+@[\\w-]+\\.[\\w.]+$', email))\n\ndef validate_username(name: str) -> bool:\n    return bool(re.match(r'^[a-zA-Z0-9_]{3,30}$', name))\n\n# CSRF token\nimport secrets\ndef generate_csrf_token() -> str:\n    return secrets.token_urlsafe(32)",
         "# Rate limiting\nfrom collections import defaultdict\nimport time\n\nclass RateLimiter:\n    def __init__(self, max_calls: int, period: float):\n        self._max = max_calls\n        self._period = period\n        self._calls: dict = defaultdict(list)\n\n    def is_allowed(self, key: str) -> bool:\n        now = time.time()\n        calls = self._calls[key]\n        # Remove expired\n        self._calls[key] = [t for t in calls if now - t < self._period]\n        if len(self._calls[key]) >= self._max:\n            return False\n        self._calls[key].append(now)\n        return True",
         "# HTTPS / TLS in Python\nimport ssl\nimport urllib.request\n\ncontext = ssl.create_default_context()\ncontext.verify_mode = ssl.CERT_REQUIRED\ncontext.check_hostname = True\n\n# Load custom CA\ncontext.load_verify_locations('ca-bundle.crt')\n\n# Mutual TLS\ncontext.load_cert_chain('client.crt', 'client.key')\n\nwith urllib.request.urlopen('https://example.com', context=context) as r:\n    data = r.read()",
     ]},
]

# ---------------------------------------------------------------------------
# MESSAGE QUEUES / KAFKA
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "kafka", "keywords": ["kafka", "consumer", "producer", "message queue", "python"],
     "snippets": [
         "from confluent_kafka import Producer, Consumer\nimport json\n\n# Producer\nproducer = Producer({'bootstrap.servers': 'localhost:9092'})\n\ndef send_event(topic: str, key: str, value: dict):\n    producer.produce(\n        topic,\n        key=key.encode(),\n        value=json.dumps(value).encode(),\n        callback=lambda err, msg: (\n            print(f'Delivered: {msg.topic()}') if not err\n            else print(f'Error: {err}')\n        )\n    )\n    producer.poll(0)\n\nsend_event('user-events', 'user-1', {'type': 'signup', 'email': 'alice@example.com'})\nproducer.flush()",
         "from confluent_kafka import Consumer\nimport json\n\nconsumer = Consumer({\n    'bootstrap.servers': 'localhost:9092',\n    'group.id':          'my-consumer-group',\n    'auto.offset.reset': 'earliest',\n})\nconsumer.subscribe(['user-events'])\n\ntry:\n    while True:\n        msg = consumer.poll(timeout=1.0)\n        if msg is None: continue\n        if msg.error(): print(f'Error: {msg.error()}'); continue\n        event = json.loads(msg.value())\n        print(f'Received: {event}')\nfinally:\n    consumer.close()",
     ]},
    {"lang": "python", "topic": "rabbitmq", "keywords": ["rabbitmq", "amqp", "pika", "message", "queue"],
     "snippets": [
         "import pika\nimport json\n\n# Publisher\nconn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))\nchannel = conn.channel()\nchannel.exchange_declare(exchange='events', exchange_type='topic', durable=True)\n\ndef publish(routing_key: str, data: dict):\n    channel.basic_publish(\n        exchange='events',\n        routing_key=routing_key,\n        body=json.dumps(data),\n        properties=pika.BasicProperties(delivery_mode=2)  # persistent\n    )\n\npublish('user.signup', {'id': 1, 'email': 'alice@example.com'})\nconn.close()",
     ]},
]

# ---------------------------------------------------------------------------
# ELASTICSEARCH
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "elasticsearch", "keywords": ["elasticsearch", "search", "index", "query", "python"],
     "snippets": [
         "from elasticsearch import AsyncElasticsearch\n\nes = AsyncElasticsearch('http://localhost:9200')\n\nasync def index_document(index: str, id: str, doc: dict):\n    await es.index(index=index, id=id, document=doc)\n\nasync def search(index: str, query: str, size: int = 10) -> list:\n    resp = await es.search(\n        index=index,\n        query={\n            'multi_match': {\n                'query': query,\n                'fields': ['title^2', 'content', 'tags'],\n            }\n        },\n        size=size,\n        highlight={'fields': {'content': {}}}\n    )\n    return [hit['_source'] for hit in resp['hits']['hits']]",
     ]},
]

# ---------------------------------------------------------------------------
# MONGODB
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "mongodb", "keywords": ["mongodb", "motor", "document", "collection", "nosql"],
     "snippets": [
         "from motor.motor_asyncio import AsyncIOMotorClient\nfrom bson import ObjectId\nfrom datetime import datetime\n\nclient = AsyncIOMotorClient('mongodb://localhost:27017')\ndb     = client['myapp']\nusers  = db['users']\n\nasync def create_user(data: dict) -> str:\n    data['created_at'] = datetime.utcnow()\n    result = await users.insert_one(data)\n    return str(result.inserted_id)\n\nasync def find_users(query: dict, limit: int = 20) -> list:\n    cursor = users.find(query).sort('created_at', -1).limit(limit)\n    return [doc async for doc in cursor]\n\nasync def update_user(id: str, update: dict) -> bool:\n    result = await users.update_one(\n        {'_id': ObjectId(id)},\n        {'$set': update, '$currentDate': {'updated_at': True}}\n    )\n    return result.modified_count > 0",
     ]},
]

# ---------------------------------------------------------------------------
# DEVOPS — GITHUB ACTIONS
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "yaml", "topic": "github_actions", "keywords": ["github actions", "ci cd", "workflow", "deploy", "yaml"],
     "snippets": [
         "# .github/workflows/ci.yml\nname: CI\non:\n  push:         { branches: [main] }\n  pull_request: { branches: [main] }\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with: { python-version: '3.12' }\n      - run: pip install -r requirements.txt\n      - run: pytest --cov=. --cov-report=xml\n      - uses: codecov/codecov-action@v4",
         "# Deploy workflow\nname: Deploy\non:\n  push: { branches: [main] }\n\njobs:\n  deploy:\n    runs-on: ubuntu-latest\n    environment: production\n    steps:\n      - uses: actions/checkout@v4\n      - name: Build Docker image\n        run: docker build -t ${{ secrets.REGISTRY }}/app:${{ github.sha }} .\n      - name: Push image\n        run: |\n          echo ${{ secrets.REGISTRY_TOKEN }} | docker login -u ${{ secrets.REGISTRY_USER }} --password-stdin\n          docker push ${{ secrets.REGISTRY }}/app:${{ github.sha }}\n      - name: Deploy to server\n        uses: appleboy/ssh-action@v1\n        with:\n          host:     ${{ secrets.HOST }}\n          username: ${{ secrets.USER }}\n          key:      ${{ secrets.SSH_KEY }}\n          script:   cd /app && docker compose pull && docker compose up -d",
     ]},
]

# ---------------------------------------------------------------------------
# TERRAFORM
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "hcl", "topic": "terraform", "keywords": ["terraform", "aws", "resource", "variable", "module"],
     "snippets": [
         "# Terraform AWS EC2 instance\nterraform {\n  required_providers {\n    aws = { source = \"hashicorp/aws\", version = \"~> 5.0\" }\n  }\n}\n\nprovider \"aws\" { region = var.region }\n\nvariable \"region\"        { default = \"us-east-1\" }\nvariable \"instance_type\" { default = \"t3.micro\" }\n\nresource \"aws_instance\" \"app\" {\n  ami           = data.aws_ami.ubuntu.id\n  instance_type = var.instance_type\n  key_name      = aws_key_pair.deployer.key_name\n\n  tags = { Name = \"my-app\", Env = terraform.workspace }\n}\n\noutput \"public_ip\" { value = aws_instance.app.public_ip }",
         "# Terraform S3 + CloudFront\nresource \"aws_s3_bucket\" \"frontend\" {\n  bucket = \"my-app-frontend\"\n}\n\nresource \"aws_s3_bucket_public_access_block\" \"frontend\" {\n  bucket                  = aws_s3_bucket.frontend.id\n  block_public_acls       = true\n  block_public_policy     = true\n  ignore_public_acls      = true\n  restrict_public_buckets = true\n}\n\nresource \"aws_cloudfront_distribution\" \"cdn\" {\n  enabled             = true\n  default_root_object = \"index.html\"\n  origin {\n    domain_name = aws_s3_bucket.frontend.bucket_regional_domain_name\n    origin_id   = \"S3-frontend\"\n  }\n}",
     ]},
]

# ---------------------------------------------------------------------------
# MORE PYTHON ASYNC
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "asyncio_advanced", "keywords": ["asyncio", "semaphore", "queue", "event", "python"],
     "snippets": [
         "import asyncio\n\n# Semaphore — limit concurrent connections\nasync def fetch(session, url, semaphore):\n    async with semaphore:\n        async with session.get(url) as r:\n            return await r.json()\n\nasync def main(urls):\n    sem = asyncio.Semaphore(10)  # max 10 concurrent\n    async with aiohttp.ClientSession() as session:\n        tasks = [fetch(session, url, sem) for url in urls]\n        return await asyncio.gather(*tasks, return_exceptions=True)",
         "import asyncio\n\n# Async queue (producer–consumer)\nasync def producer(queue: asyncio.Queue, items: list):\n    for item in items:\n        await queue.put(item)\n        await asyncio.sleep(0.1)\n    await queue.put(None)  # sentinel\n\nasync def consumer(queue: asyncio.Queue, worker_id: int):\n    while True:\n        item = await queue.get()\n        if item is None:\n            await queue.put(None)  # pass sentinel on\n            break\n        await process(item)\n        queue.task_done()\n\nasync def main():\n    q = asyncio.Queue(maxsize=100)\n    await asyncio.gather(producer(q, data), consumer(q, 1), consumer(q, 2))",
         "# FastAPI background tasks and WebSocket\nfrom fastapi import FastAPI, WebSocket, BackgroundTasks\n\napp = FastAPI()\n\n@app.post('/send-email')\nasync def send_email_endpoint(email: str, bg: BackgroundTasks):\n    bg.add_task(send_email, email)  # non-blocking\n    return {'status': 'queued'}\n\nclients: list[WebSocket] = []\n\n@app.websocket('/ws')\nasync def ws_endpoint(ws: WebSocket):\n    await ws.accept()\n    clients.append(ws)\n    try:\n        while True:\n            data = await ws.receive_text()\n            for c in clients:\n                await c.send_text(f'broadcast: {data}')\n    except Exception:\n        clients.remove(ws)",
     ]},
]

# ---------------------------------------------------------------------------
# ADVANCED SQL — Window functions, JSON, Full-text
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "sql", "topic": "analytics", "keywords": ["window function", "percentile", "running total", "sql"],
     "snippets": [
         "-- Advanced window functions\nSELECT\n  order_id,\n  amount,\n  created_at,\n  SUM(amount) OVER (ORDER BY created_at\n                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,\n  AVG(amount) OVER (ORDER BY created_at\n                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7,\n  NTILE(4)    OVER (ORDER BY amount DESC) AS quartile,\n  PERCENT_RANK() OVER (ORDER BY amount)   AS pct_rank\nFROM orders;",
         "-- LATERAL JOIN (apply)\nSELECT u.name, recent.title, recent.created_at\nFROM users u\nCROSS JOIN LATERAL (\n  SELECT title, created_at\n  FROM posts\n  WHERE user_id = u.id\n  ORDER BY created_at DESC\n  LIMIT 3\n) recent;\n\n-- DISTINCT ON (PostgreSQL)\nSELECT DISTINCT ON (user_id)\n  user_id, title, created_at\nFROM posts\nORDER BY user_id, created_at DESC;",
         "-- Pivot table with crosstab\nSELECT\n  product,\n  SUM(CASE WHEN month = 1 THEN revenue END) AS jan,\n  SUM(CASE WHEN month = 2 THEN revenue END) AS feb,\n  SUM(CASE WHEN month = 3 THEN revenue END) AS mar\nFROM sales\nGROUP BY product;\n\n-- Time-series gap fill\nWITH days AS (\n  SELECT generate_series(\n    '2024-01-01'::date,\n    '2024-12-31'::date,\n    '1 day'\n  )::date AS day\n)\nSELECT d.day, COALESCE(s.revenue, 0) AS revenue\nFROM days d\nLEFT JOIN daily_sales s ON s.day = d.day;",
     ]},
]

# ---------------------------------------------------------------------------
# MORE GO — Web frameworks, database
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "go", "topic": "gin_framework", "keywords": ["gin", "router", "middleware", "rest", "go"],
     "snippets": [
         "package main\n\nimport (\n\t\"net/http\"\n\t\"github.com/gin-gonic/gin\"\n)\n\nfunc main() {\n\tr := gin.Default()\n\tr.Use(gin.Logger(), gin.Recovery())\n\n\tapi := r.Group(\"/api\", AuthMiddleware())\n\t{\n\t\tapi.GET(\"/users\",    listUsers)\n\t\tapi.POST(\"/users\",   createUser)\n\t\tapi.GET(\"/users/:id\", getUser)\n\t}\n\tr.Run(\":8080\")\n}\n\nfunc listUsers(c *gin.Context) {\n\tpage  := c.DefaultQuery(\"page\", \"1\")\n\tusers := db.ListUsers(page)\n\tc.JSON(http.StatusOK, gin.H{\"users\": users, \"page\": page})\n}",
         "// Go database with sqlx\nimport (\n\t\"github.com/jmoiron/sqlx\"\n\t_ \"github.com/lib/pq\"\n)\n\ntype User struct {\n\tID    int    `db:\"id\"`\n\tName  string `db:\"name\"`\n\tEmail string `db:\"email\"`\n}\n\nfunc GetUsers(db *sqlx.DB, limit int) ([]User, error) {\n\tvar users []User\n\terr := db.Select(&users,\n\t\t\"SELECT id,name,email FROM users ORDER BY id LIMIT $1\", limit)\n\treturn users, err\n}\n\nfunc CreateUser(db *sqlx.DB, u User) (int, error) {\n\tvar id int\n\terr := db.QueryRow(\n\t\t\"INSERT INTO users(name,email) VALUES($1,$2) RETURNING id\",\n\t\tu.Name, u.Email,\n\t).Scan(&id)\n\treturn id, err\n}",
     ]},
]

# ---------------------------------------------------------------------------
# MORE RUST — Axum web framework
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "rust", "topic": "axum", "keywords": ["axum", "tokio", "web", "handler", "rust"],
     "snippets": [
         "use axum::{\n    extract::{Path, Query, State},\n    http::StatusCode,\n    response::Json,\n    routing::{get, post},\n    Router,\n};\nuse serde::{Deserialize, Serialize};\n\n#[derive(Serialize, Deserialize)]\nstruct User { id: u32, name: String }\n\nasync fn list_users(State(db): State<DB>) -> Json<Vec<User>> {\n    Json(db.get_users().await)\n}\n\nasync fn get_user(Path(id): Path<u32>, State(db): State<DB>)\n    -> Result<Json<User>, StatusCode>\n{\n    db.find_user(id).await\n        .map(Json)\n        .ok_or(StatusCode::NOT_FOUND)\n}\n\n#[tokio::main]\nasync fn main() {\n    let app = Router::new()\n        .route(\"/api/users\",     get(list_users))\n        .route(\"/api/users/:id\", get(get_user))\n        .with_state(DB::new().await);\n    axum::Server::bind(&\"0.0.0.0:8080\".parse().unwrap())\n        .serve(app.into_make_service()).await.unwrap();\n}",
     ]},
]

# ---------------------------------------------------------------------------
# MORE JAVA — CompletableFuture, Optional
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "java", "topic": "modern_java", "keywords": ["completablefuture", "optional", "records", "sealed", "java"],
     "snippets": [
         "// Java Records (Java 16+)\npublic record User(Long id, String name, String email) {\n    // Compact constructor for validation\n    public User {\n        Objects.requireNonNull(name, \"name required\");\n        email = email.toLowerCase();\n    }\n\n    public static User of(String name, String email) {\n        return new User(null, name, email);\n    }\n}",
         "// CompletableFuture\nCompletableFuture<User> userFuture    = fetchUserAsync(1L);\nCompletableFuture<List<Order>> orders = fetchOrdersAsync(1L);\n\nCompletableFuture.allOf(userFuture, orders)\n    .thenRun(() -> {\n        User user         = userFuture.join();\n        List<Order> ords  = orders.join();\n        sendEmail(user, ords);\n    })\n    .exceptionally(ex -> { log.error(\"Failed\", ex); return null; });\n\n// Chain\nCompletableFuture<String> result = fetchUser(id)\n    .thenApply(User::getName)\n    .thenCompose(name -> fetchProfile(name))\n    .thenApply(ProfileDTO::toJson);",
         "// Optional\nOptional<User> userOpt = repo.findByEmail(email);\n\n// Transform\nString name = userOpt\n    .filter(User::isActive)\n    .map(User::getName)\n    .orElse(\"Anonymous\");\n\n// Throw if absent\nUser user = userOpt.orElseThrow(() -> new NotFoundException(email));\n\n// Side-effect if present\nuserOpt.ifPresent(u -> cache.put(u.getId(), u));\n\n// orElseGet (lazy)\nUser defaultUser = userOpt.orElseGet(() -> createDefault(email));",
     ]},
]

# ---------------------------------------------------------------------------
# PROMETHEUS / MONITORING
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "monitoring", "keywords": ["prometheus", "metrics", "grafana", "alerting", "python"],
     "snippets": [
         "from prometheus_client import Counter, Histogram, Gauge, start_http_server\nimport time\n\n# Metrics\nREQUESTS   = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])\nLATENCY    = Histogram('http_request_duration_seconds', 'Request latency', ['endpoint'],\n                        buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5])\nACTIVE_CONN = Gauge('active_connections', 'Active DB connections')\n\n# FastAPI middleware\nfrom fastapi import Request\n\nasync def metrics_middleware(request: Request, call_next):\n    start = time.time()\n    resp  = await call_next(request)\n    REQUESTS.labels(request.method, request.url.path, resp.status_code).inc()\n    LATENCY.labels(request.url.path).observe(time.time() - start)\n    return resp",
     ]},
]

# ---------------------------------------------------------------------------
# gRPC
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "grpc", "keywords": ["grpc", "protobuf", "proto", "rpc", "python"],
     "snippets": [
         "# user.proto\n# syntax = \"proto3\";\n# service UserService {\n#   rpc GetUser(GetUserRequest) returns (UserResponse);\n#   rpc ListUsers(ListUsersRequest) returns (stream UserResponse);\n# }\n# message GetUserRequest  { int32 id = 1; }\n# message UserResponse    { int32 id = 1; string name = 2; string email = 3; }\n\n# gRPC server (Python)\nimport grpc\nfrom concurrent import futures\nimport user_pb2, user_pb2_grpc\n\nclass UserServicer(user_pb2_grpc.UserServiceServicer):\n    def GetUser(self, request, context):\n        user = db.get_user(request.id)\n        if not user:\n            context.set_code(grpc.StatusCode.NOT_FOUND)\n            return user_pb2.UserResponse()\n        return user_pb2.UserResponse(id=user.id, name=user.name, email=user.email)\n\nserver = grpc.server(futures.ThreadPoolExecutor(max_workers=10))\nuser_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)\nserver.add_insecure_port('[::]:50051')\nserver.start()\nserver.wait_for_termination()",
     ]},
]

# ---------------------------------------------------------------------------
# MORE KOTLIN — Android, Ktor
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "kotlin", "topic": "ktor", "keywords": ["ktor", "routing", "serialization", "server", "kotlin"],
     "snippets": [
         "// Ktor server\nimport io.ktor.server.application.*\nimport io.ktor.server.engine.*\nimport io.ktor.server.netty.*\nimport io.ktor.server.routing.*\nimport io.ktor.server.response.*\nimport io.ktor.server.request.*\nimport io.ktor.serialization.kotlinx.json.*\n\nfun main() {\n    embeddedServer(Netty, port = 8080) {\n        install(ContentNegotiation) { json() }\n        routing {\n            get(\"/api/users\") {\n                call.respond(userService.getAll())\n            }\n            post(\"/api/users\") {\n                val user = call.receive<CreateUserRequest>()\n                val created = userService.create(user)\n                call.respond(HttpStatusCode.Created, created)\n            }\n        }\n    }.start(wait = true)\n}",
     ]},
]

# ---------------------------------------------------------------------------
# MORE BASH — Advanced patterns
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "bash", "topic": "advanced_bash", "keywords": ["heredoc", "trap", "parallel", "jq", "bash"],
     "snippets": [
         "#!/bin/bash\n# Heredoc\ncat <<'EOF' > config.yaml\nhost: localhost\nport: 8080\ndebug: false\nEOF\n\n# Process substitution\ndiff <(sort file1.txt) <(sort file2.txt)\n\n# Named pipes\nmkfifo /tmp/pipe\ncmd1 > /tmp/pipe &\ncmd2 < /tmp/pipe\n\n# xargs parallel execution\nfind . -name '*.log' | xargs -P4 -I{} gzip {}",
         "#!/bin/bash\n# jq for JSON processing\ndata=$(curl -s https://api.example.com/users)\n\n# Extract fields\necho $data | jq '.[] | {id, name}'\n\n# Filter\necho $data | jq '[.[] | select(.active == true)]'\n\n# Transform\necho $data | jq 'map({(.id | tostring): .name}) | add'\n\n# Environment-based config\nexport DB_URL=$(jq -r '.database.url' config.json)\n\n# Arrays in bash\ndeclare -A config\nconfig[host]='localhost'\nconfig[port]='5432'\necho \"${config[host]}:${config[port]}\"",
     ]},
]

# ---------------------------------------------------------------------------
# MORE DESIGN PATTERNS
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "patterns_behavioral", "keywords": ["state machine", "chain of responsibility", "mediator", "python"],
     "snippets": [
         "# State machine\nfrom enum import Enum, auto\nfrom typing import Callable\n\nclass State(Enum):\n    IDLE     = auto()\n    RUNNING  = auto()\n    PAUSED   = auto()\n    STOPPED  = auto()\n\nclass StateMachine:\n    _transitions = {\n        State.IDLE:    {State.RUNNING},\n        State.RUNNING: {State.PAUSED, State.STOPPED},\n        State.PAUSED:  {State.RUNNING, State.STOPPED},\n        State.STOPPED: set(),\n    }\n\n    def __init__(self): self.state = State.IDLE\n\n    def transition(self, new_state: State):\n        if new_state not in self._transitions[self.state]:\n            raise ValueError(f'Invalid: {self.state} → {new_state}')\n        self.state = new_state",
         "# Event sourcing pattern\nfrom dataclasses import dataclass\nfrom datetime import datetime\nfrom typing import List\n\n@dataclass\nclass Event:\n    type: str\n    data: dict\n    timestamp: datetime\n\nclass Account:\n    def __init__(self):\n        self.balance = 0\n        self._events: List[Event] = []\n\n    def apply(self, event: Event):\n        if event.type == 'deposit':    self.balance += event.data['amount']\n        elif event.type == 'withdraw': self.balance -= event.data['amount']\n        self._events.append(event)\n\n    def deposit(self, amount: float):\n        self.apply(Event('deposit', {'amount': amount}, datetime.utcnow()))\n\n    def get_events(self): return list(self._events)",
         "# Middleware pipeline (chain of responsibility)\nfrom typing import Callable, Any\n\nHandler = Callable[[dict, Callable], Any]\n\nclass Pipeline:\n    def __init__(self):\n        self._handlers: list[Handler] = []\n\n    def use(self, handler: Handler) -> 'Pipeline':\n        self._handlers.append(handler)\n        return self\n\n    def run(self, request: dict) -> Any:\n        index = 0\n        def next_handler(req):\n            nonlocal index\n            if index >= len(self._handlers):\n                return req\n            handler = self._handlers[index]\n            index += 1\n            return handler(req, next_handler)\n        return next_handler(request)",
     ]},
]

# ---------------------------------------------------------------------------
# MORE ASSEMBLY — ARM64
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "assembly", "topic": "arm64", "keywords": ["arm64", "aarch64", "register", "instruction", "assembly"],
     "snippets": [
         "// ARM64 (AArch64) overview\n// Registers: x0-x30 (64-bit), w0-w30 (32-bit), xzr (zero)\n// Calling convention (AAPCS64):\n//   args:    x0-x7   (first 8 integer/pointer args)\n//   return:  x0 (x1 for 128-bit)\n//   callee-saved: x19-x28, x29 (fp), x30 (lr)\n\n// Hello World (Linux AArch64)\n.section .data\n    msg: .ascii \"Hello, ARM!\\n\"\n    len = . - msg\n.section .text\n.global _start\n_start:\n    mov x8, #64        // sys_write\n    mov x0, #1         // stdout\n    adr x1, msg        // buffer\n    mov x2, #len       // length\n    svc #0\n    mov x8, #93        // sys_exit\n    xor x0, x0, x0\n    svc #0",
         "// ARM64 SIMD (NEON) — add two float arrays\n// x0 = dst ptr, x1 = src1 ptr, x2 = src2 ptr, x3 = count\nfloat_add:\n    cmp  x3, #4\n    b.lt .scalar\n.loop:\n    ld1  {v0.4s}, [x1], #16   // load 4 floats from src1\n    ld1  {v1.4s}, [x2], #16   // load 4 floats from src2\n    fadd v0.4s, v0.4s, v1.4s  // add element-wise\n    st1  {v0.4s}, [x0], #16   // store result\n    subs x3, x3, #4\n    b.ge .loop\n.scalar:\n    // handle remaining elements\n    ret",
     ]},
]

# ---------------------------------------------------------------------------
# SOLID PRINCIPLES
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "solid", "keywords": ["SOLID", "SRP", "OCP", "LSP", "DIP", "python"],
     "snippets": [
         "# Single Responsibility Principle (SRP)\n# Bad: one class does everything\n# Good: each class has one job\n\nclass UserValidator:\n    def validate(self, data: dict) -> list[str]:\n        errors = []\n        if not data.get('email'): errors.append('Email required')\n        if len(data.get('password','')) < 8: errors.append('Password too short')\n        return errors\n\nclass UserRepository:\n    def save(self, user: dict) -> dict: ...\n    def find_by_email(self, email: str) -> dict | None: ...\n\nclass UserService:\n    def __init__(self, repo: UserRepository, validator: UserValidator):\n        self._repo = repo\n        self._validator = validator\n    def create(self, data: dict) -> dict:\n        if errs := self._validator.validate(data):\n            raise ValueError(errs)\n        return self._repo.save(data)",
         "# Open/Closed + Dependency Inversion\nfrom abc import ABC, abstractmethod\n\nclass NotificationChannel(ABC):\n    @abstractmethod\n    def send(self, to: str, message: str) -> None: ...\n\nclass EmailChannel(NotificationChannel):\n    def send(self, to, message): print(f'Email → {to}: {message}')\n\nclass SMSChannel(NotificationChannel):\n    def send(self, to, message): print(f'SMS → {to}: {message}')\n\nclass SlackChannel(NotificationChannel):   # new channel: no change to existing code\n    def send(self, to, message): print(f'Slack → {to}: {message}')\n\nclass NotificationService:\n    def __init__(self, channel: NotificationChannel):  # inject abstraction\n        self._ch = channel\n    def notify(self, user, msg):\n        self._ch.send(user.contact, msg)",
     ]},
]

# ---------------------------------------------------------------------------
# MORE TESTING
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "advanced_testing", "keywords": ["hypothesis", "property based", "faker", "factory boy", "testing"],
     "snippets": [
         "# Hypothesis — property-based testing\nfrom hypothesis import given, strategies as st\n\n@given(st.lists(st.integers()))\ndef test_sort_idempotent(nums):\n    assert sorted(sorted(nums)) == sorted(nums)\n\n@given(st.text(min_size=1))\ndef test_encode_decode(s):\n    assert s.encode('utf-8').decode('utf-8') == s\n\n@given(\n    st.integers(min_value=1, max_value=1000),\n    st.integers(min_value=1, max_value=1000)\n)\ndef test_add_commutative(a, b):\n    assert add(a, b) == add(b, a)",
         "# pytest fixtures — database testing\nimport pytest\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker\n\n@pytest.fixture(scope='session')\ndef engine():\n    return create_engine('sqlite:///:memory:')\n\n@pytest.fixture(autouse=True)\ndef db_session(engine):\n    Base.metadata.create_all(engine)\n    Session = sessionmaker(bind=engine)\n    session = Session()\n    yield session\n    session.rollback()\n    session.close()\n    Base.metadata.drop_all(engine)\n\n@pytest.fixture\ndef user(db_session):\n    u = User(name='Alice', email='alice@test.com')\n    db_session.add(u)\n    db_session.flush()\n    return u",
         "# Mock external services\nimport pytest\nfrom unittest.mock import AsyncMock, patch\n\n@pytest.mark.asyncio\nasync def test_send_email():\n    with patch('myapp.email.smtp_client') as mock_smtp:\n        mock_smtp.send = AsyncMock(return_value={'status': 'sent'})\n        result = await send_welcome_email('alice@example.com')\n        assert result['status'] == 'sent'\n        mock_smtp.send.assert_called_once_with(\n            to='alice@example.com',\n            subject='Welcome!',\n            body=ANY\n        )",
     ]},
]

# ---------------------------------------------------------------------------
# MORE PYTHON STDLIB
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "stdlib_collections", "keywords": ["collections", "deque", "namedtuple", "defaultdict", "python"],
     "snippets": [
         "from collections import Counter, defaultdict, deque, ChainMap, OrderedDict\n\n# Counter\nwords = 'the quick brown fox jumps over the lazy dog'.split()\nword_freq = Counter(words)\nprint(word_freq.most_common(3))\nword_freq.update(['the', 'fox'])\n\n# ChainMap — layered configs\ndefaults  = {'debug': False, 'port': 8000}\nenv_cfg   = {'port': 9000}\ncfg = ChainMap(env_cfg, defaults)\nprint(cfg['port'])   # 9000 (env overrides default)",
         "from collections import deque\n\n# Sliding window max (monotonic deque)\ndef sliding_max(arr: list, k: int) -> list:\n    dq = deque()  # stores indices\n    result = []\n    for i, x in enumerate(arr):\n        while dq and arr[dq[-1]] <= x:\n            dq.pop()\n        dq.append(i)\n        if dq[0] <= i - k:\n            dq.popleft()\n        if i >= k - 1:\n            result.append(arr[dq[0]])\n    return result",
     ]},
    {"lang": "python", "topic": "stdlib_datetime", "keywords": ["datetime", "timezone", "dateutil", "arrow", "python"],
     "snippets": [
         "from datetime import datetime, timezone, timedelta, date\nimport zoneinfo\n\n# Timezone-aware datetime\nnow_utc    = datetime.now(timezone.utc)\nnow_moscow = datetime.now(zoneinfo.ZoneInfo('Europe/Moscow'))\n\n# Convert timezone\ndef to_local(dt: datetime, tz: str) -> datetime:\n    return dt.astimezone(zoneinfo.ZoneInfo(tz))\n\n# Arithmetic\ntomorrow    = date.today() + timedelta(days=1)\nnext_monday = date.today() + timedelta(days=7 - date.today().weekday())\ndiff        = datetime(2025, 1, 1) - datetime.now(timezone.utc).replace(tzinfo=None)\nprint(f'{diff.days} days until 2025')",
     ]},
    {"lang": "python", "topic": "stdlib_pathlib", "keywords": ["pathlib", "path", "glob", "walk", "python"],
     "snippets": [
         "from pathlib import Path\n\n# Path operations\nroot  = Path('/workspace/project')\npy_files = list(root.rglob('*.py'))\ntest_files = [f for f in py_files if f.stem.startswith('test_')]\n\nfor f in test_files:\n    print(f.relative_to(root))  # relative path\n    print(f.stat().st_size)     # file size\n\n# Read/write\nconfig = root / 'config' / 'settings.json'\nconfig.parent.mkdir(parents=True, exist_ok=True)\nconfig.write_text(json.dumps({'debug': False}), encoding='utf-8')\ndata = json.loads(config.read_text())\n\n# Temp files\nimport tempfile\nwith tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False) as f:\n    json.dump(data, f)\n    tmp_path = Path(f.name)",
     ]},
    {"lang": "python", "topic": "stdlib_io", "keywords": ["io", "BytesIO", "StringIO", "stream", "python"],
     "snippets": [
         "import io\nimport gzip\nimport base64\n\n# In-memory bytes operations\nbuf = io.BytesIO()\nwith gzip.GzipFile(fileobj=buf, mode='wb') as gz:\n    gz.write(b'Hello World ' * 1000)\ncompressed = buf.getvalue()\nprint(f'Compressed: {len(compressed)} bytes')\n\n# Base64 encode\nb64 = base64.b64encode(compressed).decode()\n\n# Decompress\nbuf2 = io.BytesIO(compressed)\nwith gzip.GzipFile(fileobj=buf2) as gz:\n    original = gz.read()",
     ]},
]

# ---------------------------------------------------------------------------
# HTTP CACHING / REST DESIGN
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "rest_design", "keywords": ["rest", "http", "status codes", "headers", "etag"],
     "snippets": [
         "# HTTP status codes\n# 200 OK          — successful GET, PUT, PATCH\n# 201 Created     — successful POST\n# 204 No Content  — successful DELETE\n# 400 Bad Request — invalid input\n# 401 Unauthorized — not authenticated\n# 403 Forbidden   — authenticated but no permission\n# 404 Not Found   — resource missing\n# 409 Conflict    — duplicate / state conflict\n# 422 Unprocessable Entity — validation error\n# 429 Too Many Requests — rate limited\n# 500 Internal Server Error\n# 503 Service Unavailable\n\n# REST URL conventions\n# GET    /api/users          — list\n# POST   /api/users          — create\n# GET    /api/users/{id}     — read one\n# PUT    /api/users/{id}     — full update\n# PATCH  /api/users/{id}     — partial update\n# DELETE /api/users/{id}     — delete\n# GET    /api/users/{id}/posts — nested resource",
         "# ETag caching in FastAPI\nfrom fastapi import Request, Response\nimport hashlib\nimport json\n\ndef etag_from(data) -> str:\n    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()\n\n@app.get('/api/users/{id}')\nasync def get_user(id: int, request: Request, response: Response):\n    user = await db.get_user(id)\n    if not user: raise HTTPException(404)\n    tag = etag_from(user)\n    if request.headers.get('If-None-Match') == tag:\n        return Response(status_code=304)\n    response.headers['ETag'] = tag\n    response.headers['Cache-Control'] = 'private, max-age=60'\n    return user",
     ]},
]

# ---------------------------------------------------------------------------
# PYTHON TYPING ADVANCED
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "typing_advanced", "keywords": ["TypeGuard", "ParamSpec", "Concatenate", "overload", "python"],
     "snippets": [
         "from typing import TypeGuard, overload, Union, Literal\nfrom typing import ParamSpec, TypeVar, Callable\n\n# TypeGuard\ndef is_string_list(val: list) -> TypeGuard[list[str]]:\n    return all(isinstance(x, str) for x in val)\n\n# @overload\n@overload\ndef process(x: int)   -> str: ...\n@overload\ndef process(x: str)   -> int: ...\ndef process(x: Union[int,str]) -> Union[str,int]:\n    if isinstance(x, int): return str(x)\n    return len(x)\n\n# Literal types\nMode = Literal['read', 'write', 'append']\ndef open_file(path: str, mode: Mode) -> None: ...",
         "from typing import ParamSpec, Callable, TypeVar\nfrom functools import wraps\nimport time\n\nP = ParamSpec('P')\nR = TypeVar('R')\n\ndef retry(times: int = 3, delay: float = 1.0):\n    def decorator(fn: Callable[P, R]) -> Callable[P, R]:\n        @wraps(fn)\n        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:\n            for attempt in range(times):\n                try:\n                    return fn(*args, **kwargs)\n                except Exception as e:\n                    if attempt == times - 1: raise\n                    time.sleep(delay * (attempt + 1))\n        return wrapper\n    return decorator",
     ]},
]

# ---------------------------------------------------------------------------
# OPENAPI / SWAGGER
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "yaml", "topic": "openapi", "keywords": ["openapi", "swagger", "api spec", "schema", "yaml"],
     "snippets": [
         "# OpenAPI 3.1 specification\nopenapi: 3.1.0\ninfo:\n  title: My API\n  version: 1.0.0\n  description: REST API\n\npaths:\n  /api/users:\n    get:\n      summary: List users\n      parameters:\n        - name: page\n          in: query\n          schema: { type: integer, default: 1 }\n      responses:\n        '200':\n          content:\n            application/json:\n              schema:\n                type: array\n                items: { $ref: '#/components/schemas/User' }\n    post:\n      requestBody:\n        required: true\n        content:\n          application/json:\n            schema: { $ref: '#/components/schemas/CreateUser' }\n\ncomponents:\n  schemas:\n    User:\n      type: object\n      properties:\n        id:    { type: integer }\n        name:  { type: string }\n        email: { type: string, format: email }\n      required: [id, name, email]",
     ]},
]

# ---------------------------------------------------------------------------
# WEBSOCKET ADVANCED
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "websocket_server", "keywords": ["websockets", "broadcast", "room", "chat", "python"],
     "snippets": [
         "import asyncio\nimport json\nfrom fastapi import FastAPI, WebSocket, WebSocketDisconnect\nfrom typing import DefaultDict\nfrom collections import defaultdict\n\napp = FastAPI()\n\nclass ConnectionManager:\n    def __init__(self):\n        self._rooms: DefaultDict[str, set[WebSocket]] = defaultdict(set)\n\n    async def join(self, ws: WebSocket, room: str):\n        await ws.accept()\n        self._rooms[room].add(ws)\n\n    def leave(self, ws: WebSocket, room: str):\n        self._rooms[room].discard(ws)\n\n    async def broadcast(self, room: str, data: dict, exclude: WebSocket = None):\n        dead = set()\n        for ws in self._rooms[room]:\n            if ws is exclude: continue\n            try: await ws.send_json(data)\n            except: dead.add(ws)\n        self._rooms[room] -= dead\n\nmgr = ConnectionManager()\n\n@app.websocket('/ws/{room}')\nasync def ws(websocket: WebSocket, room: str):\n    await mgr.join(websocket, room)\n    try:\n        while True:\n            msg = await websocket.receive_json()\n            await mgr.broadcast(room, msg, exclude=websocket)\n    except WebSocketDisconnect:\n        mgr.leave(websocket, room)",
     ]},
]

# ---------------------------------------------------------------------------
# PYTHON DECORATORS ADVANCED
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "python", "topic": "decorators_advanced", "keywords": ["decorator", "class decorator", "parametrised", "stacking", "python"],
     "snippets": [
         "import functools\nfrom typing import Callable, TypeVar\n\nF = TypeVar('F', bound=Callable)\n\n# Decorator with optional arguments\ndef cached(fn=None, *, maxsize=128):\n    if fn is None:\n        return lambda f: cached(f, maxsize=maxsize)\n    memo = {}\n    @functools.wraps(fn)\n    def wrapper(*args):\n        if args not in memo:\n            if len(memo) >= maxsize:\n                memo.pop(next(iter(memo)))\n            memo[args] = fn(*args)\n        return memo[args]\n    wrapper.cache_clear = memo.clear\n    return wrapper\n\n@cached\ndef fib(n): return n if n < 2 else fib(n-1)+fib(n-2)\n\n@cached(maxsize=256)\ndef heavy(x, y): ...",
         "# Class-based decorator\nclass Retry:\n    def __init__(self, times=3, exceptions=(Exception,)):\n        self.times = times\n        self.exceptions = exceptions\n\n    def __call__(self, fn):\n        @functools.wraps(fn)\n        def wrapper(*args, **kwargs):\n            for i in range(self.times):\n                try: return fn(*args, **kwargs)\n                except self.exceptions:\n                    if i == self.times - 1: raise\n        return wrapper\n\n@Retry(times=5, exceptions=(ConnectionError, TimeoutError))\ndef call_api(): ...",
     ]},
]

# ---------------------------------------------------------------------------
# MORE LINUX / SYSADMIN
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "bash", "topic": "systemd", "keywords": ["systemd", "service", "unit", "journald", "linux"],
     "snippets": [
         "# systemd service unit file\n# /etc/systemd/system/myapp.service\n[Unit]\nDescription=My Python Application\nAfter=network.target postgresql.service\nRequires=postgresql.service\n\n[Service]\nType=exec\nUser=appuser\nWorkingDirectory=/opt/myapp\nExecStart=/opt/myapp/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000\nRestart=on-failure\nRestartSec=5\nEnvironmentFile=/opt/myapp/.env\n\n# Security hardening\nNoNewPrivileges=true\nPrivateTmp=true\nProtectSystem=strict\nReadWritePaths=/opt/myapp/data\n\n[Install]\nWantedBy=multi-user.target\n\n# Commands:\n# systemctl daemon-reload\n# systemctl enable --now myapp\n# journalctl -u myapp -f",
     ]},
]

# ---------------------------------------------------------------------------
# ZERO-DOWNTIME DEPLOYMENT PATTERNS
# ---------------------------------------------------------------------------
KNOWLEDGE += [
    {"lang": "yaml", "topic": "deployment_patterns", "keywords": ["blue green", "canary", "rolling update", "deployment", "kubernetes"],
     "snippets": [
         "# Kubernetes Rolling Update (zero downtime)\napiVersion: apps/v1\nkind: Deployment\nmetadata: { name: api }\nspec:\n  replicas: 3\n  strategy:\n    type: RollingUpdate\n    rollingUpdate:\n      maxUnavailable: 0    # never have less than 3 pods\n      maxSurge: 1          # allow 4 pods during update\n  template:\n    spec:\n      containers:\n        - name: api\n          image: myapp:v2\n          readinessProbe:\n            httpGet: { path: /health, port: 8000 }\n            initialDelaySeconds: 10\n            periodSeconds: 5\n          lifecycle:\n            preStop:\n              exec:\n                command: [\"sleep\", \"10\"]  # drain connections",
     ]},
]

# ---------------------------------------------------------------------------
# GENERATE CELLS
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    main()
