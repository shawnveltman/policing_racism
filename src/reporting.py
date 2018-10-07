import glob

import pandas as pd


class ReportManager:
    def __init__(self, index_column='county_fips'):
        self.index_column = index_column

    def consolidate_reports(self, directory,extension='.csv',report_name="/master_report.csv"):
        files = glob.glob(directory + "/*" + extension)
        master_report = pd.DataFrame()
        for file in files:
            summary = pd.read_csv(file,index_col=self.index_column)
            master_report = pd.concat([master_report, summary])

        master_filename = directory + report_name
        master_report.to_csv(master_filename)