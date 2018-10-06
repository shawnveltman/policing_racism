import pandas as pd

class Stop:
    def __init__(self, stop_filepath,acs=None):
        self.acs = acs
        self.df = self.load_dataframe(stop_filepath)
        self.summary = self.create_summary()
        self.add_acs_data_to_summary()
        self.add_differences()

    def load_dataframe(self, filepath):
        df = pd.read_csv(filepath)
        df = df[df['county_fips'].notna()]
        df = df[df['driver_race'].notna()]
        df['driver_race'] = df['driver_race'].str.lower()
        df['county_fips'] = df['county_fips'].astype(int).astype(str)
        cols_to_drop = ['location_raw', 'county_name', 'driver_race_raw']

        if 'officer_id' in df.columns:
            df['state_officer_id'] = df['state'].str.lower() + df['officer_id'].astype(int).astype(str)
            cols_to_drop.append('officer_id')

        df = df.drop(cols_to_drop, axis=1)

        return df

    def create_summary(self):
        summary = self.add_stop_percentage_to_summary_table()
        pivot = self.create_single_columns_from_summary_table(summary)

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
        individual_label = 'stops'
        summary[individual_label] = summary['id']
        summary = summary[[individual_label]]
        stop_percentage_label = 'stop_percentage'
        summary[stop_percentage_label] = summary[individual_label] / summary[individual_label].groupby(level=0).sum()
        return summary

    def add_acs_data_to_summary(self):
        if not self.acs:
            return

        merge = pd.merge(self.summary, self.acs.summary, on='county_fips')
        self.summary = merge

    def add_differences(self):
        if not self.acs:
            return

        columns = self.summary.columns
        for race in self.acs.races:
            col_name = race + "_difference"
            stop_percentage_name = race + "_stop_percentage"
            pop_percentage_name = race + "_percentage"
            if (pop_percentage_name in columns) and (stop_percentage_name in columns):
                self.summary[col_name] = self.summary[stop_percentage_name] - self.summary[pop_percentage_name]

        return True
