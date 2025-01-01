CREATE TABLE IF NOT EXISTS airplane (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
base_weight INTEGER,
fuel_per_km INTEGER,
runway_length INTEGER,
food_per_passenger INTEGER
);


CREATE TABLE IF NOT EXISTS airport (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
runway_length INTEGER
);