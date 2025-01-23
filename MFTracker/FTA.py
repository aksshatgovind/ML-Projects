import csv
from collections import defaultdict
from copy import deepcopy
import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime


class FundAllocation:
    def __init__(self, fund_name):
        """
        Initializes the fund tracker with the given fund name.
        
        :param fund_name: Name of the mutual fund
        """
        self.fund_name = fund_name
        self.history = []                               # Stores the history of changes
        self.current_state = defaultdict(dict)          # Current allocation state
        self.history.append({'date': None, 'state': deepcopy(self.current_state)})  

    def add_allocation(self, date, asset, allocation_percent):
        """
        Add or update an allocation for the given fund and date.
        
        :param date: The date of the allocation change
        :param asset: The asset type (e.g., Stocks, Bonds, Cash)
        :param allocation_percent: The allocation percentage for the asset
        """
        self.current_state[date][asset] = allocation_percent
        self._log_change(date)

    def update_allocation(self, date, asset, allocation_percent):
        """
        Update the allocation for a specific asset on a given date.
        
        :param date: The date of the allocation change
        :param asset: The asset type (e.g., Stocks, Bonds, Cash)
        :param allocation_percent: The new allocation percentage for the asset
        """
        if date in self.current_state and asset in self.current_state[date]:
            self.current_state[date][asset] = allocation_percent
            self._log_change(date)
        else:
            print(f"No allocation found for {asset} on {date}. Creating new allocation.")
            self.add_allocation(date, asset, allocation_percent)

    def remove_allocation(self, date, asset):
        """
        Remove an asset allocation for a specific date.
        
        :param date: The date of the allocation change
        :param asset: The asset type (e.g., Stocks, Bonds, Cash)
        """
        if date in self.current_state and asset in self.current_state[date]:
            del self.current_state[date][asset]
            self._log_change(date)
        else:
            print(f"Allocation for {asset} on {date} not found!")

    def _log_change(self, date):
        """
        Log the current state to history to track changes along with the date.
        """
        self.history.append({'date': date, 'state': deepcopy(self.current_state)})

    def get_changes_by_date(self, start_date, end_date):
        """
        Get a list of changes made so far within a specified date range.
        
        :param start_date: Start date for filtering changes
        :param end_date: End date for filtering changes
        :return: List of changes within the specified date range
        """
        changes = []
        # Convert start_date and end_date to datetime if they are not None
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return []

        # Loop through history and find the changes in the specified range
        for record in self.history:
            date = record['date']
            # Skip if the date is None or invalid
            if date is None:
                continue
            
            date = datetime.strptime(date, '%Y-%m-%d')  # Ensure date is datetime object for comparison
            if start_date <= date <= end_date:
                previous_state = self.history[self.history.index(record) - 1]['state'] if self.history.index(record) > 0 else {}
                current_state = record['state']
                change = {
                    "date": date.strftime('%Y-%m-%d'),
                    "changes": self._diff(previous_state, current_state)
                }
                changes.append(change)
        return changes

    def _diff(self, prev_state, curr_state):
        """
        Calculate the difference between two states (allocations).
        
        :param prev_state: The previous state of allocations
        :param curr_state: The current state of allocations
        :return: A dictionary containing the differences
        """
        diff = defaultdict(list)
        for date in set(prev_state.keys()).union(curr_state.keys()):
            prev = prev_state.get(date, {})
            curr = curr_state.get(date, {})
            
            # Check for differences
            for key in prev.keys() | curr.keys():
                if prev.get(key) != curr.get(key):
                    diff[date].append({
                        "asset": key,
                        "old_value": prev.get(key),
                        "new_value": curr.get(key)
                    })
        return dict(diff)

    def print_state(self):
        """
        Display the current state of the mutual fund allocation.
        """
        print(json.dumps(self.current_state, indent=4))


def load_fund_data_from_csv(file_path):
    fund_data = defaultdict(FundAllocation)
    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fund_name = row['fund_name']
            date = row['date']
            asset = row['asset']
            allocation = float(row['allocation'])
            
            if fund_name not in fund_data:
                fund_data[fund_name] = FundAllocation(fund_name)
            
            fund_data[fund_name].add_allocation(date, asset, allocation)
    
    return fund_data


# GUI 
def display_changes(changes, text_widget):
    """Display the changes made to the fund allocations within the specified date range."""
    text_widget.delete(1.0, tk.END)
    if not changes:
        text_widget.insert(tk.END, "No changes for the specified date range.\n")
    else:
        text_widget.insert(tk.END, "Allocations that changed during the specified date range:\n")
        for change in changes:
            text_widget.insert(tk.END, f"\nChanges for date {change['date']}:\n")
            for asset, change_details in change['changes'].items():
                text_widget.insert(tk.END, f"  Asset: {asset}\n")
                for detail in change_details:
                    text_widget.insert(tk.END, f"    Old Value: {detail['old_value']}%\n")
                    text_widget.insert(tk.END, f"    New Value: {detail['new_value']}%\n")


def on_button_click(fund_name, start_date, end_date, fund_data, text_widget):
    """Handle the button click event."""
    if fund_name in fund_data:
        fund_tracker = fund_data[fund_name]
        changes = fund_tracker.get_changes_by_date(start_date, end_date)
        display_changes(changes, text_widget)
    else:
        text_widget.insert(tk.END, f"Fund {fund_name} not found!\n")


def main():
    root = tk.Tk()
    root.title("Fund Allocation Tracker")

    tk.Label(root, text="Enter Fund Name:").pack()
    fund_name_entry = tk.Entry(root)
    fund_name_entry.pack()

    tk.Label(root, text="Enter Start Date (YYYY-MM-DD):").pack()
    start_date_entry = tk.Entry(root)
    start_date_entry.pack()

    tk.Label(root, text="Enter End Date (YYYY-MM-DD):").pack()
    end_date_entry = tk.Entry(root)
    end_date_entry.pack()

    button = tk.Button(root, text="Show Changes", command=lambda: on_button_click(fund_name_entry.get(),
                                                                               start_date_entry.get(),
                                                                               end_date_entry.get(),
                                                                               fund_data,
                                                                               output_text))
    button.pack()

    output_text = tk.Text(root, height=20, width=100)
    output_text.pack()

    # Load fund data from CSV
    fund_data = load_fund_data_from_csv('MFTracker/mutual_fund_data.csv')

    root.mainloop()


if __name__ == "__main__":
    main()
