CREATE TABLE output_data_by_field_minutely (event_time timestamp PRIMARY KEY, year int, value int, output_id int, field text);
INSERT INTO output_data_by_field_minutely (event_time, year, value, output_id, field) VALUES ('2015-01-20T12:00:00.000Z', 2015, 50, 1, 'test_name_1');
INSERT INTO output_data_by_field_minutely (event_time, year, value, output_id, field) VALUES ('2015-02-20T12:00:00.000Z', 2015, 50, 1, 'test_name_1');
INSERT INTO output_data_by_field_minutely (event_time, year, value, output_id, field) VALUES ('2015-03-20T12:00:00.000Z', 2015, 50, 1, 'test_name_2');
CREATE TABLE unprovisioned_data (event_time timestamp PRIMARY KEY, date text, year int, value int, feed_key text, field_descriptor text);
INSERT INTO unprovisioned_data (event_time, date, year, value, feed_key, field_descriptor) VALUES ('2015-01-20T12:00:00.000Z', '2015-01', 2015, 50, 'test_key_1', 'test_descriptor_1');
INSERT INTO unprovisioned_data (event_time, date, year, value, feed_key, field_descriptor) VALUES ('2015-02-20T12:00:00.000Z', '2015-02', 2015, 50, 'test_key_1', 'test_descriptor_1');
INSERT INTO unprovisioned_data (event_time, date, year, value, feed_key, field_descriptor) VALUES ('2015-03-20T12:00:00.000Z', '2015-03', 2015, 50, 'test_key_2', 'test_descriptor_2');