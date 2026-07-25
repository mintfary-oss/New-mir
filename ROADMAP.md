# ROADMAP — New-mir Neural Network Development Plan

> **Цель проекта:** Создать лёгкую, умную нейросеть, которая работает
> на любом компьютере, понимает все языки и не требует мощного оборудования.
> Будущее — за доступными технологиями.

---

## ТЕКУЩЕЕ СОСТОЯНИЕ (v1.x — baseline)

### Что есть сейчас
- Transformer decoder на чистом NumPy (без PyTorch/TensorFlow)
- ~145K параметров (embed_dim=64, 2 слоя, ff_dim=256)
- ASCII-only токенизатор (96 символов)
- Honeycomb-память для хранения весов
- Система seed-файлов для автообучения при старте
- Docker-контейнер, веб-интерфейс
- Seed-данные: Python, Rust, Pulumi, Kimi-K2, OpenAI Cookbook,
  TypeScript, Awesome-Python, Rust Book

### Известные проблемы
| Проблема | Причина | Критичность |
|---|---|---|
| Не понимает русский | ASCII токенизатор, кириллица → `???` | КРИТИЧНО |
| Слабые ответы | Только 145K параметров, 2 слоя | ВЫСОКАЯ |
| Обучается только lm_head | Нет backprop через embedding | ВЫСОКАЯ |
| max_seq=512 токенов | Ограниченный контекст | СРЕДНЯЯ |

---

## ФАЗА 1: ФУНДАМЕНТ (v2.0) — в работе

**Срок:** текущий спринт
**Статус:** 🔄 В процессе

### 1.1 Байтовый токенизатор [ГОТОВО]
- [x] Добавить `ByteTokenizer` (vocab=258: 256 байт + PAD + UNK)
- [x] Русский, китайский, арабский, японский — работают автоматически
- [x] Backward compatibility: `CharTokenizer` остаётся для старых весов
- [x] Auto-detect токенизатора при загрузке весов (vocab_size ≤ 98 → old)

### 1.2 Увеличение модели [ГОТОВО]
- [x] embed_dim: 64 → 256 (4x)
- [x] num_heads: 4 → 8 (2x)
- [x] num_layers: 2 → 4 (2x глубже)
- [x] ff_dim: 256 → 1024 (4x)
- [x] max_seq: 512 → 1024 (2x контекст)
- [x] Итого: ~6M параметров, ~24MB RAM — запускается на любом ноутбуке

### 1.3 Обучение embedding слоя [ГОТОВО]
- [x] Добавить gradient step для `tok_emb` в `fine_tune_on_examples`
- [x] `d_hidden = probs @ lm_head.T` → обновляет embedding для каждого токена
- [x] Результат: модель действительно учится на русских текстах

### 1.4 Русские обучающие данные [ГОТОВО]
- [x] `russian_language.md`: 18KB комплексных данных
  - Разговорный язык, диалоги, грамматика
  - Технический словарь (нейросети, программирование)
  - Русская литература, цитаты
  - Вопросы и ответы по AI/ML на русском
  - Примеры кода с русскими комментариями

---

## ФАЗА 2: КАЧЕСТВО ОБУЧЕНИЯ (v2.1)

**Срок:** следующий спринт
**Цель:** Модель должна генерировать осмысленные ответы на русском

### 2.1 Полный backpropagation
Сейчас обновляются только `lm_head` и `tok_emb`.
Нужно: обновлять все веса через все слои.

```
Приоритет обновления весов (от самого важного):
1. lm_head       ← уже реализовано
2. tok_emb       ← уже реализовано (v2.0)
3. ff_w1, ff_w2  ← следующий шаг
4. attn_wq/k/v/o ← после FF layers
5. ln1_g/b, ln2_g/b ← последними
```

Реализация: добавить `_backward()` функцию в `neural_core.py` с
полным BPTT (Backpropagation Through Time) через все Transformer блоки.

### 2.2 Adam optimizer
Заменить SGD на Adam для более стабильного обучения:

```python
# Вместо: w.lm_head -= lr * grad
# Использовать Adam:
m = beta1 * m + (1 - beta1) * grad      # moment 1
v = beta2 * v + (1 - beta2) * grad**2   # moment 2
w -= lr * m / (sqrt(v) + eps)           # adaptive step
```

Преимущества Adam:
- Адаптивная скорость обучения для каждого параметра
- Устойчив к шуму в градиентах
- Быстрее сходится на практике

### 2.3 Расширение обучающих данных на русском
- [ ] Wikipedia на русском (первые 1000 статей, краткие)
- [ ] Русские технические тексты (документация, туториалы)
- [ ] Параллельные тексты RU-EN для понимания переводов
- [ ] Диалоги: вопрос-ответ пары на русском

Цель: ≥200KB качественного русского текста в seed.

### 2.4 Gradient clipping
Предотвращает "взрыв градиентов" при обучении:

```python
grad_norm = np.sqrt(sum(np.sum(g**2) for g in grads))
if grad_norm > max_norm:
    for g in grads:
        g *= max_norm / grad_norm
```

---

## ФАЗА 3: АРХИТЕКТУРА (v2.5)

**Срок:** 2-3 спринта
**Цель:** Архитектурные улучшения без роста требований к железу

### 3.1 RoPE позиционное кодирование
Заменить обучаемые позиционные embedding на Rotary Position Embedding (RoPE).

Преимущества:
- Лучше обобщается на длинные последовательности
- Используется в LLaMA, Mistral, Qwen
- Не требует дополнительных параметров
- Позволяет экстраполировать за пределы max_seq

```python
def _rope(x: np.ndarray, seq_pos: np.ndarray) -> np.ndarray:
    """Apply Rotary Position Embedding."""
    d = x.shape[-1]
    theta = 1.0 / (10000 ** (np.arange(0, d, 2) / d))
    angles = seq_pos[:, None] * theta[None, :]
    cos = np.cos(angles)
    sin = np.sin(angles)
    x1, x2 = x[..., ::2], x[..., 1::2]
    return np.stack([x1*cos - x2*sin, x1*sin + x2*cos], axis=-1).reshape(x.shape)
```

### 3.2 Grouped Query Attention (GQA)
Уменьшает память и вычисления при сохранении качества.
Используется в LLaMA 3, Mistral, Gemma.

```
Стандартное внимание:  Q heads = K heads = V heads = 8
GQA (groups=2):        Q heads = 8, K/V heads = 2
Экономия памяти: 4x для KV-cache
```

### 3.3 SwiGLU активация
Заменить GELU на SwiGLU в feed-forward слоях:

```python
def _swiglu(x, w1, w2, w3):
    """SwiGLU: лучше GELU, используется в LLaMA."""
    return (x @ w1) * sigmoid(x @ w3) @ w2
```

Показывает лучшее качество по сравнению с GELU при тех же параметрах.

### 3.4 Weight tying
Связать веса `tok_emb` и `lm_head` (стандартная техника):

```python
# lm_head использует транспонированные embedding веса
logits = hidden @ self.weights.tok_emb.T  # вместо @ lm_head
```

Преимущества: -10% параметров, лучшая согласованность input/output.

---

## ФАЗА 4: МНОГОЯЗЫЧНОСТЬ (v3.0)

**Срок:** 4-6 спринтов
**Цель:** Уверенная работа на RU, EN, ZH, DE, FR, ES

### 4.1 Многоязычные обучающие данные
Seed-файлы для каждого языка:

| Язык | Планируемый файл | Размер |
|---|---|---|
| Русский | russian_language.md | 18KB ✓ |
| Английский | english_language.md | 30KB |
| Немецкий | german_basics.md | 20KB |
| Французский | french_basics.md | 20KB |
| Китайский | chinese_basics.md | 25KB |
| Испанский | spanish_basics.md | 20KB |
| Японский | japanese_basics.md | 20KB |
| Арабский | arabic_basics.md | 20KB |

### 4.2 Языковая идентификация
Автоматически определять язык запроса и настраивать генерацию:

```python
def detect_language(text: str) -> str:
    """Определить язык текста по byte-распределению."""
    bytes_ = text.encode("utf-8")
    cyrillic = sum(1 for b in bytes_ if 0xD0 <= b <= 0xD1)
    cjk = sum(1 for b in bytes_ if 0xE4 <= b <= 0xE9)
    if cyrillic / len(bytes_) > 0.3: return "ru"
    if cjk / len(bytes_) > 0.3: return "zh"
    return "en"
```

### 4.3 Language-aware generation
Использовать язык запроса для настройки temperature и stop sequences:

```python
LANGUAGE_CONFIGS = {
    "ru": {"temperature": 0.85, "stop": ["---", "Конец"]},
    "en": {"temperature": 0.80, "stop": ["---", "End."]},
    "zh": {"temperature": 0.90, "stop": ["---", "结束"]},
}
```

---

## ФАЗА 5: ПРОИЗВОДИТЕЛЬНОСТЬ (v3.5)

**Срок:** параллельно с фазой 4
**Цель:** В 10x быстрее при том же качестве

### 5.1 KV-cache
Кэшировать key/value матрицы внимания между токенами.
Даёт 2-5x ускорение инференса:

```
Без кэша:  каждый новый токен пересчитывает всю историю
С кэшем:   только новый токен вычисляет attention с кэшированными KV
```

### 5.2 Квантизация INT8
Перевести веса с float32 на int8:

```python
def quantize_int8(weights: np.ndarray) -> tuple[np.ndarray, float]:
    """Квантизовать веса до INT8, возвращает (quantized, scale)."""
    scale = weights.abs().max() / 127.0
    return (weights / scale).astype(np.int8), scale
```

Результат: в 4x меньше памяти (24MB → 6MB), 2x быстрее на CPU.

### 5.3 Vectorized inference
Использовать einsum и np.tensordot для батч-обработки:

```python
# Вместо цикла по слоям — векторизованный forward pass
logits = np.einsum('td,dv->tv', hidden, lm_head)
```

### 5.4 Опциональный Numba JIT
Для пользователей с Numba — автоматическое JIT-компилирование:

```python
try:
    from numba import njit
    _forward_jit = njit(_forward)
except ImportError:
    _forward_jit = _forward  # fallback на NumPy
```

---

## ФАЗА 6: СПЕЦИАЛИЗАЦИЯ (v4.0)

**Срок:** долгосрочная
**Цель:** Специализированные возможности

### 6.1 Instruction tuning
Обучить модель следовать инструкциям в формате:
```
<|system|> Ты — умный помощник New-mir.
<|user|> Как установить Python?
<|assistant|> ...
```

### 6.2 RAG (Retrieval Augmented Generation)
Поиск по Honeycomb-памяти и добавление контекста в запрос:

```
1. Запрос пользователя → embedding
2. Поиск похожих текстов в памяти (cosine similarity)
3. Добавить найденный контекст в промпт
4. Генерация с учётом реального контекста
```

### 6.3 Tool calling
Возможность вызывать внешние инструменты:

```python
TOOLS = {
    "calculator": lambda expr: eval(expr),
    "search_memory": lambda q: memory.search(q),
    "get_time": lambda: datetime.now().isoformat(),
}
```

### 6.4 Streaming improvements
Улучшить потоковую генерацию: меньше latency первого токена.

---

## ЦЕЛЕВЫЕ МЕТРИКИ

| Версия | Параметры | RAM | Языки | Качество (subjective) |
|---|---|---|---|---|
| v1.x (было) | 145K | 8 MB | EN only | очень слабый |
| **v2.0 (сейчас)** | **6M** | **24 MB** | **все (байты)** | **базовый** |
| v2.5 | 6M | 24 MB | все | приемлемый |
| v3.0 | 15M | 60 MB | RU/EN/ZH++ | хороший |
| v4.0 | 30M | 120 MB | все | очень хороший |

**Принцип:** Никогда не превышать 512MB RAM. Работает на любом компьютере.

---

## ПРИНЦИПЫ РАЗРАБОТКИ

1. **Лёгкость** — модель должна запускаться на компьютере с 1GB RAM
2. **Универсальность** — поддержка всех языков через байтовый токенизатор
3. **Открытость** — весь код на GitHub, понятный и документированный
4. **Постепенность** — каждая фаза улучшает модель без поломки предыдущего
5. **Честность** — не обещаем невозможного, чётко описываем ограничения
6. **Pure Python** — только NumPy, без PyTorch/TensorFlow (опционально)

---

## ИЗВЕСТНЫЕ ОГРАНИЧЕНИЯ

Некоторые вещи **не планируются** для New-mir:
- Параметры > 1 миллиарда (требует GPU)
- Обучение с нуля на больших корпусах (нужен датацентр)
- Замена больших коммерческих моделей (GPT-4, Claude) — не цель
- Выполнение задач, требующих глубокого рассуждения (пока)

New-mir — это **эффективная, честная, работающая на любом железе** модель.
Не замена GPT-4. Альтернатива для тех, у кого нет мощного компьютера.

---

## ИСТОРИЯ ВЕРСИЙ

| Версия | Дата | Изменения |
|---|---|---|
| v1.0 | 2026-07 | Базовая архитектура, ASCII токенизатор |
| v1.1 | 2026-07 | Per-file seed tracking, исправление gradient shape |
| v1.2 | 2026-07 | Kimi-K2 seed data (MoE, deployment, tool-calls) |
| v1.3 | 2026-07 | OpenAI Cookbook, Awesome-Python, Rust Book, Pulumi Examples, TypeScript Handbook |
| **v2.0** | **2026-07** | **ByteTokenizer, 6M params, tok_emb training, Russian seed data** |

---

*Документ обновляется с каждым релизом.*
*Последнее обновление: июль 2026*
