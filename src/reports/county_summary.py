import pandas as pd

from src.reports.generalsummary import GeneralSummary


class CountySummary:
    def __init__(self,stop,output_directory='data/summaries'):
        self.output_directory = output_directory
        self.stop = stop
        self.summary = None

    def create_summary(self):
        if self.stop.chunk is None:
            self.stop.load_dataframe()
        else:
            generalsummary = GeneralSummary()
            chunked_summary = generalsummary.create_chunked_summary(self.stop)
            self.summary = chunked_summary

        self.summary = self.create_summary_internals()

        export_filename = self.stop.filepath.split('/')[-1]
        export_path = self.output_directory + '/' + export_filename
        self.summary.to_csv(export_path)

        return self.summary

    def create_summary_internals(self):
        if self.stop.chunk is None:
            generalsummary = GeneralSummary()
            summary = generalsummary.add_stop_percentage_to_summary_table(self.stop)
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

    def add_acs_data_to_summary(self, summary):
        if not self.stop.acs:
            return summary

        merge = pd.merge(summary, self.stop.acs.summary, on='county_fips')
        return merge
