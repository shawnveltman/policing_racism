import pandas as pd
from shapely.geometry import Point

from src.community_survey import CommunitySurvey
from src.department import Department
from src.overlap import Overlap


def test_can_find_department_from_gps_point(precinct):
    department = precinct.precinct_containing_point(Point(-97.738652, 30.2669))
    assert department == '2'

def test_department_has_population_stats(texas):
    race_filepath = 'data/provided-data/Dept_37-00027/37-00027_ACS_data/37-00027_ACS_race-sex-age/ACS_15_5YR_DP05_with_ann.csv'
    community = CommunitySurvey(race_filepath)
    department_shapefile_path = "data/provided-data/Dept_37-00027/37-00027_Shapefiles/APD_DIST.shp"
    precinct = Department(department_shapefile_path)
    overlap = Overlap(census=texas, departments=precinct)
    precinct.add_demographic_status(overlap.matrix, community)
    # print(precinct.add_demographic_status(overlap.matrix, community))


