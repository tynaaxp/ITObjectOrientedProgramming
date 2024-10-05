#Phuong Thai, U32184606, phuongtranxuanthai@usf.edu

from collections import OrderedDict
import csv
from datetime import datetime

class DamReader:
    """
    A class to read and process dam information from a CSV file.
    """
    def __init__(self, filename: str):
        """
        Initialize the DamReader with a specific filename.
        """
        self.filename = filename
        self.dam_dict = {}

    def file_to_dict(self):
        """
        Reads the CSV file and stores dam information in a dictionary.

        Returns:
            A dictionary mapping states to lists of dam information.
        """
        try:
            with open(self.filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)  # Use DictReader to easily access columns by name
                for row in reader:
                    state = row['State'].strip()
                    # Collect all dam info, including the year
                    dam_info = [row['CrestElevation'], row['CrestLength'], row['StructuralHeight'],
                                row['Name'], row['Watercourse'], row['County'], row['Latitude'],
                                row['Longitude'], row['Year']]
                    # Append the dam_info list to the list of dams in dam_dict under the state key
                    self.dam_dict.setdefault(state, []).append(dam_info)
        except FileNotFoundError:
            print(f"[FileNotFoundError] file does not exist: '{self.filename}'")
        return self.dam_dict

    def average_age_by_state(self, state: str = None):
        """
        Calculates the average age of dams by state.

        Returns:
            The average age of the dams in the specified state or overall if no state is specified.
        """
        current_year = datetime.now().year
        total_age = 0
        dam_count = 0
        for st, dams in self.dam_dict.items():
            if state is None or state == st:
                for dam in dams:
                    year_built = int(dam[8])
                    total_age += current_year - year_built
                    dam_count += 1
        return total_age / dam_count if dam_count else 0

    def oldest_youngest_by_state(self, state: str = None):
        """
        Finds the oldest and youngest dams by state.

        Returns:
            A message string detailing the oldest and youngest dams in the specified state or overall.
        """
        oldest_age = 0
        youngest_age = float('inf')
        oldest_dam_info = ('', '', 0)  # Name, state, year
        youngest_dam_info = ('', '', float('inf'))  # Name, state, year
        current_year = datetime.now().year

        for st, dams in self.dam_dict.items():
            if state is None or state == st:
                for dam in dams:
                    year_built = int(dam[8])
                    age = current_year - year_built
                    if oldest_age < age:
                        oldest_age = age
                        oldest_dam_info = (dam[3], st, year_built)
                    elif oldest_age == age:
                        oldest_dam_info = (*oldest_dam_info, dam[3], st, year_built)
                    if youngest_age > age:
                        youngest_age = age
                        youngest_dam_info = (dam[3], st, year_built)
                    elif youngest_age == age:
                        youngest_dam_info = (*youngest_dam_info, dam[3], st, year_built)

        # Oldest dams
        oldest_dams = [oldest_dam_info[i:i+3] for i in range(0, len(oldest_dam_info), 3)]
        oldest_msg = f"--Oldest dam(s)--\nBuilt in {oldest_dams[0][2]}"
        for dam_name, dam_state, _ in oldest_dams:
            oldest_msg += f"\n{dam_name}({dam_state})"

        # Youngest dams
        youngest_dams = [youngest_dam_info[i:i+3] for i in range(0, len(youngest_dam_info), 3)]
        youngest_msg = f"--Youngest dam(s)--\nBuilt in {youngest_dams[0][2]}"
        for dam_name, dam_state, _ in youngest_dams:
            youngest_msg += f"\n{dam_name}({dam_state})"

        return f"{oldest_msg}\n\n{youngest_msg}"
            
if __name__ == "__main__":
    dams0 = DamReader('file.csv')

    dams_dict = dams0.file_to_dict()

    dams0 = DamReader('Downloads/review code/dams0.csv')
    dams_dict = dams0.file_to_dict()
    print(dams0.dam_dict)

    dams1 = DamReader('Downloads/review code/dams1.csv')
    dams_dict = dams1.file_to_dict()
    print(dams1.dam_dict)

    avg = dams0.average_age_by_state()
    print(int(avg))

    avg = dams1.average_age_by_state()
    print(int(avg))

    msg = dams0.oldest_youngest_by_state()
    print(msg)

    msg = dams1.oldest_youngest_by_state()
    print(msg)

    msg = dams1.oldest_youngest_by_state("ID")
    print(msg)