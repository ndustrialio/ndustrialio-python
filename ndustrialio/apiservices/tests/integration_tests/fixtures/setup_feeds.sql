INSERT INTO feed_types(type, down_after) VALUES
('test_feed_type', 60);

INSERT INTO feeds(status, feed_type_id, key, facility_id, timezone, routing_keys, token, degraded_threshold, critical_threshold, created_at, updated_at) VALUES
('Active', 1, 'key_1', 10, 'UTC', '[routing_key_1]', 'token_1', 0.8, 0.2, '1999-01-08 04:05:06', '2000-01-08 04:05:06'),
('Active', 1, 'key_2', 20, 'UTC', '[routing_key_2]', 'token_2', 0.8, 0.2, '1999-02-08 04:05:06', '2000-02-08 04:05:06'),
('Active', 1, 'key_3', 30, 'UTC', '[routing_key_3]', 'token_3', 0.8, 0.2, '1999-03-08 04:05:06', '2000-03-08 04:05:06'),
('Active', 1, 'key_4', 40, 'UTC', '[routing_key_4]', 'token_4', 0.8, 0.2, '1999-04-08 04:05:06', '2000-04-08 04:05:06'),
('Active', 1, 'key_5', 50, 'UTC', '[routing_key_5]', 'token_5', 0.8, 0.2, '1999-05-08 04:05:06', '2000-05-08 04:05:06'),
('Active', 1, 'key_6', 60, 'UTC', '[routing_key_6]', 'token_6', 0.8, 0.2, '1999-06-08 04:05:06', '2000-06-08 04:05:06'),
('Active', 1, 'key_7', 70, 'UTC', '[routing_key_7]', 'token_7', 0.8, 0.2, '1999-07-08 04:05:06', '2000-07-08 04:05:06');

INSERT INTO output_types(type, category) VALUES
('test_output_type', 'test_output_category');

INSERT INTO outputs(feed_id, label, output_type_id, facility_id, created_at, updated_at) VALUES
(1, 'test_label_1', 1, 20, '1999-01-08 04:05:06', '2000-01-08 04:05:06'),
(1, 'test_label_2', 1, 20, '1999-01-08 04:05:06', '2000-01-08 04:05:06'),
(2, 'test_label_3', 1, 20, '1999-01-08 04:05:06', '2000-01-08 04:05:06');


INSERT INTO output_fields(output_id, field_descriptor, field_human_name, value_type, feed_key) VALUES
(1, 'test_descriptor_1', 'test_name_1', 'string', 'key_1'),
(1, 'test_descriptor_2', 'test_name_2', 'string', 'key_1'),
(1, 'test_descriptor_3', 'test_name_3', 'string', 'key_1'),
(1, 'test_descriptor_4', 'test_name_4', 'string', 'key_2');
