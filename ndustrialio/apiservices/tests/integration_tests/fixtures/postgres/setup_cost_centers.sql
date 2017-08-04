INSERT INTO cost_centers(name, descriptor, facility_id, activity_start) VALUES
('test_cost_center_name_1', 'test_cost_center_descriptor_1', 1, '2000-12-08 04:05:06'),
('test_cost_center_name_2', 'test_cost_center_descriptor_2', 1, '2000-13-08 04:05:06'),
('test_cost_center_name_3', 'test_cost_center_descriptor_3', 2, '2000-14-08 04:05:06'),
('test_cost_center_name_4', 'test_cost_center_descriptor_4', 3, '2000-15-08 04:05:06');

INSERT INTO attributes(is_default, name, type, units) VALUES
(TRUE, 'test_attribute_name_1', 'test_attribute_type_1', 'test_attribute_units_1');