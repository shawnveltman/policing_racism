import pandas as pd

class AcsData:
    def __init__(self,filepath="data/acs.csv"):
        self.filepath = filepath
        self.df = self.load_data()
        self.rename_columns()

    def create_summary(self):
        races = ['white', 'black', 'native', 'pacific_islander', 'other', 'asian','hispanic']

        summary = self.df.groupby('fips').sum()
        for race in races:
            col_name = race + '_percentage'
            summary[col_name] = summary[race] / summary['total_population']

        return summary

    def rename_columns(self):
        fips = self.df['GEO.id2'].astype('str').str[:5]

        hispanic_values = ['HD01_VD12','HD01_VD13','HD01_VD14','HD01_VD15','HD01_VD16','HD01_VD17','HD01_VD18',
                           'HD01_VD19','HD01_VD20','HD01_VD21']

        race_cols = ['HD01_VD01','HD01_VD03','HD01_VD04','HD01_VD06']
        native_cols = ['HD01_VD05','HD01_VD07','HD01_VD08']

        combined_cols = hispanic_values + race_cols + native_cols
        df = self.df[combined_cols]
        df[combined_cols] = df[combined_cols].astype(int)
        df['fips'] = fips

        df['hispanic'] = df[hispanic_values].sum(axis=1)
        df['other'] = df[native_cols].sum(axis=1)

        df.drop(hispanic_values,axis=1,inplace=True)
        col_names = {
            'HD01_VD01': 'total_population',
            'HD01_VD03': 'white',
            'HD01_VD04': 'black',
            'HD01_VD06': 'asian',
            'fips': 'fips',
            'hispanic':'hispanic',
            'other':'other'
        }

        df.rename(columns=col_names, inplace=True)
        self.df = df

    def load_data(self):
        community_data = pd.read_csv(self.filepath, encoding="ISO-8859-1")
        data = community_data[1:]
        return data