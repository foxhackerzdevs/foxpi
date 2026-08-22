# 🦊 FoxPi

**High-precision terminal π explorer — Chudnovsky, Ramanujan, Machin, and BBP spigot algorithms.**

[![Python](https://img.shields.io/badge/Python-%3E%3D3.8-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Algorithms](https://img.shields.io/badge/Algorithms-4-orange)](#algorithms)
[![Precision](https://img.shields.io/badge/Precision-Arbitrary-purple)](#decimal-digit-computation)

FoxPi is a pure-Python command-line toolkit for computing, exploring, benchmarking, and validating π using several classical and modern algorithms.

It supports arbitrary-precision decimal computation with **Chudnovsky**, **Ramanujan**, and **Machin**, plus direct hexadecimal digit extraction using the **Bailey–Borwein–Plouffe (BBP)** formula.

The implementation uses integer-scaled arithmetic and includes an independent test suite that checks computed decimal and hexadecimal digits against reference values rather than merely comparing algorithms against themselves.

---

## ✨ Features

- 🧮 Arbitrary-precision decimal computation of π
- ⚡ Chudnovsky computation with binary splitting
- 📜 Ramanujan's rapidly convergent hypergeometric series
- 📐 Classical Machin formula
- 🔢 BBP hexadecimal digit extraction
- 🔬 Term-by-term convergence exploration
- 📊 Built-in algorithm benchmarking
- 🧱 Integer-scaled arithmetic for high-precision calculations
- 🧪 Automated tests against independent reference digits
- 📦 Standard-library implementation with no runtime dependencies
- 🐍 Python package/CLI entry point via `pyproject.toml`
- 📄 MIT licensed

---

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Reference](#cli-reference)
  - [`digits`](#digits)
  - [`explore`](#explore)
  - [`compare`](#compare)
  - [`bbp`](#bbp)
- [Algorithms](#algorithms)
  - [Chudnovsky](#chudnovsky)
  - [Ramanujan](#ramanujan)
  - [Machin](#machin)
  - [BBP](#bbp-hexadecimal-spigot)
- [Precision and Implementation](#precision-and-implementation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Development](#development)
- [Performance](#performance)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

---

# Installation

## Requirements

FoxPi requires:

- **Python 3.8 or newer**
- `pip` for optional editable/package installation

The project declares **no runtime third-party dependencies**.

## Clone the repository

```bash
git clone https://github.com/foxhackerzdevs/foxpi.git
cd foxpi
```

## Run directly

You can run FoxPi directly from the repository:

```bash
python cli.py digits 100
```

For example:

```text
π (100 digits) using Chudnovsky:
3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
Time: 0.00xxs
```

## Install the CLI

FoxPi defines a `foxpi` console-script entry point in `pyproject.toml`.

### Install from PyPI

If a published package is available:

```bash
python3 -m pip install foxpi
```

Then run:

```bash
foxpi digits 100
```

### Install from Source

Clone the repository:

```bash
git clone https://github.com/foxhackerzdevs/foxpi.git
cd foxpi
```

Install it in editable mode:

```bash
python -m pip install -e .
```

Then use:

```bash
foxpi digits 100
```

The project metadata currently identifies the package as version `0.1.1`.

---

# 🚀 Quick Start

Compute 100 digits of π:

```bash
python cli.py digits 100
```

Use Chudnovsky explicitly:

```bash
python cli.py digits 1000 --method chudnovsky
```

Use Ramanujan:

```bash
python cli.py digits 1000 --method ramanujan
```

Use Machin:

```bash
python cli.py digits 1000 --method machin
```

Explore convergence:

```bash
python cli.py explore --method chudnovsky --terms 15
```

Benchmark the 1000-digit Chudnovsky and Machin implementations:

```bash
python cli.py compare
```

Extract 16 hexadecimal digits beginning at hexadecimal position 100:

```bash
python cli.py bbp 100
```

---

# 🖥️ CLI Reference

FoxPi exposes four commands:

```text
foxpi
├── digits
├── explore
├── compare
└── bbp
```

The same commands can be run through `python cli.py` when working directly from the repository. The CLI requires a subcommand; invoking it without one displays the command-line usage information and exits with an error.

---

## `digits`

Compute a requested number of decimal digits of π.

```bash
python cli.py digits COUNT
```

### Arguments

| Argument | Description |
|---|---|
| `COUNT` | Number of decimal digits requested |
| `--method` | `chudnovsky`, `ramanujan`, or `machin` |

The default method is **Chudnovsky**.

### Examples

```bash
python cli.py digits 50
```

```bash
python cli.py digits 1000 --method chudnovsky
```

```bash
python cli.py digits 1000 --method ramanujan
```

```bash
python cli.py digits 1000 --method machin
```

FoxPi also raises Python's integer-to-string digit limit when necessary so large requested precisions can be printed on Python versions that impose the default conversion limit.

### Input validation

Negative decimal digit counts are rejected:

```text
Error: digit count must be >= 0
```

---

# `explore`

Explore the convergence of the Ramanujan or Chudnovsky series.

```bash
python cli.py explore
```

### Options

```bash
--method ramanujan
--method chudnovsky
--terms N
```

The default method is Ramanujan and the default number of displayed terms is 30.

### Examples

```bash
python cli.py explore
```

```bash
python cli.py explore --method ramanujan --terms 20
```

```bash
python cli.py explore --method chudnovsky --terms 10
```

The command displays intermediate π estimates and finishes with a convergence table containing the iteration, term information, and a π preview.

For visualization purposes, the Chudnovsky convergence generator recomputes binary-splitting results at each step rather than using the optimized one-shot computation. The implementation explicitly treats this as suitable for the small number of terms used by `explore`.

---

# `compare`

Benchmark the currently configured algorithm implementations.

```bash
python cli.py compare
```

The current benchmark compares:

- Chudnovsky
- Machin

Both are benchmarked at **1000 decimal digits**.

Example:

```text
Benchmarking algorithms...

Algorithm       | Precision (Digits)   | Time Elapsed (s)
------------------------------------------------------------
Chudnovsky      | 1000                 | ...
Machin          | 1000                 | ...
```

> **Note:** Benchmark times depend on the Python version, processor, operating system, and system load. Treat the output as a local comparison rather than a universal performance ranking.

---

# `bbp`

Extract hexadecimal digits of π using the Bailey–Borwein–Plouffe formula.

```bash
python cli.py bbp POSITION
```

`POSITION=1` refers to the first hexadecimal digit after the hexadecimal point.

### Examples

```bash
python cli.py bbp 1
```

```bash
python cli.py bbp 25
```

```bash
python cli.py bbp 1000
```

FoxPi returns **16 hexadecimal digits** beginning at the requested position.

Example:

```text
Extracting 16 hex digits of π starting at position 1:
243F6A8885A308D3
(BBP Spigot — hexadecimal)
```

Positions below `1` are rejected by the CLI.

---

# 🧮 Algorithms

FoxPi currently implements four π-related algorithms.

| Algorithm | Output | Primary purpose |
|---|---|---|
| **Chudnovsky** | Decimal | High-precision computation |
| **Ramanujan** | Decimal | Rapid convergence / exploration |
| **Machin** | Decimal | Classical formula / comparison |
| **BBP** | Hexadecimal | Direct digit extraction |

---

## Chudnovsky

The Chudnovsky series is FoxPi's primary high-precision decimal computation method.

The implementation uses **binary splitting** to evaluate the series efficiently using large integers. It estimates approximately 14 decimal digits of π per iteration and calculates the number of required terms from the requested precision.

The implementation also uses additional guard precision internally before scaling the final result back to the requested number of digits.

### Use it for

- High-precision π computation
- Large decimal digit counts
- The default `digits` method

Example:

```bash
python cli.py digits 10000 --method chudnovsky
```

---

## Ramanujan

FoxPi implements Ramanujan's 1914 hypergeometric series for `1/π`:

```text
1/π =
(2√2 / 9801)
×
Σ [
  (4k)! × (1103 + 26390k)
  /
  ((k!)⁴ × 396⁴ᵏ)
]
```

The implementation maintains the calculation using scaled integers and updates the hypergeometric numerator and denominator iteratively.

### Use it for

- Studying rapid series convergence
- Mathematical exploration
- High-precision decimal calculation

Example:

```bash
python cli.py digits 1000 --method ramanujan
```

Or explore it interactively:

```bash
python cli.py explore --method ramanujan --terms 20
```

---

## Machin

FoxPi implements the classical Machin identity:

```text
π = 4 × (4 arccot(5) − arccot(239))
```

The arccotangent series is evaluated using scaled integer arithmetic.

### Use it for

- A compact classical π formula
- Mathematical education
- Comparing an older approach with Chudnovsky

Example:

```bash
python cli.py digits 500 --method machin
```

---

## BBP hexadecimal spigot

The Bailey–Borwein–Plouffe formula provides a particularly useful property: hexadecimal digits of π can be extracted starting at a selected position without first calculating all preceding hexadecimal digits.

FoxPi's implementation uses Python's `Decimal` arithmetic with additional precision rather than native binary floating point. The implementation generates exactly 16 hexadecimal digits for each request.

Example:

```bash
python cli.py bbp 1
```

Expected first 16 hexadecimal fractional digits:

```text
243F6A8885A308D3
```

---

# 🎯 Precision and Implementation

FoxPi intentionally avoids relying on a third-party arbitrary-precision mathematics package for its core calculations.

The decimal algorithms use **scaled integers**. Additional guard digits are calculated internally and removed from the final integer representation before output.

The project also provides its own integer square-root implementation based on Newton-Raphson iteration:

```python
isqrt(n)
```

It:

- Rejects negative inputs with `ValueError`
- Returns `0` for zero
- Computes the integer floor square root for positive integers

This helper is covered by the test suite.

---

# 🧪 Testing

FoxPi includes a test suite under `tests/`.

Run it with Python's standard `unittest` framework:

```bash
python -m unittest discover -s tests -v
```

The tests cover:

- Integer square roots
- Chudnovsky decimal computation
- Ramanujan decimal computation
- Chudnovsky convergence terms
- Machin decimal computation
- BBP hexadecimal extraction
- Generator termination
- Invalid square-root input

The π tests are deliberately checked against **independently generated reference digits** rather than simply comparing one FoxPi implementation against another. The repository's tests document reference values generated using `mpmath` at 250 decimal digits of working precision.

### Decimal verification

The Chudnovsky implementation is tested at:

```text
1
10
50
100
194
```

decimal places/digits according to the test suite's precision convention. Ramanujan and Machin are also checked against the reference decimal sequence.

### BBP verification

BBP output is independently checked at positions:

```text
1
25
50
100
```

with 16 hexadecimal digits verified at each position.

---

# 📁 Project Structure

The current repository contains:

```text
foxpi/
├── core/
│   ├── algorithms.py
│   └── visualize.py
│
├── tests/
│   └── test_algorithms.py
│
├── .gitignore
├── LICENSE
├── README.md
├── cli.py
└── pyproject.toml
```

### `cli.py`

Defines the `foxpi` command-line interface and dispatches commands to the mathematical and visualization modules.

### `core/algorithms.py`

Contains the mathematical implementations:

- `get_ramanujan_pi_terms`
- `get_chudnovsky_pi_terms`
- `compute_chudnovsky_pi`
- `compute_machin_pi`
- `generate_bbp_spigot`
- `isqrt`

### `core/visualize.py`

Provides terminal rendering helpers for convergence and benchmark results.

### `tests/test_algorithms.py`

Contains independent-reference verification tests for the mathematical implementations.

### `pyproject.toml`

Defines the package metadata and exposes:

```text
foxpi = cli:main
```

as the installed console command.

---

# 🛠️ Development

Create a development checkout:

```bash
git clone https://github.com/foxhackerzdevs/foxpi.git
cd foxpi
```

Run the CLI directly:

```bash
python cli.py --help
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

Install in editable mode:

```bash
python -m pip install -e .
```

Then:

```bash
foxpi --help
```

---

# ⚡ Performance

Performance depends heavily on requested precision.

For general high-precision decimal computation, Chudnovsky is the intended high-performance implementation. Its binary-splitting approach reduces the overhead of evaluating the series term-by-term.

The built-in benchmark provides a convenient way to compare Chudnovsky and Machin on the current machine:

```bash
python cli.py compare
```

Keep in mind that:

- Larger precisions require substantially larger integers.
- Memory requirements increase with precision.
- Runtime depends on the Python implementation and CPU.
- Benchmark results are machine-specific.
- `explore` is intentionally optimized for visualization rather than maximum throughput.

---

# ⚠️ Limitations

FoxPi is primarily an educational, experimental, and mathematical exploration tool.

### Very large precisions

Arbitrary precision does not mean unlimited practical precision. Extremely large requests can consume considerable CPU time and memory.

### BBP output

The BBP command currently emits 16 hexadecimal digits per invocation rather than providing a configurable output length.

### Benchmark scope

The `compare` command currently benchmarks Chudnovsky and Machin at a fixed 1000-digit precision. It is not a general benchmarking framework.

### Convergence visualization

The Chudnovsky convergence generator intentionally recomputes binary-splitting results for each displayed step. This makes it appropriate for exploration but not for replacing the optimized computation routine.

---

# 🤝 Contributing

Contributions, improvements, bug reports, and mathematical enhancements are welcome.

Potential areas for development include:

- Additional π algorithms
- More efficient incremental convergence calculations
- Configurable BBP output length
- Expanded benchmark configuration
- More comprehensive CLI tests
- Performance profiling
- Packaging and distribution improvements
- Additional reference-value tests
- Documentation improvements

## Suggested workflow

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Add or update tests where appropriate.
5. Run the test suite.
6. Open a pull request with a clear description of the change.

Before submitting a mathematical algorithm change, include independent reference validation whenever practical.

---

# 📜 License

FoxPi is released under the **MIT License**.

Copyright © 2026 Fox Hackerz.

See [`LICENSE`](LICENSE) for the complete license text.

---

# 🔗 Repository

**GitHub:**  
https://github.com/foxhackerzdevs/foxpi

**Project homepage:**  
https://foxhackerzdevs.github.io/foxpi/

---

## 🦊 Why FoxPi?

FoxPi brings several historically important π algorithms together in one small, dependency-free command-line project.

It is designed not only to **calculate π**, but also to make the underlying computational ideas easy to experiment with:

```text
             ┌──────────────────────┐
             │        FoxPi         │
             │   π Explorer 🦊      │
             └──────────┬───────────┘
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
  Decimal π         Convergence      Hexadecimal π
        │               │                │
   ┌────┼────┐      ┌───┴────┐          │
   │    │    │      │        │          ▼
   ▼    ▼    ▼      ▼        ▼        BBP
  Chu  Ram  Mach  Ramanujan Chud
  dnov  anu  in
  sky   jan
```

**Compute it. Explore it. Benchmark it. Verify it. 🦊**
