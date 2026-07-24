// Rust Programming Language — Basic Examples
// New-mir seed training data

// ─── Variables and Types ──────────────────────────────────────────────────────

fn variables_demo() {
    // Immutable by default
    let x: i32 = 42;
    let name: &str = "New-mir";
    let pi: f64 = 3.14159;
    let flag: bool = true;

    // Mutable variables
    let mut counter: u64 = 0;
    counter += 1;

    // String ownership
    let owned: String = String::from("Hello, Rust!");
    let slice: &str = &owned[0..5];

    println!("x={x}, name={name}, pi={pi}, flag={flag}");
    println!("counter={counter}, slice={slice}");
}

// ─── Ownership and Borrowing ──────────────────────────────────────────────────

fn ownership_demo() {
    // Move semantics
    let s1 = String::from("hello");
    let s2 = s1; // s1 is moved, no longer valid

    // Clone to copy
    let s3 = String::from("world");
    let s4 = s3.clone(); // both s3 and s4 are valid
    println!("{s2} {s3} {s4}");

    // Borrowing (immutable reference)
    let len = calculate_length(&s4);
    println!("Length of '{s4}' is {len}");

    // Mutable borrowing
    let mut mutable_str = String::from("hello");
    change(&mut mutable_str);
    println!("{mutable_str}");
}

fn calculate_length(s: &String) -> usize {
    s.len() // s goes out of scope but doesn't drop the data
}

fn change(some_string: &mut String) {
    some_string.push_str(", world");
}

// ─── Structs ──────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
struct NeuralCell {
    id: String,
    capacity: usize,
    used: usize,
    data: Vec<u8>,
}

impl NeuralCell {
    fn new(id: &str, capacity: usize) -> Self {
        NeuralCell {
            id: id.to_string(),
            capacity,
            used: 0,
            data: Vec::new(),
        }
    }

    fn fill_ratio(&self) -> f64 {
        self.used as f64 / self.capacity as f64
    }

    fn is_full(&self) -> bool {
        self.fill_ratio() >= 0.70
    }

    fn write(&mut self, bytes: &[u8]) -> Result<(), &'static str> {
        if self.used + bytes.len() > self.capacity {
            return Err("Cell capacity exceeded");
        }
        self.data.extend_from_slice(bytes);
        self.used += bytes.len();
        Ok(())
    }
}

// ─── Enums and Pattern Matching ───────────────────────────────────────────────

#[derive(Debug)]
enum CompressionAlgorithm {
    Lz4,
    Zstd { level: i32 },
    Zlib,
    None,
}

fn compress(data: &[u8], algo: &CompressionAlgorithm) -> Vec<u8> {
    match algo {
        CompressionAlgorithm::Lz4 => {
            println!("Compressing with LZ4");
            data.to_vec() // placeholder
        }
        CompressionAlgorithm::Zstd { level } => {
            println!("Compressing with Zstd level {level}");
            data.to_vec()
        }
        CompressionAlgorithm::Zlib => {
            println!("Compressing with zlib");
            data.to_vec()
        }
        CompressionAlgorithm::None => data.to_vec(),
    }
}

// ─── Traits ───────────────────────────────────────────────────────────────────

trait Encode {
    fn encode(&self, data: &[u8]) -> Vec<String>;
    fn decode(&self, slots: &[String]) -> Vec<u8>;
    fn slot_count(&self) -> usize;
}

struct QrEncoder {
    slots: Vec<(String, Vec<u8>)>,
}

impl QrEncoder {
    fn new() -> Self {
        QrEncoder { slots: Vec::new() }
    }
}

impl Encode for QrEncoder {
    fn encode(&self, data: &[u8]) -> Vec<String> {
        // Real implementation would generate QR matrices
        vec![format!("slot_{}", data.len())]
    }

    fn decode(&self, slots: &[String]) -> Vec<u8> {
        // Real implementation would decode QR matrices
        slots.join(",").into_bytes()
    }

    fn slot_count(&self) -> usize {
        self.slots.len()
    }
}

// ─── Error Handling ───────────────────────────────────────────────────────────

use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
enum AppError {
    ParseError(ParseIntError),
    IoError(String),
    TrainingError { filename: String, reason: String },
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::ParseError(e) => write!(f, "Parse error: {e}"),
            AppError::IoError(msg) => write!(f, "I/O error: {msg}"),
            AppError::TrainingError { filename, reason } => {
                write!(f, "Training error for '{filename}': {reason}")
            }
        }
    }
}

fn parse_cell_id(s: &str) -> Result<u64, AppError> {
    s.parse::<u64>().map_err(AppError::ParseError)
}

// ─── Iterators and Closures ───────────────────────────────────────────────────

fn iterator_demo() {
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    // Map, filter, collect
    let even_squares: Vec<u32> = numbers
        .iter()
        .filter(|&&x| x % 2 == 0)
        .map(|&x| x * x)
        .collect();
    println!("Even squares: {even_squares:?}");

    // Sum and product
    let total: u32 = numbers.iter().sum();
    let product: u32 = numbers.iter().product();
    println!("Sum={total}, Product={product}");

    // Find and position
    let first_gt5 = numbers.iter().find(|&&x| x > 5);
    println!("First > 5: {first_gt5:?}");
}

// ─── Generics ─────────────────────────────────────────────────────────────────

fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

struct Pair<T> {
    first: T,
    second: T,
}

impl<T: std::fmt::Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.first >= self.second {
            println!("First is larger: {}", self.first);
        } else {
            println!("Second is larger: {}", self.second);
        }
    }
}

// ─── Async / Await ────────────────────────────────────────────────────────────

// async fn fetch_training_data(url: &str) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
//     let response = reqwest::get(url).await?;
//     let bytes = response.bytes().await?;
//     Ok(bytes.to_vec())
// }

// ─── Main ──────────────────────────────────────────────────────────────────────

fn main() {
    println!("=== New-mir Rust Training Data ===\n");

    variables_demo();
    ownership_demo();
    iterator_demo();

    let cell = NeuralCell::new("cell_001", 1024);
    println!("\nCell: {:?}", cell);
    println!("Fill ratio: {:.2}%", cell.fill_ratio() * 100.0);
    println!("Is full: {}", cell.is_full());

    let algo = CompressionAlgorithm::Zstd { level: 3 };
    let data = b"Hello, Rust!";
    let compressed = compress(data, &algo);
    println!("\nCompressed {} -> {} bytes", data.len(), compressed.len());

    let numbers = vec![34, 50, 25, 100, 65];
    println!("\nLargest number: {}", largest(&numbers));
}
