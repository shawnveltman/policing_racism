from src.acsdata import AcsData
from src.reporting import ReportManager

acs = AcsData()
reporting = ReportManager()
reporting.run_stop_county_reports()
reporting.consolidate_reports()
reporting.update_base_stop_report(acs=acs)