import os

import pandas as pd

from officerid import OfficerId
from reporting import ReportManager


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
    reporter.run_stop_county_reports(input_directory='data/stop_data', output_directory='data/summaries', acs=acs)

    assert filepath in reporter.skipped_files


def test_runs_files_that_do_not_have_reports(acs):
    directory = "data/summaries"
    filepath = directory + "/stops_test.csv"

    if os.path.exists(filepath):
        os.remove(filepath)

    assert os.path.exists(filepath) is False

    reporter = ReportManager()
    reporter.run_stop_county_reports(input_directory='data/stop_data', output_directory='data/summaries', acs=acs)

    assert os.path.exists(filepath) is True


def test_master_report_has_three_counties(acs):
    # Delete files in report directory
    delete_all_files()

    reporter = ReportManager()
    output_directory = 'data/summaries'
    reporter.run_stop_county_reports(input_directory='data/stop_data', output_directory=output_directory, acs=acs)
    reporter.consolidate_reports(output_directory)

    master_report = pd.read_csv(output_directory + '/master_report.csv', dtype={'county_fips': str})
    assert len(master_report) == 3
    first_county = master_report[master_report['county_fips'] == '56001']
    assert first_county['white_stop_percentage'][0] == 0.91


def test_officer_id_master_report_has_correct_difference_percentagas(acs):
    officer_id_summary_directory = 'data/summaries/officer_id'
    delete_all_files(officer_id_summary_directory)
    reporter = ReportManager()
    output_directory = officer_id_summary_directory
    reporter.run_stop_county_reports(input_directory='data/stop_data', output_directory=output_directory, acs=acs,
                                     stopmodel=OfficerId)
    reporter.consolidate_reports(output_directory)
    master_report = pd.read_csv(output_directory + '/master_report.csv', dtype={'county_fips': str})
    df = reporter.update_base_stop_report(acs=acs, filepath=officer_id_summary_directory + '/master_report.csv',
                                          index_col=None)
    wy272 = df['state_officer_id'] == 'wy272'
    fips = df['county_fips'] == '56001'
    black_excess = df[wy272 & fips].iloc[0]['black_stop_proportion_excess']

    assert black_excess > 17.583497 and black_excess < 17.583498

def test_clear_reporting_dirs():
    delete_all_files()
    officer_id_summary_directory = 'data/summaries/officer_id'
    delete_all_files(officer_id_summary_directory)


def delete_all_files(directory="data/summaries"):
    if os.path.isdir(directory):
        for filename in os.listdir(directory):
            directory_filename = directory + "/" + filename
            if filename != '.DS_Store' and os.path.isfile(directory_filename):
                os.unlink(directory_filename)
