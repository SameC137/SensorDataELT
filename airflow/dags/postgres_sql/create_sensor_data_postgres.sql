CREATE TABLE IF NOT EXISTS sensor_data(sense_id BIGSERIAL  PRIMARY KEY,
        date_time TIMESTAMP , station_id INT, col3 FLOAT, col4 FLOAT, col5 FLOAT, col6 FLOAT, col7 FLOAT,
        col8 FLOAT, col9 FLOAT, col10 FLOAT, col11 FLOAT, col12 FLOAT, col13 FLOAT, col14 FLOAT, col15 FLOAT, col16 FLOAT, 
        col17 FLOAT, col18 FLOAT, col19 FLOAT, col20 FLOAT, col21 FLOAT, col22 FLOAT, 
        col23 FLOAT, col24 FLOAT, col25 FLOAT, col26 FLOAT,FOREIGN KEY (station_id)
        REFERENCES station_info(station_id)
        ON DELETE CASCADE);