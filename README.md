# 🦊 FoxPi

**High-precision π explorer and mathematical visualization toolkit for the command line.**

FoxPi is a Python-based CLI application for computing and exploring the digits of π using several famous algorithms. It provides fast high-precision computation, convergence visualization, benchmarking tools, and hexadecimal digit extraction via the Bailey–Borwein–Plouffe (BBP) formula.

---

# Table of Contents

* [Features](#features)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)

  * Compute Digits
  * Explore Convergence
  * Compare Algorithms
  * BBP Hexadecimal Digits
* [Algorithms Implemented](#algorithms-implemented)
* [Examples](#examples)
* [Dependencies](#dependencies)
* [Configuration](#configuration)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)

---

# Features

* Compute π to an arbitrary number of decimal digits.
* Multiple computation algorithms:

  * Chudnovsky Algorithm
  * Ramanujan Series
  * Machin Formula
* Interactive convergence exploration.
* Benchmark algorithm performance.
* Extract hexadecimal digits directly using the BBP formula.
* Pure Python implementation using integer arithmetic for high precision.
* No third-party dependencies.

---

# Project Structure

```text
foxpi/
│
├── cli.py                # Command-line interface
└── core/
    ├── algorithms.py     # Mathematical algorithms
    └── visualize.py      # CLI visualization utilities
```

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd foxpi
```

Python 3.9+ is recommended.

No external packages are required.

Run with a subcommand:

```bash
python cli.py digits 100
```

`python cli.py` alone (with no subcommand) prints usage and exits with an error — a subcommand (`digits`, `explore`, `compare`, or `bbp`) is required.

or

```bash
python -m cli
```

---

# Usage

## Compute Decimal Digits

Compute π using one of the supported algorithms.

```bash
python cli.py digits 1000
```

Specify the algorithm:

```bash
python cli.py digits 5000 --method chudnovsky
```

```bash
python cli.py digits 1000 --method ramanujan
```

```bash
python cli.py digits 1000 --method machin
```

---

## Explore Convergence

Watch the approximation converge term by term.

```bash
python cli.py explore
```

Choose an algorithm:

```bash
python cli.py explore --method ramanujan
```

```bash
python cli.py explore --method chudnovsky
```

Limit the number of displayed terms:

```bash
python cli.py explore --terms 20
```

---

## Compare Algorithms

Benchmark the available implementations.

```bash
python cli.py compare
```

Current benchmark compares:

* Chudnovsky
* Machin

---

## Extract Hexadecimal Digits (BBP)

Retrieve hexadecimal digits beginning at a specified position without computing previous digits.

```bash
python cli.py bbp 1
```

Example:

```bash
python cli.py bbp 1000
```

Outputs the next 16 hexadecimal digits beginning at that position.

---

# Algorithms Implemented

## Chudnovsky Algorithm

* Modern state-of-the-art series for computing π.
* Approximately **14 decimal digits per term**.
* Uses **binary splitting** for efficient large integer arithmetic.
* Suitable for very high precision.

---

## Ramanujan Series

* Classic 1914 hypergeometric series.
* Extremely rapid convergence.
* Integer-scaled implementation for numerical stability.

---

## Machin Formula

Uses

```
π = 4 × (4 arccot(5) − arccot(239))
```

Advantages:

* Simple
* Educational
* Useful for comparison against faster modern methods

---

## Bailey–Borwein–Plouffe (BBP)

Supports direct extraction of hexadecimal digits of π.

Unlike traditional algorithms, BBP allows accessing hexadecimal digits beginning at an arbitrary position without computing all preceding digits.

---

# Examples

Compute 100 digits:

```bash
python cli.py digits 100
```

Compute 5000 digits using Chudnovsky:

```bash
python cli.py digits 5000 --method chudnovsky
```

Visualize convergence:

```bash
python cli.py explore --method chudnovsky --terms 15
```

Benchmark:

```bash
python cli.py compare
```

Extract hexadecimal digits:

```bash
python cli.py bbp 250
```

---

# Dependencies

Only Python standard library modules are used:

* argparse
* decimal
* pathlib
* sys
* time
* typing

No external dependencies are required.

---

# Configuration

There are currently no configuration files.

Precision and algorithm selection are controlled through command-line arguments.

---

# Troubleshooting

### Import errors

Ensure the project directory structure matches the expected layout:

```text
core/
    algorithms.py
    visualize.py
```

---

### Slow execution

Very large digit counts require significant CPU time.

For best performance:

* Prefer the Chudnovsky algorithm.
* Use Ramanujan for convergence exploration.
* Use Machin primarily for educational purposes and comparisons.

---

### Unexpected precision

Higher requested precision naturally requires more computation time and memory due to large integer arithmetic.

---

# Contributing

Contributions are welcome.

Possible improvements include:

* Additional π algorithms
* Parallel binary splitting
* Progress bars
* Graphical convergence plots
* Export benchmark results
* Automated testing
* Packaging for PyPI

---

# License

No license information was provided in the source files.

Consider adding a `LICENSE` file (for example MIT, Apache-2.0, or GPL-3.0) before publishing the project.
