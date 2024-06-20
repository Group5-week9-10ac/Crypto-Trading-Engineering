import os
import pandas as pd

def create_folder(folder):
    """
    Create a folder if it doesn't exist.

    Args:
    - folder (str): Folder path.
    """
    os.makedirs(folder, exist_ok=True)

def save_data(data, filename, folder='data'):
    """
    Save data as CSV file.

    Args:
    - data (pd.DataFrame): Data to be saved.
    - filename (str): Name of the CSV file.
    - folder (str, optional): Folder where the file will be saved. Default is 'data'.
    """
    create_folder(folder)
    filepath = os.path.join(folder, filename)
    data.to_csv(filepath, index=False)
