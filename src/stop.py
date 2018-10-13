import datetime

import pandas as pd


class Stop:
    def __init__(self, stop_filepath=None, acs=None, chunk=None, chunksize=1000000, groupby_columns=['county_fips', 'driver_race'], output_directory='data/summaries'):
        self.output_directory = output_directory
        self.groupby_columns = groupby_columns
        self.df = None
        self.acs = acs
        self.filepath = stop_filepath
        self.chunk = chunk
        self.chunksize = chunksize
        self.summary = None


    def load_dataframe(self):
        if self.chunk is None:
            df = pd.read_csv(self.filepath, dtype={'county_fips': str})
        else:
            df = self.chunk

        df = df[df['county_fips'].notna()]
        df = df[df['driver_race'].notna()]
        if (len(df) > 0):
            df['driver_race'] = df['driver_race'].str.lower()

        cols_to_drop = ['location_raw', 'county_name', 'driver_race_raw']

        df['state_officer_id'] = ''

        if 'officer_id' in df.columns:
            officer_id = df['officer_id'].astype(str)
            df['state_officer_id'] = df['state'].str.lower() + officer_id
            cols_to_drop.append('officer_id')

        df = df.drop(cols_to_drop, axis=1)

        self.df = df
        return True

    def create_summary(self):
        if self.chunk is None:
            self.load_dataframe()
        else:
            chunked_summary = self.create_chunked_summary()
            self.summary = chunked_summary

        self.summary = self.create_summary_internals()

        self.export_file()

        return self.summary

    def export_file(self):
        export_filename = self.filepath.split('/')[-1]
        export_path = self.output_directory + '/' + export_filename
        self.summary.to_csv(export_path)

    def create_chunked_summary(self):
        total_summary = pd.DataFrame()
        counter = 1
        for chunk in pd.read_csv(self.filepath, chunksize=self.chunksize, dtype={'county_fips': str}):
            now = datetime.datetime.now()
            print(self.filepath + " - " + str(self.chunksize * counter) + " - " + now.strftime("%H:%M:%S"))
            self.chunk = chunk
            self.load_dataframe()
            summary = self.add_stop_percentage_to_summary_table()
            total_summary = pd.concat([total_summary, summary])
            counter = counter + 1

        group = total_summary.reset_index()
        group = group.groupby(self.groupby_columns).agg('sum')
        return group

    def add_stop_percentage_to_summary_table(self):
        summary = self.df.groupby(self.groupby_columns).agg('count')
        summary = summary[['id']]
        summary['stops'] = summary['id']
        summary = summary[['stops']]
        return summary

    def create_summary_internals(self):
        if self.chunk is None:
            self.summary = self.add_stop_percentage_to_summary_table()

        self.create_stop_percentage()

        pivot = self.create_single_columns_from_summary_table()

        pivot = self.add_acs_data_to_summary(pivot)

        if pivot is None:
            return self.summary

        return pivot

    def create_stop_percentage(self):
        stop_percentage_label = 'stop_percentage'
        self.summary[stop_percentage_label] = self.summary['stops'] / self.summary['stops'].groupby(level=0).sum()

    def create_single_columns_from_summary_table(self):
        summary = self.summary.reset_index()
        melt = summary.melt(id_vars=self.groupby_columns, value_vars=['stops', 'stop_percentage'])
        pivot = melt.pivot_table(index=['county_fips'], columns=['driver_race', 'variable'], values='value')
        pivot.columns = ['_'.join(col).strip() for col in pivot.columns.values]
        pivot.columns = pivot.columns.get_level_values(0)
        return pivot

    def add_acs_data_to_summary(self,pivot):
        if not self.acs:
            return self.summary

        merge = pd.merge(pivot, self.acs.summary, on='county_fips')
        return merge

