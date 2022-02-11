CREATE DATABASE IF NOT EXISTS aviation;

CREATE TABLE aviation.airline_accidents
(
  `EventId` String,
  `InvestigationType` Nullable(String),
  `AccidentNumber` String,
  `EventDate` Nullable(Date),
  `Location` Nullable(String),
  `Country` Nullable(String),
  `Latitude` Nullable(Float64),
  `Longitude` Nullable(Float64),
  `AirportCode` Nullable(String),
  `AirportName` Nullable(String),
  `InjurySeverity` String,
  `AircraftDamage` Nullable(String),
  `AircraftCategory` Nullable(String),
  `RegistrationNumber` Nullable(String),
  `Make` Nullable(String),
  `Model` Nullable(String),
  `AmateurBuilt` Nullable(Boolean),
  `NumberofEngines` Nullable(UInt8),
  `EngineType` Nullable(String),
  `FARDescription` Nullable(String),
  `Schedule` Nullable(String),
  `PurposeofFlight` Nullable(String),
  `AirCarrier` Nullable(String),
  `TotalFatalInjuries` UInt16,
  `TotalSeriousInjuries` UInt16,
  `TotalMinorInjuries` UInt16,
  `TotalUninjured` UInt16,
  `WeatherCondition` Nullable(String),
  `BroadPhaseofFlight` Nullable(String),
  `ReportPublicationDate` Nullable(Date)
)
ENGINE = MergeTree()
ORDER BY sipHash64(EventId)
SAMPLE BY sipHash64(EventId);

CREATE TABLE aviation.faa_incidents_data
(
  `AIDSReportNumber` String,
  `LocalEventDate` Date,
  `EventCity` Nullable(String),
  `EventState` Nullable(String),
  `EventAirport` Nullable(String),
  `EventType` String,
  `AircraftDamage` Nullable(String),
  `FlightPhase` Nullable(String),
  `AircraftMake` Nullable(String),
  `AircraftModel` Nullable(String),
  `AircraftSeries` Nullable(String),
  `Operator` Nullable(String),
  `PrimaryFlightType` Nullable(String),
  `FlightConductCode` Nullable(String),
  `FlightPlanFiledCode` Nullable(String),
  `AircraftRegistrationNbr` String,
  `TotalFatalities` UInt16,
  `TotalInjuries` UInt16,
  `AircraftEngineMake` Nullable(String),
  `AircraftEngineModel` Nullable(String),
  `EngineGroupCode` Nullable(String),
  `NbrofEngines` Nullable(UInt8),
  `PICCertificateType` Nullable(String),
  `PICFlightTimeTotalHrs` Nullable(Float64),
  `PICFlightTimeTotalMake-Model` Nullable(Float64),
  `.1` Nullable(Float64)
)
ENGINE = MergeTree()
ORDER BY sipHash64(AIDSReportNumber)
SAMPLE BY sipHash64(AIDSReportNumber);

CREATE TABLE aviation.ntsb_aviation_data
(
  `NTSB_RPRT_NBR` String,
  `ACFT_REGIST_NBR` Nullable(String),
  `ACFT_SERIAL_NBR` Nullable(String),
  `EV_TYPE_DESC` String,
  `EVENT_LCL_DATE` Date,
  `LOC_STATE_CODE_STD` Nullable(String),
  `ARPT_NAME_STD` Nullable(String),
  `FLTCNDCT_DESC` Nullable(String),
  `OPRTR_SCHED_DESC` Nullable(String),
  `OPRTR_NSDC_NAME_STD` Nullable(String),
  `ACFT_NSDC_MAKE_STD` Nullable(String),
  `ACFT_NSDC_MODEL_STD` Nullable(String),
  `ACFT_NSDC_SERIES_STD` Nullable(String),
  `REPORT_STATUS` Nullable(String),
  `INJURY_DESC` Nullable(String),
  `FLIGHT_PHASE_DESC` Nullable(String)
)
ENGINE = MergeTree()
ORDER BY sipHash64(NTSB_RPRT_NBR)
SAMPLE BY sipHash64(NTSB_RPRT_NBR);

CREATE TABLE aviation.world_aircraft_accident_summary
(
  `WAASSubsetEventId` String,
  `LocalEventDate` Date,
  `Aircraft` String,
  `AircraftOperator` String,
  `EventLocation` String,
  `CrewFatalities` UInt16,
  `CrewInjured` UInt16,
  `CrewAboard` UInt16,
  `PAXFatalities` UInt16,
  `PAXInjuries` UInt16,
  `PAXAboard` UInt16
)
ENGINE = MergeTree()
ORDER BY sipHash64(WAASSubsetEventId)
SAMPLE BY sipHash64(WAASSubsetEventId);
