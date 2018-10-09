import pytest

from src.acsdata import AcsData
from src.reports.county_summary import CountySummary
from src.stop import Stop

@pytest.fixture
def acs():
    acs_filepath = "data/acs_test.csv"
    return AcsData(acs_filepath)


@pytest.fixture
def stops():
    stops = Stop(stop_filepath='data/stops_test.csv')
    countySummary = CountySummary(stops)
    countySummary.create_summary()

    return countySummary


@pytest.fixture
def acsStops(acs):
    stops = Stop(stop_filepath='data/stops_test.csv', acs=acs)

    countySummary = CountySummary(stops)
    countySummary.create_summary()

    return countySummary


@pytest.fixture
def chunkedStops(acs):
    stops = Stop(stop_filepath="data/stops_test_no_officer_id.csv", chunk=True, acs=acs, chunksize=10)
    countySummary = CountySummary(stops)
    countySummary.create_summary()

    return countySummary
