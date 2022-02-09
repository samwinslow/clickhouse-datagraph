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
