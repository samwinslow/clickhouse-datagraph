import re
# from utils import read_dataset


base_dir = 'datasets/aviation'

city_regex = r'([\w\s]+),'
state_abbreviations = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


def get_city(location=''):
  match = re.match(city_regex, location)
  if match:
    return match.groups()[0]
  else:
    return location


def get_state(location=''):
  state = location[-2:].upper()
  return state if state in state_abbreviations else None


# Standard columns (left) are mapped from source columns (right)
# You can also pass a lambda that optionally takes a row argument and returns a value.

dataset_property_mappings = {
  'airline_accidents.csv' : {
    'EventId':                    'EventId',
    'EventDate':                  'EventDate',
    'EventType':                  'InvestigationType',
    'SourceDataset':              lambda: 'airline_accidents',
    'AgencyReportNumber':         'AccidentNumber',
    'AgencyReportType':           lambda: 'NTSB',
    'AgencyReportDate':           'ReportPublicationDate',
    'City':                       lambda row: get_city(row['Location']),
    'StateCode':                  lambda row: get_state(row['Location']),
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
    'AircraftSeries':             lambda: None,
    'AircraftAmateurBuilt':       'AmateurBuilt',
    'AircraftOperator':           'AirCarrier',
    'AircraftEngineMake':         lambda: None,
    'AircraftEngineModel':        lambda: None,
    'AircraftEngineGroupCode':    lambda: None,
    'AircraftEngineType':         'AircraftEngineType',
    'AircraftEngineCount':        'NumberofEngines',
    'AircraftRegistrationNumber': 'RegistrationNumber',
    'AircraftSerialNumber':       lambda: None,
    'FlightType':                 'PurposeofFlight',
    'FlightConductCode':          lambda: None,
    'FlightPlanFiledCode':        'Schedule',
    'FlightPhase':                'BroadPhaseofFlight',
    'FlightWeatherCondition':     'WeatherCondition',
    'PilotCertificateType':       lambda: None,
    'PilotFlightTimeTotal':       lambda: None,
    'PilotFlightTimeInType':      lambda: None,
  },
  'faa_incidents_data.csv': {
    # TODO
  },
  'ntsb_aviation_data.csv': {
    # TODO
  },
  'world_aircraft_accident_summary.csv': {
    # TODO
  }
}
