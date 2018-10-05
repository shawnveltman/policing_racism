import pandas as pd


class Incident:
    def __init__(self, incidents_path):
        df = pd.read_csv(incidents_path)
        self.df = df[1:]

    def clean_dataframe(self):
        self.get_datetime_index()
        self.remove_no_gps()
        return self.df

    def get_datetime_index(self):
        combined_datetime = self.get_combined_datetime()
        self.df['DATETIME'] = pd.to_datetime(combined_datetime)
        self.df.drop(['INCIDENT_DATE'], axis=1, inplace=True)

    def get_combined_datetime(self):
        combined_datetime = self.df['INCIDENT_DATE']
        keys = self.df.keys()
        if 'INCIDENT_TIME' in keys:
            combined_datetime = self.df['INCIDENT_DATE'].str.cat(self.df['INCIDENT_TIME'], sep=' ')
            self.df.drop(['INCIDENT_TIME'], axis=1, inplace=True)

        return combined_datetime

    def remove_no_gps(self):
        return self.df.dropna(subset=['LOCATION_LATITUDE', 'LOCATION_LONGITUDE'], inplace=True)