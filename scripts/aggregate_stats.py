import pandas
from utils import read_dataset


base_dir = 'datasets/aviation/cleaned'

datasets = [
  'airline_accidents.csv',
  'faa_incidents_data.csv',
  'ntsb_aviation_data.csv',
  'world_aircraft_accident_summary.csv'
]

for dataset in datasets:
  source_path = '/'.join([base_dir, dataset])
  df = read_dataset(source_path)
  print('Count of null rows by column:')
  print(df.isnull().sum(), '\n')

  print(f'Head of {dataset}:')
  pandas.set_option('display.max_columns', None)
  print(df.head(10), '\n\n')
