# Trims whitespace and sets completely empty rows to None, saving the file in place.

from utils import read_dataset

datasets = [
  'datasets/aviation/airline_accidents.csv',
  'datasets/aviation/faa_incidents_data.csv',
  'datasets/aviation/ntsb_aviation_data.csv',
  'datasets/aviation/world_aircraft_accident_summary.csv'
]

for dataset in datasets:
  df = read_dataset(dataset)
  df_cleaned = df.replace(['^\s+', '\s+$', '^\s+$'], ['', '', None], regex=True)
  df_cleaned.to_csv(dataset, index=False)
