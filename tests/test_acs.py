from src.acsdata import AcsData


def test_columns_renamed_and_hispanic_values_aggregated_on_import():
    acs_filepath = "data/acs_test.csv"
    acs = AcsData(acs_filepath)

    assert acs.df['hispanic'].sum() > 0

def test_summary_works():
    acs_filepath = "data/acs_test.csv"
    acs = AcsData(acs_filepath)
    summary = acs.create_summary()

    hispanic_percentage = summary.loc['10010']['hispanic_percentage']
    assert hispanic_percentage > 0.07524
    assert hispanic_percentage < 0.07525

