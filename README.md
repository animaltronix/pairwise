# Pairwise Testing Generator

A Python application for generating test configuration combinations using pairwise (all pairs) testing algorithms with support for parameter constraints.

## Features

- **Greedy Algorithm**: Implements the greedy pairwise testing algorithm
- **Flexible Input**: Add unlimited parameters and values
- **Constraint Support**: Define parameter dependencies and invalid combinations
- **Export Options**: Export results to Excel (.xlsx) or CSV format
- **Simple UI**: Easy-to-use interface with tabbed interface
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

## Constraint System

The application supports parameter constraints to handle real-world dependencies:

### Example: Soft-Synth Testing
- **Format**: VST3, AUv3, Desktop Stand Alone
- **DAW**: Logic, Pro Tools, Ableton (only for plugin formats)
- **Constraints**:
  - IF Format = 'Desktop Stand Alone' THEN DAW must be empty
  - IF Format = 'VST3' THEN DAW must not be empty
  - IF Format = 'AUv3' THEN DAW must not be empty

### Constraint Syntax
- **Conditions**: `parameter = 'value'`, `parameter != 'value'`
- **Actions**: `parameter must be empty`, `parameter must not be empty`
- **Format**: `IF condition THEN action`

## Workflow

1. **Add Parameters**: Define all parameters and their possible values
2. **Add Constraints**: Define dependencies between parameters
3. **Generate Test Cases**: Algorithm respects constraints and generates valid combinations
4. **Export Results**: Save to Excel or CSV format 