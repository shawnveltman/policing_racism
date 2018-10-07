import datetime

import pandas as pd

from src.acsdata import AcsData
from src.stop import Stop

acs = AcsData()
file = "data/stop_data/IA-clean.csv"
chunksize = 10 ** 5
stops = Stop(stop_filepath=file,chunk=True,acs=acs,chunksize=chunksize)
