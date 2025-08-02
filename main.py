"""
Pairwise Testing Generator - Main Application

A GUI application for generating test configuration combinations using pairwise testing algorithms.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from typing import Dict, List, Set, Tuple

from pairwise_algorithms import get_algorithm
from export_utils import export_to_excel, export_to_csv, get_export_summary
from constraint_engine import ConstraintEngine
from constraint_builder import ConstraintBuilder


class PairwiseTestingApp:
    """Main application class for the pairwise testing generator."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Pairwise Testing Generator")
        self.root.geometry("1400x900")
        
        # Data storage
        self.parameters = {}  # {parameter_name: [values]}
        self.test_cases = []
        self.constraint_engine = ConstraintEngine()
        self.all_pairs = set()  # Store all pairs for highlighting
        self.covered_pairs = set()  # Track covered pairs
        self.test_case_pairs = []  # Store which pairs each test case covers
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create and layout all UI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Pairwise Testing Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Parameters tab
        self.create_parameters_tab()
        
        # Constraints tab
        self.create_constraints_tab()
        
        # Algorithm and generate section
        self.create_algorithm_section(main_frame)
        
        # Results section
        self.create_results_section(main_frame)
        
        # Export section
        self.create_export_section(main_frame)
        
    def create_parameters_tab(self):
        """Create the parameters tab."""
        params_frame = ttk.Frame(self.notebook)
        self.notebook.add(params_frame, text="Parameters")
        
        # Parameters section
        self.create_parameters_section(params_frame)
        
    def create_constraints_tab(self):
        """Create the constraints tab."""
        constraints_frame = ttk.Frame(self.notebook)
        self.notebook.add(constraints_frame, text="Constraints")
        
        # Constraints section
        self.create_constraints_section(constraints_frame)
        
    def create_parameters_section(self, parent):
        """Create the parameters input section."""
        # Parameters frame
        params_frame = ttk.LabelFrame(parent, text="Parameters", padding="10")
        params_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        params_frame.columnconfigure(1, weight=1)
        params_frame.rowconfigure(3, weight=1)
        
        # Parameter name entry
        ttk.Label(params_frame, text="Parameter Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.param_name_var = tk.StringVar()
        param_name_entry = ttk.Entry(params_frame, textvariable=self.param_name_var)
        param_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Parameter values entry
        ttk.Label(params_frame, text="Values (comma-separated):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.param_values_var = tk.StringVar()
        param_values_entry = ttk.Entry(params_frame, textvariable=self.param_values_var)
        param_values_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Add parameter button
        add_param_btn = ttk.Button(params_frame, text="Add Parameter", command=self.add_parameter)
        add_param_btn.grid(row=1, column=2, padx=(10, 0))
        
        # Parameters list
        ttk.Label(params_frame, text="Current Parameters:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        # Create Treeview for parameters
        self.params_tree = ttk.Treeview(params_frame, columns=("values",), show="tree headings", height=10)
        self.params_tree.heading("#0", text="Parameter")
        self.params_tree.heading("values", text="Values")
        self.params_tree.column("#0", width=150)
        self.params_tree.column("values", width=400)
        self.params_tree.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for parameters
        params_scrollbar = ttk.Scrollbar(params_frame, orient=tk.VERTICAL, command=self.params_tree.yview)
        params_scrollbar.grid(row=3, column=3, sticky=(tk.N, tk.S))
        self.params_tree.configure(yscrollcommand=params_scrollbar.set)
        
        # Remove parameter button
        remove_param_btn = ttk.Button(params_frame, text="Remove Selected", command=self.remove_parameter)
        remove_param_btn.grid(row=4, column=0, columnspan=3, pady=(5, 0))
        
    def create_constraints_section(self, parent):
        """Create the constraints input section."""
        # Constraints frame
        constraints_frame = ttk.LabelFrame(parent, text="Constraints", padding="10")
        constraints_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        constraints_frame.columnconfigure(1, weight=1)
        constraints_frame.rowconfigure(6, weight=1)
        
        # Constraint form
        self.create_constraint_form(constraints_frame)
        
        # Example constraints
        self.create_example_constraints(constraints_frame)
        
        # Constraints list
        self.create_constraints_list(constraints_frame)
        
    def create_constraint_form(self, parent):
        """Create the constraint form with dropdowns."""
        form_frame = ttk.LabelFrame(parent, text="Add Constraint", padding="10")
        form_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        form_frame.columnconfigure(1, weight=1)
        
        # Row 1: IF parameter operator value
        ttk.Label(form_frame, text="IF").grid(row=0, column=0, padx=(0, 5))
        
        # Parameter dropdown
        self.param1_var = tk.StringVar()
        self.param1_combo = ttk.Combobox(form_frame, textvariable=self.param1_var, state="readonly")
        self.param1_combo.grid(row=0, column=1, padx=5)
        
        # Operator dropdown
        self.operator_var = tk.StringVar()
        self.operator_combo = ttk.Combobox(form_frame, textvariable=self.operator_var, 
                                          values=ConstraintBuilder.get_operators(), state="readonly")
        self.operator_combo.grid(row=0, column=2, padx=5)
        
        # Value dropdown (populated based on selected parameter)
        self.value1_var = tk.StringVar()
        self.value1_combo = ttk.Combobox(form_frame, textvariable=self.value1_var, state="readonly")
        self.value1_combo.grid(row=0, column=3, padx=5)
        
        # Row 2: THEN parameter must/must not be nil/not be nil
        ttk.Label(form_frame, text="THEN").grid(row=1, column=0, padx=(0, 5), pady=(10, 0))
        
        # Action parameter dropdown
        self.action_param_var = tk.StringVar()
        self.action_param_combo = ttk.Combobox(form_frame, textvariable=self.action_param_var, state="readonly")
        self.action_param_combo.grid(row=1, column=1, padx=5, pady=(10, 0))
        
        # Must dropdown
        self.must_var = tk.StringVar()
        self.must_combo = ttk.Combobox(form_frame, textvariable=self.must_var,
                                       values=ConstraintBuilder.get_must_options(), state="readonly")
        self.must_combo.grid(row=1, column=2, padx=5, pady=(10, 0))
        
        # Nil dropdown
        self.nil_var = tk.StringVar()
        self.nil_combo = ttk.Combobox(form_frame, textvariable=self.nil_var,
                                      values=ConstraintBuilder.get_nil_options(), state="readonly")
        self.nil_combo.grid(row=1, column=3, padx=5, pady=(10, 0))
        
        # Description entry
        ttk.Label(form_frame, text="Description:").grid(row=1, column=4, padx=(10, 5), pady=(10, 0))
        self.constraint_desc_var = tk.StringVar()
        constraint_desc_entry = ttk.Entry(form_frame, textvariable=self.constraint_desc_var)
        constraint_desc_entry.grid(row=1, column=5, padx=5, pady=(10, 0))
        
        # Add constraint button
        add_constraint_btn = ttk.Button(form_frame, text="Add Constraint", command=self.add_constraint)
        add_constraint_btn.grid(row=2, column=0, columnspan=6, pady=(10, 0))
        
        # Bind events to update dropdowns
        self.param1_combo.bind('<<ComboboxSelected>>', self.update_value_dropdown)
        self.operator_combo.bind('<<ComboboxSelected>>', self.update_value_field)
        self.action_param_combo.bind('<<ComboboxSelected>>', self.update_nil_dropdown)
        
    def create_example_constraints(self, parent):
        """Create example constraints section."""
        example_frame = ttk.LabelFrame(parent, text="Example Constraints", padding="5")
        example_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        examples = [
            "IF Format equals 'Desktop Stand Alone' THEN DAW must be nil",
            "IF Format equals 'VST3' THEN DAW must not be nil",
            "IF Format equals 'AUv3' THEN DAW must not be nil"
        ]
        
        for i, example in enumerate(examples):
            ttk.Label(example_frame, text=f"• {example}", font=("Arial", 9)).grid(row=i, column=0, sticky=tk.W, padx=5)
        
    def create_constraints_list(self, parent):
        """Create the constraints list section."""
        # Constraints list
        ttk.Label(parent, text="Current Constraints:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        # Create Treeview for constraints
        self.constraints_tree = ttk.Treeview(parent, columns=("description",), show="tree headings", height=8)
        self.constraints_tree.heading("#0", text="Constraint")
        self.constraints_tree.heading("description", text="Description")
        self.constraints_tree.column("#0", width=500)
        self.constraints_tree.column("description", width=200)
        self.constraints_tree.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for constraints
        constraints_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.constraints_tree.yview)
        constraints_scrollbar.grid(row=3, column=3, sticky=(tk.N, tk.S))
        self.constraints_tree.configure(yscrollcommand=constraints_scrollbar.set)
        
        # Remove constraint button
        remove_constraint_btn = ttk.Button(parent, text="Remove Selected", command=self.remove_constraint)
        remove_constraint_btn.grid(row=4, column=0, columnspan=3, pady=(5, 0))
        
    def create_algorithm_section(self, parent):
        """Create the algorithm selection section."""
        algo_frame = ttk.LabelFrame(parent, text="Algorithm", padding="10")
        algo_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(algo_frame, text="Select Algorithm:").grid(row=0, column=0, sticky=tk.W)
        self.algorithm_var = tk.StringVar(value="greedy")
        algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var, 
                                      values=["greedy"], state="readonly")
        algorithm_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Generate button
        generate_btn = ttk.Button(algo_frame, text="Generate Test Cases", 
                                 command=self.generate_test_cases)
        generate_btn.grid(row=0, column=2, padx=(20, 0))
        
    def create_results_section(self, parent):
        """Create the results display section."""
        results_frame = ttk.LabelFrame(parent, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(2, weight=1)
        
        # Results info
        self.results_info_var = tk.StringVar(value="No test cases generated yet.")
        results_info_label = ttk.Label(results_frame, textvariable=self.results_info_var)
        results_info_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(results_frame, text="Statistics", padding="5")
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Statistics labels
        self.total_combinations_var = tk.StringVar(value="Total combinations: 0")
        self.total_pairs_var = tk.StringVar(value="Total pairs: 0")
        
        ttk.Label(stats_frame, textvariable=self.total_combinations_var).grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(stats_frame, textvariable=self.total_pairs_var).grid(row=0, column=1, sticky=tk.W, padx=20)
        
        # Results treeview
        self.results_tree = ttk.Treeview(results_frame, show="tree headings", height=8)
        self.results_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for results
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        results_scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
    def create_export_section(self, parent):
        """Create the export section."""
        export_frame = ttk.LabelFrame(parent, text="Export", padding="10")
        export_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Export buttons
        export_excel_btn = ttk.Button(export_frame, text="Export to Excel", command=self.export_excel)
        export_excel_btn.grid(row=0, column=0, padx=(0, 10))
        
        export_csv_btn = ttk.Button(export_frame, text="Export to CSV", command=self.export_csv)
        export_csv_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Export status
        self.export_status_var = tk.StringVar(value="")
        export_status_label = ttk.Label(export_frame, textvariable=self.export_status_var, 
                                       foreground="green")
        export_status_label.grid(row=0, column=2, padx=(10, 0))
        
    def update_parameter_dropdowns(self):
        """Update parameter dropdowns with current parameters."""
        param_names = list(self.parameters.keys())
        self.param1_combo['values'] = param_names
        self.action_param_combo['values'] = param_names
        
    def update_value_dropdown(self, event=None):
        """Update value dropdown based on selected parameter."""
        param_name = self.param1_var.get()
        if param_name in self.parameters:
            values = self.parameters[param_name]
            self.value1_combo['values'] = values
            self.value1_var.set("")  # Clear previous selection
        
    def update_value_field(self, event=None):
        """Update value field visibility based on operator."""
        operator = self.operator_var.get()
        if operator in ["is nil", "is not nil"]:
            self.value1_combo.config(state="disabled")
            self.value1_var.set("")
        else:
            self.value1_combo.config(state="readonly")
            
    def update_nil_dropdown(self, event=None):
        """Update nil dropdown based on selected action parameter."""
        action_param = self.action_param_var.get()
        if action_param in self.parameters:
            # For now, we'll use the standard nil options
            # In the future, this could be customized based on the parameter
            pass
        
    def add_parameter(self):
        """Add a new parameter to the list."""
        name = self.param_name_var.get().strip()
        values_str = self.param_values_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter a parameter name.")
            return
            
        if not values_str:
            messagebox.showerror("Error", "Please enter parameter values.")
            return
            
        # Parse values
        values = [v.strip() for v in values_str.split(",") if v.strip()]
        if not values:
            messagebox.showerror("Error", "Please enter at least one value.")
            return
            
        # Check for duplicate parameter names
        if name in self.parameters:
            messagebox.showerror("Error", f"Parameter '{name}' already exists.")
            return
            
        # Add parameter
        self.parameters[name] = values
        
        # Add to treeview
        values_display = ", ".join(values)
        self.params_tree.insert("", "end", text=name, values=(values_display,))
        
        # Update constraint dropdowns
        self.update_parameter_dropdowns()
        
        # Clear input fields
        self.param_name_var.set("")
        self.param_values_var.set("")
        
    def remove_parameter(self):
        """Remove the selected parameter."""
        selection = self.params_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a parameter to remove.")
            return
            
        item = selection[0]
        param_name = self.params_tree.item(item, "text")
        
        # Remove from data
        if param_name in self.parameters:
            del self.parameters[param_name]
            
        # Remove from treeview
        self.params_tree.delete(item)
        
        # Update constraint dropdowns
        self.update_parameter_dropdowns()
        
    def add_constraint(self):
        """Add a new constraint using the form inputs."""
        # Get form values
        param1 = self.param1_var.get().strip()
        operator = self.operator_var.get()
        value1 = self.value1_var.get().strip()
        action_param = self.action_param_var.get().strip()
        must_option = self.must_var.get()
        nil_option = self.nil_var.get()
        description = self.constraint_desc_var.get().strip()
        
        # Validate inputs
        is_valid, error_msg = ConstraintBuilder.validate_constraint(
            param1, operator, value1, action_param, must_option, nil_option
        )
        
        if not is_valid:
            messagebox.showerror("Error", error_msg)
            return
            
        try:
            # Build constraint
            constraint = ConstraintBuilder.build_constraint(
                param1, operator, value1, action_param, must_option, nil_option
            )
            
            # Add description if provided
            if description:
                constraint.description = description
            
            # Add to engine
            self.constraint_engine.add_constraint(
                constraint.condition, constraint.action, constraint.description
            )
            
            # Add to treeview
            self.constraints_tree.insert("", "end", text=str(constraint), 
                                       values=(description,))
            
            # Clear form
            self.param1_var.set("")
            self.operator_var.set("")
            self.value1_var.set("")
            self.action_param_var.set("")
            self.must_var.set("")
            self.nil_var.set("")
            self.constraint_desc_var.set("")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add constraint: {str(e)}")
        
    def remove_constraint(self):
        """Remove the selected constraint."""
        selection = self.constraints_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a constraint to remove.")
            return
            
        item = selection[0]
        constraint_text = self.constraints_tree.item(item, "text")
        
        # Find and remove constraint
        constraints = self.constraint_engine.get_constraints()
        for i, constraint in enumerate(constraints):
            if str(constraint) == constraint_text:
                self.constraint_engine.remove_constraint(i)
                break
                
        # Remove from treeview
        self.constraints_tree.delete(item)
        
    def calculate_statistics(self):
        """Calculate and display statistics."""
        if not self.parameters:
            return
            
        # Calculate total combinations
        total_combinations = 1
        for values in self.parameters.values():
            total_combinations *= len(values)
        
        # Calculate total pairs
        param_names = list(self.parameters.keys())
        param_values = list(self.parameters.values())
        total_pairs = 0
        
        for i in range(len(param_names)):
            for j in range(i + 1, len(param_names)):
                total_pairs += len(param_values[i]) * len(param_values[j])
        
        # Update statistics
        self.total_combinations_var.set(f"Total combinations: {total_combinations}")
        self.total_pairs_var.set(f"Total pairs: {total_pairs}")
            
    def generate_test_cases(self):
        """Generate test cases using the selected algorithm."""
        if not self.parameters:
            messagebox.showerror("Error", "Please add at least one parameter.")
            return
            
        try:
            # Get algorithm
            algorithm_name = self.algorithm_var.get()
            algorithm = get_algorithm(algorithm_name)
            
            # Generate test cases with constraints
            self.test_cases = algorithm.generate_test_cases(self.parameters, self.constraint_engine)
            
            # Calculate statistics and update covered pairs
            self.calculate_statistics()
            self.update_covered_pairs()
            
            # Update results display
            self.update_results_display()
            
            if self.test_cases:
                messagebox.showinfo("Success", f"Generated {len(self.test_cases)} test cases!")
            else:
                messagebox.showwarning("Warning", "No valid test cases found. Check your constraints.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate test cases: {str(e)}")
            
    def update_covered_pairs(self):
        """Update the covered pairs count from the generated test cases."""
        self.covered_pairs.clear()
        self.test_case_pairs.clear()
        
        for test_case in self.test_cases:
            test_case_pairs = self._get_pairs_from_test_case(test_case)
            self.covered_pairs.update(test_case_pairs)
            self.test_case_pairs.append(test_case_pairs)
        
        # Update the covered pairs display
        # self.covered_pairs_var.set(f"Covered pairs: {len(self.covered_pairs)}") # This line is removed
            
    def update_results_display(self):
        """Update the results display with generated test cases."""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        if not self.test_cases:
            self.results_info_var.set("No test cases generated.")
            return
            
        # Get parameter names for columns
        param_names = list(self.test_cases[0].keys())
        
        # Configure columns
        self.results_tree["columns"] = param_names
        for param in param_names:
            self.results_tree.heading(param, text=param)
            self.results_tree.column(param, width=100)
            
        # Add test cases with cell-level highlighting
        for i, test_case in enumerate(self.test_cases):
            values = [test_case[param] for param in param_names]
            item = self.results_tree.insert("", "end", text=f"Test Case {i+1}", values=values)
            
            # Highlight specific cells that form pairs
            if i < len(self.test_case_pairs):
                test_case_pairs = self.test_case_pairs[i]
                self.highlight_pair_cells(item, test_case_pairs, param_names)
            
        # Update info
        summary = get_export_summary(self.test_cases)
        self.results_info_var.set(
            f"Generated {summary['total_test_cases']} test cases for {summary['parameters']} parameters."
        )
        
    def highlight_pair_cells(self, item, pairs, param_names):
        """Highlight specific cells that form pairs in a test case using Unicode superscript numbers."""
        # Unicode superscript numbers: ¹, ², ³, ⁴, ⁵, ⁶, ⁷, ⁸, ⁹, ¹⁰, etc.
        superscript_map = {
            1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹', 10: '¹⁰',
            11: '¹¹', 12: '¹²', 13: '¹³', 14: '¹⁴', 15: '¹⁵', 16: '¹⁶', 17: '¹⁷', 18: '¹⁸', 19: '¹⁹', 20: '²⁰'
        }
        
        # Get current values
        current_values = list(self.results_tree.item(item)['values'])
        
        # Track which pairs each value belongs to
        value_pairs = {}
        
        # For each pair, track which values are involved
        for i, pair in enumerate(pairs, 1):
            param1, value1 = pair[0]
            param2, value2 = pair[1]
            
            # Find the column indices for these parameters
            try:
                col1_idx = param_names.index(param1)
                col2_idx = param_names.index(param2)
                
                # Track which pairs each value belongs to
                if col1_idx not in value_pairs:
                    value_pairs[col1_idx] = []
                if col2_idx not in value_pairs:
                    value_pairs[col2_idx] = []
                    
                value_pairs[col1_idx].append(i)
                value_pairs[col2_idx].append(i)
                
            except ValueError:
                # Parameter not found in column names
                pass
        
        # Update values with superscript numbers
        for col_idx, pair_numbers in value_pairs.items():
            # Create superscript string for all pairs this value belongs to
            superscript_str = ''.join([superscript_map.get(num, str(num)) for num in pair_numbers])
            current_values[col_idx] = f"{current_values[col_idx]}{superscript_str}"
        
        # Update the item with the modified values
        self.results_tree.item(item, values=current_values)
        
    def _get_pairs_from_test_case(self, test_case: Dict[str, str]) -> Set[Tuple]:
        """Extract all pairs from a single test case."""
        pairs = set()
        param_items = list(test_case.items())
        
        for i in range(len(param_items)):
            for j in range(i + 1, len(param_items)):
                pairs.add((param_items[i], param_items[j]))
        
        return pairs
        
    def export_excel(self):
        """Export test cases to Excel format."""
        if not self.test_cases:
            messagebox.showwarning("Warning", "No test cases to export. Please generate test cases first.")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if filename:
                filepath = export_to_excel(self.test_cases, filename)
                self.export_status_var.set(f"Exported to: {filepath}")
                messagebox.showinfo("Success", f"Test cases exported to:\n{filepath}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to Excel: {str(e)}")
            
    def export_csv(self):
        """Export test cases to CSV format."""
        if not self.test_cases:
            messagebox.showwarning("Warning", "No test cases to export. Please generate test cases first.")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                filepath = export_to_csv(self.test_cases, filename)
                self.export_status_var.set(f"Exported to: {filepath}")
                messagebox.showinfo("Success", f"Test cases exported to:\n{filepath}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to CSV: {str(e)}")


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = PairwiseTestingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main() 