import pytest

from src.community_survey import CommunitySurvey
from src.incident import Incident


@pytest.fixture
def community():
    race_filepath = 'data/provided-data/Dept_37-00027/37-00027_ACS_data/37-00027_ACS_race-sex-age/ACS_15_5YR_DP05_with_ann.csv'
    community = CommunitySurvey(race_filepath)
    community.set_census_tract('48217960100')
    return community

@pytest.fixture
def incidents():
    incidents_path = "data/provided-data/Dept_37-00027/37-00027_UOF-P_2014-2016_prepped.csv"
    return Incident(incidents_path)
