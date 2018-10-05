import sys

import fiona
import matplotlib.pyplot as plt
import pandas as pd
from fiona.crs import to_string
from pyproj import Proj
from shapely.geometry import Polygon, Point


class Census:
    def __init__(self, census_path):
        self.census_path = census_path
        self.polygons = self.get_coords()

    def get_coords(self):
        census_shapefile = fiona.open(self.census_path)
        census_boundaries = {}
        for row in census_shapefile:
            geoid = row['properties']['GEOID']
            coordinates = row['geometry']['coordinates'][0]
            if len(coordinates) > 2:
                census_boundaries[geoid] = Polygon(coordinates)
        return census_boundaries

    def census_area_containing_point(self, point):
        for id, polygon in self.polygons.items():
            if polygon.contains(point):
                return id

        return False

class Department:
    all_departments = None

    def __init__(self, department_shapefile_path):
        self.shapefile = fiona.open(department_shapefile_path)
        self.crs_string = to_string(self.shapefile.crs)
        if self.crs_string == '':
            sys.exit("The Department Shapefile did not contain a .prj file "
                     "with encoding information.  Please add that file to the directory.")
        self.polygons = self.convert_department_shapefile_to_gps_polygons()

    def convert_department_shapefile_to_gps_polygons(self):
        all_departments = {}
        for rec in self.shapefile:
            coords = rec['geometry']['coordinates']
            for area in coords:
                department_polygon = []
                for coord in area:
                    myproj = Proj(self.crs_string, preserve_units=True)
                    newcoord = myproj(coord[0], coord[1], inverse=True)
                    department_polygon.append(newcoord)
                length_of_department_polygon = len(department_polygon)
                if(length_of_department_polygon > 2):
                    all_departments[rec['id']] = Polygon(department_polygon)
        return all_departments

    def precinct_containing_point(self, point):
        for id, polygon in self.polygons.items():
            if polygon.contains(point):
                return id

        return False

class Incidents:
    def __init__(self, incidents_path):
        df = pd.read_csv(incidents_path)
        self.df = df[1:]

    def load_dataframe(self):
        return self.df

    def get_dataframe(self):
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


class Overlap:
    def percentage_of_county_in_precinct(self, census, departments):
        final_array = []
        for county_id, county_polygon in census.polygons.items():
            for precinct_id, precinct_polygon in departments.polygons.items():
                row_array = {}
                row_array['county_id'] = county_id
                row_array['precinct_id'] = precinct_id

                county_overlap = county_polygon.intersection(precinct_polygon)
                county_in_precinct = (county_overlap.area / county_polygon.area) * 100
                row_array['county_in_precinct'] = county_in_precinct

                precinct_overlap = precinct_polygon.intersection(county_polygon)
                precinct_in_county = (precinct_overlap.area / precinct_polygon.area) * 100
                row_array['precinct_in_county'] = precinct_in_county

                final_array.append(row_array)

        return final_array

state_shapefile_path = "state-data/texas/cb_2017_48_tract_500k.shp"
department_shapefile_path = "provided-data/Dept_37-00027/37-00027_Shapefiles/APD_DIST.shp"
incidents_path = "provided-data/Dept_37-00027/37-00027_UOF-P_2014-2016_prepped.csv"

department = Department(department_shapefile_path)

census = Census(state_shapefile_path)
# census_containing_point = census.census_area_containing_point(Point(-97.738652, 30.2669))
# print(census_containing_point)

# incidents = Incidents(incidents_path)
# incidents_df = incidents.get_dataframe()
# print("Loaded Incidents")
#

overlap = Overlap()
overlap_percentage = overlap.percentage_of_county_in_precinct(census, department)
print("Loaded overlap")
overlap_df = pd.DataFrame(overlap_percentage)
print(overlap_df[(overlap_df['county_in_precinct'] > 1)])

# TO DO:
# 1. From GPS coordinate of incident, determine which precinct it occured in
# 2. From GPS coordinate of incident, determine which Census tract it occured in
# 3. Attach Precinct ID and Census ID to each incident type
# 4. Determine overlap % of Census Tracts with Precincts (separate table / dataframe?  Pivot table, at any rate)
# 5. For each precinct, count total # of white, black, and other minority residents
# 6. Create function to determine if coordinates need to be converted
# 7.

import shapefile as shp

department_shapefile_path = "provided-data/Dept_37-00027/37-00027_Shapefiles/APD_DIST.shp"
sf = shp.Reader(department_shapefile_path)

plt.figure()
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    plt.plot(x, y)
plt.show()
