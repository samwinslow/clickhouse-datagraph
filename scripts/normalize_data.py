import re
import numpy

import pandas
from utils import read_dataset


base_dir = 'datasets/aviation'

state_abbreviations = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
airline_fatality_regex = r'Fatal\((\d+)\)'


def get_state(location=''):
  if (type(location) == str):
    state = location[-2:].upper()
    if state in state_abbreviations:
      return state
  return None


def fix_int(floating_int):
  value = numpy.nan_to_num(floating_int)
  return int(value)


def airline_accidents_get_severity(severity_raw=''):
  match = re.match(airline_fatality_regex, severity_raw)
  if match:
    return 'Fatal'
  else:
    return severity_raw


# Transform function generator that returns regex group match.
def regex_matcher(regex, default_none=False):
  if (not regex):
    raise Exception('Regex supplied to generator missing or invalid')
  def built_function(haystack=''):
    if (type(haystack) != str):
      return None
    match = re.search(regex, haystack)
    if match:
      return match.groups()[0]
    else:
      return None if default_none else haystack
  return built_function


# Transform function that operates as a row-wise selector.
def airline_accidents_get_fatal_count(row):
  fatal_count_given = row['TotalFatalInjuries']
  severity_given = row['InjurySeverity']
  fatal_count = fix_int(fatal_count_given)
  severity = airline_accidents_get_severity(severity_given)
  row['InjuryFatalCount'] = fatal_count
  row['InjurySeverity'] = severity

  if not fatal_count:
    if severity == 'Fatal':
      match = re.match(airline_fatality_regex, severity_given)
      if match:
        count = int(match.groups()[0])
        row['InjuryFatalCount'] = count
  
  return row


def waas_get_fatal_count(row) -> int:
  crew = fix_int(row['CrewFatalities'])
  pax = fix_int(row['PAXFatalities'])
  total = crew + pax
  return fix_int(total)


def waas_get_injured_count(row) -> int:
  crew = fix_int(row['CrewInjured'])
  pax = fix_int(row['PAXInjuries'])
  total = crew + pax
  return fix_int(total)


def waas_get_aboard_count(row) -> int:
  crew = fix_int(row['CrewAboard'])
  pax = fix_int(row['PAXAboard'])
  total = crew + pax
  return fix_int(total)


def waas_get_uninjured_count(row) -> int:
  aboard = waas_get_aboard_count(row)
  fatal = waas_get_fatal_count(row)
  injured = waas_get_injured_count(row)
  total = aboard - (fatal + injured)
  return fix_int(max(total, 0))


def waas_get_fatal(row):
  row['InjuryFatalCount'] = waas_get_fatal_count(row)
  return row


def waas_get_injured(row):
  row['InjurySeriousCount'] = waas_get_injured_count(row)
  return row


def waas_get_uninjured(row):
  row['InjuryUninjuredCount'] = waas_get_uninjured_count(row)
  return row


# Output columns (keys) are mapped from source columns (values).
#
# 'SourceColumn' == { 'col': 'SourceColumn' }
# Optionally, pass a transform function that will be applied to each element in `col`
# You can also pass a `literal` value that will be inserted down the whole column

get_city = regex_matcher(r'([^,]+),')
waas_get_acft_make = regex_matcher(r'^([\w\d]+)\s', True)
waas_get_acft_model = regex_matcher(r'^[\w\d]+\s([\w\d\-\.]+)')
waas_get_acft_series = regex_matcher(r'(\d)+$', True) # Note: only supports numerical series, e.g. 737-800
waas_get_country = regex_matcher(r'([A-Z]{2})$')

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
    'InjuryFatalCount':           { 'row': True, 'transform': airline_accidents_get_fatal_count },
    'InjurySeriousCount':         { 'col': 'TotalSeriousInjuries', 'transform': fix_int },
    'InjuryMinorCount':           { 'col': 'TotalMinorInjuries', 'transform': fix_int },
    'InjuryUninjuredCount':       { 'col': 'TotalUninjured', 'transform': fix_int },
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
    'AircraftEngineCount':        { 'col': 'NumberofEngines', 'transform': fix_int },
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
    'AircraftEngineCount':        { 'col': 'NbrofEngines', 'transform': fix_int },
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
  'ntsb_aviation_data.csv': {
    'EventId':                    'NTSB_RPRT_NBR',
    'EventDate':                  'EVENT_LCL_DATE',
    'EventType':                  'EV_TYPE_DESC',
    'SourceDataset':              { 'literal': 'ntsb_aviation_data' },
    'AgencyReportNumber':         'NTSB_RPRT_NBR',
    'AgencyReportType':           { 'literal': 'NTSB' },
    'AgencyReportDate':           { 'literal': None },
    'City':                       { 'literal': None },
    'StateCode':                  'LOC_STATE_CODE_STD',
    'Country':                    { 'literal': 'United States' },
    'Latitude':                   { 'literal': None },
    'Longitude':                  { 'literal': None },
    'AirportCode':                { 'literal': None },
    'AirportName':                'ARPT_NAME_STD',
    'InjurySeverity':             'INJURY_DESC',
    'InjuryFatalCount':           { 'literal': None },
    'InjurySeriousCount':         { 'literal': None },
    'InjuryMinorCount':           { 'literal': None },
    'InjuryUninjuredCount':       { 'literal': None },
    'AircraftDamageSeverity':     { 'literal': None },
    'AircraftMake':               'ACFT_NSDC_MAKE_STD',
    'AircraftModel':              'ACFT_NSDC_MODEL_STD',
    'AircraftSeries':             'ACFT_NSDC_SERIES_STD',
    'AircraftAmateurBuilt':       { 'literal': None },
    'AircraftOperator':           'OPRTR_NSDC_NAME_STD',
    'AircraftEngineMake':         { 'literal': None },
    'AircraftEngineModel':        { 'literal': None },
    'AircraftEngineGroupCode':    { 'literal': None },
    'AircraftEngineType':         { 'literal': None },
    'AircraftEngineCount':        { 'literal': None },
    'AircraftRegistrationNumber': { 'literal': None },
    'AircraftSerialNumber':       'ACFT_SERIAL_NBR',
    'FlightType':                 { 'literal': None },
    'FlightConductCode':          'FLTCNDCT_DESC',
    'FlightPlanFiledCode':        'OPRTR_SCHED_DESC',
    'FlightPhase':                'FLIGHT_PHASE_DESC',
    'FlightWeatherCondition':     { 'literal': None },
    'PilotCertificateType':       { 'literal': None },
    'PilotFlightTimeTotal':       { 'literal': None },
    'PilotFlightTimeInType':      { 'literal': None },
  },
  'world_aircraft_accident_summary.csv': {
    'EventId':                    'WAASSubsetEventId',
    'EventDate':                  'LocalEventDate',
    'EventType':                  { 'literal': None },
    'SourceDataset':              { 'literal': 'WAAS' },
    'AgencyReportNumber':         { 'literal': None },
    'AgencyReportType':           { 'literal': 'WAAS' },
    'AgencyReportDate':           { 'literal': None },
    'City':                       { 'literal': None },
    'StateCode':                  { 'literal': None },
    'Country':                    { 'col': 'EventLocation', 'transform': waas_get_country },
    'Latitude':                   { 'literal': None },
    'Longitude':                  { 'literal': None },
    'AirportCode':                { 'literal': None },
    'AirportName':                { 'literal': None },
    'InjurySeverity':             { 'literal': None },
    'InjuryFatalCount':           { 'row': True, 'transform': waas_get_fatal },
    'InjurySeriousCount':         { 'row': True, 'transform': waas_get_injured },
    'InjuryMinorCount':           { 'literal': None },
    'InjuryUninjuredCount':       { 'row': True, 'transform': waas_get_uninjured },
    'AircraftDamageSeverity':     { 'literal': None },
    'AircraftMake':               { 'col': 'Aircraft', 'transform': waas_get_acft_make },
    'AircraftModel':              { 'col': 'Aircraft', 'transform': waas_get_acft_model },
    'AircraftSeries':             { 'col': 'Aircraft', 'transform': waas_get_acft_series },
    'AircraftAmateurBuilt':       { 'literal': None },
    'AircraftOperator':           'AircraftOperator',
    'AircraftEngineMake':         { 'literal': None },
    'AircraftEngineModel':        { 'literal': None },
    'AircraftEngineGroupCode':    { 'literal': None },
    'AircraftEngineType':         { 'literal': None },
    'AircraftEngineCount':        { 'literal': None },
    'AircraftRegistrationNumber': { 'literal': None },
    'AircraftSerialNumber':       { 'literal': None },
    'FlightType':                 { 'literal': None },
    'FlightConductCode':          { 'literal': None },
    'FlightPlanFiledCode':        { 'literal': None },
    'FlightPhase':                { 'literal': None },
    'FlightWeatherCondition':     { 'literal': None },
    'PilotCertificateType':       { 'literal': None },
    'PilotFlightTimeTotal':       { 'literal': None },
    'PilotFlightTimeInType':      { 'literal': None },
  }
}


def has_callable_transform(input_source):
  return 'transform' in input_source and callable(input_source['transform'])


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
      if has_callable_transform(input_source):
        input_col_transformed = input_col.apply(input_source['transform'])
      output_df[col] = input_col_transformed
    elif 'row' in input_source:
      if not has_callable_transform(input_source):
        raise Exception('A transform function must be specified when using `row`.')
      transform = input_source['transform']
      output_df[col] = source_df.apply(transform, axis='columns')[col]

  output_df.to_csv(output_path, index=False)
