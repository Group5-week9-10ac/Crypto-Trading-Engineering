import os
import pandas as pd
from sklearn.model_selection import train_test_split as sk_train_test_split

def create_folder(folder):
    """
    Create a folder if it doesn't exist.

    Args:
    - folder (str): Folder path.
    """
    os.makedirs(folder, exist_ok=True)

def save_data(data, filename, folder='data'):
    """
    Save data as a CSV file.

    Args:
    - data (pd.DataFrame): Data to be saved.
    - filename (str): Name of the CSV file.
    - folder (str, optional): Folder where the file will be saved. Default is 'data'.
    """
    create_folder(folder)
    filepath = os.path.join(folder, filename)
    data.to_csv(filepath, index=False)

def load_data(filepath):
    """
    Load data from a CSV file.

    Args:
    - filepath (str): Path to the CSV file.

    Returns:
    - pd.DataFrame: Loaded data.
    """
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        print(f"File {filepath} does not exist.")
        return None
