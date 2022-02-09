# Trims whitespace and sets completely empty rows to None, saving the file in place.

import pandas
import chardet

datasets = [
  'datasets/aviation/airline_accidents.csv',
  'datasets/aviation/faa_incidents_data.csv',
  'datasets/aviation/ntsb_aviation_data.csv',
  'datasets/aviation/world_aircraft_accident_summary.csv'
]
default_encoding = 'latin1'

for dataset in datasets:
  print(f"Reading dataset {dataset}")
  encoding = default_encoding
  with open(dataset, 'rb') as raw:
    result = chardet.detect(raw.read(100000))
    encoding = default_encoding if result['encoding'] == 'ascii' else result['encoding']
    print(f"  using codec '{encoding}'...")

  df = pandas.read_csv(dataset, encoding=encoding)
  df_cleaned = df.replace(['^\s+', '\s+$', '^\s+$'], ['', '', None], regex=True)
  df_cleaned.to_csv(dataset)
