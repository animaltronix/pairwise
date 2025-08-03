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
        Generate test cases using the greedy algorithm with simple constraint filtering.
        
        Simple 3-step approach:
        1. Generate ALL possible pairs
        2. Filter out invalid pairs using constraints as lookup table
        3. Generate test cases using only valid pairs
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
        
        print(f"Total possible test cases: {total_combinations}")
        
        # STEP 1: Generate ALL possible pairs
        all_possible_pairs = self._generate_all_pairs(param_names, param_values)
        print(f"Total possible pairs to cover: {len(all_possible_pairs)}")
        
        # STEP 2: Filter out invalid pairs using constraints as lookup table
        valid_pairs = all_possible_pairs.copy()
        if constraint_engine:
            print(f"Filtering pairs using {len(constraint_engine.get_constraints())} constraints...")
            valid_pairs = self._filter_pairs_simple(valid_pairs, constraint_engine)
            print(f"Valid pairs after filtering: {len(valid_pairs)}")
        
        if not valid_pairs:
            print("Warning: No valid pairs found after applying constraints!")
            return []
        
        # Print all valid pairs for debugging
        print("All valid pairs to cover:")
        for i, pair in enumerate(sorted(valid_pairs), 1):
            print(f"  {i}. {pair}")
        
        # STEP 3: Generate test cases using only valid pairs
        test_cases = []
        covered_pairs = set()
        
        # Continue until all valid pairs are covered
        iteration = 0
        while len(covered_pairs) < len(valid_pairs):
            iteration += 1
            best_test_case = None
            best_coverage = 0
            best_new_pairs = set()
            
            # Generate all possible combinations for candidate test cases
            all_combinations = self._generate_all_combinations(param_names, param_values)
            
            # Try all combinations for the next test case
            for test_case in all_combinations:
                # Calculate how many new valid pairs this test case would cover
                test_case_pairs = self._get_pairs_from_test_case(test_case)
                new_valid_pairs = test_case_pairs.intersection(valid_pairs - covered_pairs)
                
                if len(new_valid_pairs) > best_coverage:
                    best_coverage = len(new_valid_pairs)
                    best_test_case = test_case
                    best_new_pairs = new_valid_pairs
            
            if best_test_case is None:
                print(f"Warning: No test case found to cover remaining pairs at iteration {iteration}")
                break
            
            test_cases.append(best_test_case)
            covered_pairs.update(best_new_pairs)
            
            print(f"\nTest Case {len(test_cases)}: {best_test_case}")
            print(f"  Covers {len(best_new_pairs)} new valid pairs:")
            for pair in sorted(best_new_pairs):
                print(f"    - {pair}")
            print(f"  Total valid pairs covered so far: {len(covered_pairs)}/{len(valid_pairs)}")
        
        print(f"\nFinal result: {len(test_cases)} test cases generated")
        print(f"Valid pairs covered: {len(covered_pairs)}/{len(valid_pairs)}")
        
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

    def _filter_pairs_simple(self, pairs: Set[Tuple], constraint_engine: ConstraintEngine) -> Set[Tuple]:
        """Filter out pairs that violate constraints using a lookup table."""
        valid_pairs = set()
        
        # Get all stored constraints
        constraints = constraint_engine.get_constraints()
        print(f"DEBUG: Checking {len(pairs)} pairs against {len(constraints)} constraints")
        
        for pair in pairs:
            # Convert pair to a test case for evaluation
            param1, value1 = pair[0]
            param2, value2 = pair[1]
            test_case = {param1: value1, param2: value2}
            
            # Check if this pair violates any constraint
            is_valid = True
            for constraint in constraints:
                # Check if this constraint involves the parameters in our pair
                if self._constraint_involves_parameters(constraint, param1, param2):
                    # Evaluate the constraint
                    if not self._evaluate_constraint_simple(test_case, constraint):
                        is_valid = False
                        print(f"DEBUG: Pair {pair} violates constraint: {constraint}")
                        break
            
            if is_valid:
                valid_pairs.add(pair)
                print(f"DEBUG: Pair {pair} is VALID")
            else:
                print(f"DEBUG: Pair {pair} is INVALID")
        
        return valid_pairs
    
    def _constraint_involves_parameters(self, constraint, param1: str, param2: str) -> bool:
        """Check if a constraint involves the given parameters."""
        condition = constraint.condition.lower()
        action = constraint.action.lower()
        
        # Check if either parameter appears in condition or action
        return param1.lower() in condition or param2.lower() in condition or param1.lower() in action or param2.lower() in action
    
    def _evaluate_constraint_simple(self, test_case: Dict[str, str], constraint) -> bool:
        """Simple constraint evaluation - returns True if constraint is satisfied."""
        try:
            # Parse condition and action
            condition_result = self._evaluate_condition_simple(test_case, constraint.condition)
            action_result = self._evaluate_action_simple(test_case, constraint.action)
            
            print(f"DEBUG: Evaluating constraint: {constraint}")
            print(f"DEBUG: Test case: {test_case}")
            print(f"DEBUG: Condition: '{constraint.condition}' -> {condition_result}")
            print(f"DEBUG: Action: '{constraint.action}' -> {action_result}")
            
            # If condition is true, action must also be true
            if condition_result:
                result = action_result
                print(f"DEBUG: Condition is TRUE, action result: {result}")
                return result
            else:
                # If condition is false, constraint is satisfied (no violation)
                print(f"DEBUG: Condition is FALSE, constraint satisfied")
                return True
                
        except Exception as e:
            print(f"Warning: Could not evaluate constraint '{constraint}': {e}")
            return True
    
    def _evaluate_condition_simple(self, test_case: Dict[str, str], condition: str) -> bool:
        """Simple condition evaluation."""
        # Handle "parameter = 'value'" pattern
        if "=" in condition and "'" in condition:
            parts = condition.split("=")
            if len(parts) == 2:
                param_name = parts[0].strip()
                expected_value = parts[1].strip().strip("'")
                actual_value = test_case.get(param_name, "")
                return actual_value == expected_value
        
        return False
    
    def _evaluate_action_simple(self, test_case: Dict[str, str], action: str) -> bool:
        """Simple action evaluation."""
        print(f"DEBUG: Evaluating action: '{action}'")
        
        # Handle "parameter must be specific_value" pattern
        if "must be" in action.lower():
            parts = action.split()
            if len(parts) >= 4 and parts[1] == "must" and parts[2] == "be":
                param_name = parts[0]
                required_value = parts[3]
                actual_value = test_case.get(param_name, "")
                result = actual_value == required_value
                print(f"DEBUG: 'must be' pattern - param: {param_name}, required: {required_value}, actual: {actual_value}, result: {result}")
                return result
        
        # Handle "parameter must not be specific_value" pattern
        if "must not be" in action.lower():
            parts = action.split()
            if len(parts) >= 5 and parts[1] == "must" and parts[2] == "not" and parts[3] == "be":
                param_name = parts[0]
                forbidden_value = parts[4]
                actual_value = test_case.get(param_name, "")
                result = actual_value != forbidden_value
                print(f"DEBUG: 'must not be' pattern - param: {param_name}, forbidden: {forbidden_value}, actual: {actual_value}, result: {result}")
                return result
        
        print(f"DEBUG: No pattern matched, returning True")
        return True


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