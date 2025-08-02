# Quick Start Guide

## Installation

1. **Install Python 3.8+** (if not already installed)
2. **Install dependencies:**
   ```bash
   pip3 install pandas openpyxl
   ```

## Running the Application

1. **Start the application:**
   ```bash
   python3 main.py
   ```

2. **Add Parameters (Parameters Tab):**
   - Enter a parameter name (e.g., "Format")
   - Enter comma-separated values (e.g., "VST3, AUv3, Desktop Stand Alone")
   - Click "Add Parameter"
   - Repeat for all parameters

3. **Add Constraints (Constraints Tab):**
   - Enter constraint in format: `IF condition THEN action`
   - Examples:
     - `IF Format = 'Desktop Stand Alone' THEN DAW must be empty`
     - `IF Format = 'VST3' THEN DAW must not be empty`
   - Add optional description
   - Click "Add Constraint"

4. **Generate Test Cases:**
   - Select the algorithm (currently only "greedy" available)
   - Click "Generate Test Cases"
   - View results in the Results section

5. **Export Results:**
   - Click "Export to Excel" or "Export to CSV"
   - Choose save location and filename

## Example Usage: Soft-Synth Testing

**Input Parameters:**
- Format: VST3, AUv3, Desktop Stand Alone
- DAW: Logic, Pro Tools, Ableton
- Sample Rate: 44.1kHz, 48kHz, 96kHz
- Buffer Size: 64, 128, 256, 512

**Constraints:**
- IF Format = 'Desktop Stand Alone' THEN DAW must be empty
- IF Format = 'VST3' THEN DAW must not be empty
- IF Format = 'AUv3' THEN DAW must not be empty

**Expected Output:**
- 12 test cases (instead of 108 full combinations)
- 88.9% reduction in test cases
- All valid parameter pairs covered
- Invalid combinations excluded

## Constraint Syntax

### Conditions
- `parameter = 'value'` - Parameter equals specific value
- `parameter != 'value'` - Parameter does not equal specific value

### Actions
- `parameter must be empty` - Parameter must have no value
- `parameter must not be empty` - Parameter must have a value

### Examples
- `IF Format = 'Desktop Stand Alone' THEN DAW must be empty`
- `IF Browser = 'Chrome' THEN OS must not be empty`
- `IF Network = 'Offline' THEN Server must be empty`

## Features

- ✅ **Greedy Algorithm**: Efficient pairwise testing
- ✅ **Unlimited Parameters**: Add as many parameters as needed
- ✅ **Unlimited Values**: Add as many values per parameter as needed
- ✅ **Constraint Support**: Handle parameter dependencies
- ✅ **Excel Export**: Export to .xlsx format
- ✅ **CSV Export**: Export to .csv format
- ✅ **Tabbed Interface**: Easy navigation between parameters and constraints
- ✅ **Extensible**: Ready for additional algorithms

## File Structure

```
all-pairs/
├── main.py                 # Main application
├── pairwise_algorithms.py  # Core algorithms
├── constraint_engine.py    # Constraint handling
├── export_utils.py        # Export functionality
├── test_algorithm.py      # Algorithm test script
├── test_constraints.py    # Constraint test script
├── requirements.txt       # Dependencies
├── README.md             # Project documentation
├── QUICK_START.md        # This file
└── example_config.json   # Example configuration
```

## Troubleshooting

**If you get "command not found: python":**
- Use `python3` instead of `python`

**If you get import errors:**
- Make sure you've installed the dependencies: `pip3 install pandas openpyxl`

**If the UI doesn't appear:**
- Make sure you're running the command from the project directory
- Check that tkinter is available (usually included with Python)

**If constraints aren't working:**
- Check the constraint syntax format: `IF condition THEN action`
- Make sure parameter names match exactly (case-sensitive)
- Verify that the condition and action are properly formatted 