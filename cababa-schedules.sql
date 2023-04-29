--transaction 1
t1r1: select * from rides where u_email = 'kamille_kuphal@hotmail.com';
t1w1: INSERT INTO rides (receipt_no, pickup_time, pickup_loc, drop_time, drop_loc, vehicle_no, d_email, u_email, distance, fare, rating, ongoing) VALUES ('3#kamille_kuphal@hotmail.com', '2018-04-01 12:00:00', 'IIIT Delhi', '2018-04-01 12:30:00', 'IIT Delhi', 'HR14IF9096', 'harmony.steuber@nikolaus.biz', 'kamille_kuphal@hotmail.com', 10, 100, 0, 1);
t1w2: update rides set ongoing = NULL where u_email = 'kamille_kuphal@hotmail.com';

--transaction 2
t2r1: select * from rides where u_email = 'krystina_fay@hotmail.com';
t2w1: INSERT INTO rides (receipt_no, pickup_time, pickup_loc, drop_time, drop_loc, vehicle_no, d_email, u_email, distance, fare, rating, ongoing) VALUES ('2#krystina_fay@hotmail.com', '2018-04-01 12:00:00', 'IIIT Delhi', '2018-04-01 12:30:00', 'IIT Delhi', 'HR14IF9096', 'harmony.steuber@nikolaus.biz', 'krystina_fay@hotmail.com', 10, 100, 0, 1);
t2w2: update rides set ongoing = NULL where u_email = 'krystina_fay@hotmail.com';

-- no conflict -> non conflict serializable

--schedule 1
t1r1, t1w1, t1w2, t2r1, t2w1, t2w2

--schedule 2
t2r1, t1r1, t1w2, t2w1, t2w2, t1w1

--transaction 3
t3wa1: update users set first_name = 'kam' where user_email = 'kamille_kuphal@hotmail.com';
t3ra1: select * from users where u_email = 'kamille_kuphal@hotmail.com';
t3wa2: update users set pswd = 'abcdefgh' where user_email = 'kamille_kuphal@hotmail.com';
t3ra2: select * from users where u_email = 'kamille_kuphal@hotmail.com';

--transaction 4
t4rb: select * from rides where u_email = 'kamille_kuphal@hotmail.com';
t4wa: update users set last_name = 'kuphal' where user_email = 'kamille_kuphal@hotmail.com';

--schedule 1 - Not confict serializable
t3wa1, t3ra1, t4rb, t4wa, t3wa2, t3ra2

--schedule 2 - conflict serializable
t3wa1, t3ra1, t4rb, t3wa2, t3ra2, t4wa

--transaction 5
t5wa: INSERT INTO rides (receipt_no, pickup_time, pickup_loc, drop_time, drop_loc, vehicle_no, d_email, u_email, distance, fare, rating, ongoing) VALUES ('2#kamille_kuphal@hotmail.com', '2018-04-01 12:00:00', 'IIIT Delhi', '2018-04-01 12:30:00', 'IIT Delhi', 'HR14IF9096', 'harmony.steuber@nikolaus.biz', 'kamille_kuphal@hotmail.com', 10, 100, 0, 1);
t5ra1: select * from rides where u_email = 'kamille_kuphal@hotmail.com';
t5wb: update drivers set driver_availibity = 'UNAVAILABLE' where driver_email = 'harmony.steuber@nikolaus.biz';
t5ra2: select * from rides where u_email = 'kamille_kuphal@hotmail.com';

--transaction 6
t6wb: update drivers set total_trips = total_trips + 1 where driver_email = 'harmony.steuber@nikolaus.biz';
t6wa: update rides set ongoing = NULL where u_email = 'kamille_kuphal@hotmail.com';
t6ra: select * from rides where u_email = 'kamille_kuphal@hotmail.com' and ongoing is NULL order by drop time desc limit 1;
t6rb: select * from drivers where driver_email = 'harmony.steuber@nikolaus.biz';

--schedule 1 - conflict serializable
t6wb, t6wa, t6ra, t5wa, t5ra1, t6rb, t5wb, t5ra2

--schedule 2 - non conflict serializable
t6wb, t5wa, t5ra1, t6wa, t6ra, t5wb, t5ra2, t6rb

