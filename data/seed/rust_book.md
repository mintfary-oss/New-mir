# The Rust Programming Language Book

# Introduction

> Note: This edition of the book is the same as [The Rust Programming
> Language][nsprust] available in print and ebook format from [No Starch
> Press][nsp].

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Welcome to _The Rust Programming Language_, an introductory book about Rust.
The Rust programming language helps you write faster, more reliable software.
High-level ergonomics and low-level control are often at odds in programming
language design; Rust challenges that conflict. Through balancing powerful
technical capacity and a great developer experience, Rust gives you the option
to control low-level details (such as memory usage) without all the hassle
traditionally associated with such control.

## Who Rust Is For

Rust is ideal for many people for a variety of reasons. Let’s look at a few of
the most important groups.

### Teams of Developers

Rust is proving to be a productive tool for collaborating among large teams of
developers with varying levels of systems programming knowledge. Low-level code
is prone to various subtle bugs, which in most other languages can only be
caught through extensive testing and careful code review by experienced
developers. In Rust, the compiler plays a gatekeeper role by refusing to
compile code with these elusive bugs, including concurrency bugs. By working
alongside the compiler, the team can spend its time focusing on the program’s
logic rather than chasing down bugs.

Rust also brings contemporary developer tools to the systems programming world:

- Cargo, the included dependency manager and build tool, makes adding,
  compiling, and managing dependencies painless and consistent across the Rust
  ecosystem.
- The `rustfmt` formatting tool ensures a consistent coding style across
  developers.
- The Rust Language Server powers integrated development environment (IDE)
  integration for code completion and inline error messages.

By using these and other tools in the Rust ecosystem, developers can be
productive while writing systems-level code.

### Students

Rust is for students and those who are interested in learning about systems
concepts. Using Rust, many people have learned about topics like operating
systems development. The community is very welcoming and happy to answer
students’ questions. Through efforts such as this book, the Rust teams want to
make systems concepts more accessible to more people, especially those new to
programming.

### Companies

Hundreds of companies, large and small, use Rust in production for a variety of
tasks, including command line tools, web services, DevOps tooling, embedded
devices, audio and video analysis and transcoding, cryptocurrencies,
bioinformatics, search engines, Internet of Things applications, machine
learning, and even major parts of the Firefox web browser.

### Open Source Developers

Rust is for people who want to build the Rust programming language, community,
developer tools, and libraries. We’d love to have you contribute to the Rust
language.

### People Who Value Speed and Stability

Rust is for people who crave speed and stability in a language. By speed, we
mean both how quickly Rust code can run and the speed at which Rust lets you
write programs. The Rust compiler’s checks ensure stability through feature
additions and refactoring. This is in contrast to the brittle legacy code in
languages without these checks, which developers are often afraid to modify. By
striving for zero-cost abstractions—higher-level features that compile to
lower-level code as fast as code written manually—Rust endeavors to make safe
code be fast code as well.

The Rust language hopes to support many other users as well; those mentioned
here are merely some of the biggest stakeholders. Overall, Rust’s greatest
ambition is to eliminate the trade-offs that programmers have accepted for
decades by providing safety _and_ productivity, speed _and_ ergonomics. Give
Rust a try, and see if its choices work for you.

## Who This Book Is For

This book assumes that you’ve written code in another programming language, but
it doesn’t make any assumptions about which one. We’ve tried to make the
material broadly accessible to those from a wide variety of programming
backgrounds. We don’t spend a lot of time talking about what programming _is_
or how to think about it. If you’re entirely new to programming, you would be
better served by reading a book that specifically provides an introduction to
programming.

## How to Use This Book

In general, this book assumes that you’re reading it in sequence from front to
back. Later chapters build on concepts in earlier chapters, and earlier
chapters might not delve into details on a particular topic but will revisit
the topic in a later chapter.

You’ll find two kinds of chapters in this book: concept chapters and project
chapters. In concept chapters, you’ll learn about an aspect of Rust. In project
chapters, we’ll build small programs together, applying what you’ve learned so
far. Chapter 2, Chapter 12, and Chapter 21 are project chapters; the rest are
concept chapters.

**Chapter 1** explains how to install Rust, how to write a “Hello, world!”
program, and how to use Cargo, Rust’s package manager and build tool. **Chapter
2** is a hands-on introduction to writing a program in Rust, having you build
up a number-guessing game. Here, we cover concepts at a high level, and later
chapters will provide additional detail. If you want to get your hands dirty
right away, Chapter 2 is the place for that. If you’re a particularly
meticulous learner who prefers to learn every detail before moving on to the
next, you might want to skip Chapter 2 and go straight to **Chapter 3**, which
covers Rust features that are similar to those of other programming languages;
then, you can return to Chapter 2 when you’d like to work on a project applying
the details you’ve learned.

In **Chapter 4**, you’ll learn about Rust’s ownership system. **Chapter 5**
discusses structs and methods. **Chapter 6** covers enums, `match` expressions,
and the `if let` and `let...else` control flow constructs. You’ll use structs
and enums to make custom types.

In **Chapter 7**, you’ll learn about Rust’s module system and about privacy
rules for organizing your code and its public application programming interface
(API). **Chapter 8** discusses some common collection data structures that the
standard library provides: vectors, strings, and hash maps. **Chapter 9**
explores Rust’s error-handling philosophy and techniques.

**Chapter 10** digs into generics, traits, and lifetimes, which give you the
power to define code that applies to multiple types. **Chapter 11** is all
about testing, which even with Rust’s safety guarantees is necessary to ensure
that your program’s logic is correct. In **Chapter 12**, we’ll build our own
implementation of a subset of functionality from the `grep` command line tool
that searches for text within files. For this, we’ll use many of the concepts
we discussed in the previous chapters.

**Chapter 13** explores closures and iterators: features of Rust that come from
functional programming languages. In **Chapter 14**, we’ll examine Cargo in
more depth and talk about best practices for sharing your libraries with
others. **Chapter 15** discusses smart pointers that the standard library
provides and the traits that enable their functionality.

In **Chapter 16**, we’ll walk through different models of concurrent
programming and talk about how Rust helps you program in multiple threads
fearlessly. In **Chapter 17**, we build on that by exploring Rust’s async and
await syntax, along with tasks, futures, and streams, and the lightweight
concurrency model they enable.

**Chapter 18** looks at how Rust idioms compare to object-oriented programming
principles you might be familiar with. **Chapter 19** is a reference on
patterns and pattern matching, which are powerful ways of expressing ideas
throughout Rust programs. **Chapter 20** contains a smorgasbord of advanced
topics of interest, including unsafe Rust, macros, and more about lifetimes,
traits, types, functions, and closures.

In **Chapter 21**, we’ll complete a project in which we’ll implement a
low-level multithreaded web server!

Finally, some appendixes contain useful information about the language in a
more reference-like format. **Appendix A** covers Rust’s keywords, **Appendix
B** covers Rust’s operators and symbols, **Appendix C** covers derivable traits
provided by the standard library, **Appendix D** covers some useful development
tools, and **Appendix E** explains Rust editions. In **Appendix F**, you can
find translations of the book, and in **Appendix G** we’ll cover how Rust is
made and what nightly Rust is.

There is no wrong way to read this book: If you want to skip ahead, go for it!
You might have to jump back to earlier chapters if you experience any
confusion. But do whatever works for you.

<span id="ferris"></span>

An important part of the process of learning Rust is learning how to read the
error messages the compiler displays: These will guide you toward working code.
As such, we’ll provide many examples that don’t compile along with the error
message the compiler will show you in each situation. Know that if you enter
and run a random example, it may not compile! Make sure you read the
surrounding text to see whether the example you’re trying to run is meant to
error. In most situations, we’ll lead you to the correct version of any code
that doesn’t compile. Ferris will also help you distinguish code that isn’t
meant to work:

| Ferris                                                                                                           | Meaning                                          |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris with a question mark"/>            | This code does not compile!                      |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris throwing up their hands"/>                   | This code panics!                                |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris with one claw up, shrugging"/> | This code does not produce the desired behavior. |

In most situations, we’ll lead you to the correct version of any code that
doesn’t compile.

## Source Code

The source files from which this book is generated can be found on
[GitHub][book].

[book]: https://github.com/rust-lang/book/tree/main/src

# Getting Started

Let’s start your Rust journey! There’s a lot to learn, but every journey starts
somewhere. In this chapter, we’ll discuss:

- Installing Rust on Linux, macOS, and Windows
- Writing a program that prints `Hello, world!`
- Using `cargo`, Rust’s package manager and build system

## Installation

The first step is to install Rust. We’ll download Rust through `rustup`, a
command line tool for managing Rust versions and associated tools. You’ll need
an internet connection for the download.

> Note: If you prefer not to use `rustup` for some reason, please see the
> [Other Rust Installation Methods page][otherinstall] for more options.

The following steps install the latest stable version of the Rust compiler.
Rust’s stability guarantees ensure that all the examples in the book that
compile will continue to compile with newer Rust versions. The output might
differ slightly between versions because Rust often improves error messages and
warnings. In other words, any newer, stable version of Rust you install using
these steps should work as expected with the content of this book.

> ### Command Line Notation
>
> In this chapter and throughout the book, we’ll show some commands used in the
> terminal. Lines that you should enter in a terminal all start with `$`. You
> don’t need to type the `$` character; it’s the command line prompt shown to
> indicate the start of each command. Lines that don’t start with `$` typically
> show the output of the previous command. Additionally, PowerShell-specific
> examples will use `>` rather than `$`.

### Installing `rustup` on Linux or macOS

If you’re using Linux or macOS, open a terminal and enter the following command:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

The command downloads a script and starts the installation of the `rustup`
tool, which installs the latest stable version of Rust. You might be prompted
for your password. If the install is successful, the following line will appear:

```text
Rust is installed now. Great!
```

You will also need a _linker_, which is a program that Rust uses to join its
compiled outputs into one file. It is likely you already have one. If you get
linker errors, you should install a C compiler, which will typically include a
linker. A C compiler is also useful because some common Rust packages depend on
C code and will need a C compiler.

On macOS, you can get a C compiler by running:

```console
$ xcode-select --install
```

Linux users should generally install GCC or Clang, according to their
distribution’s documentation. For example, if you use Ubuntu, you can install
the `build-essential` package.

### Installing `rustup` on Windows

On Windows, go to [https://www.rust-lang.org/tools/install][install]<!-- ignore
--> and follow the instructions for installing Rust. At some point in the
installation, you’ll be prompted to install Visual Studio. This provides a
linker and the native libraries needed to compile programs. If you need more
help with this step, see
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!--
ignore -->.

The rest of this book uses commands that work in both _cmd.exe_ and PowerShell.
If there are specific differences, we’ll explain which to use.

### Troubleshooting

To check whether you have Rust installed correctly, open a shell and enter this
line:

```console
$ rustc --version
```

You should see the version number, commit hash, and commit date for the latest
stable version that has been released, in the following format:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

If you see this information, you have installed Rust successfully! If you don’t
see this information, check that Rust is in your `%PATH%` system variable as
follows.

In Windows CMD, use:

```console
> echo %PATH%
```

In PowerShell, use:

```powershell
> echo $env:Path
```

In Linux and macOS, use:

```console
$ echo $PATH
```

If that’s all correct and Rust still isn’t working, there are a number of
places you can get help. Find out how to get in touch with other Rustaceans (a
silly nickname we call ourselves) on [the community page][community].

### Updating and Uninstalling

Once Rust is installed via `rustup`, updating to a newly released version is
easy. From your shell, run the following update script:

```console
$ rustup update
```

To uninstall Rust and `rustup`, run the following uninstall script from your
shell:

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### Reading the Local Documentation

The installation of Rust also includes a local copy of the documentation so
that you can read it offline. Run `rustup doc` to open the local documentation
in your browser.

Any time a type or function is provided by the standard library and you’re not
sure what it does or how to use it, use the application programming interface
(API) documentation to find out!

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Using Text Editors and IDEs

This book makes no assumptions about what tools you use to author Rust code.
Just about any text editor will get the job done! However, many text editors and
integrated development environments (IDEs) have built-in support for Rust. You
can always find a fairly current list of many editors and IDEs on [the tools
page][tools] on the Rust website.

### Working Offline with This Book

In several examples, we will use Rust packages beyond the standard library. To
work through those examples, you will either need to have an internet connection
or to have downloaded those dependencies ahead of time. To download the
dependencies ahead of time, you can run the following commands. (We’ll explain
what `cargo` is and what each of these commands does in detail later.)

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

This will cache the downloads for these packages so you will not need to
download them later. Once you have run this command, you do not need to keep the
`get-dependencies` folder. If you have run this command, you can use the
`--offline` flag with all `cargo` commands in the rest of the book to use these
cached versions instead of attempting to use the network.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools

## Hello, World!

Now that you’ve installed Rust, it’s time to write your first Rust program.
It’s traditional when learning a new language to write a little program that
prints the text `Hello, world!` to the screen, so we’ll do the same here!

> Note: This book assumes basic familiarity with the command line. Rust makes
> no specific demands about your editing or tooling or where your code lives, so
> if you prefer to use an IDE instead of the command line, feel free to use your
> favorite IDE. Many IDEs now have some degree of Rust support; check the IDE’s
> documentation for details. The Rust team has been focusing on enabling great
> IDE support via `rust-analyzer`. See [Appendix D][devtools]<!-- ignore -->
> for more details.

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### Project Directory Setup

You’ll start by making a directory to store your Rust code. It doesn’t matter
to Rust where your code lives, but for the exercises and projects in this book,
we suggest making a _projects_ directory in your home directory and keeping all
your projects there.

Open a terminal and enter the following commands to make a _projects_ directory
and a directory for the “Hello, world!” project within the _projects_ directory.

For Linux, macOS, and PowerShell on Windows, enter this:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

For Windows CMD, enter this:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

### Rust Program Basics

Next, make a new source file and call it _main.rs_. Rust files always end with
the _.rs_ extension. If you’re using more than one word in your filename, the
convention is to use an underscore to separate them. For example, use
_hello_world.rs_ rather than _helloworld.rs_.

Now open the _main.rs_ file you just created and enter the code in Listing 1-1.

<Listing number="1-1" file-name="main.rs" caption="A program that prints `Hello, world!`">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Save the file and go back to your terminal window in the
_~/projects/hello_world_ directory. On Linux or macOS, enter the following
commands to compile and run the file:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

On Windows, enter the command `.\main` instead of `./main`:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

Regardless of your operating system, the string `Hello, world!` should print to
the terminal. If you don’t see this output, refer back to the
[“Troubleshooting”][troubleshooting]<!-- ignore --> part of the Installation
section for ways to get help.

If `Hello, world!` did print, congratulations! You’ve officially written a Rust
program. That makes you a Rust programmer—welcome!

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### The Anatomy of a Rust Program

Let’s review this “Hello, world!” program in detail. Here’s the first piece of
the puzzle:

```rust
fn main() {

}
```

These lines define a function named `main`. The `main` function is special: It
is always the first code that runs in every executable Rust program. Here, the
first line declares a function named `main` that has no parameters and returns
nothing. If there were parameters, they would go inside the parentheses (`()`).

The function body is wrapped in `{}`. Rust requires curly brackets around all
function bodies. It’s good style to place the opening curly bracket on the same
line as the function declaration, adding one space in between.

> Note: If you want to stick to a standard style across Rust projects, you can
> use an automatic formatter tool called `rustfmt` to format your code in a
> particular style (more on `rustfmt` in
> [Appendix D][devtools]<!-- ignore -->). The Rust team has included this tool
> with the standard Rust distribution, as `rustc` is, so it should already be
> installed on your computer!

The body of the `main` function holds the following code:

```rust
println!("Hello, world!");
```

This line does all the work in this little program: It prints text to the
screen. There are three important details to notice here.

First, `println!` calls a Rust macro. If it had called a function instead, it
would be entered as `println` (without the `!`). Rust macros are a way to write
code that generates code to extend Rust syntax, and we’ll discuss them in more
detail in [Chapter 20][ch20-macros]<!-- ignore -->. For now, you just need to
know that using a `!` means that you’re calling a macro instead of a normal
function and that macros don’t always follow the same rules as functions.

Second, you see the `"Hello, world!"` string. We pass this string as an argument
to `println!`, and the string is printed to the screen.

Third, we end the line with a semicolon (`;`), which indicates that this
expression is over, and the next one is ready to begin. Most lines of Rust code
end with a semicolon.

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### Compilation and Execution

You’ve just run a newly created program, so let’s examine each step in the
process.

Before running a Rust program, you must compile it using the Rust compiler by
entering the `rustc` command and passing it the name of your source file, like
this:

```console
$ rustc main.rs
```

If you have a C or C++ background, you’ll notice that this is similar to `gcc`
or `clang`. After compiling successfully, Rust outputs a binary executable.

On Linux, macOS, and PowerShell on Windows, you can see the executable by
entering the `ls` command in your shell:

```console
$ ls
main  main.rs
```

On Linux and macOS, you’ll see two files. With PowerShell on Windows, you’ll
see the same three files that you would see using CMD. With CMD on Windows, you
would enter the following:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

This shows the source code file with the _.rs_ extension, the executable file
(_main.exe_ on Windows, but _main_ on all other platforms), and, when using
Windows, a file containing debugging information with the _.pdb_ extension.
From here, you run the _main_ or _main.exe_ file, like this:

```console
$ ./main # or .\main on Windows
```

If your _main.rs_ is your “Hello, world!” program, this line prints `Hello,
world!` to your terminal.

If you’re more familiar with a dynamic language, such as Ruby, Python, or
JavaScript, you might not be used to compiling and running a program as
separate steps. Rust is an _ahead-of-time compiled_ language, meaning you can
compile a program and give the executable to someone else, and they can run it
even without having Rust installed. If you give someone a _.rb_, _.py_, or
_.js_ file, they need to have a Ruby, Python, or JavaScript implementation
installed (respectively). But in those languages, you only need one command to
compile and run your program. Everything is a trade-off in language design.

Just compiling with `rustc` is fine for simple programs, but as your project
grows, you’ll want to manage all the options and make it easy to share your
code. Next, we’ll introduce you to the Cargo tool, which will help you write
real-world Rust programs.

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html

## Hello, Cargo!

Cargo is Rust’s build system and package manager. Most Rustaceans use this tool
to manage their Rust projects because Cargo handles a lot of tasks for you,
such as building your code, downloading the libraries your code depends on, and
building those libraries. (We call the libraries that your code needs
_dependencies_.)

The simplest Rust programs, like the one we’ve written so far, don’t have any
dependencies. If we had built the “Hello, world!” project with Cargo, it would
only use the part of Cargo that handles building your code. As you write more
complex Rust programs, you’ll add dependencies, and if you start a project
using Cargo, adding dependencies will be much easier to do.

Because the vast majority of Rust projects use Cargo, the rest of this book
assumes that you’re using Cargo too. Cargo comes installed with Rust if you
used the official installers discussed in the
[“Installation”][installation]<!-- ignore --> section. If you installed Rust
through some other means, check whether Cargo is installed by entering the
following in your terminal:

```console
$ cargo --version
```

If you see a version number, you have it! If you see an error, such as `command
not found`, look at the documentation for your method of installation to
determine how to install Cargo separately.

### Creating a Project with Cargo

Let’s create a new project using Cargo and look at how it differs from our
original “Hello, world!” project. Navigate back to your _projects_ directory
(or wherever you decided to store your code). Then, on any operating system,
run the following:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

The first command creates a new directory and project called _hello_cargo_.
We’ve named our project _hello_cargo_, and Cargo creates its files in a
directory of the same name.

Go into the _hello_cargo_ directory and list the files. You’ll see that Cargo
has generated two files and one directory for us: a _Cargo.toml_ file and a
_src_ directory with a _main.rs_ file inside.

It has also initialized a new Git repository along with a _.gitignore_ file.
Git files won’t be generated if you run `cargo new` within an existing Git
repository; you can override this behavior by using `cargo new --vcs=git`.

> Note: Git is a common version control system. You can change `cargo new` to
> use a different version control system or no version control system by using
> the `--vcs` flag. Run `cargo new --help` to see the available options.

Open _Cargo.toml_ in your text editor of choice. It should look similar to the
code in Listing 1-2.

<Listing number="1-2" file-name="Cargo.toml" caption="Contents of *Cargo.toml* generated by `cargo new`">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

This file is in the [_TOML_][toml]<!-- ignore --> (_Tom’s Obvious, Minimal
Language_) format, which is Cargo’s configuration format.

The first line, `[package]`, is a section heading that indicates that the
following statements are configuring a package. As we add more information to
this file, we’ll add other sections.

The next three lines set the configuration information Cargo needs to compile
your program: the name, the version, and the edition of Rust to use. We’ll talk
about the `edition` key in [Appendix E][appendix-e]<!-- ignore -->.

The last line, `[dependencies]`, is the start of a section for you to list any
of your project’s dependencies. In Rust, packages of code are referred to as
_crates_. We won’t need any other crates for this project, but we will in the
first project in Chapter 2, so we’ll use this dependencies section then.

Now open _src/main.rs_ and take a look:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo has generated a “Hello, world!” program for you, just like the one we
wrote in Listing 1-1! So far, the differences between our project and the
project Cargo generated are that Cargo placed the code in the _src_ directory,
and we have a _Cargo.toml_ configuration file in the top directory.

Cargo expects your source files to live inside the _src_ directory. The
top-level project directory is just for README files, license information,
configuration files, and anything else not related to your code. Using Cargo
helps you organize your projects. There’s a place for everything, and
everything is in its place.

If you started a project that doesn’t use Cargo, as we did with the “Hello,
world!” project, you can convert it to a project that does use Cargo. Move the
project code into the _src_ directory and create an appropriate _Cargo.toml_
file. One easy way to get that _Cargo.toml_ file is to run `cargo init`, which
will create it for you automatically.

### Building and Running a Cargo Project

Now let’s look at what’s different when we build and run the “Hello, world!”
program with Cargo! From your _hello_cargo_ directory, build your project by
entering the following command:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

This command creates an executable file in _target/debug/hello_cargo_ (or
_target\debug\hello_cargo.exe_ on Windows) rather than in your current
directory. Because the default build is a debug build, Cargo puts the binary in
a directory named _debug_. You can run the executable with this command:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

If all goes well, `Hello, world!` should print to the terminal. Running `cargo
build` for the first time also causes Cargo to create a new file at the top
level: _Cargo.lock_. This file keeps track of the exact versions of
dependencies in your project. This project doesn’t have dependencies, so the
file is a bit sparse. You won’t ever need to change this file manually; Cargo
manages its contents for you.

We just built a project with `cargo build` and ran it with
`./target/debug/hello_cargo`, but we can also use `cargo run` to compile the
code and then run the resultant executable all in one command:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Using `cargo run` is more convenient than having to remember to run `cargo
build` and then use the whole path to the binary, so most developers use `cargo
run`.

Notice that this time we didn’t see output indicating that Cargo was compiling
`hello_cargo`. Cargo figured out that the files hadn’t changed, so it didn’t
rebuild but just ran the binary. If you had modified your source code, Cargo
would have rebuilt the project before running it, and you would have seen this
output:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo also provides a command called `cargo check`. This command quickly checks
your code to make sure it compiles but doesn’t produce an executable:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Why would you not want an executable? Often, `cargo check` is much faster than
`cargo build` because it skips the step of producing an executable. If you’re
continually checking your work while writing the code, using `cargo check` will
speed up the process of letting you know if your project is still compiling! As
such, many Rustaceans run `cargo check` periodically as they write their
program to make sure it compiles. Then, they run `cargo build` when they’re
ready to use the executable.

Let’s recap what we’ve learned so far about Cargo:

- We can create a project using `cargo new`.
- We can build a project using `cargo build`.
- We can build and run a project in one step using `cargo run`.
- We can build a project without producing a binary to check for errors using
  `cargo check`.
- Instead of saving the result of the build in the same directory as our code,
  Cargo stores it in the _target/debug_ directory.

An additional advantage of using Cargo is that the commands are the same no
matter which operating system you’re working on. So, at this point, we’ll no
longer provide specific instructions for Linux and macOS versus Windows.

### Building for Release

When your project is finally ready for release, you can use `cargo build
--release` to compile it with optimizations. This command will create an
executable in _target/release_ instead of _target/debug_. The optimizations
make your Rust code run faster, but turning them on lengthens the time it takes
for your program to compile. This is why there are two different profiles: one
for development, when you want to rebuild quickly and often, and another for
building the final program you’ll give to a user that won’t be rebuilt
repeatedly and that will run as fast as possible. If you’re benchmarking your
code’s running time, be sure to run `cargo build --release` and benchmark with
the executable in _target/release_.

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### Leveraging Cargo’s Conventions

With simple projects, Cargo doesn’t provide a lot of value over just using
`rustc`, but it will prove its worth as your programs become more intricate.
Once programs grow to multiple files or need a dependency, it’s much easier to
let Cargo coordinate the build.

Even though the `hello_cargo` project is simple, it now uses much of the real
tooling you’ll use in the rest of your Rust career. In fact, to work on any
existing projects, you can use the following commands to check out the code
using Git, change to that project’s directory, and build:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

For more information about Cargo, check out [its documentation][cargo].

## Summary

You’re already off to a great start on your Rust journey! In this chapter, you
learned how to:

- Install the latest stable version of Rust using `rustup`.
- Update to a newer Rust version.
- Open locally installed documentation.
- Write and run a “Hello, world!” program using `rustc` directly.
- Create and run a new project using the conventions of Cargo.

This is a great time to build a more substantial program to get used to reading
and writing Rust code. So, in Chapter 2, we’ll build a guessing game program.
If you would rather start by learning how common programming concepts work in
Rust, see Chapter 3 and then return to Chapter 2.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/

# Common Programming Concepts

This chapter covers concepts that appear in almost every programming language
and how they work in Rust. Many programming languages have much in common at
their core. None of the concepts presented in this chapter are unique to Rust,
but we’ll discuss them in the context of Rust and explain the conventions
around using them.

Specifically, you’ll learn about variables, basic types, functions, comments,
and control flow. These foundations will be in every Rust program, and learning
them early will give you a strong core to start from.

> #### Keywords
>
> The Rust language has a set of _keywords_ that are reserved for use by the
> language only, much as in other languages. Keep in mind that you cannot use
> these words as names of variables or functions. Most of the keywords have
> special meanings, and you’ll be using them to do various tasks in your Rust
> programs; a few have no current functionality associated with them but have
> been reserved for functionality that might be added to Rust in the future. You
> can find the list of the keywords in [Appendix A][appendix_a]<!-- ignore -->.

[appendix_a]: appendix-01-keywords.md

## Variables and Mutability

As mentioned in the [“Storing Values with
Variables”][storing-values-with-variables]<!-- ignore --> section, by default,
variables are immutable. This is one of many nudges Rust gives you to write
your code in a way that takes advantage of the safety and easy concurrency that
Rust offers. However, you still have the option to make your variables mutable.
Let’s explore how and why Rust encourages you to favor immutability and why
sometimes you might want to opt out.

When a variable is immutable, once a value is bound to a name, you can’t change
that value. To illustrate this, generate a new project called _variables_ in
your _projects_ directory by using `cargo new variables`.

Then, in your new _variables_ directory, open _src/main.rs_ and replace its
code with the following code, which won’t compile just yet:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Save and run the program using `cargo run`. You should receive an error message
regarding an immutability error, as shown in this output:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

This example shows how the compiler helps you find errors in your programs.
Compiler errors can be frustrating, but really they only mean your program
isn’t safely doing what you want it to do yet; they do _not_ mean that you’re
not a good programmer! Experienced Rustaceans still get compiler errors.

You received the error message `` cannot assign twice to immutable variable `x` `` because you tried to assign a second value to the immutable `x` variable.

It’s important that we get compile-time errors when we attempt to change a
value that’s designated as immutable, because this very situation can lead to
bugs. If one part of our code operates on the assumption that a value will
never change and another part of our code changes that value, it’s possible
that the first part of the code won’t do what it was designed to do. The cause
of this kind of bug can be difficult to track down after the fact, especially
when the second piece of code changes the value only _sometimes_. The Rust
compiler guarantees that when you state that a value won’t change, it really
won’t change, so you don’t have to keep track of it yourself. Your code is thus
easier to reason through.

But mutability can be very useful and can make code more convenient to write.
Although variables are immutable by default, you can make them mutable by
adding `mut` in front of the variable name as you did in [Chapter
2][storing-values-with-variables]<!-- ignore -->. Adding `mut` also conveys
intent to future readers of the code by indicating that other parts of the code
will be changing this variable’s value.

For example, let’s change _src/main.rs_ to the following:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

When we run the program now, we get this:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

We’re allowed to change the value bound to `x` from `5` to `6` when `mut` is
used. Ultimately, deciding whether to use mutability or not is up to you and
depends on what you think is clearest in that particular situation.

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

### Declaring Constants

Like immutable variables, _constants_ are values that are bound to a name and
are not allowed to change, but there are a few differences between constants
and variables.

First, you aren’t allowed to use `mut` with constants. Constants aren’t just
immutable by default—they’re always immutable. You declare constants using the
`const` keyword instead of the `let` keyword, and the type of the value _must_
be annotated. We’ll cover types and type annotations in the next section,
[“Data Types”][data-types]<!-- ignore -->, so don’t worry about the details
right now. Just know that you must always annotate the type.

Constants can be declared in any scope, including the global scope, which makes
them useful for values that many parts of code need to know about.

The last difference is that constants may be set only to a constant expression,
not the result of a value that could only be computed at runtime.

Here’s an example of a constant declaration:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

The constant’s name is `THREE_HOURS_IN_SECONDS`, and its value is set to the
result of multiplying 60 (the number of seconds in a minute) by 60 (the number
of minutes in an hour) by 3 (the number of hours we want to count in this
program). Rust’s naming convention for constants is to use all uppercase with
underscores between words. The compiler is able to evaluate a limited set of
operations at compile time, which lets us choose to write out this value in a
way that’s easier to understand and verify, rather than setting this constant
to the value 10,800. See the [Rust Reference’s section on constant
evaluation][const-eval] for more information on what operations can be used
when declaring constants.

Constants are valid for the entire time a program runs, within the scope in
which they were declared. This property makes constants useful for values in
your application domain that multiple parts of the program might need to know
about, such as the maximum number of points any player of a game is allowed to
earn, or the speed of light.

Naming hardcoded values used throughout your program as constants is useful in
conveying the meaning of that value to future maintainers of the code. It also
helps to have only one place in your code that you would need to change if the
hardcoded value needed to be updated in the future.

### Shadowing

As you saw in the guessing game tutorial in [Chapter
2][comparing-the-guess-to-the-secret-number]<!-- ignore -->, you can declare a
new variable with the same name as a previous variable. Rustaceans say that the
first variable is _shadowed_ by the second, which means that the second
variable is what the compiler will see when you use the name of the variable.
In effect, the second variable overshadows the first, taking any uses of the
variable name to itself until either it itself is shadowed or the scope ends.
We can shadow a variable by using the same variable’s name and repeating the
use of the `let` keyword as follows:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

This program first binds `x` to a value of `5`. Then, it creates a new variable
`x` by repeating `let x =`, taking the original value and adding `1` so that
the value of `x` is `6`. Then, within an inner scope created with the curly
brackets, the third `let` statement also shadows `x` and creates a new
variable, multiplying the previous value by `2` to give `x` a value of `12`.
When that scope is over, the inner shadowing ends and `x` returns to being `6`.
When we run this program, it will output the following:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

Shadowing is different from marking a variable as `mut` because we’ll get a
compile-time error if we accidentally try to reassign to this variable without
using the `let` keyword. By using `let`, we can perform a few transformations
on a value but have the variable be immutable after those transformations have
completed.

The other difference between `mut` and shadowing is that because we’re
effectively creating a new variable when we use the `let` keyword again, we can
change the type of the value but reuse the same name. For example, say our
program asks a user to show how many spaces they want between some text by
inputting space characters, and then we want to store that input as a number:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

The first `spaces` variable is a string type, and the second `spaces` variable
is a number type. Shadowing thus spares us from having to come up with
different names, such as `spaces_str` and `spaces_num`; instead, we can reuse
the simpler `spaces` name. However, if we try to use `mut` for this, as shown
here, we’ll get a compile-time error:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

The error says we’re not allowed to mutate a variable’s type:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Now that we’ve explored how variables work, let’s look at more data types they
can have.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html

## Data Types

Every value in Rust is of a certain _data type_, which tells Rust what kind of
data is being specified so that it knows how to work with that data. We’ll look
at two data type subsets: scalar and compound.

Keep in mind that Rust is a _statically typed_ language, which means that it
must know the types of all variables at compile time. The compiler can usually
infer what type we want to use based on the value and how we use it. In cases
when many types are possible, such as when we converted a `String` to a numeric
type using `parse` in the [“Comparing the Guess to the Secret
Number”][comparing-the-guess-to-the-secret-number]<!-- ignore --> section in
Chapter 2, we must add a type annotation, like this:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

If we don’t add the `: u32` type annotation shown in the preceding code, Rust
will display the following error, which means the compiler needs more
information from us to know which type we want to use:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

You’ll see different type annotations for other data types.

### Scalar Types

A _scalar_ type represents a single value. Rust has four primary scalar types:
integers, floating-point numbers, Booleans, and characters. You may recognize
these from other programming languages. Let’s jump into how they work in Rust.

#### Integer Types

An _integer_ is a number without a fractional component. We used one integer
type in Chapter 2, the `u32` type. This type declaration indicates that the
value it’s associated with should be an unsigned integer (signed integer types
start with `i` instead of `u`) that takes up 32 bits of space. Table 3-1 shows
the built-in integer types in Rust. We can use any of these variants to declare
the type of an integer value.

<span class="caption">Table 3-1: Integer Types in Rust</span>

| Length  | Signed  | Unsigned |
| ------- | ------- | -------- |
| 8-bit   | `i8`    | `u8`     |
| 16-bit  | `i16`   | `u16`    |
| 32-bit  | `i32`   | `u32`    |
| 64-bit  | `i64`   | `u64`    |
| 128-bit | `i128`  | `u128`   |
| Architecture-dependent | `isize` | `usize`  |

Each variant can be either signed or unsigned and has an explicit size.
_Signed_ and _unsigned_ refer to whether it’s possible for the number to be
negative—in other words, whether the number needs to have a sign with it
(signed) or whether it will only ever be positive and can therefore be
represented without a sign (unsigned). It’s like writing numbers on paper: When
the sign matters, a number is shown with a plus sign or a minus sign; however,
when it’s safe to assume the number is positive, it’s shown with no sign.
Signed numbers are stored using [two’s complement][twos-complement]<!-- ignore
--> representation.

Each signed variant can store numbers from −(2<sup>n − 1</sup>) to 2<sup>n −
1</sup> − 1 inclusive, where _n_ is the number of bits that variant uses. So, an
`i8` can store numbers from −(2<sup>7</sup>) to 2<sup>7</sup> − 1, which equals
−128 to 127. Unsigned variants can store numbers from 0 to 2<sup>n</sup> − 1,
so a `u8` can store numbers from 0 to 2<sup>8</sup> − 1, which equals 0 to 255.

Additionally, the `isize` and `usize` types depend on the architecture of the
computer your program is running on: 64 bits if you’re on a 64-bit architecture
and 32 bits if you’re on a 32-bit architecture.

You can write integer literals in any of the forms shown in Table 3-2. Note
that number literals that can be multiple numeric types allow a type suffix,
such as `57u8`, to designate the type. Number literals can also use `_` as a
visual separator to make the number easier to read, such as `1_000`, which will
have the same value as if you had specified `1000`.

<span class="caption">Table 3-2: Integer Literals in Rust</span>

| Number literals  | Example       |
| ---------------- | ------------- |
| Decimal          | `98_222`      |
| Hex              | `0xff`        |
| Octal            | `0o77`        |
| Binary           | `0b1111_0000` |
| Byte (`u8` only) | `b'A'`        |

So how do you know which type of integer to use? If you’re unsure, Rust’s
defaults are generally good places to start: Integer types default to `i32`.
The primary situation in which you’d use `isize` or `usize` is when indexing
some sort of collection.

> ##### Integer Overflow
>
> Let’s say you have a variable of type `u8` that can hold values between 0 and
> 255. If you try to change the variable to a value outside that range, such as
> 256, _integer overflow_ will occur, which can result in one of two behaviors.
> When you’re compiling in debug mode, Rust includes checks for integer overflow
> that cause your program to _panic_ at runtime if this behavior occurs. Rust
> uses the term _panicking_ when a program exits with an error; we’ll discuss
> panics in more depth in the [“Unrecoverable Errors with
> `panic!`”][unrecoverable-errors-with-panic]<!-- ignore --> section in Chapter
> 9.
>
> When you’re compiling in release mode with the `--release` flag, Rust does
> _not_ include checks for integer overflow that cause panics. Instead, if
> overflow occurs, Rust performs _two’s complement wrapping_. In short, values
> greater than the maximum value the type can hold “wrap around” to the minimum
> of the values the type can hold. In the case of a `u8`, the value 256 becomes
> 0, the value 257 becomes 1, and so on. The program won’t panic, but the
> variable will have a value that probably isn’t what you were expecting it to
> have. Relying on integer overflow’s wrapping behavior is considered an error.
>
> To explicitly handle the possibility of overflow, you can use these families
> of methods provided by the standard library for primitive numeric types:
>
> - Wrap in all compilation modes with the `wrapping_*` methods, such as 
>   `wrapping_add`.
> - Return the `None` value if there is overflow with the `checked_*` methods.
> - Return the value and a Boolean indicating whether there was overflow with
>   the `overflowing_*` methods.
> - Saturate at the value’s minimum or maximum values with the `saturating_*`
>   methods.

#### Floating-Point Types

Rust also has two primitive types for _floating-point numbers_, which are
numbers with decimal points. Rust’s floating-point types are `f32` and `f64`,
which are 32 bits and 64 bits in size, respectively. The default type is `f64`
because on modern CPUs, it’s roughly the same speed as `f32` but is capable of
more precision. All floating-point types are signed.

Here’s an example that shows floating-point numbers in action:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

Floating-point numbers are represented according to the IEEE-754 standard.

#### Numeric Operations

Rust supports the basic mathematical operations you’d expect for all the number
types: addition, subtraction, multiplication, division, and remainder. Integer
division truncates toward zero to the nearest integer. The following code shows
how you’d use each numeric operation in a `let` statement:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Each expression in these statements uses a mathematical operator and evaluates
to a single value, which is then bound to a variable. [Appendix
B][appendix_b]<!-- ignore --> contains a list of all operators that Rust
provides.

#### The Boolean Type

As in most other programming languages, a Boolean type in Rust has two possible
values: `true` and `false`. Booleans are one byte in size. The Boolean type in
Rust is specified using `bool`. For example:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

The main way to use Boolean values is through conditionals, such as an `if`
expression. We’ll cover how `if` expressions work in Rust in the [“Control
Flow”][control-flow]<!-- ignore --> section.

#### The Character Type

Rust’s `char` type is the language’s most primitive alphabetic type. Here are
some examples of declaring `char` values:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Note that we specify `char` literals with single quotation marks, as opposed to
string literals, which use double quotation marks. Rust’s `char` type is 4
bytes in size and represents a Unicode scalar value, which means it can
represent a lot more than just ASCII. Accented letters; Chinese, Japanese, and
Korean characters; emojis; and zero-width spaces are all valid `char` values in
Rust. Unicode scalar values range from `U+0000` to `U+D7FF` and `U+E000` to
`U+10FFFF` inclusive. However, a “character” isn’t really a concept in Unicode,
so your human intuition for what a “character” is may not match up with what a
`char` is in Rust. We’ll discuss this topic in detail in [“Storing UTF-8
Encoded Text with Strings”][strings]<!-- ignore --> in Chapter 8.

### Compound Types

_Compound types_ can group multiple values into one type. Rust has two
primitive compound types: tuples and arrays.

#### The Tuple Type

A _tuple_ is a general way of grouping together a number of values with a
variety of types into one compound type. Tuples have a fixed length: Once
declared, they cannot grow or shrink in size.

We create a tuple by writing a comma-separated list of values inside
parentheses. Each position in the tuple has a type, and the types of the
different values in the tuple don’t have to be the same. We’ve added optional
type annotations in this example:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

The variable `tup` binds to the entire tuple because a tuple is considered a
single compound element. To get the individual values out of a tuple, we can
use pattern matching to destructure a tuple value, like this:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

This program first creates a tuple and binds it to the variable `tup`. It then
uses a pattern with `let` to take `tup` and turn it into three separate
variables, `x`, `y`, and `z`. This is called _destructuring_ because it breaks
the single tuple into three parts. Finally, the program prints the value of
`y`, which is `6.4`.

We can also access a tuple element directly by using a period (`.`) followed by
the index of the value we want to access. For example:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

This program creates the tuple `x` and then accesses each element of the tuple
using their respective indices. As with most programming languages, the first
index in a tuple is 0.

The tuple without any values has a special name, _unit_. This value and its
corresponding type are both written `()` and represent an empty value or an
empty return type. Expressions implicitly return the unit value if they don’t
return any other value.

#### The Array Type

Another way to have a collection of multiple values is with an _array_. Unlike
a tuple, every element of an array must have the same type. Unlike arrays in
some other languages, arrays in Rust have a fixed length.

We write the values in an array as a comma-separated list inside square
brackets:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

Arrays are useful when you want your data allocated on the stack, the same as
the other types we have seen so far, rather than the heap (we will discuss the
stack and the heap more in [Chapter 4][stack-and-heap]<!-- ignore -->) or when
you want to ensure that you always have a fixed number of elements. An array
isn’t as flexible as the vector type, though. A vector is a similar collection
type provided by the standard library that _is_ allowed to grow or shrink in
size because its contents live on the heap. If you’re unsure whether to use an
array or a vector, chances are you should use a vector. [Chapter
8][vectors]<!-- ignore --> discusses vectors in more detail.

However, arrays are more useful when you know the number of elements will not
need to change. For example, if you were using the names of the month in a
program, you would probably use an array rather than a vector because you know
it will always contain 12 elements:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

You write an array’s type using square brackets with the type of each element,
a semicolon, and then the number of elements in the array, like so:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Here, `i32` is the type of each element. After the semicolon, the number `5`
indicates the array contains five elements.

You can also initialize an array to contain the same value for each element by
specifying the initial value, followed by a semicolon, and then the length of
the array in square brackets, as shown here:

```rust
let a = [3; 5];
```

The array named `a` will contain `5` elements that will all be set to the value
`3` initially. This is the same as writing `let a = [3, 3, 3, 3, 3];` but in a
more concise way.

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### Array Element Access

An array is a single chunk of memory of a known, fixed size that can be
allocated on the stack. You can access elements of an array using indexing,
like this:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

In this example, the variable named `first` will get the value `1` because that
is the value at index `[0]` in the array. The variable named `second` will get
the value `2` from index `[1]` in the array.

#### Invalid Array Element Access

Let’s see what happens if you try to access an element of an array that is past
the end of the array. Say you run this code, similar to the guessing game in
Chapter 2, to get an array index from the user:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

This code compiles successfully. If you run this code using `cargo run` and
enter `0`, `1`, `2`, `3`, or `4`, the program will print out the corresponding
value at that index in the array. If you instead enter a number past the end of
the array, such as `10`, you’ll see output like this:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

The program resulted in a runtime error at the point of using an invalid
value in the indexing operation. The program exited with an error message and
didn’t execute the final `println!` statement. When you attempt to access an
element using indexing, Rust will check that the index you’ve specified is less
than the array length. If the index is greater than or equal to the length,
Rust will panic. This check has to happen at runtime, especially in this case,
because the compiler can’t possibly know what value a user will enter when they
run the code later.

This is an example of Rust’s memory safety principles in action. In many
low-level languages, this kind of check is not done, and when you provide an
incorrect index, invalid memory can be accessed. Rust protects you against this
kind of error by immediately exiting instead of allowing the memory access and
continuing. Chapter 9 discusses more of Rust’s error handling and how you can
write readable, safe code that neither panics nor allows invalid memory access.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md

## Functions

Functions are prevalent in Rust code. You’ve already seen one of the most
important functions in the language: the `main` function, which is the entry
point of many programs. You’ve also seen the `fn` keyword, which allows you to
declare new functions.

Rust code uses _snake case_ as the conventional style for function and variable
names, in which all letters are lowercase and underscores separate words.
Here’s a program that contains an example function definition:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

We define a function in Rust by entering `fn` followed by a function name and a
set of parentheses. The curly brackets tell the compiler where the function
body begins and ends.

We can call any function we’ve defined by entering its name followed by a set
of parentheses. Because `another_function` is defined in the program, it can be
called from inside the `main` function. Note that we defined `another_function`
_after_ the `main` function in the source code; we could have defined it before
as well. Rust doesn’t care where you define your functions, only that they’re
defined somewhere in a scope that can be seen by the caller.

Let’s start a new binary project named _functions_ to explore functions
further. Place the `another_function` example in _src/main.rs_ and run it. You
should see the following output:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

The lines execute in the order in which they appear in the `main` function.
First the “Hello, world!” message prints, and then `another_function` is called
and its message is printed.

### Parameters

We can define functions to have _parameters_, which are special variables that
are part of a function’s signature. When a function has parameters, you can
provide it with concrete values for those parameters. Technically, the concrete
values are called _arguments_, but in casual conversation, people tend to use
the words _parameter_ and _argument_ interchangeably for either the variables
in a function’s definition or the concrete values passed in when you call a
function.

In this version of `another_function` we add a parameter:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Try running this program; you should get the following output:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

The declaration of `another_function` has one parameter named `x`. The type of
`x` is specified as `i32`. When we pass `5` in to `another_function`, the
`println!` macro puts `5` where the pair of curly brackets containing `x` was
in the format string.

In function signatures, you _must_ declare the type of each parameter. This is
a deliberate decision in Rust’s design: Requiring type annotations in function
definitions means the compiler almost never needs you to use them elsewhere in
the code to figure out what type you mean. The compiler is also able to give
more-helpful error messages if it knows what types the function expects.

When defining multiple parameters, separate the parameter declarations with
commas, like this:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

This example creates a function named `print_labeled_measurement` with two
parameters. The first parameter is named `value` and is an `i32`. The second is
named `unit_label` and is type `char`. The function then prints text containing
both the `value` and the `unit_label`.

Let’s try running this code. Replace the program currently in your _functions_
project’s _src/main.rs_ file with the preceding example and run it using `cargo
run`:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Because we called the function with `5` as the value for `value` and `'h'` as
the value for `unit_label`, the program output contains those values.

### Statements and Expressions

Function bodies are made up of a series of statements optionally ending in an
expression. So far, the functions we’ve covered haven’t included an ending
expression, but you have seen an expression as part of a statement. Because
Rust is an expression-based language, this is an important distinction to
understand. Other languages don’t have the same distinctions, so let’s look at
what statements and expressions are and how their differences affect the bodies
of functions.

- _Statements_ are instructions that perform some action and do not return
  a value.
- _Expressions_ evaluate to a resultant value.

Let’s look at some examples.

We’ve actually already used statements and expressions. Creating a variable and
assigning a value to it with the `let` keyword is a statement. In Listing 3-1,
`let y = 6;` is a statement.

<Listing number="3-1" file-name="src/main.rs" caption="A `main` function declaration containing one statement">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

Function definitions are also statements; the entire preceding example is a
statement in itself. (As we’ll see shortly, calling a function is not a
statement, though.)

Statements do not return values. Therefore, you can’t assign a `let` statement
to another variable, as the following code tries to do; you’ll get an error:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

When you run this program, the error you’ll get looks like this:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

The `let y = 6` statement does not return a value, so there isn’t anything for
`x` to bind to. This is different from what happens in other languages, such as
C and Ruby, where the assignment returns the value of the assignment. In those
languages, you can write `x = y = 6` and have both `x` and `y` have the value
`6`; that is not the case in Rust.

Expressions evaluate to a value and make up most of the rest of the code that
you’ll write in Rust. Consider a math operation, such as `5 + 6`, which is an
expression that evaluates to the value `11`. Expressions can be part of
statements: In Listing 3-1, the `6` in the statement `let y = 6;` is an
expression that evaluates to the value `6`. Calling a function is an
expression. Calling a macro is an expression. A new scope block created with
curly brackets is an expression, for example:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

This expression:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

is a block that, in this case, evaluates to `4`. That value gets bound to `y`
as part of the `let` statement. Note the `x + 1` line without a semicolon at
the end, which is unlike most of the lines you’ve seen so far. Expressions do
not include ending semicolons. If you add a semicolon to the end of an
expression, you turn it into a statement, and it will then not return a value.
Keep this in mind as you explore function return values and expressions next.

### Functions with Return Values

Functions can return values to the code that calls them. We don’t name return
values, but we must declare their type after an arrow (`->`). In Rust, the
return value of the function is synonymous with the value of the final
expression in the block of the body of a function. You can return early from a
function by using the `return` keyword and specifying a value, but most
functions return the last expression implicitly. Here’s an example of a
function that returns a value:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

There are no function calls, macros, or even `let` statements in the `five`
function—just the number `5` by itself. That’s a perfectly valid function in
Rust. Note that the function’s return type is specified too, as `-> i32`. Try
running this code; the output should look like this:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

The `5` in `five` is the function’s return value, which is why the return type
is `i32`. Let’s examine this in more detail. There are two important bits:
First, the line `let x = five();` shows that we’re using the return value of a
function to initialize a variable. Because the function `five` returns a `5`,
that line is the same as the following:

```rust
let x = 5;
```

Second, the `five` function has no parameters and defines the type of the
return value, but the body of the function is a lonely `5` with no semicolon
because it’s an expression whose value we want to return.

Let’s look at another example:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

Running this code will print `The value of x is: 6`. But what happens if we
place a semicolon at the end of the line containing `x + 1`, changing it from
an expression to a statement?

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

Compiling this code will produce an error, as follows:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

The main error message, `mismatched types`, reveals the core issue with this
code. The definition of the function `plus_one` says that it will return an
`i32`, but statements don’t evaluate to a value, which is expressed by `()`,
the unit type. Therefore, nothing is returned, which contradicts the function
definition and results in an error. In this output, Rust provides a message to
possibly help rectify this issue: It suggests removing the semicolon, which
would fix the error.

## Control Flow

The ability to run some code depending on whether a condition is `true` and the
ability to run some code repeatedly while a condition is `true` are basic
building blocks in most programming languages. The most common constructs that
let you control the flow of execution of Rust code are `if` expressions and
loops.

### `if` Expressions

An `if` expression allows you to branch your code depending on conditions. You
provide a condition and then state, “If this condition is met, run this block
of code. If the condition is not met, do not run this block of code.”

Create a new project called _branches_ in your _projects_ directory to explore
the `if` expression. In the _src/main.rs_ file, input the following:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

All `if` expressions start with the keyword `if`, followed by a condition. In
this case, the condition checks whether or not the variable `number` has a
value less than 5. We place the block of code to execute if the condition is
`true` immediately after the condition inside curly brackets. Blocks of code
associated with the conditions in `if` expressions are sometimes called _arms_,
just like the arms in `match` expressions that we discussed in the [“Comparing
the Guess to the Secret Number”][comparing-the-guess-to-the-secret-number]<!--
ignore --> section of Chapter 2.

Optionally, we can also include an `else` expression, which we chose to do
here, to give the program an alternative block of code to execute should the
condition evaluate to `false`. If you don’t provide an `else` expression and
the condition is `false`, the program will just skip the `if` block and move on
to the next bit of code.

Try running this code; you should see the following output:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Let’s try changing the value of `number` to a value that makes the condition
`false` to see what happens:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Run the program again, and look at the output:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

It’s also worth noting that the condition in this code _must_ be a `bool`. If
the condition isn’t a `bool`, we’ll get an error. For example, try running the
following code:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

The `if` condition evaluates to a value of `3` this time, and Rust throws an
error:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

The error indicates that Rust expected a `bool` but got an integer. Unlike
languages such as Ruby and JavaScript, Rust will not automatically try to
convert non-Boolean types to a Boolean. You must be explicit and always provide
`if` with a Boolean as its condition. If we want the `if` code block to run
only when a number is not equal to `0`, for example, we can change the `if`
expression to the following:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

Running this code will print `number was something other than zero`.

#### Handling Multiple Conditions with `else if`

You can use multiple conditions by combining `if` and `else` in an `else if`
expression. For example:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

This program has four possible paths it can take. After running it, you should
see the following output:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

When this program executes, it checks each `if` expression in turn and executes
the first body for which the condition evaluates to `true`. Note that even
though 6 is divisible by 2, we don’t see the output `number is divisible by 2`,
nor do we see the `number is not divisible by 4, 3, or 2` text from the `else`
block. That’s because Rust only executes the block for the first `true`
condition, and once it finds one, it doesn’t even check the rest.

Using too many `else if` expressions can clutter your code, so if you have more
than one, you might want to refactor your code. Chapter 6 describes a powerful
Rust branching construct called `match` for these cases.

#### Using `if` in a `let` Statement

Because `if` is an expression, we can use it on the right side of a `let`
statement to assign the outcome to a variable, as in Listing 3-2.

<Listing number="3-2" file-name="src/main.rs" caption="Assigning the result of an `if` expression to a variable">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

The `number` variable will be bound to a value based on the outcome of the `if`
expression. Run this code to see what happens:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Remember that blocks of code evaluate to the last expression in them, and
numbers by themselves are also expressions. In this case, the value of the
whole `if` expression depends on which block of code executes. This means the
values that have the potential to be results from each arm of the `if` must be
the same type; in Listing 3-2, the results of both the `if` arm and the `else`
arm were `i32` integers. If the types are mismatched, as in the following
example, we’ll get an error:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

When we try to compile this code, we’ll get an error. The `if` and `else` arms
have value types that are incompatible, and Rust indicates exactly where to
find the problem in the program:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

The expression in the `if` block evaluates to an integer, and the expression in
the `else` block evaluates to a string. This won’t work, because variables must
have a single type, and Rust needs to know definitively at compile time what
type the `number` variable is. Knowing the type of `number` lets the compiler
verify the type is valid everywhere we use `number`. Rust wouldn’t be able to
do that if the type of `number` was only determined at runtime; the compiler
would be more complex and would make fewer guarantees about the code if it had
to keep track of multiple hypothetical types for any variable.

### Repetition with Loops

It’s often useful to execute a block of code more than once. For this task,
Rust provides several _loops_, which will run through the code inside the loop
body to the end and then start immediately back at the beginning. To experiment
with loops, let’s make a new project called _loops_.

Rust has three kinds of loops: `loop`, `while`, and `for`. Let’s try each one.

#### Repeating Code with `loop`

The `loop` keyword tells Rust to execute a block of code over and over again
either forever or until you explicitly tell it to stop.

As an example, change the _src/main.rs_ file in your _loops_ directory to look
like this:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

When we run this program, we’ll see `again!` printed over and over continuously
until we stop the program manually. Most terminals support the keyboard shortcut
<kbd>ctrl</kbd>-<kbd>C</kbd> to interrupt a program that is stuck in a continual
loop. Give it a try:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

The symbol `^C` represents where you pressed <kbd>ctrl</kbd>-<kbd>C</kbd>.

You may or may not see the word `again!` printed after the `^C`, depending on
where the code was in the loop when it received the interrupt signal.

Fortunately, Rust also provides a way to break out of a loop using code. You
can place the `break` keyword within the loop to tell the program when to stop
executing the loop. Recall that we did this in the guessing game in the
[“Quitting After a Correct Guess”][quitting-after-a-correct-guess]<!-- ignore
--> section of Chapter 2 to exit the program when the user won the game by
guessing the correct number.

We also used `continue` in the guessing game, which in a loop tells the program
to skip over any remaining code in this iteration of the loop and go to the
next iteration.

#### Returning Values from Loops

One of the uses of a `loop` is to retry an operation you know might fail, such
as checking whether a thread has completed its job. You might also need to pass
the result of that operation out of the loop to the rest of your code. To do
this, you can add the value you want returned after the `break` expression you
use to stop the loop; that value will be returned out of the loop so that you
can use it, as shown here:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

Before the loop, we declare a variable named `counter` and initialize it to
`0`. Then, we declare a variable named `result` to hold the value returned from
the loop. On every iteration of the loop, we add `1` to the `counter` variable,
and then check whether the `counter` is equal to `10`. When it is, we use the
`break` keyword with the value `counter * 2`. After the loop, we use a
semicolon to end the statement that assigns the value to `result`. Finally, we
print the value in `result`, which in this case is `20`.

You can also `return` from inside a loop. While `break` only exits the current
loop, `return` always exits the current function.

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Disambiguating with Loop Labels

If you have loops within loops, `break` and `continue` apply to the innermost
loop at that point. You can optionally specify a _loop label_ on a loop that
you can then use with `break` or `continue` to specify that those keywords
apply to the labeled loop instead of the innermost loop. Loop labels must begin
with a single quote. Here’s an example with two nested loops:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

The outer loop has the label `'counting_up`, and it will count up from 0 to 2.
The inner loop without a label counts down from 10 to 9. The first `break` that
doesn’t specify a label will exit the inner loop only. The `break
'counting_up;` statement will exit the outer loop. This code prints:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### Streamlining Conditional Loops with while

A program will often need to evaluate a condition within a loop. While the
condition is `true`, the loop runs. When the condition ceases to be `true`, the
program calls `break`, stopping the loop. It’s possible to implement behavior
like this using a combination of `loop`, `if`, `else`, and `break`; you could
try that now in a program, if you’d like. However, this pattern is so common
that Rust has a built-in language construct for it, called a `while` loop. In
Listing 3-3, we use `while` to loop the program three times, counting down each
time, and then, after the loop, to print a message and exit.

<Listing number="3-3" file-name="src/main.rs" caption="Using a `while` loop to run code while a condition evaluates to `true`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

This construct eliminates a lot of nesting that would be necessary if you used
`loop`, `if`, `else`, and `break`, and it’s clearer. While a condition
evaluates to `true`, the code runs; otherwise, it exits the loop.

#### Looping Through a Collection with `for`

You can choose to use the `while` construct to loop over the elements of a
collection, such as an array. For example, the loop in Listing 3-4 prints each
element in the array `a`.

<Listing number="3-4" file-name="src/main.rs" caption="Looping through each element of a collection using a `while` loop">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Here, the code counts up through the elements in the array. It starts at index
`0` and then loops until it reaches the final index in the array (that is,
when `index < 5` is no longer `true`). Running this code will print every
element in the array:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

All five array values appear in the terminal, as expected. Even though `index`
will reach a value of `5` at some point, the loop stops executing before trying
to fetch a sixth value from the array.

However, this approach is error-prone; we could cause the program to panic if
the index value or test condition is incorrect. For example, if you changed the
definition of the `a` array to have four elements but forgot to update the
condition to `while index < 4`, the code would panic. It’s also slow, because
the compiler adds runtime code to perform the conditional check of whether the
index is within the bounds of the array on every iteration through the loop.

As a more concise alternative, you can use a `for` loop and execute some code
for each item in a collection. A `for` loop looks like the code in Listing 3-5.

<Listing number="3-5" file-name="src/main.rs" caption="Looping through each element of a collection using a `for` loop">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

When we run this code, we’ll see the same output as in Listing 3-4. More
importantly, we’ve now increased the safety of the code and eliminated the
chance of bugs that might result from going beyond the end of the array or not
going far enough and missing some items. Machine code generated from `for`
loops can be more efficient as well because the index doesn’t need to be
compared to the length of the array at every iteration.

Using the `for` loop, you wouldn’t need to remember to change any other code if
you changed the number of values in the array, as you would with the method
used in Listing 3-4.

The safety and conciseness of `for` loops make them the most commonly used loop
construct in Rust. Even in situations in which you want to run some code a
certain number of times, as in the countdown example that used a `while` loop
in Listing 3-3, most Rustaceans would use a `for` loop. The way to do that
would be to use a `Range`, provided by the standard library, which generates
all numbers in sequence starting from one number and ending before another
number.

Here’s what the countdown would look like using a `for` loop and another method
we’ve not yet talked about, `rev`, to reverse the range:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

This code is a bit nicer, isn’t it?

## Summary

You made it! This was a sizable chapter: You learned about variables, scalar
and compound data types, functions, comments, `if` expressions, and loops! To
practice with the concepts discussed in this chapter, try building programs to
do the following:

- Convert temperatures between Fahrenheit and Celsius.
- Generate the *n*th Fibonacci number.
- Print the lyrics to the Christmas carol “The Twelve Days of Christmas,”
  taking advantage of the repetition in the song.

When you’re ready to move on, we’ll talk about a concept in Rust that _doesn’t_
commonly exist in other programming languages: ownership.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess

# Understanding Ownership

Ownership is Rust’s most unique feature and has deep implications for the rest
of the language. It enables Rust to make memory safety guarantees without
needing a garbage collector, so it’s important to understand how ownership
works. In this chapter, we’ll talk about ownership as well as several related
features: borrowing, slices, and how Rust lays data out in memory.

## What Is Ownership?

_Ownership_ is a set of rules that govern how a Rust program manages memory.
All programs have to manage the way they use a computer’s memory while running.
Some languages have garbage collection that regularly looks for no-longer-used
memory as the program runs; in other languages, the programmer must explicitly
allocate and free the memory. Rust uses a third approach: Memory is managed
through a system of ownership with a set of rules that the compiler checks. If
any of the rules are violated, the program won’t compile. None of the features
of ownership will slow down your program while it’s running.

Because ownership is a new concept for many programmers, it does take some time
to get used to. The good news is that the more experienced you become with Rust
and the rules of the ownership system, the easier you’ll find it to naturally
develop code that is safe and efficient. Keep at it!

When you understand ownership, you’ll have a solid foundation for understanding
the features that make Rust unique. In this chapter, you’ll learn ownership by
working through some examples that focus on a very common data structure:
strings.

> ### The Stack and the Heap
>
> Many programming languages don’t require you to think about the stack and the
> heap very often. But in a systems programming language like Rust, whether a
> value is on the stack or the heap affects how the language behaves and why
> you have to make certain decisions. Parts of ownership will be described in
> relation to the stack and the heap later in this chapter, so here is a brief
> explanation in preparation.
>
> Both the stack and the heap are parts of memory available to your code to use
> at runtime, but they are structured in different ways. The stack stores
> values in the order it gets them and removes the values in the opposite
> order. This is referred to as _last in, first out (LIFO)_. Think of a stack of
> plates: When you add more plates, you put them on top of the pile, and when
> you need a plate, you take one off the top. Adding or removing plates from
> the middle or bottom wouldn’t work as well! Adding data is called _pushing
> onto the stack_, and removing data is called _popping off the stack_. All
> data stored on the stack must have a known, fixed size. Data with an unknown
> size at compile time or a size that might change must be stored on the heap
> instead.
>
> The heap is less organized: When you put data on the heap, you request a
> certain amount of space. The memory allocator finds an empty spot in the heap
> that is big enough, marks it as being in use, and returns a _pointer_, which
> is the address of that location. This process is called _allocating on the
> heap_ and is sometimes abbreviated as just _allocating_ (pushing values onto
> the stack is not considered allocating). Because the pointer to the heap is a
> known, fixed size, you can store the pointer on the stack, but when you want
> the actual data, you must follow the pointer. Think of being seated at a
> restaurant. When you enter, you state the number of people in your group, and
> the host finds an empty table that fits everyone and leads you there. If
> someone in your group comes late, they can ask where you’ve been seated to
> find you.
>
> Pushing to the stack is faster than allocating on the heap because the
> allocator never has to search for a place to store new data; that location is
> always at the top of the stack. Comparatively, allocating space on the heap
> requires more work because the allocator must first find a big enough space
> to hold the data and then perform bookkeeping to prepare for the next
> allocation.
>
> Accessing data in the heap is generally slower than accessing data on the
> stack because you have to follow a pointer to get there. Contemporary
> processors are faster if they jump around less in memory. Continuing the
> analogy, consider a server at a restaurant taking orders from many tables.
> It’s most efficient to get all the orders at one table before moving on to
> the next table. Taking an order from table A, then an order from table B,
> then one from A again, and then one from B again would be a much slower
> process. By the same token, a processor can usually do its job better if it
> works on data that’s close to other data (as it is on the stack) rather than
> farther away (as it can be on the heap).
>
> When your code calls a function, the values passed into the function
> (including, potentially, pointers to data on the heap) and the function’s
> local variables get pushed onto the stack. When the function is over, those
> values get popped off the stack.
>
> Keeping track of what parts of code are using what data on the heap,
> minimizing the amount of duplicate data on the heap, and cleaning up unused
> data on the heap so that you don’t run out of space are all problems that
> ownership addresses. Once you understand ownership, you won’t need to think
> about the stack and the heap very often. But knowing that the main purpose of
> ownership is to manage heap data can help explain why it works the way it
> does.

### Ownership Rules

First, let’s take a look at the ownership rules. Keep these rules in mind as we
work through the examples that illustrate them:

- Each value in Rust has an _owner_.
- There can only be one owner at a time.
- When the owner goes out of scope, the value will be dropped.

### Variable Scope

Now that we’re past basic Rust syntax, we won’t include all the `fn main() {`
code in the examples, so if you’re following along, make sure to put the
following examples inside a `main` function manually. As a result, our examples
will be a bit more concise, letting us focus on the actual details rather than
boilerplate code.

As a first example of ownership, we’ll look at the scope of some variables. A
_scope_ is the range within a program for which an item is valid. Take the
following variable:

```rust
let s = "hello";
```

The variable `s` refers to a string literal, where the value of the string is
hardcoded into the text of our program. The variable is valid from the point at
which it’s declared until the end of the current scope. Listing 4-1 shows a
program with comments annotating where the variable `s` would be valid.

<Listing number="4-1" caption="A variable and the scope in which it is valid">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-01/src/main.rs:here}}
```

</Listing>

In other words, there are two important points in time here:

- When `s` comes _into_ scope, it is valid.
- It remains valid until it goes _out of_ scope.

At this point, the relationship between scopes and when variables are valid is
similar to that in other programming languages. Now we’ll build on top of this
understanding by introducing the `String` type.

### The `String` Type

To illustrate the rules of ownership, we need a data type that is more complex
than those we covered in the [“Data Types”][data-types]<!-- ignore --> section
of Chapter 3. The types covered previously are of a known size, can be stored
on the stack and popped off the stack when their scope is over, and can be
quickly and trivially copied to make a new, independent instance if another
part of code needs to use the same value in a different scope. But we want to
look at data that is stored on the heap and explore how Rust knows when to
clean up that data, and the `String` type is a great example.

We’ll concentrate on the parts of `String` that relate to ownership. These
aspects also apply to other complex data types, whether they are provided by
the standard library or created by you. We’ll discuss non-ownership aspects of
`String` in [Chapter 8][ch8]<!-- ignore -->.

We’ve already seen string literals, where a string value is hardcoded into our
program. String literals are convenient, but they aren’t suitable for every
situation in which we may want to use text. One reason is that they’re
immutable. Another is that not every string value can be known when we write
our code: For example, what if we want to take user input and store it? It is
for these situations that Rust has the `String` type. This type manages
data allocated on the heap and as such is able to store an amount of text that
is unknown to us at compile time. You can create a `String` from a string
literal using the `from` function, like so:

```rust
let s = String::from("hello");
```

The double colon `::` operator allows us to namespace this particular `from`
function under the `String` type rather than using some sort of name like
`string_from`. We’ll discuss this syntax more in the [“Methods”][methods]<!--
ignore --> section of Chapter 5, and when we talk about namespacing with
modules in [“Paths for Referring to an Item in the Module
Tree”][paths-module-tree]<!-- ignore --> in Chapter 7.

This kind of string _can_ be mutated:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-01-can-mutate-string/src/main.rs:here}}
```

So, what’s the difference here? Why can `String` be mutated but literals
cannot? The difference is in how these two types deal with memory.

### Memory and Allocation

In the case of a string literal, we know the contents at compile time, so the
text is hardcoded directly into the final executable. This is why string
literals are fast and efficient. But these properties only come from the string
literal’s immutability. Unfortunately, we can’t put a blob of memory into the
binary for each piece of text whose size is unknown at compile time and whose
size might change while running the program.

With the `String` type, in order to support a mutable, growable piece of text,
we need to allocate an amount of memory on the heap, unknown at compile time,
to hold the contents. This means:

- The memory must be requested from the memory allocator at runtime.
- We need a way of returning this memory to the allocator when we’re done with
  our `String`.

That first part is done by us: When we call `String::from`, its implementation
requests the memory it needs. This is pretty much universal in programming
languages.

However, the second part is different. In languages with a _garbage collector
(GC)_, the GC keeps track of and cleans up memory that isn’t being used
anymore, and we don’t need to think about it. In most languages without a GC,
it’s our responsibility to identify when memory is no longer being used and to
call code to explicitly free it, just as we did to request it. Doing this
correctly has historically been a difficult programming problem. If we forget,
we’ll waste memory. If we do it too early, we’ll have an invalid variable. If
we do it twice, that’s a bug too. We need to pair exactly one `allocate` with
exactly one `free`.

Rust takes a different path: The memory is automatically returned once the
variable that owns it goes out of scope. Here’s a version of our scope example
from Listing 4-1 using a `String` instead of a string literal:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-02-string-scope/src/main.rs:here}}
```

There is a natural point at which we can return the memory our `String` needs
to the allocator: when `s` goes out of scope. When a variable goes out of
scope, Rust calls a special function for us. This function is called
`drop`, and it’s where the author of `String` can put
the code to return the memory. Rust calls `drop` automatically at the closing
curly bracket.

> Note: In C++, this pattern of deallocating resources at the end of an item’s
> lifetime is sometimes called _Resource Acquisition Is Initialization (RAII)_.
> The `drop` function in Rust will be familiar to you if you’ve used RAII
> patterns.

This pattern has a profound impact on the way Rust code is written. It may seem
simple right now, but the behavior of code can be unexpected in more
complicated situations when we want to have multiple variables use the data
we’ve allocated on the heap. Let’s explore some of those situations now.

<!-- Old headings. Do not remove or links may break. -->

<a id="ways-variables-and-data-interact-move"></a>

#### Variables and Data Interacting with Move

Multiple variables can interact with the same data in different ways in Rust.
Listing 4-2 shows an example using an integer.

<Listing number="4-2" caption="Assigning the integer value of variable `x` to `y`">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-02/src/main.rs:here}}
```

</Listing>

We can probably guess what this is doing: “Bind the value `5` to `x`; then, make
a copy of the value in `x` and bind it to `y`.” We now have two variables, `x`
and `y`, and both equal `5`. This is indeed what is happening, because integers
are simple values with a known, fixed size, and these two `5` values are pushed
onto the stack.

Now let’s look at the `String` version:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-03-string-move/src/main.rs:here}}
```

This looks very similar, so we might assume that the way it works would be the
same: That is, the second line would make a copy of the value in `s1` and bind
it to `s2`. But this isn’t quite what happens.

Take a look at Figure 4-1 to see what is happening to `String` under the
covers. A `String` is made up of three parts, shown on the left: a pointer to
the memory that holds the contents of the string, a length, and a capacity.
This group of data is stored on the stack. On the right is the memory on the
heap that holds the contents.

<img alt="Two tables: the first table contains the representation of s1 on the
stack, consisting of its length (5), capacity (5), and a pointer to the first
value in the second table. The second table contains the representation of the
string data on the heap, byte by byte." src="img/trpl04-01.svg" class="center"
style="width: 50%;" />

<span class="caption">Figure 4-1: The representation in memory of a `String`
holding the value `"hello"` bound to `s1`</span>

The length is how much memory, in bytes, the contents of the `String` are
currently using. The capacity is the total amount of memory, in bytes, that the
`String` has received from the allocator. The difference between length and
capacity matters, but not in this context, so for now, it’s fine to ignore the
capacity.

When we assign `s1` to `s2`, the `String` data is copied, meaning we copy the
pointer, the length, and the capacity that are on the stack. We do not copy the
data on the heap that the pointer refers to. In other words, the data
representation in memory looks like Figure 4-2.

<img alt="Three tables: tables s1 and s2 representing those strings on the
stack, respectively, and both pointing to the same string data on the heap."
src="img/trpl04-02.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-2: The representation in memory of the variable
`s2` that has a copy of the pointer, length, and capacity of `s1`</span>

The representation does _not_ look like Figure 4-3, which is what memory would
look like if Rust instead copied the heap data as well. If Rust did this, the
operation `s2 = s1` could be very expensive in terms of runtime performance if
the data on the heap were large.

<img alt="Four tables: two tables representing the stack data for s1 and s2,
and each points to its own copy of string data on the heap."
src="img/trpl04-03.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-3: Another possibility for what `s2 = s1` might
do if Rust copied the heap data as well</span>

Earlier, we said that when a variable goes out of scope, Rust automatically
calls the `drop` function and cleans up the heap memory for that variable. But
Figure 4-2 shows both data pointers pointing to the same location. This is a
problem: When `s2` and `s1` go out of scope, they will both try to free the
same memory. This is known as a _double free_ error and is one of the memory
safety bugs we mentioned previously. Freeing memory twice can lead to memory
corruption, which can potentially lead to security vulnerabilities.

To ensure memory safety, after the line `let s2 = s1;`, Rust considers `s1` as
no longer valid. Therefore, Rust doesn’t need to free anything when `s1` goes
out of scope. Check out what happens when you try to use `s1` after `s2` is
created; it won’t work:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/src/main.rs:here}}
```

You’ll get an error like this because Rust prevents you from using the
invalidated reference:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/output.txt}}
```

If you’ve heard the terms _shallow copy_ and _deep copy_ while working with
other languages, the concept of copying the pointer, length, and capacity
without copying the data probably sounds like making a shallow copy. But
because Rust also invalidates the first variable, instead of being called a
shallow copy, it’s known as a _move_. In this example, we would say that `s1`
was _moved_ into `s2`. So, what actually happens is shown in Figure 4-4.

<img alt="Three tables: tables s1 and s2 representing those strings on the
stack, respectively, and both pointing to the same string data on the heap.
Table s1 is grayed out because s1 is no longer valid; only s2 can be used to
access the heap data." src="img/trpl04-04.svg" class="center" style="width:
50%;" />

<span class="caption">Figure 4-4: The representation in memory after `s1` has
been invalidated</span>

That solves our problem! With only `s2` valid, when it goes out of scope it
alone will free the memory, and we’re done.

In addition, there’s a design choice that’s implied by this: Rust will never
automatically create “deep” copies of your data. Therefore, any _automatic_
copying can be assumed to be inexpensive in terms of runtime performance.

#### Scope and Assignment

The inverse of this is true for the relationship between scoping, ownership, and
memory being freed via the `drop` function as well. When you assign a completely
new value to an existing variable, Rust will call `drop` and free the original
value’s memory immediately. Consider this code, for example:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04b-replacement-drop/src/main.rs:here}}
```

We initially declare a variable `s` and bind it to a `String` with the value
`"hello"`. Then, we immediately create a new `String` with the value `"ahoy"`
and assign it to `s`. At this point, nothing is referring to the original value
on the heap at all. Figure 4-5 illustrates the stack and heap data now:

<img alt="One table representing the string value on the stack, pointing to
the second piece of string data (ahoy) on the heap, with the original string
data (hello) grayed out because it cannot be accessed anymore."
src="img/trpl04-05.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-5: The representation in memory after the initial
value has been replaced in its entirety</span>

The original string thus immediately goes out of scope. Rust will run the `drop`
function on it and its memory will be freed right away. When we print the value
at the end, it will be `"ahoy, world!"`.

<!-- Old headings. Do not remove or links may break. -->

<a id="ways-variables-and-data-interact-clone"></a>

#### Variables and Data Interacting with Clone

If we _do_ want to deeply copy the heap data of the `String`, not just the
stack data, we can use a common method called `clone`. We’ll discuss method
syntax in Chapter 5, but because methods are a common feature in many
programming languages, you’ve probably seen them before.

Here’s an example of the `clone` method in action:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-05-clone/src/main.rs:here}}
```

This works just fine and explicitly produces the behavior shown in Figure 4-3,
where the heap data _does_ get copied.

When you see a call to `clone`, you know that some arbitrary code is being
executed and that code may be expensive. It’s a visual indicator that something
different is going on.

#### Stack-Only Data: Copy

There’s another wrinkle we haven’t talked about yet. This code using
integers—part of which was shown in Listing 4-2—works and is valid:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-06-copy/src/main.rs:here}}
```

But this code seems to contradict what we just learned: We don’t have a call to
`clone`, but `x` is still valid and wasn’t moved into `y`.

The reason is that types such as integers that have a known size at compile
time are stored entirely on the stack, so copies of the actual values are quick
to make. That means there’s no reason we would want to prevent `x` from being
valid after we create the variable `y`. In other words, there’s no difference
between deep and shallow copying here, so calling `clone` wouldn’t do anything
different from the usual shallow copying, and we can leave it out.

Rust has a special annotation called the `Copy` trait that we can place on
types that are stored on the stack, as integers are (we’ll talk more about
traits in [Chapter 10][traits]<!-- ignore -->). If a type implements the `Copy`
trait, variables that use it do not move, but rather are trivially copied,
making them still valid after assignment to another variable.

Rust won’t let us annotate a type with `Copy` if the type, or any of its parts,
has implemented the `Drop` trait. If the type needs something special to happen
when the value goes out of scope and we add the `Copy` annotation to that type,
we’ll get a compile-time error. To learn about how to add the `Copy` annotation
to your type to implement the trait, see [“Derivable
Traits”][derivable-traits]<!-- ignore --> in Appendix C.

So, what types implement the `Copy` trait? You can check the documentation for
the given type to be sure, but as a general rule, any group of simple scalar
values can implement `Copy`, and nothing that requires allocation or is some
form of resource can implement `Copy`. Here are some of the types that
implement `Copy`:

- All the integer types, such as `u32`.
- The Boolean type, `bool`, with values `true` and `false`.
- All the floating-point types, such as `f64`.
- The character type, `char`.
- Tuples, if they only contain types that also implement `Copy`. For example,
  `(i32, i32)` implements `Copy`, but `(i32, String)` does not.

### Ownership and Functions

The mechanics of passing a value to a function are similar to those when
assigning a value to a variable. Passing a variable to a function will move or
copy, just as assignment does. Listing 4-3 has an example with some annotations
showing where variables go into and out of scope.

<Listing number="4-3" file-name="src/main.rs" caption="Functions with ownership and scope annotated">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-03/src/main.rs}}
```

</Listing>

If we tried to use `s` after the call to `takes_ownership`, Rust would throw a
compile-time error. These static checks protect us from mistakes. Try adding
code to `main` that uses `s` and `x` to see where you can use them and where
the ownership rules prevent you from doing so.

### Return Values and Scope

Returning values can also transfer ownership. Listing 4-4 shows an example of a
function that returns some value, with similar annotations as those in Listing
4-3.

<Listing number="4-4" file-name="src/main.rs" caption="Transferring ownership of return values">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-04/src/main.rs}}
```

</Listing>

The ownership of a variable follows the same pattern every time: Assigning a
value to another variable moves it. When a variable that includes data on the
heap goes out of scope, the value will be cleaned up by `drop` unless ownership
of the data has been moved to another variable.

While this works, taking ownership and then returning ownership with every
function is a bit tedious. What if we want to let a function use a value but
not take ownership? It’s quite annoying that anything we pass in also needs to
be passed back if we want to use it again, in addition to any data resulting
from the body of the function that we might want to return as well.

Rust does let us return multiple values using a tuple, as shown in Listing 4-5.

<Listing number="4-5" file-name="src/main.rs" caption="Returning ownership of parameters">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-05/src/main.rs}}
```

</Listing>

But this is too much ceremony and a lot of work for a concept that should be
common. Luckily for us, Rust has a feature for using a value without
transferring ownership: references.

[data-types]: ch03-02-data-types.html#data-types
[ch8]: ch08-02-strings.html
[traits]: ch10-02-traits.html
[derivable-traits]: appendix-03-derivable-traits.html
[methods]: ch05-03-method-syntax.html#methods
[paths-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html

## References and Borrowing

The issue with the tuple code in Listing 4-5 is that we have to return the
`String` to the calling function so that we can still use the `String` after
the call to `calculate_length`, because the `String` was moved into
`calculate_length`. Instead, we can provide a reference to the `String` value.
A reference is like a pointer in that it’s an address we can follow to access
the data stored at that address; that data is owned by some other variable.
Unlike a pointer, a reference is guaranteed to point to a valid value of a
particular type for the life of that reference.

Here is how you would define and use a `calculate_length` function that has a
reference to an object as a parameter instead of taking ownership of the value:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:all}}
```

</Listing>

First, notice that all the tuple code in the variable declaration and the
function return value is gone. Second, note that we pass `&s1` into
`calculate_length` and, in its definition, we take `&String` rather than
`String`. These ampersands represent references, and they allow you to refer to
some value without taking ownership of it. Figure 4-6 depicts this concept.

<img alt="Three tables: the table for s contains only a pointer to the table
for s1. The table for s1 contains the stack data for s1 and points to the
string data on the heap." src="img/trpl04-06.svg" class="center" />

<span class="caption">Figure 4-6: A diagram of `&String` `s` pointing at
`String` `s1`</span>

> Note: The opposite of referencing by using `&` is _dereferencing_, which is
> accomplished with the dereference operator, `*`. We’ll see some uses of the
> dereference operator in Chapter 8 and discuss details of dereferencing in
> Chapter 15.

Let’s take a closer look at the function call here:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:here}}
```

The `&s1` syntax lets us create a reference that _refers_ to the value of `s1`
but does not own it. Because the reference does not own it, the value it points
to will not be dropped when the reference stops being used.

Likewise, the signature of the function uses `&` to indicate that the type of
the parameter `s` is a reference. Let’s add some explanatory annotations:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-08-reference-with-annotations/src/main.rs:here}}
```

The scope in which the variable `s` is valid is the same as any function
parameter’s scope, but the value pointed to by the reference is not dropped
when `s` stops being used, because `s` doesn’t have ownership. When functions
have references as parameters instead of the actual values, we won’t need to
return the values in order to give back ownership, because we never had
ownership.

We call the action of creating a reference _borrowing_. As in real life, if a
person owns something, you can borrow it from them. When you’re done, you have
to give it back. You don’t own it.

So, what happens if we try to modify something we’re borrowing? Try the code in
Listing 4-6. Spoiler alert: It doesn’t work!

<Listing number="4-6" file-name="src/main.rs" caption="Attempting to modify a borrowed value">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-06/src/main.rs}}
```

</Listing>

Here’s the error:

```console
{{#include ../listings/ch04-understanding-ownership/listing-04-06/output.txt}}
```

Just as variables are immutable by default, so are references. We’re not
allowed to modify something we have a reference to.

### Mutable References

We can fix the code from Listing 4-6 to allow us to modify a borrowed value
with just a few small tweaks that use, instead, a _mutable reference_:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-09-fixes-listing-04-06/src/main.rs}}
```

</Listing>

First, we change `s` to be `mut`. Then, we create a mutable reference with
`&mut s` where we call the `change` function and update the function signature
to accept a mutable reference with `some_string: &mut String`. This makes it
very clear that the `change` function will mutate the value it borrows.

Mutable references have one big restriction: If you have a mutable reference to
a value, you can have no other references to that value. This code that
attempts to create two mutable references to `s` will fail:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/src/main.rs:here}}
```

</Listing>

Here’s the error:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/output.txt}}
```

This error says that this code is invalid because we cannot borrow `s` as
mutable more than once at a time. The first mutable borrow is in `r1` and must
last until it’s used in the `println!`, but between the creation of that
mutable reference and its usage, we tried to create another mutable reference
in `r2` that borrows the same data as `r1`.

The restriction preventing multiple mutable references to the same data at the
same time allows for mutation but in a very controlled fashion. It’s something
that new Rustaceans struggle with because most languages let you mutate
whenever you’d like. The benefit of having this restriction is that Rust can
prevent data races at compile time. A _data race_ is similar to a race
condition and happens when these three behaviors occur:

- Two or more pointers access the same data at the same time.
- At least one of the pointers is being used to write to the data.
- There’s no mechanism being used to synchronize access to the data.

Data races cause undefined behavior and can be difficult to diagnose and fix
when you’re trying to track them down at runtime; Rust prevents this problem by
refusing to compile code with data races!

As always, we can use curly brackets to create a new scope, allowing for
multiple mutable references, just not _simultaneous_ ones:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-11-muts-in-separate-scopes/src/main.rs:here}}
```

Rust enforces a similar rule for combining mutable and immutable references.
This code results in an error:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/src/main.rs:here}}
```

Here’s the error:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/output.txt}}
```

Whew! We _also_ cannot have a mutable reference while we have an immutable one
to the same value.

Users of an immutable reference don’t expect the value to suddenly change out
from under them! However, multiple immutable references are allowed because no
one who is just reading the data has the ability to affect anyone else’s
reading of the data.

Note that a reference’s scope starts from where it is introduced and continues
through the last time that reference is used. For instance, this code will
compile because the last usage of the immutable references is in the `println!`,
before the mutable reference is introduced:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-13-reference-scope-ends/src/main.rs:here}}
```

The scopes of the immutable references `r1` and `r2` end after the `println!`
where they are last used, which is before the mutable reference `r3` is
created. These scopes don’t overlap, so this code is allowed: The compiler can
tell that the reference is no longer being used at a point before the end of
the scope.

Even though borrowing errors may be frustrating at times, remember that it’s
the Rust compiler pointing out a potential bug early (at compile time rather
than at runtime) and showing you exactly where the problem is. Then, you don’t
have to track down why your data isn’t what you thought it was.

### Dangling References

In languages with pointers, it’s easy to erroneously create a _dangling
pointer_—a pointer that references a location in memory that may have been
given to someone else—by freeing some memory while preserving a pointer to that
memory. In Rust, by contrast, the compiler guarantees that references will
never be dangling references: If you have a reference to some data, the
compiler will ensure that the data will not go out of scope before the
reference to the data does.

Let’s try to create a dangling reference to see how Rust prevents them with a
compile-time error:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/src/main.rs}}
```

</Listing>

Here’s the error:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/output.txt}}
```

This error message refers to a feature we haven’t covered yet: lifetimes. We’ll
discuss lifetimes in detail in Chapter 10. But, if you disregard the parts
about lifetimes, the message does contain the key to why this code is a problem:

```text
this function's return type contains a borrowed value, but there is no value
for it to be borrowed from
```

Let’s take a closer look at exactly what’s happening at each stage of our
`dangle` code:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-15-dangling-reference-annotated/src/main.rs:here}}
```

</Listing>

Because `s` is created inside `dangle`, when the code of `dangle` is finished,
`s` will be deallocated. But we tried to return a reference to it. That means
this reference would be pointing to an invalid `String`. That’s no good! Rust
won’t let us do this.

The solution here is to return the `String` directly:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-16-no-dangle/src/main.rs:here}}
```

This works without any problems. Ownership is moved out, and nothing is
deallocated.

### The Rules of References

Let’s recap what we’ve discussed about references:

- At any given time, you can have _either_ one mutable reference _or_ any
  number of immutable references.
- References must always be valid.

Next, we’ll look at a different kind of reference: slices.

## The Slice Type

_Slices_ let you reference a contiguous sequence of elements in a
[collection](ch08-00-common-collections.md)<!-- ignore -->. A slice is a kind
of reference, so it does not have ownership.

Here’s a small programming problem: Write a function that takes a string of
words separated by spaces and returns the first word it finds in that string.
If the function doesn’t find a space in the string, the whole string must be
one word, so the entire string should be returned.

> Note: For the purposes of introducing slices, we are assuming ASCII only in
> this section; a more thorough discussion of UTF-8 handling is in the
> [“Storing UTF-8 Encoded Text with Strings”][strings]<!-- ignore --> section
> of Chapter 8.

Let’s work through how we’d write the signature of this function without using
slices, to understand the problem that slices will solve:

```rust,ignore
fn first_word(s: &String) -> ?
```

The `first_word` function has a parameter of type `&String`. We don’t need
ownership, so this is fine. (In idiomatic Rust, functions do not take ownership
of their arguments unless they need to, and the reasons for that will become
clear as we keep going.) But what should we return? We don’t really have a way
to talk about *part* of a string. However, we could return the index of the end
of the word, indicated by a space. Let’s try that, as shown in Listing 4-7.

<Listing number="4-7" file-name="src/main.rs" caption="The `first_word` function that returns a byte index value into the `String` parameter">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:here}}
```

</Listing>

Because we need to go through the `String` element by element and check whether
a value is a space, we’ll convert our `String` to an array of bytes using the
`as_bytes` method.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:as_bytes}}
```

Next, we create an iterator over the array of bytes using the `iter` method:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:iter}}
```

We’ll discuss iterators in more detail in [Chapter 13][ch13]<!-- ignore -->.
For now, know that `iter` is a method that returns each element in a collection
and that `enumerate` wraps the result of `iter` and returns each element as
part of a tuple instead. The first element of the tuple returned from
`enumerate` is the index, and the second element is a reference to the element.
This is a bit more convenient than calculating the index ourselves.

Because the `enumerate` method returns a tuple, we can use patterns to
destructure that tuple. We’ll be discussing patterns more in [Chapter
6][ch6]<!-- ignore -->. In the `for` loop, we specify a pattern that has `i`
for the index in the tuple and `&item` for the single byte in the tuple.
Because we get a reference to the element from `.iter().enumerate()`, we use
`&` in the pattern.

Inside the `for` loop, we search for the byte that represents the space by
using the byte literal syntax. If we find a space, we return the position.
Otherwise, we return the length of the string by using `s.len()`.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:inside_for}}
```

We now have a way to find out the index of the end of the first word in the
string, but there’s a problem. We’re returning a `usize` on its own, but it’s
only a meaningful number in the context of the `&String`. In other words,
because it’s a separate value from the `String`, there’s no guarantee that it
will still be valid in the future. Consider the program in Listing 4-8 that
uses the `first_word` function from Listing 4-7.

<Listing number="4-8" file-name="src/main.rs" caption="Storing the result from calling the `first_word` function and then changing the `String` contents">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-08/src/main.rs:here}}
```

</Listing>

This program compiles without any errors and would also do so if we used `word`
after calling `s.clear()`. Because `word` isn’t connected to the state of `s`
at all, `word` still contains the value `5`. We could use that value `5` with
the variable `s` to try to extract the first word out, but this would be a bug
because the contents of `s` have changed since we saved `5` in `word`.

Having to worry about the index in `word` getting out of sync with the data in
`s` is tedious and error-prone! Managing these indices is even more brittle if
we write a `second_word` function. Its signature would have to look like this:

```rust,ignore
fn second_word(s: &String) -> (usize, usize) {
```

Now we’re tracking a starting _and_ an ending index, and we have even more
values that were calculated from data in a particular state but aren’t tied to
that state at all. We have three unrelated variables floating around that need
to be kept in sync.

Luckily, Rust has a solution to this problem: string slices.

### String Slices

A _string slice_ is a reference to a contiguous sequence of the elements of a
`String`, and it looks like this:

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-17-slice/src/main.rs:here}}
```

Rather than a reference to the entire `String`, `hello` is a reference to a
portion of the `String`, specified in the extra `[0..5]` bit. We create slices
using a range within square brackets by specifying
`[starting_index..ending_index]`, where _`starting_index`_ is the first
position in the slice and _`ending_index`_ is one more than the last position
in the slice. Internally, the slice data structure stores the starting position
and the length of the slice, which corresponds to _`ending_index`_ minus
_`starting_index`_. So, in the case of `let world = &s[6..11];`, `world` would
be a slice that contains a pointer to the byte at index 6 of `s` with a length
value of `5`.

Figure 4-7 shows this in a diagram.

<img alt="Three tables: a table representing the stack data of s, which points
to the byte at index 0 in a table of the string data &quot;hello world&quot; on
the heap. The third table represents the stack data of the slice world, which
has a length value of 5 and points to byte 6 of the heap data table."
src="img/trpl04-07.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-7: A string slice referring to part of a
`String`</span>

With Rust’s `..` range syntax, if you want to start at index 0, you can drop
the value before the two periods. In other words, these are equal:

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

By the same token, if your slice includes the last byte of the `String`, you
can drop the trailing number. That means these are equal:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

You can also drop both values to take a slice of the entire string. So, these
are equal:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> Note: String slice range indices must occur at valid UTF-8 character
> boundaries. If you attempt to create a string slice in the middle of a
> multibyte character, your program will exit with an error.

With all this information in mind, let’s rewrite `first_word` to return a
slice. The type that signifies “string slice” is written as `&str`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-18-first-word-slice/src/main.rs:here}}
```

</Listing>

We get the index for the end of the word the same way we did in Listing 4-7, by
looking for the first occurrence of a space. When we find a space, we return a
string slice using the start of the string and the index of the space as the
starting and ending indices.

Now when we call `first_word`, we get back a single value that is tied to the
underlying data. The value is made up of a reference to the starting point of
the slice and the number of elements in the slice.

Returning a slice would also work for a `second_word` function:

```rust,ignore
fn second_word(s: &String) -> &str {
```

We now have a straightforward API that’s much harder to mess up because the
compiler will ensure that the references into the `String` remain valid.
Remember the bug in the program in Listing 4-8, when we got the index to the
end of the first word but then cleared the string so our index was invalid?
That code was logically incorrect but didn’t show any immediate errors. The
problems would show up later if we kept trying to use the first word index with
an emptied string. Slices make this bug impossible and let us know much sooner
that we have a problem with our code. Using the slice version of `first_word`
will throw a compile-time error:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/src/main.rs:here}}
```

</Listing>

Here’s the compiler error:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/output.txt}}
```

Recall from the borrowing rules that if we have an immutable reference to
something, we cannot also take a mutable reference. Because `clear` needs to
truncate the `String`, it needs to get a mutable reference. The `println!`
after the call to `clear` uses the reference in `word`, so the immutable
reference must still be active at that point. Rust disallows the mutable
reference in `clear` and the immutable reference in `word` from existing at the
same time, and compilation fails. Not only has Rust made our API easier to use,
but it has also eliminated an entire class of errors at compile time!

<!-- Old headings. Do not remove or links may break. -->

<a id="string-literals-are-slices"></a>

#### String Literals as Slices

Recall that we talked about string literals being stored inside the binary. Now
that we know about slices, we can properly understand string literals:

```rust
let s = "Hello, world!";
```

The type of `s` here is `&str`: It’s a slice pointing to that specific point of
the binary. This is also why string literals are immutable; `&str` is an
immutable reference.

#### String Slices as Parameters

Knowing that you can take slices of literals and `String` values leads us to
one more improvement on `first_word`, and that’s its signature:

```rust,ignore
fn first_word(s: &String) -> &str {
```

A more experienced Rustacean would write the signature shown in Listing 4-9
instead because it allows us to use the same function on both `&String` values
and `&str` values.

<Listing number="4-9" caption="Improving the `first_word` function by using a string slice for the type of the `s` parameter">

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:here}}
```

</Listing>

If we have a string slice, we can pass that directly. If we have a `String`, we
can pass a slice of the `String` or a reference to the `String`. This
flexibility takes advantage of deref coercions, a feature we will cover in
the [“Using Deref Coercions in Functions and Methods”][deref-coercions]<!--
ignore --> section of Chapter 15.

Defining a function to take a string slice instead of a reference to a `String`
makes our API more general and useful without losing any functionality:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:usage}}
```

</Listing>

### Other Slices

String slices, as you might imagine, are specific to strings. But there’s a
more general slice type too. Consider this array:

```rust
let a = [1, 2, 3, 4, 5];
```

Just as we might want to refer to part of a string, we might want to refer to
part of an array. We’d do so like this:

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

This slice has the type `&[i32]`. It works the same way as string slices do, by
storing a reference to the first element and a length. You’ll use this kind of
slice for all sorts of other collections. We’ll discuss these collections in
detail when we talk about vectors in Chapter 8.

## Summary

The concepts of ownership, borrowing, and slices ensure memory safety in Rust
programs at compile time. The Rust language gives you control over your memory
usage in the same way as other systems programming languages. But having the
owner of data automatically clean up that data when the owner goes out of scope
means you don’t have to write and debug extra code to get this control.

Ownership affects how lots of other parts of Rust work, so we’ll talk about
these concepts further throughout the rest of the book. Let’s move on to
Chapter 5 and look at grouping pieces of data together in a `struct`.

[ch13]: ch13-02-iterators.html
[ch6]: ch06-02-match.html#patterns-that-bind-to-values
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[deref-coercions]: ch15-02-deref.html#using-deref-coercions-in-functions-and-methods
