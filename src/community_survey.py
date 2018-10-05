import pandas as pd


class CommunitySurvey:
    def __init__(self, filepath):
        self.survey = pd.read_csv(filepath)
        self.current_tract = None

    def set_census_tract(self, census_tract_id):
        if census_tract_id is None:
            self.current_tract = None
            return
        self.current_tract = self.survey[self.survey['GEO.id2'] == census_tract_id]

    def column_values_for(self, column):
        if self.current_tract is None:
            return "No Tract Set"
        return float(self.current_tract[column])

    def percent_black(self):
        return self.column_values_for('HC03_VC50')

    def percent_white(self):
        return self.column_values_for('HC03_VC49')

    def population_total(self):
        return self.column_values_for('HC01_VC43')

    def population_white(self):
        return self.column_values_for('HC01_VC49')

    def population_black(self):
        return self.column_values_for('HC01_VC50')

