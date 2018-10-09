import datetime

import pandas as pd

from src.reports.county_summary import CountySummary


class Stop:
    def __init__(self, stop_filepath=None, acs=None, chunk=None, chunksize=1000000):
        self.df = None
        self.chunked_summary = None
        self.acs = acs
        self.filepath = stop_filepath
        self.chunk = chunk
        self.chunksize = chunksize
        self.summary = None

    def load_dataframe(self):
        if self.chunk is None:
            df = pd.read_csv(self.filepath,dtype={'county_fips':str})
        else:
            df = self.chunk

        df = df[df['county_fips'].notna()]
        df = df[df['driver_race'].notna()]
        if (len(df) > 0):
            df['driver_race'] = df['driver_race'].str.lower()

        cols_to_drop = ['location_raw', 'county_name', 'driver_race_raw']

        if 'officer_id' in df.columns:
            officer_id = df['officer_id'].astype(str)
            df['state_officer_id'] = df['state'].str.lower() + officer_id
            cols_to_drop.append('officer_id')

        df = df.drop(cols_to_drop, axis=1)

        self.df = df
        return True

    def create_county_summary(self, output_directory='data/summaries'):
        county_summary = CountySummary(self)
        self.summary = county_summary.create_summary(output_directory=output_directory)

        return True




