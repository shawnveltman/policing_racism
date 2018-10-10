import pytest

from src.acsdata import AcsData
from src.reports.county_summary import CountySummary
from src.reports.generalsummary import GeneralSummary
from src.stop import Stop

@pytest.fixture
def acs():
    acs_filepath = "data/acs_test.csv"
    return AcsData(acs_filepath)


@pytest.fixture
def stops_summary():
    stops = Stop(stop_filepath='data/stops_test.csv')
    countySummary = GeneralSummary(stops)
    countySummary.create_summary()

    return countySummary

@pytest.fixture
def acs_stops(acs):
    return Stop(stop_filepath='data/stops_test.csv', acs=acs)

@pytest.fixture
def acs_stop_summary(acs_stops):
    countySummary = GeneralSummary(acs_stops)
    countySummary.create_summary()

    return countySummary


@pytest.fixture
def chunkedStops(acs):
    stops = Stop(stop_filepath="data/stops_test_no_officer_id.csv", chunk=True, acs=acs, chunksize=10)
    countySummary = GeneralSummary(stops)
    countySummary.create_summary()

    return countySummary
