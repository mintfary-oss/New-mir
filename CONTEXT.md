# CONTEXT — История проекта New-mir
# Project History & Conversation Log
#
# Этот файл создан для сохранения контекста разработки.
# В случае потери данных или смены исполнителя — читай этот файл первым.
# This file preserves development context for continuity across sessions.

---

## СУТЬ ПРОЕКТА

New-mir — лёгкая нейросеть-помощник, которая:
- Работает на **любом компьютере** (от 1GB RAM)
- Понимает **все языки** (байтовый токенизатор)
- Весит **мало** (24MB в v2.0)
- Написана на **чистом Python + NumPy** (без PyTorch/TensorFlow)
- Развёртывается через **Docker** одной командой

**Философия:** Будущее за доступными технологиями. Люди не должны покупать
мощный компьютер чтобы пользоваться нейросетью.

---

## РЕПОЗИТОРИЙ

- GitHub: https://github.com/mintfary-oss/New-mir
- Основная ветка: `main`
- Docker: `docker compose up -d --build`
- Логи: `docker logs -f new-mir`

---

## АРХИТЕКТУРА (v2.0)

### Файловая структура
```
New-mir/
├── core/
│   ├── neural_core.py      ← главный файл: трансформер, токенизатор, обучение
│   ├── chat_engine.py      ← управление диалогами, SSE-стриминг
│   ├── seed_trainer.py     ← автообучение на seed-файлах при старте
│   ├── trainer.py          ← HoneycombTrainer: обучение на загружаемых файлах
│   ├── cell_memory.py      ← Honeycomb-память (SHA-256 cells)
│   ├── binary_engine.py    ← бинарное сжатие данных
│   ├── qr_encoder.py       ← QR-кодирование данных
│   └── gpt2_backend.py     ← опциональный GPT-2 backend через HuggingFace
├── api/
│   ├── main.py             ← FastAPI приложение
│   └── converters.py       ← конверторы форматов
├── web/templates/
│   └── index.html          ← веб-интерфейс
├── data/
│   ├── seed/               ← seed-файлы для автообучения
│   └── training_stats.json ← трекинг обученных файлов (per-file)
├── ROADMAP.md              ← план развития (читай это!)
├── CONTEXT.md              ← этот файл
├── Dockerfile
└── docker-compose.yml
```

### Модель (NeuralCodeGen в neural_core.py)

**v2.0 гиперпараметры:**
```python
DEFAULT_EMBED_DIM = 256   # было: 64
DEFAULT_NUM_HEADS = 8     # было: 4
DEFAULT_NUM_LAYERS = 4    # было: 2
DEFAULT_FF_DIM = 1024     # было: 256
DEFAULT_MAX_SEQ = 1024    # было: 512
# Итого: ~6M параметров, ~24MB RAM
```

**Архитектура:**
```
ByteTokenizer (UTF-8 bytes, vocab=258)
    ↓
Token Embedding (258 × 256) + Positional Embedding (1024 × 256)
    ↓
4 × TransformerBlock:
    ├── Pre-norm Multi-Head Self-Attention (8 heads, causal mask)
    └── Pre-norm Feed-Forward (GELU, 256→1024→256)
    ↓
LayerNorm → Linear (256 × 258) → Softmax
```

---

## ТОКЕНИЗАТОР — КЛЮЧЕВОЕ ИЗМЕНЕНИЕ v2.0

### Проблема (v1.x)
`CharTokenizer` использовал только 96 ASCII символов.
Все кириллические буквы → `UNK_ID = 1` → `"?"`.

Результат: когда пользователь писал "Привет" — модель видела `??????`.
Обучение на русских текстах не давало результата.

### Решение (v2.0)
`ByteTokenizer` — байтовый токенизатор (как в GPT-2):

```python
class ByteTokenizer:
    # vocab_size = 258 (256 байт + PAD + UNK)

    def encode(self, text: str) -> list[int]:
        return list(text.encode("utf-8", errors="replace"))
        # "Привет" → [208,159,209,128,208,184,208,178,208,181,209,130]

    def decode(self, ids: list[int]) -> str:
        raw = bytes(b for b in ids if 0 <= b <= 255)
        return raw.decode("utf-8", errors="replace")
```

Любой язык работает автоматически — русский, китайский, арабский, японский.

### Backward compatibility
- Старые веса (vocab_size ≤ 98) автоматически определяются при загрузке
- `load_from_file()` и `load_from_memory()` переключаются на `CharTokenizer`
- Новые веса инициализируются с `ByteTokenizer` (vocab_size=258)

---

## ОБУЧЕНИЕ — УЛУЧШЕНИЯ v2.0

### Что было (v1.x)
```python
# Обновлялся только lm_head (выходной слой)
grad_lm = hidden.T @ probs
w.lm_head -= learning_rate * grad_lm
```

### Что стало (v2.0)
```python
# Обновляется lm_head И tok_emb (входные embedding)
grad_lm = hidden.T @ probs
w.lm_head -= learning_rate * grad_lm

# Новое: gradient для embedding слоя
d_hidden = probs @ w.lm_head.T      # (T-1, embed_dim)
emb_lr = learning_rate * 0.5
for t_idx, tok_id in enumerate(ids[:-1]):
    if 0 <= tok_id < w.vocab_size:
        w.tok_emb[tok_id] -= emb_lr * d_hidden[t_idx]
```

**Почему это важно:** Без обновления `tok_emb` байтовые embedding для
кириллических символов оставались бы случайными значениями даже после
длительного обучения. Теперь модель действительно учится представлять
русские буквы в пространстве embedding.

---

## SEED-ФАЙЛЫ (обучающие данные)

Файлы в `data/seed/` — модель обучается на них автоматически при каждом
`docker compose up --build` если файл ещё не был обучен.

Трекинг в `data/training_stats.json`:
```json
{
  "seed_trained_files": ["russian_intro.txt", "kimi_k2_readme.md", ...],
  "seed_loaded": true
}
```

### Текущий список seed-файлов

| Файл | Размер | PR | Содержание |
|---|---|---|---|
| russian_intro.txt | 3.6KB | v1.0 | Базовое введение на русском |
| multilingual.txt | 4.0KB | v1.0 | Многоязычный текст |
| python_examples.py | 3.6KB | v1.0 | Примеры кода Python |
| rust_basics.rs | 2.8KB | v1.0 | Основы Rust |
| pulumi_capabilities.txt | 16KB | v1.0 | Описание Pulumi |
| kimi_k2_readme.md | 27KB | #7 | Kimi-K2 архитектура MoE |
| kimi_k2_deploy.md | 8.7KB | #7 | Деплой Kimi-K2 |
| kimi_k2_tools.md | 10KB | #7 | Tool calling Kimi-K2 |
| openai_cookbook.md | 69KB | #8 | Промптинг, reliability, LLM |
| awesome_python.md | 83KB | #9 | 100+ Python библиотек |
| rust_book.md | 142KB | #10 | Rust book ch1,3,4 |
| pulumi_examples.md | 65KB | #11 | IaC примеры Python |
| typescript_handbook.md | 163KB | #12 | TypeScript документация |
| **russian_language.md** | **18KB** | **v2.0** | **Русский язык, диалоги, грамматика** |

### Как добавить новый seed-файл
1. Положить файл в `data/seed/`
2. Добавить имя в `SEED_FILES` список в `core/seed_trainer.py`
3. При следующем рестарте контейнера обучение произойдёт автоматически

---

## ИСТОРИЯ ИЗМЕНЕНИЙ (PR лог)

### PR #1-6 (до Kimi-K2)
- Базовая архитектура NeuralCodeGen
- Docker контейнер, веб-интерфейс
- Per-file seed tracking (вместо одного флага)
- Исправление gradient shape bug (vocab_size × T ≠ embed_dim × vocab_size)
- Hardware analysis tab
- Исправление дублирования обучения при нескольких воркерах (fcntl lock)

### PR #7 — Kimi-K2 docs
Источник: https://github.com/MoonshotAI/Kimi-K2
- `kimi_k2_readme.md` — архитектура MoE, 1T параметров
- `kimi_k2_deploy.md` — деплой vLLM/SGLang/Docker
- `kimi_k2_tools.md` — function calling, агентские workflow

### PR #8 — OpenAI Cookbook
Источник: https://github.com/openai/openai-cookbook
- Промптинг: zero-shot, few-shot, chain-of-thought
- Техники улучшения надёжности
- Работа с большими документами, embeddings

### PR #9 — Awesome Python
Источник: https://github.com/vinta/awesome-python
- 100+ категорий Python библиотек и фреймворков
- Web, Data Science, ML, CLI, DevOps, Security

### PR #10 — Rust Book
Источник: https://github.com/rust-lang/book
- Главы: intro, getting started, variables/types, ownership/borrowing
- Уникальная концепция ownership и borrowing

### PR #11 — Pulumi Examples
Источник: https://github.com/pulumi/examples
- Python примеры: s3-folder, fargate, eks, serverless, resources
- IaC паттерны для AWS

### PR #12 — TypeScript Handbook
Источник: https://github.com/microsoft/TypeScript-Handbook
(microsoft/TypeScript-Node-Starter не существует — заменён)
- Basic Types, Interfaces, Classes, Functions, Generics
- Enums, Modules, Decorators, React + TypeScript

### v2.0 (PR #13)
Источник: диагностика и рефакторинг кодовой базы
- **ByteTokenizer** — поддержка всех языков через UTF-8 байты
- **Увеличение модели**: 145K → 6M параметров
- **Обучение tok_emb** — теперь embedding слой тоже обучается
- **russian_language.md** — комплексные данные на русском (18KB)
- **ROADMAP.md** — подробный план развития до v4.0
- **CONTEXT.md** — этот файл

### v2.1 (PR #14) — Adam + FF backprop + 20× данных
- **AdamOptimizer** — адаптивный оптимизатор (Kingma & Ba 2015)
- **FF backprop**: ff_w1/b1/w2/b2 обновляются через _forward_and_cache
- **_gelu_derivative**: аналитический градиент GELU
- MAX_FINE_TUNE_CHARS: 8192 → 32768 (4×)
- FINE_TUNE_EPOCHS: 1 → 5 (5×) = итого 20× больше обучения
- Параметров обучается: 2% → 52%

### v2.2 (PR #15)
- **Полный attention backprop**: Q, K, V, O веса через softmax backward
- **Gradient clipping** в Adam (max_grad_norm=5.0) — стабильное обучение
- **_forward_and_cache** расширен: сохраняет q_h, k_h, v_h, attn, ctx
- **_backward_attn_layer**: полная математически корректная backward через MHA
- Параметров обучается: 52% → **100%** от всех 6M
- **russian_extended.md** — 48KB новых русских текстов (12 разделов)
- Итого русских данных: 79KB (31KB + 48KB)

### v2.3 (текущий PR) — Фаза 3: архитектурные улучшения
- **RoPE** (Rotary Position Embedding): заменяет обучаемые `pos_emb`.
  Позиция кодируется вращением Q/K. Нет новых параметров. Backward через
  обратное вращение: `_rope_rotate(d, cos, -sin)`.
- **SwiGLU**: заменяет GELU в FF слоях.
  `FFN(x) = (SiLU(x@w1+b1) ⊙ x@w3) @ w2 + b2`
  Добавлен `ff_w3` (D×FF) на каждый слой. Полный backward (d_gate, d_up, d_w3).
- **Weight tying**: `lm_head = tok_emb.T` — нет отдельной матрицы.
  Экономия ~660K параметров. Input/output embedding пространства совпадают.
- Параметров: 6M → ~5.3M (−10%)

---

## КЛЮЧЕВЫЕ ТЕХНИЧЕСКИЕ РЕШЕНИЯ

### Почему NumPy, а не PyTorch?
Цель — работа на любом компьютере. PyTorch требует ~500MB только на установку.
NumPy входит в стандартные дистрибутивы и весит 20MB.

### Почему байтовый токенизатор?
Символьный токенизатор требует знать все символы заранее.
Байтовый работает с любым Unicode автоматически: каждый байт = один токен.
Vocab size всего 258 — маленький и фиксированный.
Этот подход используют GPT-2, GPT-NeoX, LLaMA.

### Почему Honeycomb-память?
Хранение весов в SHA-256 адресуемых ячейках позволяет:
- Восстанавливать веса после рестарта контейнера
- Версионировать разные состояния модели
- Хранить обучающие данные вместе с весами

### Почему per-file seed tracking?
Старая система: один флаг `seed_loaded: true`.
Проблема: нельзя добавить новый seed-файл без сброса флага вручную.
Решение: список `seed_trained_files` — каждый файл отслеживается отдельно.
Добавил новый файл → при следующем рестарте он обучится автоматически.

---

## ИЗВЕСТНЫЕ ПРОБЛЕМЫ И ОГРАНИЧЕНИЯ

### Активные проблемы
1. **Мало русских данных** — 79KB лучше чем 18KB, но для устойчивого качества
   нужно 200KB+ качественного русского текста. Продолжать наполнение `data/seed/`.

2. **Нет KV-cache** — каждый токен пересчитывает всю историю.
   Исправление: Фаза 5 (ROADMAP).

### Решённые проблемы (для справки)
- **Неполный backprop** — исправлено в v2.1 (FF) и v2.2 (Attention). Теперь
  обновляются 100% весов (lm_head, tok_emb, ff_w1/b1/w2/b2, attn Q/K/V/O).
- **SGD оптимизатор** — заменён на Adam в v2.1. Адаптивная скорость обучения,
  gradient clipping (max_grad_norm=5.0) добавлен в v2.2.
- **ASCII токенизатор** — заменён на ByteTokenizer в v2.0. Все языки работают.

### Не планируется (принципиально)
- Модели > 1B параметров (требуют GPU)
- Обучение с нуля на больших корпусах
- Замена GPT-4/Claude — не цель проекта

---

## КАК ПРОДОЛЖИТЬ РАБОТУ

Если этот файл читается после потери контекста:

1. **Прочитай сначала:**
   - `ROADMAP.md` — что планируется
   - `core/neural_core.py` — вся математика модели
   - `core/seed_trainer.py` — как работает обучение

2. **Следующий приоритет** (Фаза 4 из ROADMAP — многоязычность):
   - Добавить 200KB+ русских seed-данных (сейчас 79KB)
   - GQA (Grouped Query Attention) — меньше памяти при KV-cache
   - KV-cache для ускорения инференса (Фаза 5)
   - (Фаза 3 — RoPE, SwiGLU, Weight tying — реализованы в v2.3)

3. **Команды для запуска:**
   ```bash
   # Запуск
   cd ~/new-mir && git pull origin main && docker compose up -d --build

   # Логи (видно обучение на seed-файлах)
   docker logs -f new-mir

   # Сброс трекинга (пересмотреть все seed-файлы)
   docker exec new-mir rm -f /state/training_stats.json

   # Статус обучения
   docker exec new-mir cat /state/training_stats.json
   ```

4. **Структура seed-данных:**
   Новые seed-файлы → `data/seed/` + запись в `SEED_FILES` в `seed_trainer.py`

---

## КОНТАКТЫ И КОНТЕКСТ СЕССИЙ

Разработка ведётся через Pulumi Neo AI ассистент.
Каждая сессия начинается с чтения этого файла и ROADMAP.md.

Организация Pulumi: `pame-l-ow-ik-nattfly-gmail-com`

**Принцип работы с Neo:**
- Neo читает репозиторий, понимает контекст
- Предлагает план изменений, ждёт подтверждения
- Вносит изменения, создаёт PR
- После merge изменения применяются при следующем `docker compose up --build`

---

*Создан: июль 2026*
*Последнее обновление: июль 2026 (v2.3)*
