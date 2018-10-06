import pandas as pd
from shapely.geometry import Point


class Incident:
    def __init__(self, incidents_path, department=None, census=None):
        df = pd.read_csv(incidents_path)
        self.df = df[1:]
        self.add_points()
        if(department):
            self.add_department_id(department)
        if(census):
            self.add_census_id(census)

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

    def convert_coordinates_from_department(self, precinct_crs):
        # This function should convert the X_COORDINATES & Y_COORDINATES
        # columns in a dataframe (if they exist) to GPS coordinates
        # To avoid throwing out all of the records with X_COORD & Y_COORD but
        # no lat & long
        return True

    def add_points(self):
        self.df['point'] = self.df.apply(self.convert_coords_to_point, axis=1)

    def add_department_id(self, precinct):
        self.df['department_id'] = self.df['point'].apply(precinct.precinct_containing_point)

    def add_census_id(self, census):
        self.df['census_id'] = self.df['point'].apply(census.census_area_containing_point)

    def convert_coords_to_point(self, row):
        return Point(float(row['LOCATION_LONGITUDE']),float(row['LOCATION_LATITUDE']))

