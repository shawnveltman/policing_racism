def test_returns_no_tract_set_value_if_no_tract_set(community):
    community.set_census_tract(None)
    black_population = community.population_black()
    assert black_population == "No Tract Set"

def test_can_find_black_population(community):
    black_population = community.population_black()
    assert black_population == 293

def test_can_find_black_percentage(community):
    black_population = community.percent_black()
    assert black_population == 7.8

def test_can_find_white_population(community):
    white_population = community.population_white()
    assert white_population == 3289

def test_can_find_white_percentage(community):
    white = community.percent_white()
    assert white == 87.5

def test_can_find_total_population(community):
    total_population = community.population_total()
    assert total_population == 3760
