import datetime

import pandas as pd

from src.acsdata import AcsData
from src.stop import Stop

acs = AcsData()
file = "data/stop_data/WA-clean.csv"
chunksize = 10 ** 2
counter = 1
hello = None
total_summary = pd.DataFrame()
for chunk in pd.read_csv(file, chunksize=chunksize):
    now = datetime.datetime.now()
    print("Loading " + file + " at " + now.strftime("%H:%M:%S"))
    stop = Stop(chunk=chunk, acs=acs)
    export_filename = file.split('/')[2].split('.')[0] + "_" + str(counter) + '.csv'
    stop.summary.to_csv('data/summaries/' + export_filename)
    total_summary = pd.concat([total_summary, stop.summary])
    counter = counter + 1

