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

