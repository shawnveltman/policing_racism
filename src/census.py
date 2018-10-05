import fiona
from shapely.geometry import Polygon


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