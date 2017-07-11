DROP TABLE IF EXISTS feeds;
CREATE TABLE feeds(feed_type_id integer, key varchar(20), facility_id integer, timezone varchar(20), routing_keys text, token varchar(100), degraded_threshold float, critical_threshold float);
INSERT INTO feeds(feed_type_id, key, facility_id, timezone, routing_keys, token, degraded_threshold, critical_threshold) VALUES
(1, 'key_1', 10, 'UTC', 'routing_key_1', 'token_1', 0.8, 0.2),
(2, 'key_2', 20, 'UTC', 'routing_key_2', 'token_2', 0.8, 0.2),
(3, 'key_3', 30, 'UTC', 'routing_key_3', 'token_3', 0.8, 0.2),
(4, 'key_4', 40, 'UTC', 'routing_key_4', 'token_4', 0.8, 0.2),
(5, 'key_5', 50, 'UTC', 'routing_key_5', 'token_5', 0.8, 0.2),
(6, 'key_6', 60, 'UTC', 'routing_key_6', 'token_6', 0.8, 0.2),
(7, 'key_7', 70, 'UTC', 'routing_key_7', 'token_7', 0.8, 0.2);