INSERT INTO facilities(name, organization_id) VALUES
('test_facility_1', 'test_organization_1'),
('test_facility_2', 'test_organization_2'),
('test_facility_3', 'test_organization_2'),
('test_facility_4', 'test_organization_3');

INSERT INTO systems(facility_id, name) VALUES
(1, 'test_system_1'),
(1, 'test_system_2'),
(2, 'test_system_3'),
(3, 'test_system_4'),
(3, 'test_system_5');

INSERT INTO zones(system_id, name, label) VALUES
(1, 'test_zone_name_1', 'test_zone_label_1'),
(2, 'test_zone_name_2', 'test_zone_label_2'),
(2, 'test_zone_name_3', 'test_zone_label_3'),
(3, 'test_zone_name_4', 'test_zone_label_4'),
(4, 'test_zone_name_5', 'test_zone_label_5'),
(4, 'test_zone_name_6', 'test_zone_label_6');
