from src.acsdata import AcsData
from src.officerid import OfficerId
from src.reporting import ReportManager

acs = AcsData()
officer_id_summary_directory = 'data/summaries/officer_id'

reporter = ReportManager()
output_directory = officer_id_summary_directory
reporter.run_stop_county_reports(input_directory='data/stop_data', output_directory=output_directory, acs=acs,
                                 stopmodel=OfficerId)
reporter.consolidate_reports(output_directory)
master_report = pd.read_csv(output_directory + '/master_report.csv', dtype={'county_fips': str})
df = reporter.update_base_stop_report(acs=acs, filepath=officer_id_summary_directory + '/master_report.csv',
                                      index_col=None)
