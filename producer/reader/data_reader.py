import pandas as pd


class Reader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.DataFrame()
        self.read_file()
        self.process_data()
        self.data_columns = list(self.data.columns)

    def read_file(self):
        self.data = pd.read_csv('./data/' + self.file_name,
                                sep=',',
                                header='infer',
                                encoding='iso-8859-1')

    def process_data(self):
        columns_tmp = self.data.columns
        columns_tmp = [column_name.lower() for column_name in columns_tmp]
        self.data.columns = columns_tmp
        self.data.rename(columns={'open': 'open_price',
                                  'close': 'close_price',
                                  'adj close': 'adj_close'}, inplace=True)

    def row_to_dict(self, row):
        row_dict = {}
        for key, value in zip(self.data_columns, row):
            row_dict[key] = value

        return row_dict


if __name__ == '__main__':
    reader = Reader('NFLX_2019.csv')
    print(reader.data.head())
    print(reader.data.columns)
    print(reader.row_to_dict(reader.data.iloc[0, :]))
