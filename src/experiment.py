from src.acsdata import AcsData
from src.stop import Stop

acs = AcsData()
file = "data/stop_data/SC-clean.csv"
chunksize = 10 ** 3
stops = Stop(stop_filepath=file, chunk=True,
             acs=acs,
             chunksize=chunksize)
