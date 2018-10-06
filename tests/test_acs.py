from src.acsdata import AcsData

def test_columns_renamed_and_hispanic_values_aggregated_on_import():
    acs_filepath = "data/acs_test.csv"
    acs = AcsData(acs_filepath)

    assert acs.df['hispanic'].sum() > 0

def test_summary_works():
    acs_filepath = "data/acs_test.csv"
    acs = AcsData(acs_filepath)
    summary = acs.summary
    hispanic_percentage = summary.loc['56001']['hispanic_percentage']
    assert hispanic_percentage > 0.09718257
    assert hispanic_percentage < 0.09718259

def test_population_fields_add_up_to_population_total():
    acs_filepath = "data/acs_test.csv"
    acs = AcsData(acs_filepath)
    summary = acs.summary

    r = summary.loc['56001']
    totals = r['white'] + r['black'] + r['asian'] \
                        + r['hispanic'] + r['other']
    assert totals < r['total_population']