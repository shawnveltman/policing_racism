from src.officerid import OfficerId


def test_can_groupby_officer_id(acs):
    stop = OfficerId('data/stop_data/stops_test.csv', acs=acs)
    stop.create_summary()
    hello = 'world'
