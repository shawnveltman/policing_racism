from src.stop import Stop


def test_stops_discards_rows_without_race():
    stops = Stop('data/stops_test.csv')
    assert len(stops.df) == 100


def test_summary_created_on_loading():
    stops = Stop('data/stops_test.csv')

    assert stops.summary.loc['56001']['white_stops'] == 91


def test_creates_unique_officer_id_from_state_and_officer_id():
    stops = Stop('data/stops_test.csv')
    stops = stops.df
    stops_by_officer_wy40 = stops[stops['state_officer_id'] == 'wy40']

    assert len(stops_by_officer_wy40) > 0


def test_can_merge_stop_and_acs_data():
    pass
