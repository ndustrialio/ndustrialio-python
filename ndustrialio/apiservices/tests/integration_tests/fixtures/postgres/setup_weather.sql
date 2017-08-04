INSERT INTO weather_locations(city, state, search_key) VALUES
('Raleigh', 'NC', 'Ral'),
('Durham', 'NC', 'Dur');

INSERT INTO weather_forecasts(weather_location_id, forecast_high, forecast_low, forecast_conditions, date) VALUES
(1, 70, 60, 'Cloudy', '2000-12-08'),
(1, 80, 50, 'Sunny', '2000-13-08'),
(2, 40, 30, 'Partly Cloudy', '2000-14-08');