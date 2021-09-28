DROP TYPE IF EXISTS DirectionENUM CASCADE ;
CREATE TYPE  DirectionENUM AS ENUM('E','W','N','S');
CREATE TABLE IF NOT EXISTS station_info(
    station_id INT NOT NULL PRIMARY KEY,
    Fwy INT,
    Dir DirectionENUM,
    District INT,
    County INT,
    City VARCHAR(255),
    State_PM VARCHAR(255),
    Abs_PM FLOAT,
    Latitude FLOAT,
    Longitude FLOAT,
    Length FLOAT,
    Type VARCHAR(2),
    Lanes INT,
    Name VARCHAR(255),
    User_ID_1 VARCHAR(255),
    User_ID_2 VARCHAR(255),
    User_ID_3 INT DEFAULT NULL,
    User_ID_4 FLOAT);