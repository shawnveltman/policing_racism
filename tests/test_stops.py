from stop import Stop


def test_stops_discards_rows_without_race(stops_summary):
    assert len(stops_summary.df) == 100


def test_summary_created_on_loading(acs_stop_summary):
    assert acs_stop_summary.loc['56001']['white_stops'] == 91


def test_creates_unique_officer_id_from_state_and_officer_id(stops_summary):
    stops = stops_summary.df
    stops_by_officer_wy40 = stops[stops['state_officer_id'] == 'wy40']

    assert len(stops_by_officer_wy40) > 0
    assert "officer_id" not in stops


def test_when_no_acs_given_summary_is_just_pivot(stops_summary):
    columns = stops_summary.summary.columns

    assert "white_percentage" not in columns


def test_when_acs_given_summary_contains_acs(acs_stop_summary):
    record = acs_stop_summary.loc['56001']['white_percentage']
    assert record > 0.83269
    assert record < 0.83271


def test_files_with_no_officer_id_loads():
    stops = Stop(stop_filepath="data/stop_data/stops_test_no_officer_id.csv")
    stops.create_summary()

    assert len(stops.df) > 5


def test_summary_works_when_chunking(chunkedStops):
    summary = chunkedStops
    assert summary.loc['56001']['asian_stop_percentage'] == 0.02
    assert summary.loc['56001']['white_stops'] == 91


def test_drop_rows_with_no_driver_race_data():
    stops = Stop(stop_filepath="data/stop_data/stops_test_no_driver_race.csv")
    stops.create_summary()

    assert len(stops.df) == 0
