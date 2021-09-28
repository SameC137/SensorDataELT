LOAD DATA 
INFILE '/var/lib/mysql-files/I80_stations.csv' 
INTO TABLE station_info
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
(station_id,Fwy,Dir,District,County,@vCity,@vState_PM,Abs_PM,Latitude,Longitude,@vLength,Type,Lanes,Name,User_ID_1,User_ID_2,@vUser_ID_3,@vUser_ID_4) 
SET State_PM = NULLIF( @vState_PM, ''),
    User_ID_3 = NULLIF( @vUser_ID_3, ''),
    User_ID_4 = NULLIF( @vUser_ID_4, ''),
    City = NULLIF( @vCity, ''),
    Length = NULLIF( @vLength, '');