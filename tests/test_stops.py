from src.acsdata import AcsData
from src.stop import Stop


def test_stops_discards_rows_without_race():
    stops = Stop(stop_filepath='data/stops_test.csv')
    assert len(stops.df) == 100


def test_summary_created_on_loading():
    stops = Stop(stop_filepath='data/stops_test.csv')

    assert stops.summary.loc['56001']['white_stops'] == 91


def test_creates_unique_officer_id_from_state_and_officer_id():
    stops = Stop(stop_filepath='data/stops_test.csv')
    stops = stops.df
    stops_by_officer_wy40 = stops[stops['state_officer_id'] == 'wy40']

    assert len(stops_by_officer_wy40) > 0
    assert "officer_id" not in stops


def test_when_no_acs_given_summary_is_just_pivot():
    stops = Stop('data/stops_test.csv')
    columns = stops.summary.columns

    assert "white_percentage" not in columns


def test_when_acs_given_summary_contains_acs():
    acs = AcsData('data/acs_test.csv')
    stops = Stop(stop_filepath='data/stops_test.csv', acs=acs)

    assert stops.summary.loc['56001']['white_percentage'] > 0.83269
    assert stops.summary.loc['56001']['white_percentage'] < 0.83271


def test_proportion_difference_columns_added_on_creation():
    acs = AcsData('data/acs_test.csv')
    stops = Stop(stop_filepath='data/stops_test.csv', acs=acs)

    summary = stops.summary
    assert summary.loc['56001']['white_difference'] > 0.07730
    assert summary.loc['56001']['white_difference'] < 0.07740


def test_files_with_no_officer_id_loads():
    stops = Stop(stop_filepath="data/stops_test_no_officer_id.csv")

    assert len(stops.df) > 5
