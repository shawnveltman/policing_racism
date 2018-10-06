from shapely.geometry import Point

def test_can_load_texas_shapefile_and_identify_point(texas):
    area_containing_point = texas.census_area_containing_point(Point(-97.738652, 30.2669))

    assert area_containing_point == '48453001100'

def test_nonsense_point_returns_false(texas):
    area_containing_point = texas.census_area_containing_point(Point(-197.738652, 30.2669))

    assert area_containing_point == False
