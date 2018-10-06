import pandas as pd


class Overlap:
    def __init__(self, census, departments):
        self.departments = departments
        self.census = census
        self.matrix = self.precint_and_county_overlaps()

    def precint_and_county_overlaps(self):
        final_array = []
        for county_id, county_polygon in self.census.polygons.items():
            for precinct_id, precinct_polygon in self.departments.polygons.items():
                row_array = {}
                row_array['county_id'] = county_id
                row_array['precinct_id'] = precinct_id

                county_overlap = county_polygon.intersection(precinct_polygon)
                county_in_precinct = (county_overlap.area / county_polygon.area) * 100
                row_array['county_in_precinct'] = county_in_precinct

                precinct_overlap = precinct_polygon.intersection(county_polygon)
                precinct_in_county = (precinct_overlap.area / precinct_polygon.area) * 100
                row_array['precinct_in_county'] = precinct_in_county

                final_array.append(row_array)


        df = pd.DataFrame(final_array)
        no_precinct_in_county = df['precinct_in_county'] > 0
        no_county_in_precinct = df['county_in_precinct'] > 0
        return df[no_precinct_in_county & no_county_in_precinct]