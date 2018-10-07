import os

import pandas as pd

from src.reporting import ReportManager


def test_can_consolidate_all_csv_reports_into_master_report():
    directory = "data/summaries"
    filepath = directory + "/master_report.csv"

    if os.path.exists(filepath):
        os.remove(filepath)

    reporter = ReportManager()
    reporter.consolidate_reports(directory)

    master_report = pd.read_csv(filepath)
    print(master_report['county_fips'])
    assert len(master_report[master_report['county_fips'] == 56001]) > 0
