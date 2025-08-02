"""
Constraint Engine for Pairwise Testing

Handles parameter dependencies and invalid combinations in pairwise testing.
"""

from typing import List, Dict, Set, Tuple, Any, Optional
import re


class Constraint:
    """Represents a constraint rule between parameters."""
    
    def __init__(self, condition: str, action: str, description: str = ""):
        """
        Initialize a constraint.
        
        Args:
            condition: String describing the condition (e.g., "Format = 'Desktop Stand Alone'")
            action: String describing the action (e.g., "DAW must be nil")
            description: Optional description of the constraint
        """
        self.condition = condition.strip()
        self.action = action.strip()
        self.description = description.strip()
    
    def __str__(self):
        return f"IF {self.condition} THEN {self.action}"
    
    def __repr__(self):
        return f"Constraint('{self.condition}', '{self.action}', '{self.description}')"


class ConstraintEngine:
    """Engine for evaluating and applying constraints to test cases."""
    
    def __init__(self):
        self.constraints: List[Constraint] = []
    
    def add_constraint(self, condition: str, action: str, description: str = "") -> None:
        """Add a new constraint to the engine."""
        constraint = Constraint(condition, action, description)
        self.constraints.append(constraint)
    
    def remove_constraint(self, index: int) -> bool:
        """Remove a constraint by index."""
        if 0 <= index < len(self.constraints):
            self.constraints.pop(index)
            return True
        return False
    
    def get_constraints(self) -> List[Constraint]:
        """Get all constraints."""
        return self.constraints.copy()
    
    def is_valid_test_case(self, test_case: Dict[str, str]) -> Tuple[bool, List[str]]:
        """
        Check if a test case is valid according to all constraints.
        
        Args:
            test_case: Dictionary of parameter names to values
            
        Returns:
            Tuple of (is_valid, list_of_violations)
        """
        violations = []
        
        for constraint in self.constraints:
            if not self._evaluate_constraint(test_case, constraint):
                violations.append(str(constraint))
        
        return len(violations) == 0, violations
    
    def filter_valid_combinations(self, all_combinations: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Filter out invalid combinations from a list of all possible combinations.
        
        Args:
            all_combinations: List of all possible parameter combinations
            
        Returns:
            List of valid combinations only
        """
        valid_combinations = []
        
        for combination in all_combinations:
            is_valid, violations = self.is_valid_test_case(combination)
            if is_valid:
                valid_combinations.append(combination)
        
        return valid_combinations
    
    def _evaluate_constraint(self, test_case: Dict[str, str], constraint: Constraint) -> bool:
        """
        Evaluate if a test case satisfies a specific constraint.
        
        Args:
            test_case: Dictionary of parameter names to values
            constraint: Constraint to evaluate
            
        Returns:
            True if constraint is satisfied, False otherwise
        """
        try:
            # Parse condition and action
            condition_result = self._evaluate_condition(test_case, constraint.condition)
            action_result = self._evaluate_action(test_case, constraint.action)
            
            # If condition is true, action must also be true
            if condition_result:
                return action_result
            else:
                # If condition is false, constraint is satisfied (no violation)
                return True
                
        except Exception as e:
            # If we can't evaluate the constraint, assume it's valid
            print(f"Warning: Could not evaluate constraint '{constraint}': {e}")
            return True
    
    def _evaluate_condition(self, test_case: Dict[str, str], condition: str) -> bool:
        """Evaluate a condition string against a test case."""
        # Simple condition evaluation for now
        # Supports: "parameter = 'value'", "parameter != 'value'"
        
        # Match patterns like "Format = 'Desktop Stand Alone'"
        match = re.match(r'(\w+)\s*=\s*[\'"]([^\'"]*)[\'"]', condition)
        if match:
            param_name = match.group(1)
            expected_value = match.group(2)
            actual_value = test_case.get(param_name, "")
            return actual_value == expected_value
        
        # Match patterns like "Format != 'Desktop Stand Alone'"
        match = re.match(r'(\w+)\s*!=\s*[\'"]([^\'"]*)[\'"]', condition)
        if match:
            param_name = match.group(1)
            expected_value = match.group(2)
            actual_value = test_case.get(param_name, "")
            return actual_value != expected_value
        
        # Match patterns like "DAW is nil" or "DAW must be nil"
        if "nil" in condition.lower():
            param_name = condition.split()[0]  # First word is parameter name
            actual_value = test_case.get(param_name, "")
            return actual_value == "" or actual_value is None
        
        # Match patterns like "DAW is not nil" or "DAW must not be nil"
        if "not nil" in condition.lower():
            param_name = condition.split()[0]  # First word is parameter name
            actual_value = test_case.get(param_name, "")
            return actual_value != "" and actual_value is not None
        
        return False
    
    def _evaluate_action(self, test_case: Dict[str, str], action: str) -> bool:
        """Evaluate an action string against a test case."""
        # Simple action evaluation for now
        # Supports: "parameter must be nil", "parameter must not be nil"
        
        if "must be nil" in action.lower():
            param_name = action.split()[0]  # First word is parameter name
            actual_value = test_case.get(param_name, "")
            return actual_value == "" or actual_value is None
        
        if "must not be nil" in action.lower():
            param_name = action.split()[0]  # First word is parameter name
            actual_value = test_case.get(param_name, "")
            return actual_value != "" and actual_value is not None
        
        return True


def parse_constraint_text(text: str) -> Tuple[str, str]:
    """
    Parse constraint text in format "IF condition THEN action".
    
    Args:
        text: Constraint text
        
    Returns:
        Tuple of (condition, action)
    """
    # Remove "IF" and "THEN" keywords and split
    text = text.replace("IF", "").replace("THEN", "").strip()
    
    # Find the THEN keyword (case insensitive)
    then_match = re.search(r'\bTHEN\b', text, re.IGNORECASE)
    if then_match:
        condition = text[:then_match.start()].strip()
        action = text[then_match.end():].strip()
        return condition, action
    
    # If no THEN found, try to split on common patterns
    parts = text.split(" THEN ")
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    
    # Fallback: assume everything after the first "=" is the action
    equal_match = re.search(r'=', text)
    if equal_match:
        condition = text[:equal_match.start()].strip()
        action = text[equal_match.start():].strip()
        return condition, action
    
    return "", text 