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

2. **Add Parameters:**
   - Enter a parameter name (e.g., "Browser")
   - Enter comma-separated values (e.g., "Chrome, Firefox, Safari")
   - Click "Add Parameter"
   - Repeat for all parameters

3. **Generate Test Cases:**
   - Select the algorithm (currently only "greedy" available)
   - Click "Generate Test Cases"
   - View results in the Results section

4. **Export Results:**
   - Click "Export to Excel" or "Export to CSV"
   - Choose save location and filename

## Example Usage

**Input Parameters:**
- Browser: Chrome, Firefox, Safari
- OS: Windows, Mac, Linux
- Screen Size: 1920x1080, 1366x768

**Expected Output:**
- 9 test cases (instead of 18 full combinations)
- 50% reduction in test cases
- All parameter pairs covered

## Features

- ✅ **Greedy Algorithm**: Efficient pairwise testing
- ✅ **Unlimited Parameters**: Add as many parameters as needed
- ✅ **Unlimited Values**: Add as many values per parameter as needed
- ✅ **Excel Export**: Export to .xlsx format
- ✅ **CSV Export**: Export to .csv format
- ✅ **Simple UI**: Easy-to-use interface
- ✅ **Extensible**: Ready for additional algorithms

## File Structure

```
all-pairs/
├── main.py                 # Main application
├── pairwise_algorithms.py  # Core algorithms
├── export_utils.py        # Export functionality
├── test_algorithm.py      # Test script
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