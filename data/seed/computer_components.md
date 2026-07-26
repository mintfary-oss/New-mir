# Компоненты компьютера и серверного оборудования

## Системная плата (Motherboard)

Материнская плата — основа системы, соединяет все компоненты.

### Ключевые элементы материнской платы

**Чипсет (Chipset / PCH)**
Platform Controller Hub — управляет периферией: USB, SATA, PCIe нижнего яруса.
Intel Z790: PCIe 4.0 x16 для PCH lanes, USB 3.2 Gen2x2 (20 Gbps).
AMD X670E: два чипсета (Promontory21), PCIe 5.0.

**Сокет процессора**
```
Intel LGA 1700 — Core 12/13/14 поколение (контакты на плате, CPU без иголок)
Intel LGA 1851 — Core Ultra 200 (Arrow Lake)
AMD AM5        — Ryzen 7000/8000/9000 (LGA, 1718 контактов, DDR5)
AMD AM4        — Ryzen 1000-5000 (LGA, DDR4)
Intel LGA 4677 — Xeon Sapphire Rapids (server)
AMD SP5        — EPYC Genoa (server, 6096 контактов)
```

**Слоты расширения**
```
PCIe x16  — видеокарты (GPU)
PCIe x4   — NVMe SSD (M.2 слоты), сетевые карты
PCIe x1   — звуковые карты, контроллеры
M.2       — NVMe/SATA SSD (2242, 2260, 2280, 22110 форм-факторы)
```

**Слоты памяти**
DIMM (Dual Inline Memory Module):
- DDR4: 288 пинов, 1.2V
- DDR5: 288 пинов (другое расположение!), 1.1V, встроенный PMIC

**Разъёмы питания**
24-pin ATX: основное питание платы
8-pin EPS (4+4): питание CPU
Дополнительные 8-pin: для разгона на high-end платах

**VRM (Voltage Regulator Module)**
Преобразует 12V в точное напряжение для CPU (~0.8-1.4V).
Состав: PWM-контроллер, дроссели (индукторы), MOSFETы, конденсаторы.
Количество фаз: 8-phase — бюджет, 16-phase — mainstream, 20+ phase — enthusiast.
CPU потребляет 100-300A при напряжении ~1V → мощные VRM критичны.

**Аудио**
ЦАП (DAC): Realtek ALC4080 (встроенный), ESS Sabre (high-end платы).
Линейный выход: 2 Vrms (DAC) → усилитель → наушники/колонки.
Разделение аналоговой и цифровой частей PCB снижает шум.

### Форм-факторы материнских плат
```
E-ATX  — 305 × 330 мм (workstation/HEDT)
ATX    — 305 × 244 мм (стандарт для desktop)
Micro-ATX — 244 × 244 мм (компактные системы)
Mini-ITX  — 170 × 170 мм (компактные ПК)
Mini-STX  — 147 × 140 мм (ультракомпакт)
Server: EATX, SSI-CEB, SSI-EEB
```

## Видеокарта (GPU — Graphics Processing Unit)

### Архитектура GPU

GPU и CPU — принципиально разные:
```
CPU: 8-24 мощных ядра (P-cores)    → оптимизирован для латентности
GPU: 10000+ слабых ядра (shaders)  → оптимизирован для throughput
```

NVIDIA RTX 4090 (Ada Lovelace):
```
Shader Processors (CUDA cores): 16384
Tensor Cores (AI): 512
RT Cores (Ray Tracing): 128
L2 Cache: 72 MB
Memory: 24 GB GDDR6X, 384-bit bus, 1008 GB/s
TDP: 450W
Техпроцесс: TSMC 4нм
Производительность FP32: 82.6 TFLOPS
Производительность INT8 (AI): 1321 TOPS
```

### Типы шейдеров
```
Vertex Shader   — преобразование 3D координат → 2D экран
Pixel/Fragment  — цвет каждого пикселя
Geometry Shader — генерация/изменение примитивов
Compute Shader  — общие вычисления (GPGPU)
Ray Generation  — трассировка лучей
```

### Streaming Multiprocessors (SM) — NVIDIA
Базовый блок GPU. RTX 4090 = 128 SM.
Каждый SM содержит:
- 128 CUDA cores (FP32)
- 4 Tensor Cores
- 1 RT Core
- 256KB Register File
- 128KB L1/Shared Memory

Warp = 32 потока, выполняются одновременно (SIMT).
Если потоки в warp расходятся (if/else) → divergence → потеря эффективности.

### VRAM (Video RAM)
```
GDDR6:   до 18 Gbps per pin, wide bus (256-bit)
GDDR6X:  до 21 Gbps (PAM4 encoding), RTX 3000/4000
GDDR7:   до 32 Gbps, RTX 5000
HBM2e:   307 GB/s, 3D стек (AMD MI300, NVIDIA H100)
HBM3:    665 GB/s per stack (AMD MI300X: 4 стека = 2.4 TB/s)
```

HBM (High Bandwidth Memory) — память монтируется прямо на interposer рядом с GPU.
Короткие соединения → огромная пропускная способность.

### AI-ускорители (Data Center GPU)
```
NVIDIA H100 SXM5:
  FP16: 2000 TFLOPS
  INT8: 4000 TOPS
  FP8:  8000 TOPS (Transformer Engine)
  HBM3: 80 GB, 3.35 TB/s
  NVLink: 900 GB/s (межGPU)
  TDP: 700W

AMD MI300X:
  FP16: 1307 TFLOPS
  HBM3: 192 GB, 5.3 TB/s (!)
  Infinity Fabric: 896 GB/s
```

### GPU API и GPGPU
```
OpenGL     — кроссплатформенная 3D графика (OpenGL 4.6)
Vulkan     — низкоуровневый API, меньше overhead
DirectX 12 — Windows, Xbox (аналог Vulkan)
Metal      — Apple (macOS, iOS)

CUDA       — NVIDIA GPGPU (C++, Python биндинги)
ROCm/HIP   — AMD GPGPU (совместим с CUDA API)
OpenCL     — кроссплатформенное GPGPU (устаревает)
SYCL       — Intel oneAPI, кроссплатформенное
WebGPU     — GPGPU в браузере
```

## Оперативная память (RAM)

### Типы DDR памяти
```
DDR4-3200: 25.6 GB/s, 1.2V, JEDEC
DDR4-4800: 38.4 GB/s (overclocked)
DDR5-4800: 38.4 GB/s, 1.1V, JEDEC baseline
DDR5-6400: 51.2 GB/s (AMD EXPO / Intel XMP 3.0)
DDR5-8000+: 64+ GB/s (overclocked enthusiast)
```

Параметры (тайминги): CL-tRCD-tRP-tRAS
DDR5-6000 CL30: 30-36-36-76
- CL (CAS Latency): задержка от команды READ до данных
- tRCD: Row to Column Delay
- tRP: Row Precharge time
- tRAS: Active to Precharge

Первичная латентность = CL / (частота в MHz) × 2000 нс
DDR5-6000 CL30: 30 / 6000 × 2000 = 10 нс

### ECC (Error Correcting Code)
Память с коррекцией ошибок — обязательна для серверов.
SECDED: Single Error Correct, Double Error Detect.
Добавляет 8 бит (1 байт) на каждые 64 бит → 72-бит физическая шина.
Алгоритм: коды Хэмминга расширенные.

Стоимость: +~10% к цене, незначительное снижение пропускной способности.
NVIDIA H100: HBM3 с ECC — критично для AI вычислений.

### DIMM конфигурации
```
Single-channel: 1 модуль, один 64-бит канал
Dual-channel:   2 модуля, два 64-бит канала → 2× bandwidth
Quad-channel:   4 модуля (Intel X-series, Xeon, AMD EPYC)
8-channel:      EPYC Genoa → 8× 64-бит = 512-бит шина памяти
```

AMD EPYC 9654 (96 ядер): 12 каналов DDR5-4800 → ~460 GB/s.

### LPDDR (Low Power DDR)
Для ноутбуков и мобильных устройств. Припаяна к плате (on-package у Apple).
LPDDR5X-8533: 68 GB/s (4×16-бит канала).
Apple M3 Max: LPDDR5X, 400 GB/s (unified memory).

## Накопители данных

### NVMe SSD (PCIe)

NVMe (Non-Volatile Memory Express) — протокол для SSD через PCIe.
Замена AHCI (для HDD/SATA SSD) — NVMe специально для flash.

```
Samsung 990 Pro (PCIe 4.0 x4):
  Чтение: 7450 MB/s
  Запись: 6900 MB/s
  4K IOPS: 1400K read / 1550K write
  Латентность: ~0.05 мс

WD Black SN850X (PCIe 4.0 x4):
  Чтение: 7300 MB/s
  Запись: 6600 MB/s

PCIe 5.0 NVMe (Samsung 9100 Pro, 2024):
  Чтение: 14800 MB/s
  Запись: 13400 MB/s
```

### Устройство NAND Flash
```
SLC (Single Level Cell): 1 бит/ячейка — быстро, дорого, долговечно
MLC (Multi Level Cell):  2 бит/ячейка
TLC (Triple Level Cell): 3 бит/ячейка — mainstream
QLC (Quad Level Cell):   4 бит/ячейка — дёшево, медленно, меньше записей
PLC (Penta Level Cell):  5 бит/ячейка (экспериментальные)
```

3D NAND: ячейки уложены в вертикальные слои (V-NAND).
Samsung V-NAND 9th gen: 290 слоёв.
Micron 3D NAND: 232 слоя.

Wear leveling: контроллер SSD равномерно распределяет записи.
TBW (Terabytes Written): гарантированный ресурс записи.
Samsung 990 Pro 2TB: 1200 TBW.

### SATA SSD vs NVMe
```
SATA III:  600 MB/s max (AHCI protocol overhead)
NVMe PCIe 4.0: 7000+ MB/s
```

SATA SSD (Samsung 870 EVO): достаточно для большинства задач (не узкое место).
NVMe необходим: видеомонтаж 4K+, виртуальные машины, базы данных.

### HDD (Hard Disk Drive)

Механический накопитель — магнитные пластины + головки чтения/записи.
```
Принцип: пластина крутится (5400/7200/10000/15000 RPM).
Головка летит над поверхностью на 3-5 нанометров (air bearing).
Треки (tracks) → секторы (sectors, 512B/4KB).

Скорость:
  Последовательное чтение: 150-300 MB/s (7200 RPM)
  Случайный доступ 4K: 0.5-1 MB/s (!)
  Латентность: 5-15 мс (поворот пластины + перемещение головки)

Ёмкость: до 30 TB (Seagate HAMR, 2024)
```

Технологии увеличения плотности:
- PMR (Perpendicular Magnetic Recording): перпендикулярная запись
- SMR (Shingled Magnetic Recording): перекрывающиеся треки, дешевле
- HAMR (Heat-Assisted Magnetic Recording): лазер нагревает при записи
- MAMR (Microwave-Assisted): микроволны снижают коэрцитивную силу

Применение HDD: архивное хранение, NAS, backup (низкая стоимость/TB).

### Оптические накопители (исторически)
```
CD-ROM:   700 MB,  150 KB/s (1×), ИК лазер 780нм
DVD:      4.7 GB,  1.39 MB/s (1×), красный лазер 650нм
Blu-ray:  25/50GB, 4.5 MB/s (1×), синий лазер 405нм
```

## Блок питания (PSU — Power Supply Unit)

### Преобразование напряжений
Входное: 100-240V AC, 50/60 Hz.
Выходные напряжения:
```
+12V: процессор, видеокарта, моторы — основная нагрузка
+5V:  USB, некоторые логические схемы
+3.3V: DIMM (старые платы), M.2 слоты
-12V:  RS-232 (устаревший COM-порт)
+5VSB: дежурное питание (ATX always-on, Wake-on-LAN)
```

### Топологии схем PSU

**Flyback**: простой, дешёвый, для PSU < 500W.
**LLC resonant + SR**: эффективный (~90-95%), mainstream.
**Full Bridge**: высокомощные блоки 1000W+.

### Сертификаты 80 PLUS
```
80 PLUS Bronze:  82/85/82% КПД при 20/50/100% нагрузке
80 PLUS Silver:  85/88/85%
80 PLUS Gold:    87/90/87%
80 PLUS Platinum: 90/92/89%
80 PLUS Titanium: 92/94/90%
```

Высокий КПД = меньше тепла, меньше счёт за электричество.
Разница Gold vs Titanium на 1000W системе при 24/7: ~15 Вт → ~100 кВт·ч/год (~10$).

### Разъёмы PSU
```
24-pin ATX     — материнская плата (питание чипсета, слотов)
8-pin EPS      — CPU (4+4 для совместимости)
6+2 pin PCIe   — видеокарты (до 150W каждый)
12+4 pin (12VHPWR) — RTX 4000/5000 (до 600W!)
SATA power     — накопители, вентиляторы
4-pin Molex    — старые устройства (устаревает)
```

ATX 3.0 стандарт (2022): нативный 16-pin 12VHPWR, поддержка пиковых нагрузок.

### Расчёт мощности системы
```
CPU: TDP × 1.1 (реальное потребление выше TDP под нагрузкой)
GPU: TDP × 1.1
RAM: ~5-10W total
NVMe: ~5-10W
Motherboard: ~50-80W
Fans: ~5W each
Total × 1.15 (запас)

Пример: i9-13900K (253W) + RTX 4090 (450W) + остальное ~150W = 850W → PSU 1000W
```

## Система охлаждения

### Воздушное охлаждение CPU

**Термоинтерфейс (Thermal Interface Material — TIM)**
Термопаста заполняет микронеровности между теплораспределителем (IHS) и кулером.
Типы:
- MX-4, NT-H1: ~8-12 W/m·K, безопасны, не токопроводящие
- Kryonaut Extreme: ~14 W/m·K, лучшая паста
- Жидкий металл (Conductonaut): 73 W/m·K — только для опытных (проводит ток!)

Деградация пасты: ~5-10°C прирост за 5-7 лет (высыхание).

**Башенные кулеры (Tower Coolers)**
```
Noctua NH-D15: 2 башни, 6 тепловых трубок, 140мм вентиляторы
  Рассеивание: ~250W TDP
  Уровень шума: ~19 dBA
  Масса: 1100г (требует усиленное крепление платы!)

be quiet! Dark Rock Pro 4: 7 тепловых трубок, 250W TDP
Thermalright Peerless Assassin 120: отличное соотношение цена/качество
```

Тепловые трубки (heat pipes): испарительно-конденсационный цикл.
Жидкость испаряется у основания (горячая зона) → пар идёт к верху → конденсируется → возвращается.
Эффективность: 10-100× выше меди при той же массе.

**Испарительные камеры (Vapor Chambers)**
Аналог тепловой трубки, но 2D распределение тепла.
Используются в ноутбуках, консолях, топовых кулерах.
Apple M-series чипы: vapor chamber в MacBook Pro.

### Жидкостное охлаждение (AIO / Custom loop)

**AIO (All-In-One) — необслуживаемые СЖО**
```
Corsair H150i Elite (360мм радиатор):
  Рассеивание: 350W+
  Размеры: 3 × 120мм вентилятора
  Помпа: ~2800 RPM, встроена в блок CPU

Arctic Liquid Freezer III 360: отличное охлаждение/цена
```

**Custom Loop (кастомная СЖО)**
Компоненты: помпа, резервуар (reservoir), радиатор, водоблоки (CPU, GPU, RAM).
Теплоноситель: дистиллированная вода + антикоррозионная добавка (Inhibitor).
Пропускная способность: 1-2 л/мин типично.
Эффективность: до 1.5-2°C/W (vs 0.5°C/W у лучших AIO).

### Серверное охлаждение

**High-performance fans**
```
Nidec, Delta, Sanyo Denki — промышленные серверные вентиляторы
6000-20000 RPM
80+ CFM при высоком статическом давлении
Уровень шума: 60-75 dBA (сервер в стойке = очень громко!)
```

**Жидкостное охлаждение в ЦОД**
- Direct Liquid Cooling (DLC): жидкость подводится прямо к серверу
- Rear Door Heat Exchanger: теплообменник на задней двери стойки
- Immersion cooling: серверы погружены в диэлектрическую жидкость (3M Novec, mineral oil)

NVIDIA DGX H100 (8× H100 GPU): требует 10 кВт охлаждения.
Liquid cooling: снижает PUE (Power Usage Effectiveness) до 1.03-1.1.

## Сетевое оборудование

### Сетевые карты (NIC — Network Interface Card)

**Ethernet**
```
1 GbE  — стандарт desktop/workstation (125 MB/s реально ~117 MB/s)
2.5 GbE — gaming motherboards, NAS (312 MB/s)
10 GbE — сервера, high-end NAS, workstation
25 GbE — серверы в ЦОД
100 GbE — spine/leaf коммутаторы в ЦОД
400 GbE — гиперскейлеры (Meta, Google)
```

**RDMA (Remote Direct Memory Access)**
Передача данных напрямую между RAM разных серверов без CPU.
InfiniBand (IB): 400 Gb/s HDR, латентность <1 мкс.
RoCE (RDMA over Converged Ethernet): RDMA поверх Ethernet.
iWARP: RDMA поверх TCP/IP.

NVIDIA H100 DGX: 8× H100 GPU соединены NVLink (900 GB/s), InfiniBand для межузловой связи.

**DPDK (Data Plane Development Kit)**
Обход ядра Linux для обработки пакетов в userspace.
Производительность: 100+ Mpps (millions of packets per second).

### Wi-Fi стандарты
```
Wi-Fi 5  (802.11ac):  3.5 Gbps теоретически, 5 ГГц
Wi-Fi 6  (802.11ax):  9.6 Gbps, 2.4/5 ГГц, OFDMA, MU-MIMO 8×8
Wi-Fi 6E (802.11ax):  6 ГГц диапазон добавлен, меньше интерференции
Wi-Fi 7  (802.11be):  46 Gbps теоретически, Multi-Link Operation (MLO)
                      320 МГц каналы, 4096-QAM
```

## Системы хранения данных (Storage Arrays)

### RAID (Redundant Array of Independent Disks)
```
RAID 0: Striping — данные распределены по дискам
  Скорость: N× (N дисков)
  Отказоустойчивость: 0 (один диск → всё потеряно!)

RAID 1: Mirroring — полная копия на каждом диске
  Скорость чтения: N×, записи: 1×
  Отказоустойчивость: N-1 дисков могут упасть

RAID 5: Striping + Parity
  Минимум: 3 диска
  Ёмкость: (N-1) × disk size
  Отказоустойчивость: 1 диск
  Rebuild time: часы-дни (для 10TB+ дисков: рискованно)

RAID 6: Dual Parity
  Минимум: 4 диска
  Отказоустойчивость: 2 диска
  Рекомендуется для дисков 8TB+

RAID 10: RAID 1+0 (зеркало + страйп)
  Минимум: 4 диска (по 2 в зеркалах)
  Лучший баланс производительности и надёжности
  Используется в MySQL production: RAID 10 SSD

ZFS RAID-Z2: аналог RAID 6, но с copy-on-write и checksums
```

### NAS (Network Attached Storage)
Сетевое хранилище, подключается через Ethernet.
Протоколы: NFS (Linux/Unix), SMB/CIFS (Windows), iSCSI, AFP (Apple).

Synology DS1823xs+, QNAP TS-h1290FX — примеры enterprise NAS.
Seagate IronWolf Pro / WD Gold — NAS-оптимизированные HDD.

### SAN (Storage Area Network)
Сеть хранения данных, блочный доступ (iSCSI, Fibre Channel).
Fibre Channel: 16/32/64 Gbps, специальные HBA-карты.
Используется в enterprise для shared storage (VMware vSAN, Oracle RAC).

## Серверное оборудование

### Форм-факторы серверов

**Tower (башня)**
Как обычный ПК. Для малого бизнеса, тихих помещений.
Dell PowerEdge T550, HP ProLiant ML350.

**Rack-mount (монтируемые в стойку)**
```
1U: 44.45мм высота — плотность, экономия места
2U: 88.9мм — больше места для карт, охлаждения
4U: 177.8мм — GPU серверы, много слотов
```
Стойка: 42U стандарт (1.8м), 19" ширина.

**Blade серверы**
Шасси (blade enclosure) + вычислительные лезвия.
Общие блоки питания, вентиляторы, сетевые модули.
Высокая плотность: HP BladeSystem c7000 = 16 лезвий в 10U.

**HPC (High Performance Computing)**
```
NVIDIA DGX H100:
  8× H100 SXM5 GPU
  2× Intel Xeon Platinum 8480+
  2TB DDR5 RAM
  8× 3.84TB NVMe
  8× 400 GbE (InfiniBand HDR)
  TDP: 10.2 кВт
  Цена: ~250 000$
```

### Процессоры для серверов

**Intel Xeon**
```
Xeon Scalable 3rd gen (Ice Lake-SP):
  До 40 ядер, DDR4-3200, PCIe 4.0
  8-channel memory, 6TB max
  TDP: 270W

Xeon Scalable 4th gen (Sapphire Rapids):
  До 60 ядер, DDR5-4800, PCIe 5.0
  AMX (AI acceleration built-in)
  TDP: до 350W
  EMIB (Embedded Multi-die Interconnect Bridge) packaging
```

**AMD EPYC**
```
EPYC 7003 "Milan" (Zen 3):
  До 64 ядер, DDR4-3200, PCIe 4.0
  8-channel, 4TB RAM
  TDP: до 280W

EPYC 9004 "Genoa" (Zen 4):
  До 96 ядер, DDR5-4800, PCIe 5.0
  12-channel, 6TB RAM
  TDP: до 400W
  AVX-512 поддержка

EPYC 9005 "Turin" (Zen 5, 2024):
  До 192 ядер (!), DDR5
```

**ARM серверы**
```
Ampere Altra Max:
  128 ядер (ARM Neoverse N1)
  8-channel DDR4, PCIe 4.0
  TDP: 250W

AWS Graviton 4 (ARM Neoverse V2):
  96 ядер, DDR5, отличная однопоточная производительность
  Используется в EC2 c8g/m8g instances

Apple M2 Ultra:
  24 ядра CPU, 76 ядер GPU
  Используется в Mac Studio/Mac Pro
```

### Серверная память (RDIMM, LRDIMM)

**RDIMM (Registered DIMM)**
Буферизованная память: дополнительный регистр буферирует сигналы.
Снижает нагрузку на memory controller → больше DIMM на канал.
Стандарт для серверов: до 16 RDIMM на 8-channel.

**LRDIMM (Load-Reduced DIMM)**
Более сложный буфер, изолирует нагрузку полностью.
Позволяет: до 6TB RAM на socket (Intel Xeon).
Чуть выше латентность, чем RDIMM.

**3DS (3D Stacked) RDIMM**
DRAM чипы стекованы вертикально.
128GB RDIMM на базе 3DS → экстремально большой RAM.

### IPMI / BMC (Baseboard Management Controller)

Отдельный микроконтроллер на плате — работает даже при выключенном сервере.
Аппаратный KVM (Keyboard, Video, Mouse) по сети.
```
Функции:
  - Удалённая перезагрузка/включение/выключение
  - Мониторинг температур, напряжений, скорости вентиляторов
  - Serial over LAN (SOL) — консоль по сети
  - Virtual Media — монтирование ISO образа
  - SNMP-трапы при аварии
  - Power capping (ограничение потребления)

Протокол: IPMI 2.0, Redfish (современный REST API)
Реализации: iDRAC (Dell), iLO (HPE), IPMI (Supermicro, ASRock Rack)
```

### PCIe карты расширения для серверов

**HBA (Host Bus Adapter) — Fibre Channel**
Broadcom/LSI HBA: 16/32 Gbps FC, подключение к SAN.

**RAID-контроллер**
Broadcom MegaRAID, Adaptec: RAID 5/6/10 для HDD/SSD.
Cache: до 8GB DRAM для write-back кэширования.
BBU (Battery Backup Unit): защита кэша при отключении питания.

**SmartNIC / DPU (Data Processing Unit)**
NVIDIA BlueField-3, Intel IPU: сетевая карта со встроенным ARM процессором.
Разгружает CPU: шифрование (TLS), NVMe-oF, Open vSwitch, firewall.
Использование: ЦОД, SDN (Software Defined Networking).

## Коммутаторы и сетевые стойки

### Spine-Leaf топология ЦОД
```
          [Spine 1] [Spine 2] [Spine 3]
             ↕↕↕        ↕↕↕        ↕↕↕
[Leaf 1] [Leaf 2] [Leaf 3] [Leaf 4] [Leaf 5]
   |         |        |        |        |
 Rack1     Rack2    Rack3    Rack4    Rack5
```
Каждый leaf соединён с каждым spine → любые два сервера = 2 хопа.
Масштабируется горизонтально: добавляем листья и шипы.

### Коммутаторы (Switches)
```
Cisco Catalyst 9300: L3 switch, 48×1GbE, 4×10GbE uplink
Cisco Nexus 93180YC-FX: 48×10/25GbE + 6×100GbE (ЦОД)
Arista 7060CX2-32S: 32×100GbE (spine в ЦОД)
NVIDIA Quantum-2 NDR: 64 порта × 400 Gbps InfiniBand (HPC)
```

### Кабели
```
DAC (Direct Attach Copper): до 5м, дешевле, фиксированная скорость
AOC (Active Optical Cable): >10м, оптика + трансивер встроен
Трансиверы: SFP+ (10G), SFP28 (25G), QSFP28 (100G), QSFP-DD (400G)
Одномодовое (SMF): дальние расстояния (>100м), дороже
Многомодовое (MMF): до 400м, дешевле, для ЦОД внутри
```

## Источники бесперебойного питания (UPS)

### Топологии UPS

**Standby (offline)**
Инвертор включается при потере питания (~5-20 мс переключение).
Для не критичных устройств, SOHO.

**Line-Interactive**
Автотрансформатор регулирует напряжение без переключения на батарею.
Время переключения: 2-4 мс.
APC Smart-UPS SMT 1500 — популярная модель.

**Double-Conversion (Online)**
Всегда работает через инвертор: AC → DC → AC.
Нулевое время переключения, чистая синусоида.
Для серверов, медоборудования.
Eaton 9PX, APC Symmetra — enterprise класс.

### Батареи UPS
VRLA AGM (Sealed Lead Acid): стандарт, 3-5 лет замена.
Li-ion: дороже, дольше живут (8-10 лет), меньше весят, быстрее заряжаются.
Eaton предлагает Li-ion в своих UPS.

Расчёт времени работы:
Ёмкость батареи (Вт·ч) / Нагрузка (Вт) = время (ч)
100 А·ч × 12В = 1200 Вт·ч / 500 Вт = 2.4 часа

## Специализированные ускорители

### TPU (Tensor Processing Unit) — Google
```
TPU v4 (2021):
  275 TFLOPS BF16
  32 GB HBM2 per chip
  4096 chips в Pod
  Pod: 1.1 EFLOPS (1100 PFLOPS)
  Используется для обучения моделей (PaLM, Gemini)
```

### FPGA (Field-Programmable Gate Array)
Перепрограммируемое железо: логические блоки (LUT, FF) + соединения.
Xilinx (AMD) Virtex UltraScale+: 9M Logic Cells.
Intel Stratix 10: встроенные HBM.

Применение:
- High-Frequency Trading: задержка <1 мкс
- Сетевая обработка (100GbE wirespeed)
- Pre-processing для ML inference
- SDR (Software Defined Radio)

### ASIC (Application-Specific Integrated Circuit)
Чип под конкретную задачу. Не перепрограммируемый, максимальная эффективность.
Bitcoin ASIC (Bitmain Antminer S21 Pro): 234 TH/s при 3531W.
Google TPU — тоже ASIC.

## Интерфейсы и разъёмы

### USB (Universal Serial Bus)
```
USB 2.0:   480 Mbps  (60 MB/s)
USB 3.2 Gen1: 5 Gbps    (625 MB/s)
USB 3.2 Gen2: 10 Gbps   (1.25 GB/s)
USB 3.2 Gen2×2: 20 Gbps (2.5 GB/s)
USB4 Gen2×2: 20 Gbps
USB4 Gen3×2: 40 Gbps
Thunderbolt 4: 40 Gbps (PCIe 4.0 x2 + DisplayPort 1.4)
Thunderbolt 5: 120 Gbps (bidirectional asymmetric)
USB-C: только форм-фактор разъёма, может нести USB2.0/3.x/4/TB
```

### DisplayPort / HDMI
```
DisplayPort 1.4: 32.4 Gbps → 8K@60Hz, HDR
DisplayPort 2.1: 80 Gbps → 16K@60Hz, 4K@240Hz
HDMI 2.1: 48 Gbps → 8K@60Hz, 4K@120Hz
```

### Thunderbolt
Intel разработка, лицензировано Apple.
TB4: 40 Gbps, обязателен PCIe tunnel 32 Gbps + DisplayPort 1.4.
TB5: 120 Gbps (40×3 Gbps симметричный или 80 Gbps downstream).
Daisy-chain до 6 устройств.

## Технологии охлаждения ЦОД

### PUE (Power Usage Effectiveness)
PUE = Total Facility Power / IT Equipment Power

PUE = 1.0: идеал (невозможно)
PUE = 1.1-1.2: отличный (жидкостное охлаждение)
PUE = 1.5: типичный ЦОД с воздушным охлаждением
PUE = 2.0+: старый/неэффективный ЦОД

Google: PUE 1.10, Meta: 1.11, Microsoft: 1.12.

### Холодные/горячие коридоры (Hot/Cold aisle containment)
```
     [Стойки front][Пространство][Стойки front]
      ← холодный воздух из пола ←
     [Стойки rear ][Пространство][Стойки rear ]
              → горячий воздух в потолок →
```

Cold aisle: +18-21°C, горячий воздух отводится сзади стоек.
Повышение температуры inlet: снижает затраты на охлаждение.
ASHRAE A2: inlet 10-35°C, рекомендуется 27°C.

### Immersion Cooling (погружное охлаждение)
Серверы погружаются в диэлектрическую жидкость.
Single-phase: 3M FC-40, mineral oil — жидкость остаётся жидкостью.
Two-phase: 3M Novec 7100 — кипит у сервера (56°C), конденсируется наверху.

Преимущества: PUE → 1.02, бесшумно, экономия воды.
Применение: Bitcoin mining, HPC, ультраплотные ЦОД.

## Мониторинг и управление инфраструктурой

### SNMP (Simple Network Management Protocol)
Протокол управления сетевым оборудованием.
MIB (Management Information Base) — иерархия объектов.
Версии: SNMPv1 (plain text), SNMPv2c, SNMPv3 (аутентификация, шифрование).

### DCIM (Data Center Infrastructure Management)
Программное управление ЦОД: мощность, охлаждение, место в стойках.
Nlyte, Vertiv Trellis, Schneider EcoStruxure.

### KVM over IP
IPMI + HTML5 virtual console.
ILO (HP), iDRAC (Dell), IPMI/Redfish (Supermicro).
Redfish API: современный REST замена IPMI.

### Мониторинг серверов
```bash
# Температуры и вентиляторы через lm-sensors
sensors                    # CPU/MB температуры
ipmitool sensor list       # все датчики через IPMI
ipmitool sdr list          # sensor data records
ipmitool chassis status    # статус шасси

# Дисковые температуры
smartctl -a /dev/sda       # SMART данные HDD/SSD
nvme smart-log /dev/nvme0  # NVMe health info

# Сеть
ethtool eth0               # скорость, дуплекс, статус
ip link show               # все интерфейсы
```

## Итоговая схема: путь данных в системе

```
Пользователь
    ↓
Клавиатура/Мышь → USB Controller → CPU (interrupt)
    ↓
CPU выполняет код:
  - Инструкции из I-кэша (L1, 4 такта)
  - Данные из D-кэша (L1, 5 тактов)
  - L2 промах → L3 (40 тактов)
  - L3 промах → RAM (80 нс = ~200 тактов @3 GHz)
    ↓
Memory Controller (встроен в CPU) ↔ DDR5 DIMM
    ↓
GPU (PCIe 5.0 x16 = 64 GB/s):
  - VRAM (GDDR7): 2 TB/s
  - Vertex → Fragment → Output
    ↓
Display (HDMI 2.1 или DP 2.1):
  - 4K@144Hz = 4096×2160×144×32бит ≈ 8 Gbps сырой поток
    ↓
Storage (NVMe PCIe 5.0):
  - Read: 14 GB/s (PCIe 5.0 x4)
  - NAND Flash: ~1 мкс latency
    ↓
Network (10/25/100 GbE):
  - через NIC → коммутатор → роутер → Интернет
```
