// Rust Programming Language — Basics for New-mir seed training

fn main() {
    println!("=== New-mir Rust Training Data ===");
    variables_demo();
    ownership_demo();
    iterator_demo();
}

// Variables and types
fn variables_demo() {
    let x: i32 = 42;
    let name: &str = "New-mir";
    let pi: f64 = 3.14159;
    let flag: bool = true;
    let mut counter: u64 = 0;
    counter += 1;
    let owned: String = String::from("Hello, Rust!");
    println!("x={x}, name={name}, pi={pi}, flag={flag}, counter={counter}");
    println!("owned={owned}");
}

// Ownership and borrowing
fn ownership_demo() {
    let s1 = String::from("hello");
    let s2 = s1.clone();
    println!("{s1} {s2}");
    let len = calculate_length(&s2);
    println!("Length: {len}");
    let mut mutable_str = String::from("hello");
    change(&mut mutable_str);
    println!("{mutable_str}");
}

fn calculate_length(s: &String) -> usize { s.len() }
fn change(s: &mut String) { s.push_str(", world"); }

// Structs
#[derive(Debug, Clone)]
struct NeuralCell {
    id: String,
    capacity: usize,
    used: usize,
}

impl NeuralCell {
    fn new(id: &str, capacity: usize) -> Self {
        NeuralCell { id: id.to_string(), capacity, used: 0 }
    }
    fn fill_ratio(&self) -> f64 { self.used as f64 / self.capacity as f64 }
    fn is_full(&self) -> bool { self.fill_ratio() >= 0.70 }
}

// Enums and pattern matching
#[derive(Debug)]
enum CompressionAlgo { Lz4, Zstd { level: i32 }, Zlib, None }

fn compress_name(algo: &CompressionAlgo) -> &str {
    match algo {
        CompressionAlgo::Lz4 => "lz4",
        CompressionAlgo::Zstd { level: _ } => "zstd",
        CompressionAlgo::Zlib => "zlib",
        CompressionAlgo::None => "none",
    }
}

// Error handling
#[derive(Debug)]
enum AppError { ParseError(String), IoError(String) }

fn parse_id(s: &str) -> Result<u64, AppError> {
    s.parse::<u64>().map_err(|e| AppError::ParseError(e.to_string()))
}

// Iterators and closures
fn iterator_demo() {
    let numbers = vec![1u32, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let even_squares: Vec<u32> = numbers.iter()
        .filter(|&&x| x % 2 == 0)
        .map(|&x| x * x)
        .collect();
    println!("Even squares: {even_squares:?}");
    let total: u32 = numbers.iter().sum();
    println!("Sum={total}");
}

// Generics
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list { if item > largest { largest = item; } }
    largest
}

// Traits
trait Encode {
    fn encode(&self, data: &[u8]) -> Vec<String>;
    fn slot_count(&self) -> usize;
}

struct QrEncoder { slots: Vec<String> }

impl QrEncoder {
    fn new() -> Self { QrEncoder { slots: Vec::new() } }
}

impl Encode for QrEncoder {
    fn encode(&self, data: &[u8]) -> Vec<String> {
        vec![format!("slot_{}", data.len())]
    }
    fn slot_count(&self) -> usize { self.slots.len() }
}
