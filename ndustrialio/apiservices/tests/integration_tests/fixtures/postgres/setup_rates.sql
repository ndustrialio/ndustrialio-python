INSERT INTO rate_periods(rate_schedule_id, title, period_start, period_end, is_forecast) VALUES
(1, 'test_title_1', '2000-01-08 04:05:06', '2000-02-08 04:05:06', TRUE),
(1, 'test_title_2', '2000-03-08 04:05:06', '2000-04-08 04:05:06', FALSE),
(2, 'test_title_3', '2000-05-08 04:05:06', '2000-06-08 04:05:06', TRUE),
(3, 'test_title_4', '2000-07-08 04:05:06', '2000-08-08 04:05:06', TRUE),
(3, 'test_title_5', '2000-09-08 04:05:06', '2000-10-08 04:05:06', TRUE),
(4, 'test_title_6', '2000-11-08 04:05:06', '2000-12-08 04:05:06', FALSE);

INSERT INTO rate_schedules(label, rate_schedule_type_id, is_rtp_rate, is_published) VALUES
('test_label_1', 1, TRUE, FALSE),
('test_label_2', 1, TRUE, TRUE),
('test_label_3', 2, FALSE, FALSE),
('test_label_4', 3, TRUE, FALSE),
('test_label_4', 4, TRUE, TRUE);