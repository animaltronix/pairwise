"""
Test script for the pairwise testing algorithm.

This script tests the greedy algorithm with a simple example to verify it works correctly.
"""

from pairwise_algorithms import get_algorithm


def test_greedy_algorithm():
    """Test the greedy algorithm with a simple example."""
    print("Testing Greedy Pairwise Algorithm")
    print("=" * 40)
    
    # Test parameters
    parameters = {
        "Browser": ["Chrome", "Firefox", "Safari"],
        "OS": ["Windows", "Mac", "Linux"],
        "Screen Size": ["1920x1080", "1366x768"]
    }
    
    print("Input Parameters:")
    for param, values in parameters.items():
        print(f"  {param}: {values}")
    print()
    
    # Get algorithm
    algorithm = get_algorithm("greedy")
    
    # Generate test cases
    test_cases = algorithm.generate_test_cases(parameters)
    
    print(f"Generated {len(test_cases)} test cases:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        for param, value in test_case.items():
            print(f"  {param}: {value}")
        print()
    
    # Calculate expected vs actual
    total_combinations = 1
    for values in parameters.values():
        total_combinations *= len(values)
    
    print(f"Summary:")
    print(f"  Total possible combinations: {total_combinations}")
    print(f"  Generated test cases: {len(test_cases)}")
    print(f"  Reduction: {((total_combinations - len(test_cases)) / total_combinations * 100):.1f}%")
    
    return test_cases


if __name__ == "__main__":
    test_greedy_algorithm() 