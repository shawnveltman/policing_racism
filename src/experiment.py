from src.acsdata import AcsData
from src.stop import Stop

acs = AcsData()
stops = Stop('data/stop_data/WY-clean.csv',acs=acs)
print(stops.summary.head())