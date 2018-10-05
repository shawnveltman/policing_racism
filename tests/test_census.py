from shapely.geometry import Point
from src.census import Census


def test_can_load_texas_shapefile_and_identify_point():
    state_shapefile_path = "data/state-data/texas/cb_2017_48_tract_500k.shp"
    census = Census(state_shapefile_path)
    area_containing_point = census.census_area_containing_point(Point(-97.738652, 30.2669))

    assert area_containing_point == '48453001100'


def test_nonsense_point_returns_false():
    state_shapefile_path = "data/state-data/texas/cb_2017_48_tract_500k.shp"
    census = Census(state_shapefile_path)
    area_containing_point = census.census_area_containing_point(Point(-197.738652, 30.2669))

    assert area_containing_point == False
