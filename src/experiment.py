import sys

import fiona
import matplotlib.pyplot as plt
import pandas as pd
from fiona.crs import to_string
from pyproj import Proj
from shapely.geometry import Polygon, Point

from src.census import Census




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




class Overlap:
    def precint_and_county_overlaps(self, census, departments):
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

        return pd.DataFrame(final_array)

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
overlap_percentage = overlap.precint_and_county_overlaps(census, department)
print(overlap_percentage)


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
