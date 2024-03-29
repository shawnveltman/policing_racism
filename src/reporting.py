import glob
import os

import pandas as pd
from stop import Stop

class ReportManager:
    def __init__(self, index_column='county_fips'):
        self.index_column = index_column
        self.skipped_files = []
        self.acs = None

    def consolidate_reports(self, directory='data/summaries',extension='.csv',report_name="/master_report.csv"):
        files = glob.glob(directory + "/*" + extension)
        master_filename = directory + report_name

        if os.path.exists(master_filename):
            os.remove(master_filename)

        master_report = pd.DataFrame()
        for file in files:
            if file == master_filename:
                continue
            summary = pd.read_csv(file,index_col=self.index_column)
            master_report = pd.concat([master_report, summary])

        master_report.to_csv(master_filename)

    def run_stop_county_reports(self, output_directory='data/summaries',
                                input_directory='data/stop_data',
                                extension='.csv', acs=None, skip=[], stopmodel=Stop):

        files = glob.glob(input_directory + "/*" + extension)
        for file in files:
            if file in skip:
                continue
            filename = file.split('/')[-1]
            file_path = output_directory + "/" + filename
            if os.path.exists(file_path):
                print("Skipping " + file)
                self.skipped_files.append(file_path)
            else:
                stops = stopmodel(file,acs=acs,chunk=True,output_directory=output_directory)
                stops.create_summary()

        return True

    def update_base_stop_report(self, acs,filepath='data/summaries/master_report.csv',index_col='county_fips'):
        df = pd.read_csv(filepath, index_col=index_col, dtype={'county_fips':str})
        df.fillna(0,inplace=True)
        df = self.set_total_stops(acs, df)

        columns = df.columns
        for race in acs.races:
            name = race + "_stop_proportion_excess"
            stop_percentage = race + "_stop_percentage"
            pop_percentage = race + "_percentage"
            if stop_percentage in columns:
                df[name] = (df[stop_percentage] / df[pop_percentage]) - 1

        df = self.remove_subtraction_difference_column(acs, df)

        col_names = {}
        for race in acs.races:
            new_name = race + "_population"
            col_names[race] = new_name

        self.acs = acs.df.reset_index()
        df.reset_index(inplace=True)
        # merged_df = self.add_location_text(acs, df)
        df.rename(col_names,inplace=True,axis=1)
        df.to_csv(filepath)
        return df

    def add_location_text(self, acs, df):
        acs_locations = acs.df[['county_fips', 'location_text']]
        print("Merging with ACS for county locations!")
        merged_df = pd.merge(df, acs_locations, on='county_fips', how='left')
        print("Merge Complete!")
        return merged_df

    def remove_subtraction_difference_column(self, acs, df):
        column_names = df.columns
        for race in acs.races:
            difference_col = race + "_difference"
            if difference_col in column_names:
                df.drop(difference_col, inplace=True, axis=1)
        return df

    def get_location_text(self, row):
        fips_ = row['county_fips']
        row_county_fips_ = str(int(fips_))
        while len(row_county_fips_) < 5:
            row_county_fips_ = '0' + row_county_fips_
        text_rows = self.acs[self.acs['county_fips'] == row_county_fips_]
        if len(text_rows) > 0:
            text = text_rows.iloc[0]['location_text']
        else:
            text = "Unknown"
        return text

    def set_total_stops(self, acs, df):
        df['total_stops'] = 0
        columns = df.columns
        for race in acs.races:
            column_name = race + "_stops"
            if column_name in columns:
                df['total_stops'] = df['total_stops'] + df[column_name]

        return df
