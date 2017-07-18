CREATE TABLE IF NOT EXISTS feed_types(type varchar(50), down_after integer);
DELETE FROM feed_types;
INSERT INTO feed_types(type, down_after) VALUES
('test_type', 60);
CREATE TABLE IF NOT EXISTS feeds(feed_type_id integer, key varchar(20), facility_id integer, timezone varchar(20), routing_keys text, token varchar(100), degraded_threshold float, critical_threshold float, created_at timestamp, updated_at timestamp);
DELETE FROM feeds;
