import datetime

import pandas as pd


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

    def create_summary(self,output_directory='data/summaries'):
        if self.chunk is None:
            self.load_dataframe()
        else:
            self.summary = self.create_chunked_summary()

        self.summary = self.create_summary_internals()

        export_filename = self.filepath.split('/')[-1]
        export_path = output_directory + '/' + export_filename
        self.summary.to_csv(export_path)

        return True

    def create_summary_internals(self):
        if self.chunk is None:
            summary = self.add_stop_percentage_to_summary_table()
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

    def create_single_columns_from_summary_table(self, summary):
        summary = summary.reset_index()
        melt = summary.melt(id_vars=['county_fips', 'driver_race'], value_vars=['stops', 'stop_percentage'])
        pivot = melt.pivot_table(index=['county_fips'], columns=['driver_race', 'variable'], values='value')
        pivot.columns = ['_'.join(col).strip() for col in pivot.columns.values]
        pivot.columns = pivot.columns.get_level_values(0)
        return pivot

    def add_stop_percentage_to_summary_table(self):
        summary = self.df.groupby(['county_fips', 'driver_race']).agg('count')
        summary = summary[['id']]
        summary['stops'] = summary['id']
        summary = summary[['stops']]
        return summary

    def add_acs_data_to_summary(self, summary):
        if not self.acs:
            return summary

        merge = pd.merge(summary, self.acs.summary, on='county_fips')
        return merge

    def add_differences(self, pivot):
        if not self.acs:
            return

        columns = pivot.columns
        for race in self.acs.races:
            col_name = race + "_difference"
            stop_percentage_name = race + "_stop_percentage"
            pop_percentage_name = race + "_percentage"
            if (pop_percentage_name in columns) and (stop_percentage_name in columns):
                pivot[col_name] = pivot[stop_percentage_name] - pivot[pop_percentage_name]

        return pivot

    def create_chunked_summary(self):
        total_summary = pd.DataFrame()
        counter = 1
        for chunk in pd.read_csv(self.filepath, chunksize=self.chunksize, dtype={'county_fips':str}):
            now = datetime.datetime.now()
            print(self.filepath + " - " + str(self.chunksize * counter) + " - " + now.strftime("%H:%M:%S"))
            self.chunk = chunk
            self.load_dataframe()
            summary = self.add_stop_percentage_to_summary_table()
            total_summary = pd.concat([total_summary, summary])
            counter = counter + 1

        group = total_summary.reset_index()
        group = group.groupby(['county_fips', 'driver_race']).agg('sum')
        return group
