import json
from copy import deepcopy
from collections import defaultdict
import tkinter as tk
from tkinter import ttk


class MutualFund:
    def __init__(self, fund_name, data):
        """
        Initializes the mutual fund tracker with the given data.
        
        :param fund_name: Name of the mutual fund
        :param data: Initial data in JSON format
        """
        self.fund_name = fund_name
        self.data = data  # Original data from the JSON
        self.history = []  # Stores the history of changes (snapshots of the data)
        self.current_state = self._parse_data(data)  # Current state of the mutual fund
        self.history.append({'row': 0, 'state': deepcopy(self.current_state)})  # Add initial state to history

    def _parse_data(self, data):
        """
        Parse and organize data for easier tracking of changes.
        
        :param data: The raw data (JSON) to be parsed
        :return: Parsed data structure
        """
        parsed = {}
        for item in data['ZN250']:
            instrument = item.get("Name of the Instrument")
            if instrument != "Total" and instrument != "GRAND TOTAL (AUM)":  # Ignore Total and Grand Total entries
                parsed[instrument] = {
                    "ISIN": item.get("ISIN"),
                    "Rating/Industry": item.get("Rating \/ Industry^"),
                    "Quantity": item.get("Quantity"),
                    "Market Value (Rs. in Lakhs)": item.get("Market value\n(Rs. in Lakhs)"),
                    "% to NAV": item.get("% to NAV")
                }
        return parsed

    def add_instrument(self, instrument_name, ISIN, rating_industry, quantity, market_value, nav_percent, row):
        """
        Add a new instrument to the mutual fund.

        :param instrument_name: Name of the instrument
        :param ISIN: ISIN of the instrument
        :param rating_industry: Rating/Industry type of the instrument
        :param quantity: Quantity of the instrument
        :param market_value: Market value in Lakhs
        :param nav_percent: Percentage to NAV
        :param row: Row number when this change occurred
        """
        self.current_state[instrument_name] = {
            "ISIN": ISIN,
            "Rating/Industry": rating_industry,
            "Quantity": quantity,
            "Market Value (Rs. in Lakhs)": market_value,
            "% to NAV": nav_percent
        }
        self._log_change(row)

    def remove_instrument(self, instrument_name, row):
        """
        Remove an instrument from the mutual fund.

        :param instrument_name: Name of the instrument to be removed
        :param row: Row number when this change occurred
        """
        if instrument_name in self.current_state:
            del self.current_state[instrument_name]
            self._log_change(row)
        else:
            print(f"Instrument {instrument_name} not found!")

    def update_instrument(self, instrument_name, quantity=None, market_value=None, nav_percent=None, row=None):
        """
        Update the details of an existing instrument.

        :param instrument_name: Name of the instrument to update
        :param quantity: New quantity (optional)
        :param market_value: New market value (optional)
        :param nav_percent: New NAV percentage (optional)
        :param row: Row number when this change occurred
        """
        if instrument_name in self.current_state:
            if quantity is not None:
                self.current_state[instrument_name]["Quantity"] = quantity
            if market_value is not None:
                self.current_state[instrument_name]["Market Value (Rs. in Lakhs)"] = market_value
            if nav_percent is not None:
                self.current_state[instrument_name]["% to NAV"] = nav_percent
            self._log_change(row)
        else:
            print(f"Instrument {instrument_name} not found!")

    def _log_change(self, row):
        """
        Log the current state to history to track changes along with row number.
        """
        self.history.append({'row': row, 'state': deepcopy(self.current_state)})

    def calculate_total_value(self):
        """
        Calculate the total value of the mutual fund based on the market values of the instruments.
        
        :return: Total value (Rs. in Lakhs)
        """
        total_value = 0
        for instrument in self.current_state.values():
            market_value = instrument.get("Market Value (Rs. in Lakhs)")
            if market_value is not None:
                total_value += market_value
        return total_value

    def get_changes_by_row(self, start_row, end_row):
        """
        Get a list of changes made so far within a specified row range.
        
        :param start_row: Start row for filtering changes
        :param end_row: End row for filtering changes
        :return: List of changes within the specified row range
        """
        changes = []
        for record in self.history:
            row = record['row']
            if start_row <= row <= end_row:
                previous_state = self.history[self.history.index(record) - 1]['state'] if self.history.index(record) > 0 else {}
                current_state = record['state']
                change = {
                    "row": row,
                    "changes": self._diff(previous_state, current_state)
                }
                changes.append(change)
        return changes

    def _diff(self, prev_state, curr_state):
        """
        Function to calculate the difference between two states.
        
        :param prev_state: The previous state of the mutual fund
        :param curr_state: The current state of the mutual fund
        :return: A dictionary containing the differences
        """
        diff = defaultdict(list)
        for instrument in set(prev_state.keys()).union(curr_state.keys()):
            prev = prev_state.get(instrument, {})
            curr = curr_state.get(instrument, {})
            
            # Check for differences
            for key in prev.keys() | curr.keys():
                if prev.get(key) != curr.get(key):
                    diff[instrument].append({
                        "field": key,
                        "old_value": prev.get(key),
                        "new_value": curr.get(key)
                    })
        return dict(diff)

    def print_state(self):
        """
        Display the current state of the mutual fund.
        """
        print(json.dumps(self.current_state, indent=4))


def display_changes(changes, text_widget):
    """Display the changes made to the mutual fund within the specified row range."""
    text_widget.delete(1.0, tk.END)  
    if not changes:
        text_widget.insert(tk.END, "No changes for the specified row range.\n")
    else:
        text_widget.insert(tk.END, "Funds that changed during the specified row range:\n")
        for change in changes:
            # text_widget.insert(tk.END, f"\nChanges for row {change['row']}:\n")
            for instrument, change_details in change['changes'].items():
                text_widget.insert(tk.END, f"  Instrument: {instrument}\n")
                for detail in change_details:
                    text_widget.insert(tk.END, f"    Field: {detail['field']}\n")
                    text_widget.insert(tk.END, f"    Old Value: {detail['old_value']}\n")
                    text_widget.insert(tk.END, f"    New Value: {detail['new_value']}\n")


def on_button_click(fund_name, month, mf_tracker, text_widget):
    """Handle the button click event."""
    if month == "Sep":
        with open('MFTracker/zn250_sep.json', 'r') as file:
            fund_data = json.load(file)

        total_rows = len(fund_data['ZN250'])  
        mid_val = total_rows // 2 
        start_row = 0
        end_row = mid_val

    elif month == "Oct":
        with open('MFTracker/zn250_sep.json', 'r') as file:
            fund_data = json.load(file)
        
        total_rows = len(fund_data['ZN250'])  
        mid_val = total_rows // 2 
        start_row = mid_val
        end_row = total_rows-1

    elif month == "Nov":
        with open('MFTracker/zn250_nov.json', 'r') as file:
            fund_data = json.load(file)
        
        total_rows = len(fund_data['ZN250'])  
        mid_val = total_rows // 2 
        start_row = 0
        end_row = mid_val
        
    elif month == "Dec":
        with open('MFTracker/zn250_nov.json', 'r') as file:
            fund_data = json.load(file)
        
        total_rows = len(fund_data['ZN250'])  
        mid_val = total_rows // 2 
        start_row = mid_val
        end_row = total_rows-1
            
    mf_tracker = MutualFund(fund_name, fund_data)
    
    changes = mf_tracker.get_changes_by_row(start_row, end_row)
    
    display_changes(changes, text_widget)


def main():
    root = tk.Tk()
    root.title("Mutual Fund Tracker")

    tk.Label(root, text="Enter Fund Name:").pack()
    fund_name_entry = tk.Entry(root)
    fund_name_entry.pack()

    tk.Label(root, text="Select Month (Sep, Oct, Nov, Dec):").pack()
    month_entry = tk.Entry(root)
    month_entry.pack()

    button = tk.Button(root, text="Show Changes", command=lambda: on_button_click(fund_name_entry.get(),month_entry.get(), None, output_text))
    button.pack()

    output_text = tk.Text(root, height=60, width=200)
    output_text.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
