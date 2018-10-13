from stop import Stop


class OfficerId(Stop):
    def __init__(self, stop_filepath=None, acs=None, chunk=None, chunksize=1000000,
                 groupby_columns=['county_fips', 'state_officer_id','driver_race'], output_directory='data/summaries'):
        super().__init__(stop_filepath, acs, chunk, chunksize, groupby_columns, output_directory)

    def create_single_columns_from_summary_table(self):
        summary = self.summary.reset_index()
        melt = summary.melt(id_vars=self.groupby_columns, value_vars=['stops', 'stop_percentage'])
        pivot = melt.pivot_table(index=['county_fips','state_officer_id'], columns=['driver_race', 'variable'], values='value')
        pivot.columns = ['_'.join(col).strip() for col in pivot.columns.values]
        pivot.reset_index(inplace=True)
        return pivot

    def export_file(self):
        export_filename = self.filepath.split('/')[-1]
        export_path = self.output_directory + '/' + export_filename
        self.summary.to_csv(export_path)

    def create_stop_percentage(self):
        stop_percentage_label = 'stop_percentage'
        stops_ = self.summary['stops']
        summary_groupby = self.summary.groupby(['state_officer_id', 'county_fips'])
        self.summary[stop_percentage_label] = stops_ / summary_groupby.transform(sum)['stops']
        return True
