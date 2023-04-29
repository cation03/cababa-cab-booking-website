start transaction;
SELECT * FROM users WHERE user_email = 'kamille_kuphal@hotmail.com' AND pswd = 'OmlbxxBl';

SELECT receipt_no FROM rides WHERE u_email = 'kamille_kuphal@hotmail.com' ORDER BY receipt_no DESC LIMIT 1;
SELECT reg_no FROM vehicles WHERE type_id = '1' order by rand() limit 1;
SELECT driver_email FROM drivers where current_status = 'AVAILABLE' ORDER BY RAND() LIMIT 1;
INSERT INTO rides (receipt_no, pickup_time, pickup_loc, drop_time, drop_loc, vehicle_no, d_email, u_email, distance, fare, rating, ongoing) VALUES ('2#kamille_kuphal@hotmail.com', '2018-04-01 12:00:00', 'IIIT Delhi', '2018-04-01 12:30:00', 'IIT Delhi', 'HR14IF9096', 'harmony.steuber@nikolaus.biz', 'kamille_kuphal@hotmail.com', 10, 100, 0, 1);
SAVEPOINT ridebooked;
update rides set ongoing = NULL where u_email = 'kamille_kuphal@hotmail.com';
ROLLBACK TO SAVEPOINT ridebooked;
COMMIT;