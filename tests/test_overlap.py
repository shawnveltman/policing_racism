from src.department import Department
from src.overlap import Overlap

def test_can_get_overlap_from_census_and_precinct_shapefiles(texas):
    small_precinct_path = "data/provided-data/Dept_37-00049/37-00049_Shapefiles/EPIC.shp"
    precinct = Department(small_precinct_path)

    overlap = Overlap(texas, precinct)

    no_precinct_in_county = overlap.matrix['precinct_in_county'] == 0
    no_county_in_precinct = overlap.matrix['county_in_precinct'] == 0
    no_overlap = overlap.matrix[no_county_in_precinct & no_precinct_in_county]
    assert len(no_overlap) == 0
    assert len(overlap.matrix) > 10
