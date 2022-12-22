import pandas as pd

class UserData:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
    
    def get_usernames(self, sep: str = ';') -> list:
        df = pd.read_csv(self.csv_file, sep=sep)
        usernames = df['username'].tolist()
        return usernames
