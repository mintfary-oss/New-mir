# Архитектура процессоров (CPU)

## Что такое процессор

Центральный процессор (CPU — Central Processing Unit) — главный вычислительный
компонент компьютера. Он выполняет инструкции программ: читает данные из памяти,
производит вычисления, записывает результаты.

Современный CPU — это монолитный кристалл кремния площадью ~200-600 мм²,
содержащий миллиарды транзисторов (Intel Core i9-14900K — 21 млрд транзисторов).

## Транзисторы и логические элементы

Транзистор — основной строительный блок цифровой электроники.
Работает как управляемый ключ: напряжение на затворе управляет током сток-исток.
Современный техпроцесс: 3-5 нм (TSMC N3, Intel 18A).

Логические элементы из транзисторов:
```
NOT (инвертор):   1 вход, 1 выход, 2 транзистора
NAND:             2 входа, 1 выход, 4 транзистора
NOR:              2 входа, 1 выход, 4 транзистора
AND = NAND + NOT: 6 транзисторов
OR  = NOR + NOT:  6 транзисторов
XOR:              ~12 транзисторов
```

Из NAND-элементов можно построить любую цифровую схему (функциональная полнота).

## Архитектурные парадигмы

### CISC (Complex Instruction Set Computer) — x86
- Сложные инструкции переменной длины (1-15 байт на x86)
- Одна инструкция может выполнить несколько операций
- Меньше инструкций в программе, но дольше декодирование
- Примеры: Intel x86/x86-64, AMD x86-64

Пример сложной CISC инструкции:
```asm
MOVS DWORD PTR [EDI], DWORD PTR [ESI]
; Копирует 4 байта из [ESI] в [EDI], затем увеличивает ESI и EDI на 4
; Одна инструкция = 3 операции (load, store, update pointers)
```

### RISC (Reduced Instruction Set Computer) — ARM, RISC-V
- Простые инструкции фиксированной длины (4 байта)
- Каждая инструкция — одна операция
- Больше инструкций в программе, но быстрое декодирование
- Load/Store архитектура: вычисления только с регистрами
- Примеры: ARM Cortex, Apple M-series, RISC-V, MIPS

Пример: то же действие на RISC (ARM64):
```asm
LDR W0, [X1]      ; загрузить из [X1] в W0
STR W0, [X2]      ; сохранить W0 в [X2]
ADD X1, X1, #4    ; X1 += 4
ADD X2, X2, #4    ; X2 += 4
; 4 инструкции вместо одной CISC
```

Современный факт: граница RISC/CISC размыта — x86 процессоры внутри используют
RISC-подобные микрооперации. AMD/Intel транслируют x86 → µops внутри CPU.

## Структура современного процессора

### Функциональные блоки (Pipeline stages)

```
┌─────────────────────────────────────────────────────────┐
│                     CPU Core                             │
│                                                         │
│  ┌─────────┐    ┌──────────┐    ┌────────────────────┐  │
│  │  Fetch  │───▶│  Decode  │───▶│  Rename/Allocate   │  │
│  │(получить│    │(декодиро-│    │(переименование     │  │
│  │инструк.)│    │вать)     │    │регистров)          │  │
│  └────┬────┘    └──────────┘    └─────────┬──────────┘  │
│       │                                   │             │
│  ┌────▼─────────────────────────────────▼──────────┐   │
│  │           Out-of-Order Execution Engine          │   │
│  │  ┌──────────────┐    ┌───────────────────────┐  │   │
│  │  │ Scheduler    │    │  Reorder Buffer (ROB)  │  │   │
│  │  │ (планировщик)│    │  (буфер переупорядоч.) │  │   │
│  │  └──────┬───────┘    └───────────────────────┘  │   │
│  │         │                                        │   │
│  │  ┌──────▼────────────────────────────────────┐  │   │
│  │  │     Execution Units (исполнительные блоки) │  │   │
│  │  │  ALU  ALU  AGU  FPU  SIMD  Load  Store    │  │   │
│  │  └───────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │        Cache Hierarchy                           │   │
│  │  L1-I (32KB)  L1-D (48KB)  L2 (1.25MB)  L3→   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Конвейер (Pipeline)

Конвейер позволяет выполнять несколько инструкций одновременно,
разбивая исполнение на этапы (stages).

### Классический 5-стадийный конвейер (MIPS)
```
Такт:    1    2    3    4    5    6    7    8
Инстр1: [IF] [ID] [EX] [MEM][WB]
Инстр2:      [IF] [ID] [EX] [MEM][WB]
Инстр3:           [IF] [ID] [EX] [MEM][WB]
Инстр4:                [IF] [ID] [EX] [MEM][WB]
```

Стадии:
- IF (Instruction Fetch) — получить инструкцию из кэша
- ID (Instruction Decode) — декодировать, прочитать регистры
- EX (Execute) — выполнить вычисление в ALU
- MEM (Memory) — доступ к кэшу данных
- WB (Write Back) — записать результат в регистр

Без конвейера 4 инструкции = 20 тактов. С конвейером = 8 тактов.

### Hazards (опасности конвейера)

**Data Hazard** — следующая инструкция нужна результат предыдущей:
```asm
ADD R1, R2, R3   ; результат R1 готов через 3 такта
SUB R4, R1, R5   ; нужен R1 — пузырь (stall) или forwarding
```
Решение: **Forwarding** — результат из EX передаётся в следующий EX напрямую.

**Control Hazard** — условный переход неизвестен до EX:
```asm
CMP R1, R2
BEQ label        ; куда прыгать? Знаем только через 2 такта
ADD R3, R4, R5   ; стоит ли выполнять?
```
Решение: **Branch Prediction** — предсказание + спекулятивное выполнение.

**Structural Hazard** — два этапа требуют одно и то же устройство.
Решение: дублирование ресурсов (несколько ALU, портов кэша).

### Глубина конвейера
- Intel Pentium 4 (Prescott): 31 стадия — высокая частота но огромные штрафы
- Intel Core (Sandy Bridge): 14-16 стадий — баланс
- ARM Cortex-A55: 8 стадий — энергоэффективность
- Apple M4: ~12-14 стадий (предположительно)

## Суперскалярность (Superscalar)

Суперскалярный процессор выполняет несколько инструкций за один такт.

Intel Core i9 (Golden Cove микроархитектура):
- 6 инструкций за такт (fetch width)
- До 12 µops декодируется за такт
- До 8 µops исполняется за такт (8-wide issue)

Это требует нескольких экземпляров каждого блока:
- 4 ALU (целочисленные)
- 2 FPU/SIMD
- 2 Load, 1 Store

## Внеочерёдное исполнение (Out-of-Order Execution, OoO)

Если инструкция ждёт данных — CPU выполняет следующие независимые инструкции.

```
Исходный порядок:        OoO выполнение:
1. LOAD R1, [MEM]        1. LOAD R1, [MEM]  ← ждёт 100 тактов (DRAM)
2. ADD  R2, R1, R3  -->  3. MUL R4, R5, R6  ← выполняется пока ждём LOAD
3. MUL  R4, R5, R6       4. SUB R7, R8, R9  ← выполняется пока ждём LOAD
4. SUB  R7, R8, R9       2. ADD R2, R1, R3  ← выполняется после LOAD
```

Компоненты OoO движка:

**Register Renaming (переименование регистров)**
WAW и WAR зависимости — ложные зависимости по именам регистров.
```asm
MOV R1, 5      ; запись R1
ADD R2, R1, 3  ; чтение R1 (истинная зависимость)
MOV R1, 10     ; запись R1 (WAW — Write After Write, ложная)
MUL R3, R1, 2  ; чтение R1 (использует новое R1)
```
Решение: физические регистры (PRF) vs архитектурные.
Intel Skylake: 180 физических целочисленных регистров vs 16 архитектурных.

**Reorder Buffer (ROB)**
Буфер для сохранения результатов OoO выполнения.
Инструкции завершаются (commit) в исходном порядке.
Intel Core: ROB размером 512 записей (Alder Lake).

**Reservation Stations / Scheduler**
Очередь ожидающих µops. Выдаётся на исполнение когда операнды готовы.
Intel Core: объединённый планировщик на 97 записей.

## Предсказание ветвлений (Branch Prediction)

### Статическое предсказание
- Вперёд (forward branch) → не берётся (предсказываем: not-taken)
- Назад (backward branch) → берётся (циклы чаще выполняются)

### Динамическое предсказание

**Двухбитовый счётчик (Bimodal predictor)**
```
Состояния: Strongly Taken (11) → Weakly Taken (10) → Weakly NT (01) → Strongly NT (00)
Точность на SPEC2006: ~85-90%
```

**TAGE (Tagged Geometric History Length)**
Использует несколько таблиц с разной длиной истории переходов.
Точность: >99% на типичном коде.

Используется в Intel Haswell и далее, AMD Zen 3+.

### Штраф за неверное предсказание
- Intel Skylake: ~15 тактов
- AMD Zen 3: ~15 тактов
- Apple M1: ~14 тактов (глубина конвейера меньше)

При неверном предсказании: flush pipeline (сброс), rollback спекулятивных результатов.

### Indirect Branch Predictor
Для косвенных переходов (JMP [RAX], вызов виртуальных функций в C++).
Intel: iBTB (Indirect Branch Target Buffer).
Уязвимость Spectre v2 эксплуатирует именно этот предсказатель.

## Кэш-память процессора

### Иерархия и параметры (Intel Core i9-13900K)
```
Регистры: 0 тактов,    ~кБ
L1 I$:    4 такта,     32 KB,  per core
L1 D$:    5 тактов,    48 KB,  per core
L2:       12 тактов,   1.25 MB, per core
L3 (LLC): 40 тактов,   36 MB,  shared
DRAM:     80-100 нс,   DDR5, гигабайты
NVMe SSD: ~100 мкс,    терабайты
```

### Устройство кэша (Set-Associative Cache)

Кэш делится на наборы (sets), каждый набор — N путей (ways).
Пример: 32KB L1 D-кэш, 8-way, 64B cache lines:
- 32KB / 64B = 512 cache lines
- 512 / 8 = 64 наборов (sets)
- Биты адреса: 6 бит offset, 6 бит index, остальное tag

Поиск в кэше:
```
Адрес → [tag][index][offset]
1. По index выбираем набор (64 entry)
2. Параллельно сравниваем tag со всеми 8 путями
3. Попадание (hit): возвращаем данные по offset
4. Промах (miss): загружаем из следующего уровня, вытесняем старую линию
```

### Политики замещения
- LRU (Least Recently Used): вытесняем давно неиспользованную — оптимально
- Pseudo-LRU: приближение LRU, дешевле в реализации
- RRIP (Re-Reference Interval Prediction): Intel LLC
- Random: простота, предсказуемая производительность

### Когерентность кэша (MESI Protocol)

В многоядерных CPU у каждого ядра свой L1/L2 кэш.
MESI обеспечивает согласованность данных между ядрами.

Состояния кэш-линии:
```
M (Modified)  — линия изменена, в памяти устаревшая копия
E (Exclusive) — линия чистая, только в этом кэше
S (Shared)    — линия в нескольких кэшах, не изменена
I (Invalid)   — линия недействительна
```

Пример: два ядра читают и пишут одну переменную:
```
Core0 читает X:   I→S (shared с Core1)
Core1 читает X:   I→S
Core0 пишет X:    S→M (Core1: S→I, RFO — Request For Ownership)
Core1 читает X:   I→S (Core0: M→S, flush в LLC)
```

Cache line bounce: переменная постоянно перемещается между ядрами.
False sharing: два ядра пишут разные переменные в одной кэш-линии (64B).

### Prefetcher (предзагрузчик)

Аппаратный prefetcher предсказывает какие данные понадобятся и загружает заранее.

Типы:
- Stream prefetcher: последовательный доступ → подгружает следующие линии
- Stride prefetcher: доступ с шагом N → подгружает через N байт
- IP-based: связывает инструкцию с паттерном доступа к памяти
- Компоновщик Irregular Access Pattern (Intel): сложные паттерны

Влияние на производительность:
```python
# Хорошо для prefetcher (последовательный доступ)
for i in range(1000000):
    result += arr[i]    # stride = 1 element → prefetcher загружает заранее

# Плохо (случайный доступ, pointer chasing)
node = head
while node:
    result += node.value
    node = node.next    # следующий адрес неизвестен до загрузки текущего
```

## Исполнительные блоки (Execution Units)

### ALU (Arithmetic Logic Unit)
Выполняет целочисленные операции: сложение, вычитание, AND, OR, XOR, сдвиги.
Intel Golden Cove: 4 ALU, задержка 1 такт для ADD/SUB, 3 такта для MUL.

### AGU (Address Generation Unit)
Вычисляет эффективные адреса памяти.
Формула: base + index*scale + displacement
2 AGU на ядро (для Load + Store параллельно).

### FPU (Floating Point Unit)
Вычисления с плавающей точкой (IEEE 754).
Задержки на Intel Skylake:
- FADD: 4 такта
- FMUL: 4 такта
- FDIV: 10-20 тактов (не конвейеризован!)
- FSQRT: 12-14 тактов

### SIMD блоки (Vector Units)
Выполняют одну операцию над несколькими элементами одновременно.

SSE2: 128-бит, 4×float32 или 2×float64 за раз
AVX2: 256-бит, 8×float32 или 4×float64 за раз
AVX-512: 512-бит, 16×float32 или 8×float64 за раз

Intel Core (Golden Cove):
- 2 порта для 256-бит SIMD (AVX2)
- FMA (fused multiply-add): a×b+c за одну инструкцию
- Пиковая производительность FP32: 2 порта × 8 элем × FMA = 16 GFLOPS/такт

## Микроархитектуры Intel (история)

```
Ядро          Год   Техн  Особенности
NetBurst      2000  180нм Глубокий конвейер, высокая частота, плохая IPC
Core 2        2006  65нм  Возврат к P6, хорошая IPC
Sandy Bridge  2011  32нм  ring bus, AVX, HD Graphics
Ivy Bridge    2012  22нм  FinFET транзисторы
Haswell       2013  22нм  AVX2, TSX, FMA
Broadwell     2014  14нм  Улучшен Haswell
Skylake       2015  14нм  Новый движок OoO, 4-wide decode
Kaby Lake     2016  14нм+ Оптимизация Skylake (без архит. изменений)
Coffee Lake   2017  14нм++6 ядер в mainstream, L3 увеличен
Ice Lake      2019  10нм  Sunny Cove ядра, AVX-512
Tiger Lake    2020  10нм+ Willow Cove, Xe GPU
Alder Lake    2021  Intel7 P-ядра + E-ядра (hybrid), DDR5
Raptor Lake   2022  Intel7 Больше E-ядер, выше частоты
Meteor Lake   2023  Intel4 Die disaggregation (chiplets)
Arrow Lake    2024  Intel4/20A Новые E-ядра Lion Cove
```

## Микроархитектуры AMD (история)

```
K8  (2003): первый x86-64 AMD, двухканальный контроллер памяти в CPU
K10 (2007): quad-core, Phenom
Bulldozer (2011): CMT (Clustered Multi-Threading), провал IPC
Piledriver (2012): улучшен Bulldozer
Ryzen (Zen 1, 2017): огромный скачок IPC, CCX 4-core
Zen+ (2018): 12нм, лучшие частоты
Zen 2 (2019): 7нм TSMC, chiplet дизайн, удвоен FP
Zen 3 (2020): 7нм, единый L3 на 8 ядер, +19% IPC
Zen 4 (2022): 5нм, AVX-512, DDR5, PCIe 5.0
Zen 5 (2024): 4нм/3нм, удвоен IPC AVX-512, новый front-end
```

### AMD Chiplet архитектура (Zen 2+)
CPU разбит на несколько кристаллов (chiplets):
```
CCD (Core Complex Die) × N  +  IOD (I/O Die)
 ├─ 8 ядер Zen              |   ├─ Memory Controller
 ├─ 32MB L3 кэш             |   ├─ PCIe lanes
 └─ 7нм (TSMC)              |   └─ 6нм или 12нм

Ryzen 9 7950X: 2×CCD + 1×IOD
Threadripper: до 8×CCD + 1×IOD
EPYC Genoa: 12×CCD + 1×IOD = 96 ядер
```

Межчиплетная связь: AMD Infinity Fabric (аналог PCIe, но оптимизированный).
Latency между двумя CCD: ~65 нс (vs 40 нс внутри одного CCD).

## Apple Silicon (ARM-based)

Apple M1 (2020) — революционная архитектура:
```
M1 характеристики:
  - 8 ядер CPU: 4 Firestorm (P-cores) + 4 Icestorm (E-cores)
  - 8 ядер GPU (интегрированный)
  - 16-core Neural Engine (ANE)
  - Unified Memory Architecture: CPU+GPU разделяют один пул памяти
  - Memory bandwidth: 68 GB/s (LPDDR4X, on-package)
  - Техпроцесс: TSMC 5нм
```

Причины высокой производительности M1:
1. Огромный ROB (630 записей vs 512 у Intel) → лучший OoO
2. Широкий issue (12-wide decode, 8-wide execution)
3. Большой L1 кэш (192KB I$ per P-core)
4. Высокая пропускная способность памяти (on-package)
5. Arch-specific оптимизации macOS

M4 (2024):
- TSMC 3нм
- 10 ядер CPU
- Поддержка 32GB Unified Memory
- Улучшенный Neural Engine

## Технологии многопоточности

### SMT (Simultaneous Multi-Threading)
Intel называет: Hyper-Threading (HT)
AMD называет: SMT

Одно физическое ядро выглядит как два логических.
Два потока делят исполнительные блоки, но у каждого свои:
- Регистровый файл
- Program counter (RIP)
- ROB (Reorder Buffer)
- BTB (Branch Target Buffer)

Прирост производительности SMT: +10-30% для многопоточных задач.
Не помогает (иногда вредит) для однопоточных.

Недостатки:
- Делит L1/L2 кэш между потоками → cache pollution
- Уязвимости: MDS, L1TF, Spectre (side-channel через общий кэш)

### NUMA (Non-Uniform Memory Access)

В многопроцессорных системах (2+ CPU):
```
CPU 0                    CPU 1
├─ Local RAM (Node 0)    ├─ Local RAM (Node 1)
│  Latency: 80 нс        │  Latency: 80 нс
└──────────QPI/UPI───────┘
           Remote access: 150-200 нс
```

Linux команды:
```bash
numactl --hardware          # показать NUMA топологию
numactl --cpunodebind=0 ./program  # привязать к NUMA узлу 0
taskset -c 0-7 ./program    # привязать к CPU 0-7
```

## Инструкции и расширения

### Основные расширения x86-64
```
MMX  (1997): 64-бит регистры, целочисленный SIMD
SSE  (1999): 128-бит XMM, float32 SIMD
SSE2 (2001): double, целое в XMM
SSE3/4 (2004-2007): горизонтальные операции, dot product
AVX  (2011): 256-бит YMM, 3-операндные инструкции
AVX2 (2013): 256-бит integer SIMD, FMA, gather
AVX-512 (2017): 512-бит ZMM, 32 регистра, маски
AMX  (2022): матричные операции (ускорение AI)
```

### Специальные инструкции

CPUID — информация о CPU:
```asm
MOV EAX, 1
CPUID
; EAX: family/model/stepping
; EBX: brand index, CLFLUSH size, logical CPUs
; ECX: SSE3, PCLMULQDQ, AVX, RDRAND...
; EDX: FPU, VME, PSE, TSC, MMX, SSE, SSE2...
```

RDTSC (Read Time-Stamp Counter) — счётчик тактов:
```c
uint64_t rdtsc() {
    unsigned int lo, hi;
    asm volatile ("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}
// Используется для профилирования с точностью до тактов
```

PAUSE — подсказка CPU, что мы в spinlock:
```c
while (atomic_load(&lock) != 0)
    _mm_pause();   // PAUSE инструкция — снижает энергопотребление, уменьшает memory order violations
```

CRC32 — аппаратное вычисление CRC:
```asm
CRC32 EAX, [RBX]   ; вычислить CRC32 за 1 такт
```

POPCNT — подсчёт единичных бит:
```asm
POPCNT EAX, EBX    ; EAX = количество '1' в EBX
```

## Управление питанием и частотой

### P-states (Performance States)
CPU меняет частоту и напряжение для баланса производительности/мощности.

```
Intel Turbo Boost:
  Base: 3.5 GHz (TDP = 125W)
  All-core turbo: 5.0 GHz
  Single-core turbo: 5.8 GHz

AMD Precision Boost 2:
  Base: 3.4 GHz
  Max boost: 5.7 GHz (зависит от температуры, VRM quality)
```

Алгоритм: если температура < 95°C и VRM может дать ток → увеличиваем частоту.

### C-states (Idle States)
```
C0  — активен, выполняет код
C1  — остановлен (HALT), просыпается за 1 мкс
C1E — Enhanced Halt, чуть ниже напряжение
C2  — остановлены внешние сигналы шины
C3  — кэши сброшены (flushed)
C6  — ядро без питания! Просыпается за 100-300 мкс
C8  — Core Power Gate, глубокий сон
```

### TDP (Thermal Design Power)
Тепловой пакет — максимальная тепловая мощность при устойчивой нагрузке.
Intel Core i9-13900K: TDP 125W, PL2 253W (кратковременный)
AMD Ryzen 9 7950X: TDP 170W

PL1 = долговременный лимит (TDP)
PL2 = кратковременный лимит (Turbo Boost)
PL3 = мгновенный пик

## Защита памяти и привилегированные кольца

```
Ring 0 — ядро ОС (Kernel mode)
  ├─ Полный доступ к памяти и устройствам
  └─ Прямое выполнение привилегированных инструкций

Ring 1, 2 — (редко используется, драйверы в старых ОС)

Ring 3 — пользовательский код (User mode)
  ├─ Ограниченный доступ (только своя виртуальная память)
  └─ Системные вызовы через SYSCALL/INT

Переключение Ring 3 → Ring 0:
  SYSCALL   → загружает адрес из MSR LSTAR
  INT 0x80  → прерывание (legacy 32-бит Linux)
  SYSENTER  → быстрое переключение (legacy)
```

Виртуализация (VT-x/AMD-V):
```
Ring -1 — гипервизор (VMX root mode)
  └─ Перехватывает привилегированные операции гостевых ОС
     (VMLAUNCH, VMRESUME, VM-exits)
```

## Уязвимости современных CPU

### Spectre (2018)
Эксплуатирует спекулятивное выполнение и предсказание ветвлений.
Атакующий обучает предсказатель переходов → CPU спекулятивно читает чужую память.
Через side-channel (разница во времени доступа к кэшу) утекают данные.

Mitigation: IBRS (Indirect Branch Restricted Speculation), Retpoline.

### Meltdown (2018)
Спекулятивное чтение памяти ядра из кода пользователя.
Intel исправил аппаратно начиная с Coffee Lake Refresh.
Software fix: KPTI (Kernel Page Table Isolation) — производительность -5-30%.

### MDS (2019, Intel)
RIDL, Fallout, ZombieLoad — утечка данных через буферы (Line Fill Buffer, Store Buffer).
Mitigation: microcode update, очистка буферов при VM-exit.

## Числовые характеристики современных CPU (2024)

```
                    Intel Core i9-14900K  AMD Ryzen 9 9950X   Apple M4
Ядра (P+E)          24 (8P + 16E)         16 (16P)             10 (4P+6E)
Потоки              32                    32                   10
Base clock          3.2 GHz               4.3 GHz              ~3.7 GHz
Boost clock         6.0 GHz               5.7 GHz              ~4.4 GHz
L3 Cache            36 MB                 64 MB                 12 MB ULL
TDP                 125W (PL2: 253W)      170W                  28W
Техпроцесс          Intel 7 (10нм)        TSMC 4нм              TSMC 3нм
Cinebench R23 MT    ~40000                ~50000                ~24000
Cinebench R23 ST    ~2350                 ~2500                 ~3700
```

## Системная шина и взаимодействие с периферией

### PCIe (Peripheral Component Interconnect Express)
Последовательная шина с полно-дуплексными lanes.
```
PCIe 3.0: 1 GB/s per lane
PCIe 4.0: 2 GB/s per lane  (x16 = 32 GB/s)
PCIe 5.0: 4 GB/s per lane  (x16 = 64 GB/s)
PCIe 6.0: 8 GB/s per lane  (x16 = 128 GB/s)
```

x1, x4, x8, x16 — количество lanes.
GPU обычно подключается через PCIe x16.
NVMe SSD — PCIe x4.

### DMI/FSB
Intel: DMI (Direct Media Interface) — связь CPU с PCH (Platform Controller Hub).
DMI 4.0 = 4 GB/s (PCIe 3.0 x8).

AMD: Fusion Controller Hub через USB/SATA напрямую из CPU.

### Ring Bus vs Mesh Interconnect

Intel до Skylake-X: Ring Bus — быстрый доступ до ~8 ядер.
Intel Mesh (Skylake-SP, Server): двумерная сетка для 28+ ядер.
AMD Infinity Fabric: AXI-based, 100+ GB/s внутри die.

## Виртуализация и контейнеры

Intel VT-x / AMD-V:
- VMXON / VMLAUNCH — управление виртуальными машинами
- Extended Page Tables (EPT) / Rapid Virtualization Indexing (RVI)
  — аппаратная трансляция виртуальных адресов гостя
- VMCS (Virtual Machine Control Structure) — состояние VM

Типичные VM-exit'ы: CPUID, RDMSR, WRMSR, I/O инструкции, page faults.

SR-IOV (Single Root I/O Virtualization):
Одна физическая GPU/NIC выглядит как несколько виртуальных устройств.
Каждая VM получает прямой доступ к «своей» части железа.

## Профилирование CPU

### Performance Counters (PMU)
Аппаратные счётчики событий:
```
instructions retired    — выполнено инструкций
cpu cycles              — тактов CPU
cache-misses            — промахи кэша
branch-misses           — неверные предсказания
LLC-load-misses         — промахи L3
TLB-load-misses         — промахи TLB
```

Linux perf:
```bash
perf stat ./program                     # базовая статистика
perf stat -e cache-misses ./program     # промахи кэша
perf record -g ./program               # сбор профиля
perf report                            # анализ hot-spots
perf top                               # top-like для CPU
```

IPC (Instructions Per Cycle) — ключевой показатель:
- IPC < 1: плохо (много промахов кэша, branch misses)
- IPC 1-2: типично
- IPC > 3: хорошо (векторизованный код, хорошая локальность)

### Инструменты профилирования
```
Intel VTune Profiler  — полный анализ кода, bottleneck analysis
AMD uProf             — для Ryzen/EPYC
Linux perf            — универсальный, бесплатный
Valgrind/Cachegrind   — симуляция кэша
LIKWID                — аппаратные счётчики, мониторинг
```
