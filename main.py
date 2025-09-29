# Personal Finance Tracker
# main.py - Main application file

import csv
import os
from datetime import datetime
from typing import Dict, List, Optional, Union

class FinanceTracker:
    def __init__(self, csv_file: str = "data/transactions.csv") -> None:
        self.csv_file = csv_file
        self.transactions: List[Dict[str, str]] = []
        self.categories: dict[str, float] = {}
        
    def safe_int_conversion(self, value: str) -> int:
        """safely convert string to integer"""
        try:
            return int(float(value)) #handle decimal inputs too
        except (ValueError, TypeError):
            print(f"Invalid amount value: {value} treating as 0")
            return 0
        
    def validate_transaction(self, transaction: Dict[str, str]) -> bool:
        """Validate transaction data"""
        required_fields = ["date", "description", "amount", "category"]
        
        # Check if all requierd fields exist
        if not all(field in transaction for field in required_fields):
            return False
        
        # Validate date format
        try:
            datetime.strptime(transaction["date"], "%Y-%m-%d")
        except ValueError:
            return False
        
        return True
    
    def load_data(self) -> None:
        """Load CSV data with validation"""
        try:
            with open(self.csv_file, mode="r", newline='', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                raw_transactions = list(csv_reader)
                
                # Validate and filter transactions
                valid_transactions = []
                invalid_count = 0
                
                for transaction in raw_transactions:
                    if self.validate_transaction(transaction):
                        valid_transactions.append(transaction)
                    else:
                        invalid_count += 1
                        print(f"Invalid transaction found: {transaction}")
                        
                self.transactions = valid_transactions
                
                print(f"{len(self.transactions)} valid transactions loaded.")   
                if invalid_count > 0:
                    print(f"{invalid_count} invalid transactions were found and skipped.")
                    
        except FileNotFoundError:
            print("CSV file not found.")
            self.create_sample_data()
        except PermissionError:
            print("Permission denied to read the file.")
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def create_sample_data(self) -> None:
        """Create sample data"""
        sample_data = [
            {"date": "2023-01-01", "description": "Grocery Store", "amount": "-50", "category": "Food"},
            {"date": "2023-01-02", "description": "Salary", "amount": "2000", "category": "Income"},
            {"date": "2023-01-03", "description": "Electricity Bill", "amount": "-100", "category": "Utilities"},
            {"date": "2023-01-04", "description": "Restaurant", "amount": "-75", "category": "Food"},
            {"date": "2023-01-05", "description": "Freelance Work", "amount": "500", "category": "Income"},
        ]
        try:
            os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
            with open(self.csv_file, mode="w", newline='', encoding='utf-8') as file:
                fieldnames = ["date", "description", "amount", "category"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(sample_data)
                
            print(f"Sample data created at {self.csv_file}.")
            self.load_data()
            
        except PermissionError:
            print("Permission denied to create sample file.")
        except Exception as e:
            print(f"Error creating sample data: {e}")
            
    