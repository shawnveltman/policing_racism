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

    def create_chunked_summary(self, stop):
        total_summary = pd.DataFrame()
        counter = 1
        filepath = stop.filepath
        for chunk in pd.read_csv(filepath, chunksize=stop.chunksize, dtype={'county_fips': str}):
            now = datetime.datetime.now()
            print(filepath + " - " + str(stop.chunksize * counter) + " - " + now.strftime("%H:%M:%S"))
            stop.chunk = chunk
            stop.load_dataframe()
            summary = self.add_stop_percentage_to_summary_table(stop)
            total_summary = pd.concat([total_summary, summary])
            counter = counter + 1

        group = total_summary.reset_index()
        group = group.groupby(self.groupby_columns).agg('sum')
        return group


    def add_stop_percentage_to_summary_table(self, stop):
        summary = stop.df.groupby(self.groupby_columns).agg('count')
        summary = summary[['id']]
        summary['stops'] = summary['id']
        summary = summary[['stops']]
        return summary

    def create_summary(self):
        if self.stop.chunk is None:
            self.stop.load_dataframe()
        else:
            chunked_summary = self.create_chunked_summary(self.stop)
            self.summary = chunked_summary

        self.summary = self.create_summary_internals()

        export_filename = self.stop.filepath.split('/')[-1]
        export_path = self.output_directory + '/' + export_filename
        self.summary.to_csv(export_path)

        return self.summary

    def create_summary_internals(self):
        if self.stop.chunk is None:
            summary = self.add_stop_percentage_to_summary_table(self.stop)
        else:
            summary = self.summary

        stop_percentage_label = 'stop_percentage'
        summary[stop_percentage_label] = summary['stops'] / summary['stops'].groupby(level=0).sum()
        pivot = self.create_single_columns_from_summary_table(summary)

        pivot = self.add_acs_data_to_summary(pivot)
        # pivot = self.add_differences(pivot)
        if pivot is None:
            return summary

        return pivot

    @abstractmethod
    def create_single_columns_from_summary_table(self, summary):
        pass

    def add_acs_data_to_summary(self, summary):
        if not self.stop.acs:
            return summary

        merge = pd.merge(summary, self.stop.acs.summary, on='county_fips')
        return merge

    def create_single_columns_from_summary_table(self, summary):
        summary = summary.reset_index()
        melt = summary.melt(id_vars=self.groupby_columns, value_vars=['stops', 'stop_percentage'])
        pivot = melt.pivot_table(index=['county_fips'], columns=['driver_race', 'variable'], values='value')
        pivot.columns = ['_'.join(col).strip() for col in pivot.columns.values]
        pivot.columns = pivot.columns.get_level_values(0)
        return pivot