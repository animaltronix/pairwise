"""
Constraint Builder for Pairwise Testing

Provides a form-based interface for building constraints using dropdowns and structured input.
"""

from typing import List, Dict, Tuple, Optional
from constraint_engine import Constraint, ConstraintEngine


class ConstraintBuilder:
    """Helper class for building constraints from form inputs."""
    
    OPERATORS = {
        "equals": "=",
        "not equals": "!=",
        "is nil": "is nil",
        "is not nil": "is not nil"
    }
    
    MUST_OPTIONS = {
        "must": "must",
        "must not": "must not"
    }
    
    NIL_OPTIONS = {
        "be nil": "be nil",
        "not be nil": "not be nil"
    }
    
    @staticmethod
    def build_constraint(parameter1: str, operator: str, value1: str, 
                        action_parameter: str, must_option: str, nil_option: str) -> Constraint:
        """
        Build a constraint from form inputs.
        
        Args:
            parameter1: First parameter name
            operator: Operator (equals, not equals, is nil, is not nil)
            value1: Value for comparison (if applicable)
            action_parameter: Parameter for the action
            must_option: must or must not
            nil_option: be nil or not be nil
            
        Returns:
            Constraint object
        """
        # Build condition
        if operator in ["is nil", "is not nil"]:
            condition = f"{parameter1} {operator}"
        else:
            condition = f"{parameter1} {ConstraintBuilder.OPERATORS[operator]} '{value1}'"
        
        # Build action
        action_text = f"{action_parameter} {must_option} {nil_option}"
        
        return Constraint(condition, action_text)
    
    @staticmethod
    def get_operators() -> List[str]:
        """Get available operators for dropdown."""
        return list(ConstraintBuilder.OPERATORS.keys())
    
    @staticmethod
    def get_must_options() -> List[str]:
        """Get available must options for dropdown."""
        return list(ConstraintBuilder.MUST_OPTIONS.keys())
    
    @staticmethod
    def get_nil_options() -> List[str]:
        """Get available nil options for dropdown."""
        return list(ConstraintBuilder.NIL_OPTIONS.keys())
    
    @staticmethod
    def validate_constraint(parameter1: str, operator: str, value1: str,
                          action_parameter: str, must_option: str, nil_option: str) -> Tuple[bool, str]:
        """
        Validate constraint inputs.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not parameter1.strip():
            return False, "First parameter is required"
        
        if operator in ["equals", "not equals"] and not value1.strip():
            return False, "Value is required for equals/not equals operators"
        
        if not action_parameter.strip():
            return False, "Action parameter is required"
        
        if parameter1 == action_parameter:
            return False, "Parameters cannot be the same"
        
        if not must_option:
            return False, "Must option is required"
        
        if not nil_option:
            return False, "Nil option is required"
        
        return True, "" 