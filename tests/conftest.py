import pytest

from acsdata import AcsData
from stop import Stop


@pytest.fixture
def acs():
    acs_filepath = "data/acs_test.csv"
    return AcsData(acs_filepath)


@pytest.fixture
def stops_summary():
    stops = Stop(stop_filepath='data/stop_data/stops_test.csv')
    stops.create_summary()
    return stops


@pytest.fixture
def acs_stops(acs):
    return Stop(stop_filepath='data/stop_data/stops_test.csv', acs=acs)


@pytest.fixture
def acs_stop_summary(acs_stops):
    acs_stops.create_summary()
    return acs_stops.summary


@pytest.fixture
def chunkedStops(acs):
    stops = Stop(stop_filepath="data/stop_data/stops_test_no_officer_id.csv", chunk=True, acs=acs, chunksize=10)
    return stops.create_summary()
