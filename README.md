# 🦊 FoxPi

**High-precision terminal π explorer — Chudnovsky, Ramanujan, Machin, and BBP spigot algorithms.**

[![Python](https://img.shields.io/badge/Python-%3E%3D3.8-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/foxpi)](https://pypi.org/project/foxpi/)
[![Algorithms](https://img.shields.io/badge/Algorithms-4-orange)](#algorithms)
[![Precision](https://img.shields.io/badge/Precision-Arbitrary-purple)](#precision-and-implementation)

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
- [Quick Start](#-quick-start)
- [CLI Reference](#-cli-reference)
  - [`digits`](#digits)
  - [`explore`](#explore)
  - [`compare`](#compare)
  - [`bbp`](#bbp)
- [Algorithms](#-algorithms)
  - [Chudnovsky](#chudnovsky)
  - [Ramanujan](#ramanujan)
  - [Machin](#machin)
  - [BBP](#bbp-hexadecimal-spigot)
- [Precision and Implementation](#-precision-and-implementation)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Performance](#-performance)
- [Limitations](#-limitations)
- [Contributing](#-contributing)
- [License](#-license)

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

Example output:

```text
π (100 digits) using Chudnovsky:
3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
Time: 0.00xxs
```

## Install the CLI

FoxPi defines a `foxpi` console-script entry point in `pyproject.toml`.

### Install from PyPI

```bash
python3 -m pip install foxpi
```

Then run:

```bash
foxpi digits 100
```

### Install from Source

```bash
git clone https://github.com/foxhackerzdevs/foxpi.git
cd foxpi
python -m pip install -e .
```

Then:

```bash
foxpi digits 100
```

Current version: **0.1.2**

---

# 🚀 Quick Start

```bash
# Compute 100 digits
python cli.py digits 100

# Use a specific method
python cli.py digits 1000 --method chudnovsky
python cli.py digits 1000 --method ramanujan
python cli.py digits 1000 --method machin

# Explore convergence
python cli.py explore --method chudnovsky --terms 15

# Benchmark
python cli.py compare

# Extract hexadecimal digits
python cli.py bbp 100
```

---

# - CLI Reference

FoxPi exposes four commands:

```text
foxpi
├── digits
├── explore
├── compare
└── bbp
```

The same commands can be run through `python cli.py` when working directly from the repository.

---

## `digits`

Compute a requested number of decimal digits of π.

```bash
python cli.py digits COUNT [--method METHOD]
```

| Argument | Description |
|---|---|
| `COUNT` | Number of decimal digits requested |
| `--method` | `chudnovsky` (default), `ramanujan`, or `machin` |

### Examples

```bash
python cli.py digits 50
python cli.py digits 1000 --method chudnovsky
python cli.py digits 1000 --method ramanujan
python cli.py digits 1000 --method machin
```

FoxPi automatically raises Python’s integer-to-string digit limit when necessary.

Negative digit counts are rejected.

---

## `explore`

Explore the convergence of the Ramanujan or Chudnovsky series.

```bash
python cli.py explore [--method METHOD] [--terms N]
```

- Default method: `ramanujan`
- Default terms: `30`

```bash
python cli.py explore
python cli.py explore --method ramanujan --terms 20
python cli.py explore --method chudnovsky --terms 10
```

---

## `compare`

Benchmark Chudnovsky and Machin at 1000 decimal digits.

```bash
python cli.py compare
```

---

## `bbp`

Extract 16 hexadecimal digits of π starting at a given position.

```bash
python cli.py bbp POSITION
```

`POSITION=1` is the first hexadecimal digit after the point.

```bash
python cli.py bbp 1
python cli.py bbp 25
python cli.py bbp 100
```

---

# 🧮 Algorithms

| Algorithm | Output | Primary purpose |
|---|---|---|
| **Chudnovsky** | Decimal | High-precision computation |
| **Ramanujan** | Decimal | Rapid convergence / exploration |
| **Machin** | Decimal | Classical formula / comparison |
| **BBP** | Hexadecimal | Direct digit extraction |

---

## Chudnovsky

Binary-splitting implementation of the Chudnovsky series (~14 digits per term).  
This is the default and recommended method for high-precision decimal computation.

```bash
python cli.py digits 10000 --method chudnovsky
```

---

## Ramanujan

Ramanujan’s 1914 hypergeometric series for \(1/\pi\):

\[
\frac{1}{\pi} = \frac{2\sqrt{2}}{9801} \sum_{k=0}^{\infty} \frac{(4k)! (1103 + 26390k)}{(k!)^4 396^{4k}}
\]

Excellent for studying rapid convergence.

```bash
python cli.py digits 1000 --method ramanujan
python cli.py explore --method ramanujan --terms 20
```

---

## Machin

Classical Machin formula:

\[
\pi = 4 \bigl(4\arctan\frac{1}{5} - \arctan\frac{1}{239}\bigr)
\]

```bash
python cli.py digits 500 --method machin
```

---

## BBP hexadecimal spigot

Bailey–Borwein–Plouffe formula allowing direct extraction of hexadecimal digits without computing preceding ones.

```bash
python cli.py bbp 1
# → 243F6A8885A308D3
```

---

# 🎯 Precision and Implementation

FoxPi uses **scaled-integer arithmetic** with internal guard digits.  
No third-party arbitrary-precision library is required at runtime.

A custom Newton–Raphson `isqrt` implementation is provided and covered by the test suite.

---

# 🧪 Testing

```bash
python -m unittest discover -s tests -v
```

Tests verify results against independently generated reference digits (mpmath, 250 decimal digits of working precision).

---

# 📁 Project Structure

```text
foxpi/
├── core/
│   ├── algorithms.py
│   └── visualize.py
├── tests/
│   ├── test_algorithms.py
│   └── test_cli.py
├── .gitignore
├── LICENSE
├── README.md
├── cli.py
└── pyproject.toml
```

---

# - Development

```bash
git clone https://github.com/foxhackerzdevs/foxpi.git
cd foxpi

# Run directly
python cli.py --help

# Run tests
python -m unittest discover -s tests -v

# Editable install
python -m pip install -e .
foxpi --help
```

---

# ⚡ Performance

Chudnovsky with binary splitting is the recommended high-performance path.  
Use `python cli.py compare` for a quick local benchmark.

Performance depends on Python version, CPU, and requested precision.

---

# - Limitations

- Extremely large precisions consume significant time and memory.
- BBP currently returns a fixed 16 hexadecimal digits.
- The `compare` command uses a fixed 1000-digit workload.
- Convergence exploration (`explore`) intentionally recomputes for visualization and is not optimized for speed.

---

# 🤝 Contributing

Contributions are welcome. Suggested areas:

- Additional algorithms
- Configurable BBP length
- Expanded benchmarks
- More tests
- Documentation improvements

1. Fork the repository  
2. Create a feature branch  
3. Add tests where appropriate  
4. Open a pull request

---

# 📜 License

FoxPi is released under the **MIT License**.

Copyright © 2026 Fox Hackerz

See [`LICENSE`](LICENSE) for the full text.

---

# 🔗 Links

- **GitHub:** https://github.com/foxhackerzdevs/foxpi  
- **PyPI:** https://pypi.org/project/foxpi/  
- **Homepage:** https://foxhackerzdevs.github.io/foxpi/

---

**Compute it. Explore it. Benchmark it. Verify it. 🦊**
