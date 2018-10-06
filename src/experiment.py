import pandas as pd




class Stops:
    def __init__(self,filepath):
        self.df = self.load_dataframe(filepath)

    def load_dataframe(self, filepath):
        df = pd.read_csv(filepath)
        cols_to_drop = ['location_raw', 'county_name']
        df = df.drop(cols_to_drop)
        return df


