"""
Pairwise Testing Generator - Main Application

A GUI application for generating test configuration combinations using pairwise testing algorithms.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from typing import Dict, List

from pairwise_algorithms import get_algorithm
from export_utils import export_to_excel, export_to_csv, get_export_summary


class PairwiseTestingApp:
    """Main application class for the pairwise testing generator."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Pairwise Testing Generator")
        self.root.geometry("800x600")
        
        # Data storage
        self.parameters = {}  # {parameter_name: [values]}
        self.test_cases = []
        
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
        
        # Parameters section
        self.create_parameters_section(main_frame)
        
        # Algorithm selection
        self.create_algorithm_section(main_frame)
        
        # Generate button
        generate_btn = ttk.Button(main_frame, text="Generate Test Cases", 
                                 command=self.generate_test_cases)
        generate_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Results section
        self.create_results_section(main_frame)
        
        # Export section
        self.create_export_section(main_frame)
        
    def create_parameters_section(self, parent):
        """Create the parameters input section."""
        # Parameters frame
        params_frame = ttk.LabelFrame(parent, text="Parameters", padding="10")
        params_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        params_frame.columnconfigure(1, weight=1)
        
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
        self.params_tree = ttk.Treeview(params_frame, columns=("values",), show="tree headings", height=6)
        self.params_tree.heading("#0", text="Parameter")
        self.params_tree.heading("values", text="Values")
        self.params_tree.column("#0", width=150)
        self.params_tree.column("values", width=300)
        self.params_tree.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Scrollbar for parameters
        params_scrollbar = ttk.Scrollbar(params_frame, orient=tk.VERTICAL, command=self.params_tree.yview)
        params_scrollbar.grid(row=3, column=3, sticky=(tk.N, tk.S))
        self.params_tree.configure(yscrollcommand=params_scrollbar.set)
        
        # Remove parameter button
        remove_param_btn = ttk.Button(params_frame, text="Remove Selected", command=self.remove_parameter)
        remove_param_btn.grid(row=4, column=0, columnspan=3, pady=(5, 0))
        
    def create_algorithm_section(self, parent):
        """Create the algorithm selection section."""
        algo_frame = ttk.LabelFrame(parent, text="Algorithm", padding="10")
        algo_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(algo_frame, text="Select Algorithm:").grid(row=0, column=0, sticky=tk.W)
        self.algorithm_var = tk.StringVar(value="greedy")
        algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var, 
                                      values=["greedy"], state="readonly")
        algorithm_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
    def create_results_section(self, parent):
        """Create the results display section."""
        results_frame = ttk.LabelFrame(parent, text="Results", padding="10")
        results_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Results info
        self.results_info_var = tk.StringVar(value="No test cases generated yet.")
        results_info_label = ttk.Label(results_frame, textvariable=self.results_info_var)
        results_info_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Results treeview
        self.results_tree = ttk.Treeview(results_frame, show="tree headings", height=8)
        self.results_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for results
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        results_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
    def create_export_section(self, parent):
        """Create the export section."""
        export_frame = ttk.LabelFrame(parent, text="Export", padding="10")
        export_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
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
        
    def generate_test_cases(self):
        """Generate test cases using the selected algorithm."""
        if not self.parameters:
            messagebox.showerror("Error", "Please add at least one parameter.")
            return
            
        try:
            # Get algorithm
            algorithm_name = self.algorithm_var.get()
            algorithm = get_algorithm(algorithm_name)
            
            # Generate test cases
            self.test_cases = algorithm.generate_test_cases(self.parameters)
            
            # Update results display
            self.update_results_display()
            
            messagebox.showinfo("Success", f"Generated {len(self.test_cases)} test cases!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate test cases: {str(e)}")
            
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
            
        # Add test cases
        for i, test_case in enumerate(self.test_cases, 1):
            values = [test_case[param] for param in param_names]
            self.results_tree.insert("", "end", text=f"Test Case {i}", values=values)
            
        # Update info
        summary = get_export_summary(self.test_cases)
        self.results_info_var.set(
            f"Generated {summary['total_test_cases']} test cases for {summary['parameters']} parameters."
        )
        
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