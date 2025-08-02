# Pairwise Testing Generator

A Python application for generating test configuration combinations using pairwise (all pairs) testing algorithms.

## Features

- **Greedy Algorithm**: Implements the greedy pairwise testing algorithm
- **Flexible Input**: Add unlimited parameters and values
- **Export Options**: Export results to Excel (.xlsx) or CSV format
- **Simple UI**: Easy-to-use interface for local testing
- **Extensible**: Architecture supports adding new algorithms

## Installation

1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

## How Pairwise Testing Works

Pairwise testing reduces the number of test cases by ensuring every pair of parameter values is tested together at least once. This catches most interaction bugs while keeping test suites manageable.

Example: With 3 parameters each having 3 values, instead of 27 test cases, pairwise testing might use only 6-9 test cases while still covering all parameter pairs. 