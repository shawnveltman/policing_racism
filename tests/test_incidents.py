from src.census import Census
from src.incident import Incident


def test_raw_incidents_have_records_with_no_gps_coords(incidents):
    df = incidents.df
    no_lat = df[df['LOCATION_LATITUDE'].isnull()]
    assert len(no_lat) > 0


def test_cleaned_incidents_all_have_gps_coordintes(incidents):
    df = incidents.clean_dataframe()
    no_lat = df[df['LOCATION_LATITUDE'].isnull()]
    assert len(no_lat) == 0


def test_cleaned_incidents_have_some_records(incidents):
    df = incidents.clean_dataframe()
    assert len(df) > 0


def test_can_add_department_ids_to_incidents_dataframe(incidents,precinct):
    incidents.add_department_id(precinct)
    assert len(incidents.df[incidents.df['department_id'] == '2']) > 0


def test_can_add_census_id_incidents_dataframe():
    census = Census("data/state-data/nc/cb_2017_37_tract_500k.shp")
    incidents = Incident('data/provided-data/Dept_35-00103/35-00103_UOF-OIS-P_prepped.csv',census=census)

    assert len(incidents.df[incidents.df['census_id'] == '37119004304']) > 0

