from src.acsdata import AcsData
from src.stop import Stop

acs = AcsData()
file = "data/stop_data/AZ-clean.csv"
chunksize = 10 ** 6
stops = Stop(stop_filepath=file, chunk=True,
             acs=acs,
             chunksize=chunksize)
stops.create_summary()
