# Системы памяти: иерархия, принципы работы, оптимизация

## Иерархия памяти

Память организована в иерархию: чем быстрее — тем дороже и меньше.

```
Уровень          Размер        Латентность      Пропускная способность
─────────────────────────────────────────────────────────────────────
Регистры         ~1 KB         0-1 такт         ~10 TB/s
L1 I-Cache       32-64 KB      4 такта          ~3 TB/s
L1 D-Cache       32-64 KB      5 тактов         ~3 TB/s
L2 Cache         256KB-2MB     12 тактов        ~1 TB/s
L3 Cache (LLC)   8-96 MB       30-50 тактов     ~300 GB/s
DRAM (RAM)       8-512 GB      80-100 нс        ~50-100 GB/s
NVMe SSD         500GB-8TB     ~50-100 мкс      ~7-15 GB/s
SATA SSD         500GB-4TB     ~100 мкс         ~500 MB/s
HDD              500GB-30TB    5-15 мс          ~150-300 MB/s
Tape (лента)     до 30 TB      секунды          ~400 MB/s seq
```

Принцип локальности — основа иерархии:
- **Временна́я локальность**: к недавно использованным данным обратятся снова.
- **Пространственная локальность**: если использовали адрес X, скоро понадобится X+1.

## DRAM — Dynamic Random Access Memory

### Физический принцип работы

DRAM ячейка = 1 транзистор + 1 конденсатор (1T1C).
Конденсатор хранит заряд: заряжен = 1, разряжен = 0.

Проблема: конденсатор **самопроизвольно разряжается** за ~64 мс.
Решение: **регенерация (Refresh)** — контроллер памяти периодически перечитывает
и перезаписывает все строки.

tREFI = интервал регенерации = 7.8 мкс (64 мс / 8192 строк).
tRFC = время регенерации одной строки = 260-550 нс (зависит от ёмкости).

Пока идёт refresh — память недоступна. При 64 GB DDR5:
tRFC ~550 нс каждые 7.8 мкс → ~7% времени на refresh. Это латентность.

Почему DRAM, а не SRAM (6T)?
- SRAM: 6 транзисторов/бит, быстрая (~0.2 нс), дорогая → кэш
- DRAM: 1 транзистор/бит, медленнее, дешёвая → основная память

### Структура DRAM модуля

```
DIMM
 ├─ 8-16 DRAM чипов (ranks × banks × rows × columns)
 └─ SPD (Serial Presence Detect) — EEPROM с параметрами модуля

DRAM чип (например, Samsung K4AAG165WA):
 ├─ 8 Banks (или 16 Bank Groups × 2 Banks в DDR5)
 │   └─ Каждый Bank: 32768 строк × 1024 столбца × 8 бит
 └─ Sense Amplifiers (усилители считывания) между строками
```

### Операции DRAM

**Activate (ACT)**: открываем строку (row) — копируем в Row Buffer.
tRCD = Row to Column Delay = ~12-14 нс.

**Read/Write**: доступ к данным в открытой строке через column address.
tCL = CAS Latency = ~10-14 нс (DDR5).

**Precharge (PRE)**: закрываем строку (возвращаем заряд).
tRP = Row Precharge = ~12-14 нс.

Полный цикл (closed page → read → closed):
tRCD + tCL + burst transfer = ~30-40 нс (плюс ожидание шины).

**Row Buffer Hit**: если следующий доступ в ту же строку — только tCL.
**Row Buffer Miss**: PRE + ACT + tCL = ~3× дольше.

Row Buffer Policies:
- Open Page: строка остаётся открытой → хорошо для sequential.
- Closed Page: строка закрывается сразу → лучше для random.
- Adaptive: ОС/контроллер решает динамически.

### Tайминги DDR5 (детально)

```
tCL  (CAS Latency)           — задержка от READ до первого бита
tRCD (RAS to CAS Delay)      — время открытия строки
tRP  (Row Precharge)         — время закрытия строки
tRAS (Row Active Time)       — минимальное время строки открыта
tRC  (Row Cycle Time)        — tRAS + tRP = минимальный цикл
tWR  (Write Recovery)        — после записи до precharge
tRFC (Refresh Cycle Time)    — время регенерации
tFAW (Four Activate Window)  — максимум 4 ACT за это время
tRRD (Row to Row Delay)      — между ACT в разных bank groups
```

DDR5-6000 CL30:
```
tCL=30, tRCD=36, tRP=36, tRAS=76
Реальная первичная латентность: 30 / (6000/2) нс = 10 нс
```

DDR5-7200 CL34:
```
Первичная латентность: 34 / (7200/2) нс = 9.44 нс
Быстрее тактовая → ниже латентность даже при большем CL числе
```

### Ранги и банки

**Rank**: группа чипов, обслуживающих 64-бит шину данных.
DIMM с 2 ranks: контроллер чередует (interleave) между рангами.

**Bank Group**: DDR4/5 группирует банки для увеличения параллелизма.
DDR5: 8 Bank Groups × 2 Banks = 16 банков на ранг.
Разные Bank Groups работают одновременно (tRRD_L vs tRRD_S).

## Контроллер памяти (IMC — Integrated Memory Controller)

С Intel Sandy Bridge (2011) и AMD K8 (2003) — контроллер памяти
встроен непосредственно в процессор (ранее был в Northbridge).

Преимущества:
- Меньше латентность: нет FSB
- Intel Nehalem: ~65 нс, vs Core 2: ~90 нс

Состав IMC:
```
IMC
 ├─ Scheduler (планировщик команд: ACT, READ, WRITE, PRE)
 ├─ Bank State Machine (отслеживает состояние каждого банка)
 ├─ Refresh Engine (отправляет REF-команды по tREFI)
 ├─ Write Queue + Read Queue
 └─ PHY (Physical Interface) — драйверы/приёмники шины DDR
```

Оптимизации планировщика:
- Out-of-Order: запросы к открытым строкам идут вперёд
- Write Coalescing: объединение соседних записей
- Read-to-Write turnaround: пауза при переключении направления (tRTW, tWTR)

## Типы RAM по поколениям

### DDR4 (2014—настоящее время)
```
Частота: 2133-3200 МГц (JEDEC), до 5000+ МГц (XMP/EXPO)
Напряжение: 1.2V (1.35V для XMP)
Шина данных: 64-бит + 8-бит ECC (72 бит физически с ECC)
Ширина шины данных: 64 бит
Prefetch: 8n (8 бит за одну операцию внутри)
Форм-фактор: 288-pin DIMM
Bank Groups: 4 группы × 4 банка (DDR4-3200)
Burst Length: 8
```

### DDR5 (2021—настоящее время)
```
Частота: 4800-6400 МГц (JEDEC), до 8400+ МГц (XMP 3.0/EXPO)
Напряжение: 1.1V
Два независимых 32-бит канала на DIMM (!)
  → один DIMM = два 40-бит (32+8 ECC) суб-канала
Prefetch: 16n
Форм-фактор: 288-pin (другая насечка, чем DDR4!)
Bank Groups: 8 группы × 2 банка = 16 банков
PMIC (Power Management IC) встроен в DIMM
On-Die ECC: встроенная коррекция ошибок в чипе
```

Почему DDR5 не вдвое быстрее при вдвое большем prefetch?
Потому что задержки (tCL, tRCD) тоже выросли.
Но bandwidth DDR5-6400 (51.2 GB/s) >> DDR4-3200 (25.6 GB/s).

### GDDR6 / GDDR6X (видеопамять)
```
GDDR6:  16 Gbps per pin, 256-бит шина → 512 GB/s
GDDR6X: 21 Gbps per pin (PAM4 кодирование) → 672 GB/s (RTX 3090)
GDDR7:  32 Gbps per pin → 1 TB/s (RTX 5090)
```

PAM4 (Pulse Amplitude Modulation 4): 4 уровня сигнала → 2 бита за такт.
NRZ (Non-Return-to-Zero): обычный 1 бит за такт.

### HBM (High Bandwidth Memory)

HBM — DRAM-кристаллы уложены стопкой, соединяются через through-silicon vias (TSV).
Установлены рядом с GPU на общем interposer (кремниевый посредник).

```
HBM2: 256-бит × 8 слоёв = 2048-бит шина на стек, 256 GB/s/stack
HBM2E: 307 GB/s/stack (Samsung, Hynix)
HBM3:  819 GB/s/stack (Micron)
HBM3E: 1.2 TB/s/stack

NVIDIA H100 SXM: 5 стеков HBM3 × 819 GB/s = 3.35 TB/s
AMD MI300X: 8 стеков HBM3 = 5.3 TB/s (!), 192 GB
```

Зачем GPU нужна такая пропускная способность?
16384 CUDA cores × 2 (FMA) × 16 байт / такт = нужны терабайты в секунду.
Без HBM → GPU простаивает, ожидая данных (Memory Bound).

### LPDDR (Low Power DDR — мобильные)
```
LPDDR4X: 4266 Mbps, 1.1V, 2×32-бит = 64-бит шина
LPDDR5:  6400 Mbps, 1.05V
LPDDR5X: 8533 Mbps, WCK (Write Clock) отдельно для записи
```

Apple M3 Pro: LPDDR5 в пакете с CPU.
Преимущества on-package: короткие линии → низкая задержка (~80 нс вместо ~90 нс).

## Виртуальная память

### Зачем нужна виртуальная память?

1. **Изоляция процессов**: каждый процесс думает, что у него есть всё адресное пространство.
2. **Абстракция физической памяти**: программист не знает реальные физические адреса.
3. **Swap**: программы могут использовать больше RAM, чем физически есть.
4. **Защита**: процесс не может читать память другого процесса.
5. **Shared memory**: одна физическая страница → несколько виртуальных адресов.

### Страничная организация (Paging)

Виртуальная и физическая память делится на **страницы** (pages).
Размер страниц: 4 KB (стандарт), 2 MB (hugepages), 1 GB (gigapages).

```
Виртуальный адрес (48-бит в x86-64):
  [PML4 index 9 бит][PDPT index 9 бит][PD index 9 бит][PT index 9 бит][Offset 12 бит]
  └─────────────────────────────────────────────────────────────────────────────────┘
                              48 бит = 256 TB адресного пространства
```

**Page Table (таблица страниц)**: отображение виртуальных адресов → физические.
4-уровневая таблица на x86-64 (5-уровневая — 57-бит для > 128 TB).

Каждая Page Table Entry (PTE):
```
Биты 0-11: флаги
  P (Present): страница в памяти
  R/W: чтение/запись
  U/S: user/supervisor (Ring 3 / Ring 0)
  A (Accessed): была прочитана (устанавливает MMU)
  D (Dirty): была записана
  PS (Page Size): 1 = 2MB huge page
  NX (No Execute): запретить выполнение кода
Биты 12-51: физический адрес страницы (PFN)
```

### TLB (Translation Lookaside Buffer)

Трансляция виртуального адреса → 4 обращения к памяти (4 уровня таблиц).
**TLB** — кэш трансляций адресов прямо в CPU.

```
Intel Skylake TLB структура:
  L1 ITLB: 128 entries (4KB pages), полностью ассоциативный
  L1 DTLB: 64 entries (4KB), 4-way
  L2 STLB: 1536 entries (4KB), 12-way
  Huge page ITLB: 8 entries (2MB)
  Huge page DTLB: 32 entries (2MB)
```

TLB miss → **Page Table Walk** — аппаратный обход 4 уровней таблиц.
Время: 4 × L1-miss = ~200 тактов (если таблицы в кэше) или 4 × DRAM = ~400 нс.

**ASID (Address Space ID)**: пометка TLB-записей → не нужно flush TLB при context switch.
Intel использует PCID (Process-Context Identifier, 12 бит).

**INVLPG**: инвалидация одной TLB-записи (после изменения PTE).
**CR3**: регистр, содержащий физический адрес PML4. Запись в CR3 → flush TLB.

### Huge Pages

Обычная страница 4KB → больше TLB-записей при больших данных.
HugePage 2MB: один TLB-entry = 512 × 4KB → меньше TLB-промахов.

Linux:
```bash
# Transparent Huge Pages (THP) — автоматически:
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# Явные hugepages (для базы данных, DPDK):
echo 1024 > /proc/sys/vm/nr_hugepages  # 1024 × 2MB = 2 GB
# В программе:
void* ptr = mmap(NULL, 2*1024*1024, PROT_READ|PROT_WRITE,
                 MAP_PRIVATE|MAP_ANONYMOUS|MAP_HUGETLB, -1, 0);
```

PostgreSQL: рекомендуется huge_pages=on для shared_buffers > 1 GB.
Redis, Oracle, MongoDB: выигрывают от hugepages.

### Page Fault (прерывание страницы)

Три типа:
1. **Minor fault**: страница в памяти, но не отображена в таблице — просто создать PTE.
2. **Major fault**: страница отсутствует → нужно загрузить с диска (swap).
3. **Invalid fault** → SIGSEGV (Segmentation Fault).

Стоимость major fault: ~10-15 мс (загрузка с NVMe SSD).

### Swap

Когда RAM заканчивается — ядро вытесняет страницы на диск (swap).
Алгоритм вытеснения: LRU (через бит Accessed в PTE), с учётом file-backed vs anonymous.

```
Linux swap:
  Swap partition: отдельный раздел диска
  Swap file: файл в файловой системе
  zram: сжатый swap в RAM (для систем с мало RAM)
  zswap: сжатый кэш swap-страниц в RAM перед записью на диск

Команды:
swapon -s                # показать swap
free -h                  # RAM + swap использование
vmstat 1                 # страничный трафик: si (swap in), so (swap out)
```

OOM Killer: когда RAM + swap кончается — ядро убивает процессы.
```bash
# Узнать score каждого процесса:
cat /proc/PID/oom_score
# Защитить процесс от OOM:
echo -1000 > /proc/PID/oom_score_adj
```

## Модель памяти CPU (Memory Ordering)

### Зачем нужна модель памяти?

Современные CPU переупорядочивают операции с памятью для производительности.
Это создаёт проблемы в многопоточных программах.

```
Thread 1:          Thread 2:
x = 1;             y = 1;
r1 = y;            r2 = x;
```

Можно ли получить r1=0 и r2=0 одновременно?
На x86: нет (TSO — Total Store Order).
На ARM/PowerPC: да (weakly ordered архитектуры)!

### x86 Memory Model (TSO)

Intel и AMD гарантируют TSO:
- Загрузки (loads) не переупорядочиваются относительно других загрузок.
- Сохранения (stores) не переупорядочиваются относительно других сохранений.
- Загрузки могут видеть более ранние, но ещё не committed сохранения (store forwarding).
- Сохранения могут быть отложены (Store Buffer) — другие ядра видят не сразу.

### Store Buffer и его эффекты

```
                 Core 0            Core 1
                   │                 │
              ┌────▼────┐       ┌────▼────┐
              │ Store   │       │ Store   │
              │ Buffer  │       │ Buffer  │
              └────┬────┘       └────┬────┘
                   │                 │
              ┌────▼─────────────────▼────┐
              │          L3 Cache         │
              └───────────────────────────┘
```

Store Buffer позволяет CPU продолжать работу, не ожидая записи в кэш.
SFENCE: гарантирует, что все предыдущие store дошли до кэша.
LFENCE: гарантирует, что все предыдущие load завершены.
MFENCE: полный барьер памяти.

В языках программирования:
```cpp
std::atomic<int> x{0}, y{0};

// Thread 1:
x.store(1, std::memory_order_release);  // SFENCE-like

// Thread 2:
int val = x.load(std::memory_order_acquire);  // LFENCE-like

// memory_order_seq_cst — полный барьер (MFENCE) — самый медленный
```

### Cache Coherence Protocol (MESI)

Подробнее о MESI в многоядерных системах:

```
Состояние M (Modified):
  - Данные изменены, не сохранены в памяти
  - Единственная копия во всей системе
  - При чтении другим ядром: сброс в память + переход в S

Состояние E (Exclusive):
  - Чистые данные, только в этом кэше
  - Нет необходимости писать в память при вытеснении нет
  - При чтении другим ядром: переход в S (оба)

Состояние S (Shared):
  - Несколько кэшей имеют копии
  - При записи: посылает Invalidate всем → переход в M

Состояние I (Invalid):
  - Данные устарели или отсутствуют
  - При чтении: RFO (Read For Ownership) или обычный Read
```

### False Sharing (ложное совместное использование)

Кэш-линия = 64 байта. Если два потока пишут разные переменные в одной линии:

```cpp
struct Bad {
    int counter_a;  // Thread 0 writes
    int counter_b;  // Thread 1 writes
    // оба в одной кэш-линии (8 байт < 64 байт)
};

struct Good {
    alignas(64) int counter_a;  // отдельная кэш-линия
    alignas(64) int counter_b;  // отдельная кэш-линия
};
```

False sharing → постоянный обмен кэш-линиями между ядрами → деградация до ~10% от пика.

### Влияние на производительность

```
Операция                     Латентность
─────────────────────────────────────────
Регистр → регистр            0-1 такт
L1 кэш hit                   4-5 тактов
L2 кэш hit                   12 тактов
L3 кэш hit                   30-50 тактов
DRAM (local)                 80-100 нс
DRAM (remote, NUMA)          150-200 нс
Atomic operation (uncontested) 1-20 тактов
Atomic CAS (contested)       100-1000 тактов
Lock acquire (uncontested)   25 нс
Lock acquire (contested)     мкс - мс
```

## Управление памятью в ОС

### Linux Memory Management

**Зоны памяти (Memory Zones)**:
```
ZONE_DMA    — первые 16 MB (устаревшие устройства, ISA DMA)
ZONE_DMA32  — первые 4 GB (32-бит DMA)
ZONE_NORMAL — основная область
ZONE_HIGHMEM — >896 MB в 32-бит системах (устарело)
ZONE_MOVABLE — мигрируемые страницы (для huge pages)
```

**Page Allocator (Buddy System)**:
```
Аллокатор-буддист разбивает память на блоки степеней двойки:
  [...1 page...][...2 pages...][...4 pages...][...8 pages...]
При выделении 3 страниц:
  1. Ищем блок 4 страницы
  2. Разбиваем на 2 блока по 2 → берём один блок 2 страницы + 1 страницу
При освобождении: объединяем с "буддистом" (buddy) если он свободен
```

**Slab Allocator**:
Для объектов фиксированного размера (inode, task_struct, socket...).
Хранит кэш заранее выделенных объектов → быстрое alloc/free.
Реализации: SLAB (оригинальный), SLUB (текущий в Linux), SLOB (минималистичный).

**Page Reclaim (возврат страниц)**:
```
kswapd — демон, освобождает память в фоне
  ├─ File-backed pages (page cache): сбросить на диск (fsync) или просто удалить
  │   (данные можно прочитать снова из файла)
  └─ Anonymous pages (malloc, stack): записать в swap

LRU списки:
  Active Anon   — анонимные страницы, недавно использованные
  Inactive Anon — кандидаты для swap
  Active File   — файловые страницы, недавно использованные
  Inactive File — кандидаты для удаления
```

**Memory Compaction**:
Дефрагментация памяти для создания больших непрерывных областей (нужно для huge pages).
Перемещает movable страницы, обновляет PTEs.

### NUMA (Non-Uniform Memory Access)

В многопроцессорных системах память делится по узлам (nodes).

```
     CPU 0                    CPU 1
    ┌──────┐                 ┌──────┐
    │ Core │    QPI/UPI      │ Core │
    │ Core │ ──────────────  │ Core │
    │ Core │                 │ Core │
    └──┬───┘                 └──┬───┘
       │ IMC                    │ IMC
    ┌──▼──────┐            ┌───▼─────┐
    │ Node 0  │            │ Node 1  │
    │  RAM    │            │   RAM   │
    │ 32 GB   │            │  32 GB  │
    └─────────┘            └─────────┘
    Local access: 80 нс    Remote access: 150 нс
```

**numactl** — управление NUMA:
```bash
numactl --hardware                       # показать топологию
numactl --membind=0 --cpunodebind=0 ./prog  # привязать к node 0
numactl --interleave=all ./prog          # чередовать страницы между узлами

# Информация в Linux:
cat /sys/devices/system/node/node0/meminfo
numastat                                  # статистика по узлам
```

**NUMA-оптимизации в ядре**:
- AutoNUMA: ядро отслеживает доступ к страницам и мигрирует на локальный узел
- Process migration: планировщик перемещает поток ближе к его данным
- Memory policies: MPOL_BIND, MPOL_PREFERRED, MPOL_INTERLEAVE

### Огромные страницы (Huge Pages) в Linux

```bash
# 1. Статические Huge Pages (2MB)
grep HugePages /proc/meminfo
echo 512 > /proc/sys/vm/nr_hugepages   # выделить 512×2MB=1GB
# Монтирование hugetlbfs:
mount -t hugetlbfs nodev /mnt/huge

# 2. Transparent Huge Pages (THP)
cat /sys/kernel/mm/transparent_hugepage/enabled
# Опции: always, madvise, never
echo madvise > /sys/kernel/mm/transparent_hugepage/enabled

# В программе подсказка ядру:
madvise(addr, size, MADV_HUGEPAGE);   # разрешить THP для этого региона
madvise(addr, size, MADV_NOHUGEPAGE); # запретить THP

# 3. 1GB Huge Pages (для очень больших буферов)
echo 2 > /proc/sys/vm/nr_hugepages_1gb  # в ядре нужен параметр загрузки
# hugepagesz=1G hugepages=2 (в /etc/default/grub)
```

## Кэш-оптимизации программ

### Анализ кэш-поведения

```cpp
// ПЛОХО: Column-major обход C-массива (row-major layout)
for (int j = 0; j < N; j++)
    for (int i = 0; i < N; i++)
        sum += matrix[i][j];  // прыжки по N*4 байт = много cache miss

// ХОРОШО: Row-major обход — последовательный доступ
for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
        sum += matrix[i][j];  // +4 байт каждый шаг = prefetcher работает
```

Разница: для матрицы 4096×4096 float32:
- Плохой вариант: ~40 сек (все L2/L3 промахи → DRAM)
- Хороший вариант: ~0.2 сек (данные в кэше благодаря prefetcher)

### Cache Blocking (Tiling)

Разбиваем данные на блоки, помещающиеся в кэш:

```cpp
// Матричное умножение без blocking (N=1024):
for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
        for (int k = 0; k < N; k++)
            C[i][j] += A[i][k] * B[k][j];  // B[k][j] — плохой доступ

// С blocking (BLOCK_SIZE = 32, помещается в L1):
for (int ii = 0; ii < N; ii += BLOCK_SIZE)
for (int jj = 0; jj < N; jj += BLOCK_SIZE)
for (int kk = 0; kk < N; kk += BLOCK_SIZE)
    for (int i = ii; i < min(ii+BLOCK_SIZE, N); i++)
    for (int j = jj; j < min(jj+BLOCK_SIZE, N); j++)
    for (int k = kk; k < min(kk+BLOCK_SIZE, N); k++)
        C[i][j] += A[i][k] * B[k][j];

// Ускорение: 3-10× для больших матриц
```

### Prefetch инструкции

```cpp
// Ручной prefetch для pointer chasing:
for (Node* node = head; node != nullptr; node = node->next) {
    if (node->next)
        __builtin_prefetch(node->next, 0, 1);  // prefetch for read, low temporal locality
    process(node->data);
}

// __builtin_prefetch(addr, rw, locality)
// rw: 0=read, 1=write
// locality: 0=no cache, 1=L3, 2=L2, 3=L1
```

### Structure of Arrays vs Array of Structures

```cpp
// AoS (Array of Structures) — плохо для SIMD, хорошо для single-element access
struct Particle { float x, y, z, vx, vy, vz; };
Particle particles[N];
// Обработка только x: нужно пропускать y, z, vx, vy, vz

// SoA (Structure of Arrays) — хорошо для SIMD, оптимально для массовой обработки
struct Particles {
    float x[N], y[N], z[N], vx[N], vy[N], vz[N];
};
// Обработка только x: чистый sequential access, AVX2 обрабатывает 8 за раз
```

### Stack vs Heap vs Static

```cpp
// Stack: ~8 MB по умолчанию, автоматическое управление
void func() {
    int arr[1000];  // 4 KB на стеке — быстро, но ограничено
}

// Heap: практически неограниченный
int* arr = new int[10000000];  // 40 MB — медленнее из-за malloc overhead
// malloc: ищет свободный блок в free list → может быть медленно при fragmentation

// Static: в сегменте .data или .bss
static int cache[65536];  // инициализируется один раз, всегда в памяти
```

**Memory Pool**: аллокатор для объектов одного размера:
```cpp
template<typename T, size_t N>
class Pool {
    alignas(T) char storage[sizeof(T) * N];
    T* free_list[N];
    int top = 0;
public:
    T* alloc() { return free_list[--top]; }
    void free(T* p) { free_list[top++] = p; }
};
// Быстрее malloc/free в 10-100× для частых аллокаций
```

## Инструменты анализа памяти

### Valgrind — обнаружение ошибок

```bash
valgrind --tool=memcheck ./program          # утечки, invalid access
valgrind --leak-check=full ./program        # детальный отчёт утечек
valgrind --tool=cachegrind ./program        # симуляция кэша
valgrind --tool=massif ./program            # heap profiling
```

Cachegrind выдаёт:
```
I refs:      123,456,789   # инструкции
I1 misses:       456,789   # L1 промахи (инструкции)
LLi misses:       12,345   # L3 промахи
D refs:      234,567,890   # данные (load+store)
D1 misses:     1,234,567   # L1 D-cache промахи
LL misses:        45,678   # L3 промахи данных
```

### perf — Linux профилировщик

```bash
perf stat -e L1-dcache-loads,L1-dcache-load-misses,\
             LLC-loads,LLC-load-misses,\
             dTLB-loads,dTLB-load-misses ./program

# Типичный вывод:
# L1-dcache-loads:          500,000,000
# L1-dcache-load-misses:      5,000,000  (1% miss rate — хорошо)
# LLC-loads:                  5,000,000
# LLC-load-misses:              500,000  (10% L3 miss rate — нормально)
# dTLB-loads:               500,000,000
# dTLB-load-misses:              50,000  (0.01% — отлично)
```

### AddressSanitizer (ASan)

```bash
gcc -fsanitize=address -g program.c -o program
./program

# Находит:
# - Heap buffer overflow
# - Stack buffer overflow
# - Use after free
# - Use after return
# - Memory leaks
# Overhead: ~2× по памяти, ~2× по времени
```

### Intel Memory Latency Checker (MLC)

```bash
mlc --latency_matrix   # NUMA latency matrix
mlc --bandwidth_matrix # NUMA bandwidth matrix
mlc --peak_injection_bandwidth  # пиковая полоса пропускания
```

### /proc и /sys — информация о памяти Linux

```bash
cat /proc/meminfo           # детальная информация о памяти
cat /proc/slabinfo          # slab allocator статистика
cat /proc/buddyinfo         # состояние buddy allocator
cat /sys/devices/system/node/node0/meminfo  # NUMA node 0
cat /proc/vmstat            # виртуальная память статистика

# Мониторинг:
watch -n 1 free -h          # RAM/swap в реальном времени
vmstat 1                    # виртуальная память, swap I/O
sar -r 1                    # детальная статистика памяти
```

## Технология DRAM: Rowhammer и защита

### Rowhammer атака

Физическая уязвимость DRAM (открыта в 2014):
Частое обращение к одной строке DRAM вызывает случайные bit flips в соседних строках.
Cause: электромагнитные помехи при зарядке/разрядке конденсаторов.

Эксплойт: изменить bit в page table → получить доступ к привилегированной памяти.

**Защиты**:
- Target Row Refresh (TRR): обновляет соседние строки при частом обращении
- ECC: исправляет одиночные ошибки
- Более частый refresh (повышение tREFI)
- LPDDR5/DDR5: обязательный PRAC (Per-Row Activation Counting)

### DDR5 On-Die ECC

Встроенный ECC прямо в DRAM чип (независимо от системного ECC на плате).
Исправляет ошибки внутри чипа до отправки данных контроллеру.
Снижает частоту ошибок, облегчает TRR.

## Оптимальное использование памяти в ML/AI

Модели нейронных сетей ограничены пропускной способностью памяти:

```
GPT-3 (175B параметров):
  float16: 350 GB
  A100 HBM2 memory: 80 GB × N GPU
  Нужно: 5+ GPU только для загрузки модели

Пропускная способность A100 HBM2: 2 TB/s
  Чтение 350 GB параметров: ~175 мс
  При 1000 tokens/sec inference: доминируют memory reads

Оптимизации:
  1. Quantization: float16 → int8 → int4 (в 2-4× меньше памяти)
  2. Tensor Parallelism: разбить матрицы по GPU
  3. Pipeline Parallelism: разные слои на разных GPU
  4. FlashAttention: tiles attention в кэше GPU для меньшего HBM трафика
  5. KV Cache: кэш key/value при autoregressive generation
```

FlashAttention (принцип):
```
Стандартный attention: O(N²) памяти (матрица N×N хранится в HBM)
FlashAttention: tiling → блоки помещаются в SRAM GPU (L1 аналог)
  → в 3-4× меньше HBM reads/writes
  → в 2-4× быстрее для длинных контекстов
```

## Итоговые факты о памяти

```
Главный принцип: локальность важнее скорости процессора.
  Программа с плохой локальностью на быстром CPU < программы с хорошей
  локальностью на медленном CPU.

Золотые правила:
1. Sequential access >> Random access (prefetcher работает)
2. Small working set >> Large (помещается в кэш)
3. SoA >> AoS для SIMD-обработки
4. Avoid false sharing (выравнивание по 64B)
5. Hugepages для больших буферов (меньше TLB-промахов)
6. NUMA-aware аллокация (память близко к CPU)
7. Pool allocators для частых alloc/free

Числа наизусть (latency numbers 2024):
  L1 cache:    4 нс  (5 тактов @ ~3.5 GHz)
  L2 cache:   12 нс  (12 тактов)
  L3 cache:   40 нс  (40-50 тактов)
  DRAM:       80 нс  (основная RAM)
  NVMe SSD: 100 мкс  (в 1250× медленнее RAM!)
  HDD:       10 мс   (в 125000× медленнее RAM!)
  Сеть LAN:  0.5 мс  (RTT)
  Сеть WAN:   100 мс (RTT Москва-Нью-Йорк)
```
