"""
Test script for the constraint functionality.

This script tests the constraint engine with the soft-synth example.
"""

from pairwise_algorithms import get_algorithm
from constraint_engine import ConstraintEngine


def test_soft_synth_example():
    """Test the constraint engine with the soft-synth example."""
    print("Testing Constraint Engine with Soft-Synth Example")
    print("=" * 60)
    
    # Test parameters (your soft-synth example)
    parameters = {
        "Format": ["VST3", "AUv3", "Desktop Stand Alone"],
        "DAW": ["Logic", "Pro Tools", "Ableton"],
        "Sample Rate": ["44.1kHz", "48kHz", "96kHz"],
        "Buffer Size": ["64", "128", "256", "512"]
    }
    
    print("Input Parameters:")
    for param, values in parameters.items():
        print(f"  {param}: {values}")
    print()
    
    # Create constraint engine
    constraint_engine = ConstraintEngine()
    
    # Add constraints
    constraints = [
        ("Format = 'Desktop Stand Alone'", "DAW must be empty", "Desktop has no DAW"),
        ("Format = 'VST3'", "DAW must not be empty", "VST3 needs DAW"),
        ("Format = 'AUv3'", "DAW must not be empty", "AUv3 needs DAW")
    ]
    
    print("Adding Constraints:")
    for condition, action, description in constraints:
        constraint_engine.add_constraint(condition, action, description)
        print(f"  IF {condition} THEN {action}")
    print()
    
    # Get algorithm
    algorithm = get_algorithm("greedy")
    
    # Generate test cases with constraints
    test_cases = algorithm.generate_test_cases(parameters, constraint_engine)
    
    print(f"Generated {len(test_cases)} test cases:")
    print("-" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        for param, value in test_case.items():
            print(f"  {param}: {value}")
        print()
    
    # Calculate statistics
    total_combinations = 1
    for values in parameters.values():
        total_combinations *= len(values)
    
    print(f"Summary:")
    print(f"  Total possible combinations: {total_combinations}")
    print(f"  Generated test cases: {len(test_cases)}")
    print(f"  Reduction: {((total_combinations - len(test_cases)) / total_combinations * 100):.1f}%")
    
    # Test constraint validation
    print(f"\nConstraint Validation:")
    print("-" * 30)
    
    # Test some invalid combinations
    invalid_cases = [
        {"Format": "Desktop Stand Alone", "DAW": "Logic", "Sample Rate": "44.1kHz", "Buffer Size": "128"},
        {"Format": "VST3", "DAW": "", "Sample Rate": "48kHz", "Buffer Size": "256"},
    ]
    
    for i, test_case in enumerate(invalid_cases, 1):
        is_valid, violations = constraint_engine.is_valid_test_case(test_case)
        print(f"Invalid Test Case {i}:")
        for param, value in test_case.items():
            print(f"  {param}: {value}")
        print(f"  Valid: {is_valid}")
        if not is_valid:
            print(f"  Violations: {violations}")
        print()
    
    return test_cases


if __name__ == "__main__":
    test_soft_synth_example() 