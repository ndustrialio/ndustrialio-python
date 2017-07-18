CREATE TABLE IF NOT EXISTS feed_types(type varchar(50), down_after integer);
INSERT IGNORE INTO feed_types(type, down_after) VALUES
('test_type', 60);
CREATE TABLE IF NOT EXISTS feeds(feed_type_id integer, key varchar(20), facility_id integer, timezone varchar(20), routing_keys text, token varchar(100), degraded_threshold float, critical_threshold float, created_at timestamp, updated_at timestamp);
DELETE FROM feeds;
INSERT INTO feeds(feed_type_id, key, facility_id, timezone, routing_keys, token, degraded_threshold, critical_threshold, created_at, updated_at) VALUES
(1, 'key_1', 10, 'UTC', '[routing_key_1]', 'token_1', 0.8, 0.2, '1999-01-08 04:05:06', '2000-01-08 04:05:06'),
(1, 'key_2', 20, 'UTC', '[routing_key_2]', 'token_2', 0.8, 0.2, '1999-02-08 04:05:06', '2000-02-08 04:05:06'),
(1, 'key_3', 30, 'UTC', '[routing_key_3]', 'token_3', 0.8, 0.2, '1999-03-08 04:05:06', '2000-03-08 04:05:06'),
(1, 'key_4', 40, 'UTC', '[routing_key_4]', 'token_4', 0.8, 0.2, '1999-04-08 04:05:06', '2000-04-08 04:05:06'),
(1, 'key_5', 50, 'UTC', '[routing_key_5]', 'token_5', 0.8, 0.2, '1999-05-08 04:05:06', '2000-05-08 04:05:06'),
(1, 'key_6', 60, 'UTC', '[routing_key_6]', 'token_6', 0.8, 0.2, '1999-06-08 04:05:06', '2000-06-08 04:05:06'),
(1, 'key_7', 70, 'UTC', '[routing_key_7]', 'token_7', 0.8, 0.2, '1999-07-08 04:05:06', '2000-07-08 04:05:06');