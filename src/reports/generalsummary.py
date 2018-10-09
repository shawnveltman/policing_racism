import datetime

import pandas as pd

class GeneralSummary:
    def create_chunked_summary(self, stop):
        total_summary = pd.DataFrame()
        counter = 1
        filepath = stop.filepath
        for chunk in pd.read_csv(filepath, chunksize=stop.chunksize, dtype={'county_fips': str}):
            now = datetime.datetime.now()
            print(filepath + " - " + str(stop.chunksize * counter) + " - " + now.strftime("%H:%M:%S"))
            stop.chunk = chunk
            stop.load_dataframe()
            summary = self.add_stop_percentage_to_summary_table(stop)
            total_summary = pd.concat([total_summary, summary])
            counter = counter + 1

        group = total_summary.reset_index()
        group = group.groupby(['county_fips', 'driver_race']).agg('sum')
        return group


    def add_stop_percentage_to_summary_table(self, stop):
        summary = stop.df.groupby(['county_fips', 'driver_race']).agg('count')
        summary = summary[['id']]
        summary['stops'] = summary['id']
        summary = summary[['stops']]
        return summary