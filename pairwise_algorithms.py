"""
Pairwise Testing Algorithms

This module contains implementations of various pairwise testing algorithms.
Currently supports the Greedy algorithm with extensible architecture for future algorithms.
"""

from typing import List, Dict, Set, Tuple, Any
import itertools
from abc import ABC, abstractmethod
from constraint_engine import ConstraintEngine


class PairwiseAlgorithm(ABC):
    """Abstract base class for pairwise testing algorithms."""
    
    @abstractmethod
    def generate_test_cases(self, parameters: Dict[str, List[str]], 
                          constraint_engine: ConstraintEngine = None) -> List[Dict[str, str]]:
        """
        Generate test cases using the algorithm.
        
        Args:
            parameters: Dictionary mapping parameter names to lists of possible values
            constraint_engine: Optional constraint engine for filtering invalid combinations
            
        Returns:
            List of test cases, where each test case is a dictionary mapping parameter names to values
        """
        pass


class GreedyAlgorithm(PairwiseAlgorithm):
    """Greedy algorithm for pairwise testing."""
    
    def generate_test_cases(self, parameters: Dict[str, List[str]], 
                          constraint_engine: ConstraintEngine = None) -> List[Dict[str, str]]:
        """
        Generate test cases using the greedy algorithm.
        
        The greedy algorithm works by:
        1. Identifying all possible pairs of parameter values
        2. Iteratively adding test cases that cover the most uncovered pairs
        3. Continuing until all pairs are covered
        4. Filtering out invalid combinations based on constraints
        """
        if not parameters:
            return []
        
        # Get parameter names and their values
        param_names = list(parameters.keys())
        param_values = list(parameters.values())
        
        # Calculate total combinations
        total_combinations = 1
        for values in param_values:
            total_combinations *= len(values)
        
        print(f"Total possible combinations: {total_combinations}")
        
        # Generate all possible combinations first
        all_combinations = self._generate_all_combinations(param_names, param_values)
        
        # Filter out invalid combinations based on constraints
        if constraint_engine:
            all_combinations = constraint_engine.filter_valid_combinations(all_combinations)
            print(f"Valid combinations after constraints: {len(all_combinations)}")
        
        if not all_combinations:
            print("Warning: No valid combinations found after applying constraints!")
            return []
        
        # Generate all possible pairs that need to be covered
        all_pairs = self._generate_all_pairs_from_combinations(all_combinations)
        print(f"Total pairs to cover: {len(all_pairs)}")
        
        # Print all pairs for debugging
        print("All pairs to cover:")
        for i, pair in enumerate(sorted(all_pairs), 1):
            print(f"  {i}. {pair}")
        
        # Initialize test cases and covered pairs
        test_cases = []
        covered_pairs = set()
        
        # Continue until all pairs are covered
        iteration = 0
        while len(covered_pairs) < len(all_pairs):
            iteration += 1
            best_test_case = None
            best_coverage = 0
            best_new_pairs = set()
            
            # Try all valid combinations for the next test case
            for test_case in all_combinations:
                # Calculate how many new pairs this test case would cover
                new_pairs = self._get_new_pairs(test_case, covered_pairs)
                
                if len(new_pairs) > best_coverage:
                    best_coverage = len(new_pairs)
                    best_test_case = test_case
                    best_new_pairs = new_pairs
            
            if best_test_case is None:
                print(f"Warning: No test case found to cover remaining pairs at iteration {iteration}")
                break
                
            # Add the best test case
            test_cases.append(best_test_case)
            covered_pairs.update(best_new_pairs)
            
            # Print debugging info for this test case
            print(f"\nTest Case {len(test_cases)}: {best_test_case}")
            print(f"  Covers {len(best_new_pairs)} new pairs:")
            for pair in sorted(best_new_pairs):
                print(f"    - {pair}")
            print(f"  Total pairs covered so far: {len(covered_pairs)}/{len(all_pairs)}")
            
            # Remove the used test case from available combinations
            all_combinations.remove(best_test_case)
        
        print(f"\nFinal result: {len(test_cases)} test cases generated")
        print(f"Pairs covered: {len(covered_pairs)}/{len(all_pairs)}")
        
        return test_cases
    
    def _generate_all_pairs_from_combinations(self, combinations: List[Dict[str, str]]) -> Set[Tuple]:
        """Generate all possible pairs from a list of valid combinations."""
        pairs = set()
        
        for combination in combinations:
            pairs.update(self._get_pairs_from_test_case(combination))
        
        return pairs
    
    def _generate_all_pairs(self, param_names: List[str], param_values: List[List[str]]) -> Set[Tuple]:
        """Generate all possible pairs of parameter values that need to be covered."""
        pairs = set()
        
        for i in range(len(param_names)):
            for j in range(i + 1, len(param_names)):
                param1, param2 = param_names[i], param_names[j]
                values1, values2 = param_values[i], param_values[j]
                
                for val1 in values1:
                    for val2 in values2:
                        pairs.add(((param1, val1), (param2, val2)))
        
        return pairs
    
    def _generate_all_combinations(self, param_names: List[str], param_values: List[List[str]]) -> List[Dict[str, str]]:
        """Generate all possible test case combinations."""
        combinations = []
        
        # Generate cartesian product of all parameter values
        for combination in itertools.product(*param_values):
            test_case = dict(zip(param_names, combination))
            combinations.append(test_case)
        
        return combinations
    
    def _get_pairs_from_test_case(self, test_case: Dict[str, str]) -> Set[Tuple]:
        """Extract all pairs from a single test case."""
        pairs = set()
        param_items = list(test_case.items())
        
        for i in range(len(param_items)):
            for j in range(i + 1, len(param_items)):
                pairs.add((param_items[i], param_items[j]))
        
        return pairs
    
    def _get_new_pairs(self, test_case: Dict[str, str], covered_pairs: Set[Tuple]) -> Set[Tuple]:
        """Get pairs from test case that are not already covered."""
        test_case_pairs = self._get_pairs_from_test_case(test_case)
        return test_case_pairs - covered_pairs


# Factory function to get algorithm instances
def get_algorithm(algorithm_name: str) -> PairwiseAlgorithm:
    """
    Factory function to get algorithm instances.
    
    Args:
        algorithm_name: Name of the algorithm ('greedy', etc.)
        
    Returns:
        Algorithm instance
        
    Raises:
        ValueError: If algorithm name is not supported
    """
    algorithms = {
        'greedy': GreedyAlgorithm(),
    }
    
    if algorithm_name not in algorithms:
        raise ValueError(f"Algorithm '{algorithm_name}' not supported. Available: {list(algorithms.keys())}")
    
    return algorithms[algorithm_name] 