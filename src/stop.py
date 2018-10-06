import pandas as pd

class Stop:
    def __init__(self,filepath):
        self.df = self.load_dataframe(filepath)
        self.summary = self.create_summary()

    def load_dataframe(self, filepath):
        df = pd.read_csv(filepath)
        cols_to_drop = ['location_raw', 'county_name','driver_race_raw']
        df = df.drop(cols_to_drop)
        df['driver_race'] = df['driver_race'].str.lower()
        df['county_fips'] = df['county_fips'].astype(str)
        df = df[df['county_fips'].notna()]
        return df

    def create_summary(self):
        summary = self.df.groupby(['county_fips', 'driver_race']).agg('count')
        summary = summary[['id']]
        summary['individual'] = summary['id']
        summary = summary[['individual']]
        summary['percentage'] = summary['individual'] / summary['individual'].groupby(level=0).sum()
        return summary