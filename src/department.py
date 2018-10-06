from fiona.crs import to_string
from pyproj import Proj
from shapely.geometry import Polygon, Point
import sys
import fiona
import geopandas as gpd

class Department:
    all_departments = None

    def __init__(self, department_shapefile_path):
        self.department_shapefile_path = department_shapefile_path
        self.shapefile = fiona.open(self.department_shapefile_path)
        self.crs_string = to_string(self.shapefile.crs)
        if self.crs_string == '':
            sys.exit("The Department Shapefile did not contain a .prj file "
                     "with encoding information.  Please add that file to the directory.")
        self.polygons = self.convert_department_shapefile_to_gps_polygons()
        self.demographics = None

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

    def geo_test(self):
        df = gpd.read_file(self.department_shapefile_path)
        df.crs = {'init' :'epsg:4326'}
        return df

    def add_demographic_status(self, overlap, community):
        department_ids = self.polygons.keys()
        relevant_set = overlap[overlap['precinct_id'].isin(department_ids)]
        relevant_set = relevant_set.apply(community.add_population_percentage)
        return relevant_set





