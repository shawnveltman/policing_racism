from src.reporting import ReportManager

output_directory = "data/summaries"
input_directory = 'data/stop_data'

# acs = AcsData()
reporter = ReportManager()
# reporter.run_reports(input_directory=input_directory,
#                      output_directory=output_directory,
#                      acs=acs)

reporter.consolidate_reports(directory='data/summaries')