CREATE DATABASE IF NOT EXISTS aviation;

CREATE TABLE aviation.accidents_incidents_all
(
  `EventId` String,
  `EventDate` Nullable(Date),
  `EventType` String,
  `SourceDataset` String,
  `AgencyReportNumber` String,
  `AgencyReportType` String,
  `AgencyReportDate` Nullable(Date),
  `City` Nullable(String),
  `StateCode` Nullable(String),
  `Country` Nullable(String),
  `Latitude` Nullable(Float64),
  `Longitude` Nullable(Float64),
  `AirportCode` Nullable(String),
  `AirportName` Nullable(String),
  `InjurySeverity` Nullable(String),
  `InjuryFatalCount` Nullable(UInt16),
  `InjurySeriousCount` Nullable(UInt16),
  `InjuryMinorCount` Nullable(UInt16),
  `InjuryUninjuredCount` Nullable(UInt16),
  `AircraftDamageSeverity` Nullable(String),
  `AircraftMake` Nullable(String),
  `AircraftModel` Nullable(String),
  `AircraftSeries` Nullable(String),
  `AircraftAmateurBuilt` Nullable(String),
  `AircraftOperator` Nullable(String),
  `AircraftEngineMake` Nullable(String),
  `AircraftEngineModel` Nullable(String),
  `AircraftEngineGroupCode` Nullable(String),
  `AircraftEngineType` Nullable(String),
  `AircraftEngineCount` Nullable(UInt8),
  `AircraftRegistrationNumber` Nullable(String),
  `AircraftSerialNumber` Nullable(String),
  `FlightType` Nullable(String),
  `FlightConductCode` Nullable(String),
  `FlightPlanFiledCode` Nullable(String),
  `FlightPhase` Nullable(String),
  `FlightWeatherCondition` Nullable(String),
  `PilotCertificateType` Nullable(String),
  `PilotFlightTimeTotal` Nullable(Float64),
  `PilotFlightTimeInType` Nullable(Float64)
)
ENGINE = MergeTree()
ORDER BY sipHash64(EventId)
SAMPLE BY sipHash64(EventId);
