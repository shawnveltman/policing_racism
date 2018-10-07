import pytest

from src.acsdata import AcsData
from src.stop import Stop


@pytest.fixture
def stops():
    stops = Stop(stop_filepath='data/stops_test.csv')
    stops.create_summary()
    return stops


@pytest.fixture
def acsStops():
    acs = AcsData('data/acs_test.csv')
    stops = Stop(stop_filepath='data/stops_test.csv', acs=acs)
    stops.create_summary()
    return stops


@pytest.fixture
def chunkedStops():
    acs = AcsData('data/acs_test.csv')
    stops = Stop(stop_filepath="data/stops_test_no_officer_id.csv", chunk=True, acs=acs, chunksize=10)
    stops.create_summary()
    return stops
