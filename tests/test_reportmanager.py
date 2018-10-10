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


def test_skips_files_that_already_have_reports(acs):
    # given I have a source file
    directory = "data/summaries"
    filepath = directory + "/stops_test.csv"

    # and a report file with the same name in the output directory
    if not os.path.exists(filepath):
        f = open(filepath, "w+")
        f.close()

    # that source file is not analyzed
    reporter = ReportManager()
    reporter.run_stop_county_reports(input_directory='data', output_directory='data/summaries', acs=acs, skip=['data/acs_test.csv'])

    assert filepath in reporter.skipped_files


def test_runs_files_that_do_not_have_reports(acs):
    directory = "data/summaries"
    filepath = directory + "/stops_test.csv"

    if os.path.exists(filepath):
        os.remove(filepath)

    assert os.path.exists(filepath) is False

    reporter = ReportManager()
    reporter.run_stop_county_reports(input_directory='data', output_directory='data/summaries', acs=acs, skip=['data/acs_test.csv'])

    assert os.path.exists(filepath) is True

def test_master_report_has_three_counties(acs):
    # Delete files in report directory
    delete_all_files()

    reporter = ReportManager()
    output_directory = 'data/summaries'
    reporter.run_stop_county_reports(input_directory='data', output_directory=output_directory, acs=acs,
                                     skip=['data/acs_test.csv'])
    reporter.consolidate_reports(output_directory)

    master_report = pd.read_csv(output_directory + '/master_report.csv', index_col='county_fips')
    assert len(master_report) == 3

def delete_all_files():
    directory = "data/summaries"
    for filename in os.listdir(directory):
        if filename != '.DS_Store':
            os.unlink(directory + "/" + filename)
