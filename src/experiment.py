import time
import pandas as pd
from src.acsdata import AcsData
from src.reporting import ReportManager

acs = AcsData()

reporting = ReportManager()
reporting.consolidate_reports('data/summaries')
reporting.update_base_stop_report('data/summaries/master_report.csv',acs=acs)
