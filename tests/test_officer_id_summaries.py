from src.officerid import OfficerId


def test_can_groupby_officer_id(acs):
    stop = OfficerId('data/stop_data/stops_test.csv', acs=acs)
    stop.create_summary()
    summary = stop.summary
    wy199 = summary['state_officer_id'] == 'wy199'
    first_fips = summary['county_fips'] == '56001'
    filtered_dataframe = summary[wy199 & first_fips].iloc[0]

    white_stop_percentage_ = filtered_dataframe['white_stop_percentage']
    assert white_stop_percentage_ == 4 / 6
