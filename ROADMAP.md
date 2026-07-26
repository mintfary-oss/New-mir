# ROADMAP — New-mir Neural Network Development Plan

> **Цель проекта:** Создать лёгкую, умную нейросеть, которая работает
> на любом компьютере, понимает все языки и не требует мощного оборудования.
> Будущее — за доступными технологиями.

---

## ТЕКУЩЕЕ СОСТОЯНИЕ (v2.3 — актуальное)

### Что есть сейчас
- Transformer decoder на чистом NumPy (без PyTorch/TensorFlow)
- ~5.3M параметров (embed_dim=256, 4 слоя, ff_dim=1024, max_seq=1024)
- ByteTokenizer — все языки через UTF-8 байты (vocab=258)
- AdamOptimizer с gradient clipping (max_grad_norm=5.0)
- Полный backprop: 100% весов (Attention + SwiGLU FF + tok_emb)
- **RoPE** позиционное кодирование (нет обучаемых pos_emb)
- **SwiGLU** активация в FF слоях (GELU заменён)
- **Weight tying**: lm_head = tok_emb.T
- Honeycomb-память для хранения весов
- Система seed-файлов для автообучения при старте
- Seed-данные: 15 файлов, ~79KB русских данных
- Docker-контейнер, веб-интерфейс

### Открытые проблемы
| Проблема | Причина | Критичность |
|---|---|---|
| Мало русских данных | 79KB из желаемых 200KB+ | СРЕДНЯЯ |
| Нет KV-cache | Каждый токен пересчитывает историю | СРЕДНЯЯ |
| Позиционные embedding обучаемые | RoPE лучше для длинных цепочек | НИЗКАЯ |

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

## ФАЗА 2: КАЧЕСТВО ОБУЧЕНИЯ (v2.1 / v2.2) — ЗАВЕРШЕНА ✓

**Статус:** ✅ Полностью реализовано в PR #14 (v2.1) и PR #15 (v2.2)
**Цель была:** Модель должна генерировать осмысленные ответы на русском

### 2.1 Полный backpropagation ✅
Все веса обновляются:

```
1. lm_head           ✅ v1.x
2. tok_emb           ✅ v2.0
3. ff_w1/b1/w2/b2    ✅ v2.1 — через _forward_and_cache + GELU backward
4. attn_wq/k/v/o     ✅ v2.2 — через _backward_attn_layer
```

### 2.2 Adam optimizer ✅
Реализован `class AdamOptimizer` в `neural_core.py`:
- Адаптивная скорость обучения (β₁=0.9, β₂=0.999)
- Bias correction в первых шагах
- Применяется ко всем параметрам (FF + Attention + lm_head + tok_emb)

### 2.3 Расширение обучающих данных на русском — частично ✅
- [x] `russian_language.md` — 18KB: диалоги, грамматика, техвокабуляр (v2.0)
- [x] `russian_extended.md` — 61KB: культура, наука, технологии, мотивация (v2.2)
- [ ] Wikipedia на русском (первые 1000 статей, краткие)
- [ ] Параллельные тексты RU-EN для понимания переводов
- [ ] Диалоги: вопрос-ответ пары на русском

Итого: 79KB из желаемых 200KB+. Продолжать в Фазе 3.

### 2.4 Gradient clipping ✅
Реализован в `AdamOptimizer.update()`:
```python
# max_grad_norm=5.0 — отсекает взрывной рост градиентов
grad_norm = np.sqrt(sum(np.sum(g**2) for g in all_grads))
if grad_norm > max_grad_norm:
    scale = max_grad_norm / (grad_norm + 1e-8)
    grads = {k: v * scale for k, v in grads.items()}
```

---

## ФАЗА 3: АРХИТЕКТУРА (v2.3) — ЗАВЕРШЕНА ✓

**Статус:** ✅ Реализовано в текущем PR
**Цель была:** Архитектурные улучшения без роста требований к железу

### 3.1 RoPE позиционное кодирование ✅
Заменены обучаемые позиционные embedding на Rotary Position Embedding (RoPE).

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
[ ] Отложено на Фазу 5 (требует KV-cache для полной пользы).

### 3.3 SwiGLU активация ✅
Реализовано: `FFN(x) = (SiLU(x@w1+b1) ⊙ x@w3) @ w2 + b2`
Добавлен `ff_w3` (D×FF) в `TransformerWeights`. Полный backward через d_gate/d_up/d_w3.

### 3.4 Weight tying ✅
Реализовано: `logits = hidden @ weights.tok_emb.T`
Нет отдельной матрицы `lm_head`. Экономия ~660K параметров.
Backward: `grad_lm.T` накапливается в `tok_emb`.

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
| v2.0 | 6M | 24 MB | все (байты) | базовый |
| v2.1 | 6M | 24 MB | все | лучше (Adam + FF backprop) |
| v2.2 | 6M | 24 MB | все | заметно лучше (100% backprop) |
| **v2.3 (сейчас)** | **5.3M** | **22 MB** | **все** | **лучше (RoPE+SwiGLU+WTying)** |
| v2.5 | 5.3M | 22 MB | все | приемлемый |
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
| v2.0 | 2026-07 | ByteTokenizer, 6M params, tok_emb training, Russian seed data |
| v2.1 | 2026-07 | AdamOptimizer, FF backprop (GELU grad), MAX_FINE_TUNE_CHARS 32KB, 5 эпох |
| v2.2 | 2026-07 | Attention backprop (Q/K/V/O), gradient clipping, russian_extended.md 61KB |
| **v2.3** | **2026-07** | **RoPE, SwiGLU+ff_w3, Weight tying (lm_head=tok_emb.T), −10% параметров** |

---

*Документ обновляется с каждым релизом.*
*Последнее обновление: июль 2026*
