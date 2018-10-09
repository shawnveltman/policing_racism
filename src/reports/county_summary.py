import datetime

import pandas as pd


class CountySummary:
    def __init__(self,stop):
        self.stop = stop

    def create_summary(self,output_directory='data/summaries'):
        if self.stop.chunk is None:
            self.stop.load_dataframe()
        else:
            self.stop.summary = self.create_chunked_summary()

        self.stop.summary = self.create_summary_internals()

        export_filename = self.stop.filepath.split('/')[-1]
        export_path = output_directory + '/' + export_filename
        self.stop.summary.to_csv(export_path)

        return self.stop.summary

    def create_chunked_summary(self):
        total_summary = pd.DataFrame()
        counter = 1
        filepath = self.stop.filepath
        for chunk in pd.read_csv(filepath, chunksize=self.stop.chunksize, dtype={'county_fips':str}):
            now = datetime.datetime.now()
            print(filepath + " - " + str(self.stop.chunksize * counter) + " - " + now.strftime("%H:%M:%S"))
            self.stop.chunk = chunk
            self.stop.load_dataframe()
            summary = self.add_stop_percentage_to_summary_table()
            total_summary = pd.concat([total_summary, summary])
            counter = counter + 1

        group = total_summary.reset_index()
        group = group.groupby(['county_fips', 'driver_race']).agg('sum')
        return group

    def create_summary_internals(self):
        if self.stop.chunk is None:
            summary = self.add_stop_percentage_to_summary_table()
        else:
            summary = self.stop.summary

        stop_percentage_label = 'stop_percentage'
        summary[stop_percentage_label] = summary['stops'] / summary['stops'].groupby(level=0).sum()
        pivot = self.create_single_columns_from_summary_table(summary)

        pivot = self.add_acs_data_to_summary(pivot)
        # pivot = self.add_differences(pivot)
        if pivot is None:
            return summary

        return pivot

    def create_single_columns_from_summary_table(self, summary):
        summary = summary.reset_index()
        melt = summary.melt(id_vars=['county_fips', 'driver_race'], value_vars=['stops', 'stop_percentage'])
        pivot = melt.pivot_table(index=['county_fips'], columns=['driver_race', 'variable'], values='value')
        pivot.columns = ['_'.join(col).strip() for col in pivot.columns.values]
        pivot.columns = pivot.columns.get_level_values(0)
        return pivot

    def add_stop_percentage_to_summary_table(self):
        summary = self.stop.df.groupby(['county_fips', 'driver_race']).agg('count')
        summary = summary[['id']]
        summary['stops'] = summary['id']
        summary = summary[['stops']]
        return summary

    def add_acs_data_to_summary(self, summary):
        if not self.stop.acs:
            return summary

        merge = pd.merge(summary, self.stop.acs.summary, on='county_fips')
        return merge
