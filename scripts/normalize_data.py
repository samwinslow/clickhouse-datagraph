import re

import pandas
from utils import read_dataset


base_dir = 'datasets/aviation'

city_regex = r'([\w\s]+),'
state_abbreviations = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


def get_city(location=''):
  if (type(location) != str):
    return None
  match = re.match(city_regex, location)
  if match:
    return match.groups()[0]
  else:
    return location


def get_state(location=''):
  if (type(location) == str):
    state = location[-2:].upper()
    if state in state_abbreviations:
      return state
  return None


# Output columns (keys) are mapped from source columns (values).
#
# 'SourceColumn' == { 'col': 'SourceColumn' }
# Optionally, pass a transform function that will be applied to each element in `col`
# You can also pass a `literal` value that will be inserted down the whole column

dataset_property_mappings = {
  'airline_accidents.csv': {
    'EventId':                    'EventId',
    'EventDate':                  'EventDate',
    'EventType':                  'InvestigationType',
    'SourceDataset':              { 'literal': 'airline_accidents' },
    'AgencyReportNumber':         'AccidentNumber',
    'AgencyReportType':           { 'literal': 'NTSB' },
    'AgencyReportDate':           'ReportPublicationDate',
    'City':                       { 'col': 'Location', 'transform': get_city },
    'StateCode':                  { 'col': 'Location', 'transform': get_state },
    'Country':                    'Country',
    'Latitude':                   'Latitude',
    'Longitude':                  'Longitude',
    'AirportCode':                'AirportCode',
    'AirportName':                'AirportName',
    'InjurySeverity':             'InjurySeverity',
    'InjuryFatalCount':           'TotalFatalInjuries',
    'InjurySeriousCount':         'TotalSeriousInjuries',
    'InjuryMinorCount':           'TotalMinorInjuries',
    'InjuryUninjuredCount':       'TotalUninjured',
    'AircraftDamageSeverity':     'AircraftDamage',
    'AircraftMake':               'Make',
    'AircraftModel':              'Model',
    'AircraftSeries':             { 'literal': None },
    'AircraftAmateurBuilt':       'AmateurBuilt',
    'AircraftOperator':           'AirCarrier',
    'AircraftEngineMake':         { 'literal': None },
    'AircraftEngineModel':        { 'literal': None },
    'AircraftEngineGroupCode':    { 'literal': None },
    'AircraftEngineType':         'EngineType',
    'AircraftEngineCount':        'NumberofEngines',
    'AircraftRegistrationNumber': 'RegistrationNumber',
    'AircraftSerialNumber':       { 'literal': None },
    'FlightType':                 'PurposeofFlight',
    'FlightConductCode':          { 'literal': None },
    'FlightPlanFiledCode':        'Schedule',
    'FlightPhase':                'BroadPhaseofFlight',
    'FlightWeatherCondition':     'WeatherCondition',
    'PilotCertificateType':       { 'literal': None },
    'PilotFlightTimeTotal':       { 'literal': None },
    'PilotFlightTimeInType':      { 'literal': None },
  },
  'faa_incidents_data.csv': {
    'EventId':                    'AIDSReportNumber',
    'EventDate':                  'LocalEventDate',
    'EventType':                  'EventType',
    'SourceDataset':              { 'literal': 'faa_incidents_data' },
    'AgencyReportNumber':         'AIDSReportNumber',
    'AgencyReportType':           { 'literal': 'FAA AIDS' },
    'AgencyReportDate':           { 'literal': None },
    'City':                       'EventCity',
    'StateCode':                  'EventState',
    'Country':                    { 'literal': 'United States' },
    'Latitude':                   { 'literal': None },
    'Longitude':                  { 'literal': None },
    'AirportCode':                { 'literal': None },
    'AirportName':                'EventAirport',
    'InjurySeverity':             { 'literal': None },
    'InjuryFatalCount':           'TotalFatalities',
    'InjurySeriousCount':         'TotalInjuries',
    'InjuryMinorCount':           { 'literal': None },
    'InjuryUninjuredCount':       { 'literal': None },
    'AircraftDamageSeverity':     'AircraftDamage',
    'AircraftMake':               'AircraftMake',
    'AircraftModel':              'AircraftModel',
    'AircraftSeries':             'AircraftSeries',
    'AircraftAmateurBuilt':       { 'literal': None },
    'AircraftOperator':           'Operator',
    'AircraftEngineMake':         'AircraftEngineMake',
    'AircraftEngineModel':        'AircraftEngineModel',
    'AircraftEngineGroupCode':    'EngineGroupCode',
    'AircraftEngineType':         { 'literal': None },
    'AircraftEngineCount':        'NbrofEngines',
    'AircraftRegistrationNumber': 'AircraftRegistrationNbr',
    'AircraftSerialNumber':       { 'literal': None },
    'FlightType':                 'PrimaryFlightType',
    'FlightConductCode':          'FlightConductCode',
    'FlightPlanFiledCode':        'FlightPlanFiledCode',
    'FlightPhase':                'FlightPhase',
    'FlightWeatherCondition':     { 'literal': None },
    'PilotCertificateType':       'PICCertificateType',
    'PilotFlightTimeTotal':       'PICFlightTimeTotalHrs',
    'PilotFlightTimeInType':      'PICFlightTimeTotalMake-Model',
  },
  # 'ntsb_aviation_data.csv': {
  #   # TODO
  # },
  # 'world_aircraft_accident_summary.csv': {
  #   # TODO
  # }
}


for filename in dataset_property_mappings:
  source_mapping = dataset_property_mappings[filename]
  source_path = '/'.join([base_dir, 'cleaned', filename])
  source_df = read_dataset(source_path)

  output_path = '/'.join([base_dir, 'normalized', filename])
  output_df = pandas.DataFrame()

  for col in source_mapping:
    input_source = source_mapping[col]
    if type(input_source) == str:
      output_df[col] = source_df[input_source]
    elif 'literal' in input_source:
      output_df[col] = input_source['literal']
    elif 'col' in input_source:
      input_col = source_df[input_source['col']]
      input_col_transformed = input_col
      if 'transform' in input_source and callable(input_source['transform']):
        input_col_transformed = input_col.apply(input_source['transform'])
      output_df[col] = input_col_transformed

  output_df.to_csv(output_path, index=False)
