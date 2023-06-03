USE [Wildcats]

:setvar SqlSamplesSourceDataPath "C:\Users\varun\OneDrive\Desktop\Wildcats\SQL Tables\"

:setvar DatabaseName "Wildcats"

--create statements

Create Table DimPlayer
(
[Name] varchar(50),
[Height (inches)] int,
[Weight (lbs)] int,
BirthCity varchar(50),
DraftStatus varchar(100),
Nationality varchar(100),
[Player Type] varchar(50),
PlayerID int primary key,
[Image] varchar(max),
Age int
)

Create Table DimPosition
(
PositionID int primary key,
Position varchar(2),
[Name] varchar(20)
)

Create Table DimTeam
(
TeamID int primary key,
Team varchar(4),
[Name] varchar(30)
)

Create Table DimClass
(
ClassID varchar(5) primary key,
[Name] varchar(100)
)

Create Table DimSeason
(
Season int primary key
)

Create Table FactTotals
(
SerialNumber int primary key,
GP int,
[MIN] float,
PTS	int,
FGM int,
FGA int,
[FG%] float,
_3PM int,
_3PA	int,
[_3P%]	float,
FTM int,
FTA int,
[FT%] float,
ORB	int,
DRB	int,
REB	int,
AST	int,
STL	int,
BLK	int,
TOV	int,
PF int,
Season int,
TeamID int,
PositionID int,
PlayerID int
)

Create Table FactAverages
(
SerialNumber int primary key,
GP int,
MPG float,
PPG	float,
FGM float,
FGA float,
[FG%] float,
_3PM float,
_3PA float,
[_3P%] float,
FTM float,
FTA float,
[FT%] float,
ORB	float,
DRB	float,
RPG	float,
APG	float,
SPG	float,
BPG	float,
TOV	float,
PF float,
Season int,
TeamID int,
PositionID int,
PlayerID int
)

Create Table FactAdvancedStats
(
SerialNumber int primary key,
[TS%] float,
[eFG%] float,
[Total S %] float,
[ORB%] float,
[DRB%] float,
[TRB%] float,
[AST%] float,
[TOV%] float,
[STL%] float,
[BLK%] float,
[USG%] float,
PPR	float,
PPS	float,
ORtg float,
DRtg float,
eDiff float,
FIC	float,
PER	float,
Season int,
TeamID int,
PositionID int,
PlayerID int
)

Create Table FactPerMinute
(
SerialNumber int primary key,
GP int,
[MIN] float,
PTS	float,
FGM float,
FGA float,
[FG%] float,
_3PM float,
_3PA	float,
[_3P%]	float,
FTM float,
FTA float,
[FT%] float,
ORB	float,
DRB	float,
REB	float,
AST	float,
STL	float,
BLK	float,
TOV	float,
PF float,
Season int,
TeamID int,
PositionID int,
PlayerID int
)

Create Table FactSalary
(
SerialNumber int primary key,
PlayerID int,
TeamID int,
ClassID varchar(10),
ContractValue float,
PlayerValue float,
SalaryCap float,
Season int
)

--insert statements

BULK INSERT [dbo].[DimPlayer] FROM '$(SqlSamplesSourceDataPath)DimPlayer.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

BULK INSERT [dbo].[DimTeam] FROM '$(SqlSamplesSourceDataPath)DimTeam.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

BULK INSERT [dbo].[DimClass] FROM '$(SqlSamplesSourceDataPath)DimClass.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

BULK INSERT [dbo].[DimSeason] FROM '$(SqlSamplesSourceDataPath)DimSeason.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

BULK INSERT [dbo].[FactTotals] FROM '$(SqlSamplesSourceDataPath)TotalsFact.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

BULK INSERT [dbo].[FactAverages] FROM '$(SqlSamplesSourceDataPath)AveragesFact.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

BULK INSERT [dbo].[FactAdvancedStats] FROM '$(SqlSamplesSourceDataPath)AdvancedStatsFact.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

BULK INSERT [dbo].[FactPerMinute] FROM '$(SqlSamplesSourceDataPath)PerMinuteFact.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

BULK INSERT [dbo].[FactSalary] FROM '$(SqlSamplesSourceDataPath)Salary2023Fact.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

--create relationships

AlTER TABLE FactTotals ADD CONSTRAINT 
FK_TeamID FOREIGN KEY (TeamID) REFERENCES DimTeam(TeamID);
AlTER TABLE FactTotals ADD CONSTRAINT 
FK_PositionID FOREIGN KEY (PositionID) REFERENCES DimPosition(PositionID);
AlTER TABLE FactTotals ADD CONSTRAINT 
FK_PlayerID FOREIGN KEY (PlayerID) REFERENCES DimPlayer(PlayerID);

AlTER TABLE FactAverages ADD CONSTRAINT 
FK_TeamID_Av FOREIGN KEY (TeamID) REFERENCES DimTeam(TeamID);
AlTER TABLE FactAverages ADD CONSTRAINT 
FK_PositionID_Av FOREIGN KEY (PositionID) REFERENCES DimPosition(PositionID);
AlTER TABLE FactAverages ADD CONSTRAINT 
FK_PlayerID_Av FOREIGN KEY (PlayerID) REFERENCES DimPlayer(PlayerID);

AlTER TABLE FactAdvancedStats ADD CONSTRAINT 
FK_TeamID_Ad FOREIGN KEY (TeamID) REFERENCES DimTeam(TeamID);
AlTER TABLE FactAdvancedStats ADD CONSTRAINT 
FK_PositionID_Ad FOREIGN KEY (PositionID) REFERENCES DimPosition(PositionID);
AlTER TABLE FactAdvancedStats ADD CONSTRAINT 
FK_PlayerID_Ad FOREIGN KEY (PlayerID) REFERENCES DimPlayer(PlayerID);

AlTER TABLE FactPerMinute ADD CONSTRAINT 
FK_TeamID_PM FOREIGN KEY (TeamID) REFERENCES DimTeam(TeamID);
AlTER TABLE FactPerMinute ADD CONSTRAINT 
FK_PositionID_PM FOREIGN KEY (PositionID) REFERENCES DimPosition(PositionID);
AlTER TABLE FactPerMinute ADD CONSTRAINT 
FK_PlayerID_PM FOREIGN KEY (PlayerID) REFERENCES DimPlayer(PlayerID);

AlTER TABLE FactSalary ADD CONSTRAINT 
FK_TeamID_Sal FOREIGN KEY (TeamID) REFERENCES DimTeam(TeamID);
AlTER TABLE FactSalary ADD CONSTRAINT 
FK_PlayerID_Sal FOREIGN KEY (PlayerID) REFERENCES DimPlayer(PlayerID);
AlTER TABLE FactSalary ADD CONSTRAINT 
FK_SeasonID_Sal FOREIGN KEY (Season) REFERENCES DimSeason(Season);

AlTER TABLE FactAdvancedStats ADD CONSTRAINT 
FK_SeasonIDAd FOREIGN KEY (Season) REFERENCES DimSeason(Season);
AlTER TABLE FactAverages ADD CONSTRAINT 
FK_SeasonIDAv FOREIGN KEY (Season) REFERENCES DimSeason(Season);
AlTER TABLE FactPerMinute ADD CONSTRAINT 
FK_SeasonIDPM FOREIGN KEY (Season) REFERENCES DimSeason(Season);
AlTER TABLE FactTotals ADD CONSTRAINT 
FK_SeasonIDTo FOREIGN KEY (Season) REFERENCES DimSeason(Season);