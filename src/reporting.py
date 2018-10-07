import glob
import os

import pandas as pd

from src.acsdata import AcsData
from src.stop import Stop


class ReportManager:
    def __init__(self, index_column='county_fips'):
        self.index_column = index_column
        self.skipped_files = []

    def consolidate_reports(self, directory,extension='.csv',report_name="/master_report.csv"):
        files = glob.glob(directory + "/*" + extension)
        master_report = pd.DataFrame()
        for file in files:
            summary = pd.read_csv(file,index_col=self.index_column)
            master_report = pd.concat([master_report, summary])

        master_filename = directory + report_name
        master_report.to_csv(master_filename)

    def run_reports(self, output_directory, input_directory,extension='.csv',acs=None,skip=[]):
        files = glob.glob(input_directory + "/*" + extension)
        for file in files:
            if file in skip:
                continue
            filename = file.split('/')[-1]
            file_path = output_directory + "/" + filename
            if os.path.exists(file_path):
                self.skipped_files.append(file_path)
            else:
                stops = Stop(file,acs=acs,chunk=True)
                stops.create_summary()

        return True