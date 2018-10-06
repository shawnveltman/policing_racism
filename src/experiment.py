import pandas as pd


class AcsData:
    def main(self):
        races = ['white', 'black', 'native', 'pacific_islander', 'other', 'asian']
        numeric_columns = ['total_population'] + races
        cols_to_keep = numeric_columns + ['fips']

        data = self.prepare_data(cols_to_keep, numeric_columns)

        summary = data.groupby('fips').sum()
        for race in races:
            col_name = race + '_population'
            summary[col_name] = summary[race] / summary['total_population']

        return summary

    def prepare_data(self, cols_to_keep, numeric_columns):
        data = self.load_data()
        data = self.add_fips_column(data)
        data = self.rename_columns(data)
        data = self.drop_unwanted_columns(data, cols_to_keep)
        data[numeric_columns] = data[numeric_columns].astype(int)
        return data

    def drop_unwanted_columns(self, data, cols_to_keep):
        data = data[cols_to_keep]
        return data

    def rename_columns(self, data):
        col_names = {
            'HD01_VD01': 'total_population',
            'HD01_VD03': 'white',
            'HD01_VD04': 'black',
            'HD01_VD05': 'native',
            'HD01_VD07': 'pacific_islander',
            'HD01_VD08': 'other',
            'HD01_VD06': 'asian',
            'fips': 'fips'
        }
        data.rename(columns=col_names, inplace=True)
        return data

    def add_fips_column(self, data):
        data['fips'] = data['GEO.id2'].astype('str').str[:5]
        return data

    def load_data(self):
        community_data = pd.read_csv("data/acs.csv", encoding="ISO-8859-1")
        data = community_data[1:]
        return data

class Stops:
    def __init__(self,filepath):
        self.df = self.load_dataframe(filepath)

    def load_dataframe(self, filepath):
        df = pd.read_csv(filepath)
        cols_to_drop = ['location_raw', 'county_name']
        df = df.drop(cols_to_drop)
        return df


