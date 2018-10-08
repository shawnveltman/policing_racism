import glob
import os

import pandas as pd

from src.stop import Stop


class ReportManager:
    def __init__(self, index_column='county_fips'):
        self.index_column = index_column
        self.skipped_files = []
        self.acs = None

    def consolidate_reports(self, directory,extension='.csv',report_name="/master_report.csv"):
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

    def run_reports(self, output_directory, input_directory,extension='.csv',acs=None,skip=[]):
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
                stops = Stop(file,acs=acs,chunk=True)
                stops.create_summary()

        return True

    def update_base_stop_report(self, filepath,acs):
        df = pd.read_csv(filepath,index_col='county_fips',dtype={'county_fips':str})
        df.fillna(0,inplace=True)
        df = self.set_total_stops(acs, df)

        for race in acs.races:
            name = race + "_stop_proportion_excess"
            stop_percentage = race + "_stop_percentage"
            pop_percentage = race + "_percentage"
            df[name] = (df[stop_percentage] / df[pop_percentage]) - 1

        column_names = df.columns
        for race in acs.races:
            difference_col = race + "_difference"
            if difference_col in column_names:
                df.drop(difference_col,inplace=True,axis=1)

        col_names = {}
        for race in acs.races:
            new_name = race + "_population"
            col_names[race] = new_name

        self.acs = acs.df.reset_index()
        df.reset_index(inplace=True)
        df['location_text'] = df.apply(self.get_location_text, axis=1)

        df.rename(col_names,inplace=True,axis=1)
        df.to_csv(filepath)

    def get_location_text(self, row):
        row_county_fips_ = row.loc['county_fips'].astype(int).astype(str)
        while len(row_county_fips_) < 5:
            row_county_fips_ = '0' + row_county_fips_
        print(row_county_fips_)
        text_rows = self.acs[self.acs['county_fips'] == row_county_fips_]
        if len(text_rows) > 0:
            text = text_rows.iloc[0]['location_text']
        else:
            text = "Unknown"
        return text

    def set_total_stops(self, acs, df):
        df['total_stops'] = 0
        for race in acs.races:
            column_name = race + "_stops"
            df['total_stops'] = df['total_stops'] + df[column_name]

        return df