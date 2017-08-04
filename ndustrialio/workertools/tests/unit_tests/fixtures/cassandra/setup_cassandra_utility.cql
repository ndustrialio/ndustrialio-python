CREATE TABLE output_data_by_field_latest(output_id int, event_time timestamp primary key, field text);
INSERT INTO output_data_by_field_latest(output_id, event_time, field) VALUES (1, '2015-01-20T01:00:00.000Z', 'test_field_1');
INSERT INTO output_data_by_field_latest(output_id, event_time, field) VALUES (1, '2015-01-20T02:00:00.000Z', 'test_field_2');
INSERT INTO output_data_by_field_latest(output_id, event_time, field) VALUES (1, '2015-01-20T03:00:00.000Z', 'test_field_2');
INSERT INTO output_data_by_field_latest(output_id, event_time, field) VALUES (2, '2015-01-20T04:00:00.000Z', 'test_field_3');
INSERT INTO output_data_by_field_latest(output_id, event_time, field) VALUES (2, '2015-01-10T01:00:00.000Z', 'test_field_1');
INSERT INTO output_data_by_field_latest(output_id, event_time, field) VALUES (3, '2015-01-20T05:00:00.000Z', 'test_field_3');
INSERT INTO output_data_by_field_latest(output_id, event_time, field) VALUES (3, '2015-01-20T06:00:00.000Z', 'test_field_4');

CREATE TABLE output_data_by_field_minutely(output_id int, field text, value float, event_time timestamp, year text, primary key (field, event_time));
INSERT INTO output_data_by_field_minutely(output_id, field, value, event_time, year) VALUES (1, 'test_field_1', 1.5, '2015-02-20T01:00:00.000Z', '2015');
INSERT INTO output_data_by_field_minutely(output_id, field, value, event_time, year) VALUES (2, 'test_field_2', 2.3, '2015-03-20T01:00:00.000Z', '2015');
INSERT INTO output_data_by_field_minutely(output_id, field, value, event_time, year) VALUES (2, 'test_field_2', 3.4, '2015-04-20T01:00:00.000Z', '2015');
INSERT INTO output_data_by_field_minutely(output_id, field, value, event_time, year) VALUES (2, 'test_field_3', 4.7, '2015-05-20T01:00:00.000Z', '2015');
INSERT INTO output_data_by_field_minutely(output_id, field, value, event_time, year) VALUES (3, 'test_field_4', 5.2, '2015-06-20T01:00:00.000Z', '2015');
INSERT INTO output_data_by_field_minutely(output_id, field, value, event_time, year) VALUES (3, 'test_field_5', 6.8, '2015-07-20T01:00:00.000Z', '2015');