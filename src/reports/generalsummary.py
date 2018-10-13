import datetime
from abc import abstractmethod

import pandas as pd

class GeneralSummary:
    @classmethod
    def __init__(self, stop, output_directory='data/summaries', groupby_columns=['county_fips', 'driver_race']):
        self.groupby_columns = groupby_columns
        self.summary = None
        self.output_directory = output_directory
        self.stop = stop



    @abstractmethod
    def create_single_columns_from_summary_table(self, summary):
        pass


