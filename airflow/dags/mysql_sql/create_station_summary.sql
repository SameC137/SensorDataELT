CREATE TABLE IF NOT EXISTS station_summary(
    summary_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    station_id INT,flow_99 FLOAT,flow_max FLOAT,flow_median FLOAT,flow_total FLOAT,n_obs INT, FOREIGN KEY (station_id)
        REFERENCES station_info(station_id)
        ON DELETE CASCADE);
        