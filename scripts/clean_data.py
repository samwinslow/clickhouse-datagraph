from utils import read_dataset

base_dir = 'datasets/aviation'

datasets_with_date_cols = [
  ('airline_accidents.csv', ['Event Date', 'Report Publication Date']),
  ('faa_incidents_data.csv', ['Local Event Date']),
  ('ntsb_aviation_data.csv', ['EVENT_LCL_DATE']),
  ('world_aircraft_accident_summary.csv', ['Local Event Date'])
]

for [dataset, date_columns] in datasets_with_date_cols:
  source_path = '/'.join([base_dir, dataset])
  df = read_dataset(source_path, date_columns)

  output_path = '/'.join([base_dir, 'cleaned', dataset])
  df.to_csv(output_path, index=False)
