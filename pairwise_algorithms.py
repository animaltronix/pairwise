"""
Pairwise Testing Algorithms

This module contains implementations of various pairwise testing algorithms.
Currently supports the Greedy algorithm with extensible architecture for future algorithms.
"""

from typing import List, Dict, Set, Tuple, Any
import itertools
from abc import ABC, abstractmethod


class PairwiseAlgorithm(ABC):
    """Abstract base class for pairwise testing algorithms."""
    
    @abstractmethod
    def generate_test_cases(self, parameters: Dict[str, List[str]]) -> List[Dict[str, str]]:
        """
        Generate test cases using the algorithm.
        
        Args:
            parameters: Dictionary mapping parameter names to lists of possible values
            
        Returns:
            List of test cases, where each test case is a dictionary mapping parameter names to values
        """
        pass


class GreedyAlgorithm(PairwiseAlgorithm):
    """Greedy algorithm for pairwise testing."""
    
    def generate_test_cases(self, parameters: Dict[str, List[str]]) -> List[Dict[str, str]]:
        """
        Generate test cases using the greedy algorithm.
        
        The greedy algorithm works by:
        1. Identifying all possible pairs of parameter values
        2. Iteratively adding test cases that cover the most uncovered pairs
        3. Continuing until all pairs are covered
        """
        if not parameters:
            return []
        
        # Get parameter names and their values
        param_names = list(parameters.keys())
        param_values = list(parameters.values())
        
        # Generate all possible pairs that need to be covered
        all_pairs = self._generate_all_pairs(param_names, param_values)
        
        # Initialize test cases and covered pairs
        test_cases = []
        covered_pairs = set()
        
        # Continue until all pairs are covered
        while len(covered_pairs) < len(all_pairs):
            best_test_case = None
            best_coverage = 0
            
            # Try all possible combinations for the next test case
            for test_case in self._generate_all_combinations(param_names, param_values):
                # Calculate how many new pairs this test case would cover
                new_pairs = self._get_new_pairs(test_case, covered_pairs)
                
                if len(new_pairs) > best_coverage:
                    best_coverage = len(new_pairs)
                    best_test_case = test_case
            
            if best_test_case is None:
                break
                
            # Add the best test case
            test_cases.append(best_test_case)
            covered_pairs.update(self._get_pairs_from_test_case(best_test_case))
        
        return test_cases
    
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