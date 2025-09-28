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
        