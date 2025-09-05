import pandas as pd
import json
import os

class DataManager:
    def __init__(self):
        pass

    def load_csv(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return pd.read_csv(file_path)

    def load_excel(self, file_path, sheet_name=0):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return pd.read_excel(file_path, sheet_name=sheet_name)

    def load_json(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as f:
            return json.load(f)


