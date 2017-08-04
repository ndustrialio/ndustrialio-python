INSERT INTO utility_providers(id, label, created_at, updated_at) VALUES
(1, 'test_utility_label_1', '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
(2, 'test_utility_label_2', '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
(3, 'test_utility_label_3', '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
(4, 'test_utility_label_4', '1999-01-08 04:05:06', '1999-01-08 04:05:06');

INSERT INTO rate_schedules(label, rate_schedule_type_id, utility_provider_id, is_rtp_rate, is_published, created_at, updated_at) VALUES
('test_schedule_label_1', 1, 1, TRUE, FALSE, '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
('test_schedule_label_2', 1, 2, TRUE, TRUE, '1999-01-09 04:05:06', '1999-01-09 04:05:06'),
('test_schedule_label_3', 2, 2, FALSE, FALSE, '1999-01-10 04:05:06', '1999-01-10 04:05:06'),
('test_schedule_label_4', 3, 2, TRUE, FALSE, '1999-01-11 04:05:06', '1999-01-11 04:05:06'),
('test_schedule_label_4', 4, 3, FALSE, TRUE, '1999-01-12 04:05:06', '1999-01-12 04:05:06');

INSERT INTO rate_periods(id, rate_schedule_id, title, period_start, period_end, is_forecast, created_at, updated_at) VALUES
(1, 1, 'test_period_title_1', '2000-01-08 04:05:06', '2000-12-08 04:05:06', TRUE, '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
(2, 1, 'test_period_title_2', '2001-03-08 04:05:06', '2001-04-08 04:05:06', FALSE, '1999-02-08 04:05:06', '1999-02-08 04:05:06'),
(3, 2, 'test_period_title_3', '2000-05-08 04:05:06', '2000-10-08 04:05:09', TRUE, '1999-03-08 04:05:06', '1999-03-08 04:05:06'),
(4, 3, 'test_period_title_4', '2000-07-08 04:05:06', '2000-08-08 04:05:06', TRUE, '1999-04-08 04:05:06', '1999-04-08 04:05:06'),
(5, 3, 'test_period_title_5', '2000-09-08 04:05:06', '2000-10-08 04:05:06', TRUE, '1999-05-08 04:05:06', '1999-05-08 04:05:06'),
(6, 4, 'test_period_title_6', '2000-11-08 04:05:06', '2000-11-10 04:05:06', FALSE, '1999-06-08 04:05:06', '1999-06-08 04:05:06');

INSERT INTO rate_period_rates(id, rate_period_id, rate_start, rate_end, rate, created_at, updated_at) VALUES
(1, 1, '2000-03-08 04:05:06', '2000-5-08 04:05:06', 10.0, '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
(2, 1, '2000-06-08 04:05:06', '2000-8-08 04:05:06', 7.3, '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
(3, 2, '2001-03-08 04:05:06', '2001-04-08 04:05:06', 8.6, '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
(4, 3, '2000-05-08 04:05:06', '2000-07-08 04:05:09', 4.1, '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
(5, 3, '2000-07-08 04:05:10', '2000-09-08 04:05:09', 11.1, '1999-01-08 04:05:06', '1999-01-08 04:05:06'),
(6, 5, '2000-09-08 04:05:06', '2000-08-25 04:05:06', 6.4, '1999-01-08 04:05:06', '1999-01-08 04:05:06');

INSERT INTO energy_seasons(rate_schedule_id, season_name, start_month, start_day, end_month, end_day) VALUES
(1, 'test_energy_season_name_1', 1, 1, 2, 2),
(1, 'test_energy_season_name_2', 3, 3, 4, 4),
(2, 'test_energy_season_name_3', 5, 5, 6, 6),
(3, 'test_energy_season_name_4', 7, 7, 8, 8);

INSERT INTO energy_season_periods(energy_season_id, day_of_week_start, hour_start, minute_start, day_of_week_end, hour_end, minute_end, period_name) VALUES
(1, 1, 1, 1, 2, 2, 2, 'test_energy_period_1'),
(2, 2, 2, 2, 3, 3, 3, 'test_energy_period_2'),
(3, 3, 3, 3, 4, 4, 4, 'test_energy_period_3'),
(3, 4, 4, 4, 5, 5, 5, 'test_energy_period_4'),
(4, 5, 5, 5, 6, 6, 6, 'test_energy_period_5');

INSERT INTO demand_seasons(rate_schedule_id, season_type, season_name, start_month, start_day, end_month, end_day) VALUES
(1, 'tou', 'test_demand_season_name_1', 1, 1, 2, 2),
(1, 'flat', 'test_demand_season_name_2', 2, 2, 3, 3),
(2, 'tou', 'test_demand_season_name_3', 3, 3, 4, 4),
(2, 'tou', 'test_demand_season_name_4', 4, 4, 5, 5),
(3, 'flat', 'test_demand_season_name_5', 5, 5, 6, 6),
(3, 'tou', 'test_demand_season_name_6', 6, 6, 7, 7);

INSERT INTO demand_season_periods(demand_season_id, day_of_week_start, hour_start, minute_start, day_of_week_end, hour_end, minute_end, period_name) VALUES
(1, 1, 1, 1, 2, 2, 2, 'test_demand_period_1'),
(2, 2, 2, 2, 3, 3, 3, 'test_demand_period_2'),
(3, 3, 3, 3, 4, 4, 4, 'test_demand_period_3'),
(3, 4, 4, 4, 5, 5, 5, 'test_demand_period_4'),
(6, 5, 5, 5, 6, 6, 6, 'test_demand_period_5');