CREATE TABLE IF NOT EXISTS feeds(feed_type_id integer, key varchar(20), facility_id integer, timezone varchar(20), routing_keys text, token varchar(100), degraded_threshold float, critical_threshold float, created_at timestamp default current_timestamp);
DELETE FROM feeds;