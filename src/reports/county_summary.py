from src.reports.generalsummary import GeneralSummary


class CountySummary(GeneralSummary):
    def __init__(self, stop, output_directory='data/summaries', groupby_columns=['county_fips', 'driver_race']):
        self.groupby_columns = groupby_columns
        self.output_directory = output_directory
        self.stop = stop
        self.summary = None

    def create_single_columns_from_summary_table(self, summary):
        summary = summary.reset_index()
        melt = summary.melt(id_vars=['county_fips', 'driver_race'], value_vars=['stops', 'stop_percentage'])
        pivot = melt.pivot_table(index=['county_fips'], columns=['driver_race', 'variable'], values='value')
        pivot.columns = ['_'.join(col).strip() for col in pivot.columns.values]
        pivot.columns = pivot.columns.get_level_values(0)
        return pivot
