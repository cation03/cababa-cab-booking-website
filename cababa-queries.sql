USE cababa;

-- Adding column of driver email in vehicles
ALTER TABLE vehicles ADD COLUMN d_email VARCHAR(255) NOT NULL;

-- Deleting an entry from driver based on email
delete from drivers where driver_email = "sdamore@yahoo.com";

-- Selecting the tuple from driver based on email
select * from drivers where driver_email = "sdamore@yahoo.com";

-- Adding foreign key constraint on d_email in rides
ALTER TABLE vehicles ADD CONSTRAINT 
driver_key FOREIGN KEY (d_email) REFERENCES drivers(driver_email);

-- Showing one to one mapping between drivers and vehicles
SELECT reg_no, vname, type_id,driver_email,
    first_name, last_name, phone_number, passkey, current_status,
    total_trips, rated_trips, net_rating_sum, final_rating FROM vehicles JOIN drivers
    ON drivers.driver_email = vehicles.d_email;

-- Showing the ride history of a user from latest to oldest 
SELECT * FROM rides WHERE u_email = "berta_magana@gmail.com" AND ongoing IS NULL ORDER BY drop_time DESC;

-- Selecting 10 user emails from user table
select user_email from users limit 10;

-- Inserting a tuple in users
INSERT INTO users (user_email, first_name, last_name, phno, pswd) VALUES 
('alaska345@gmail.com', 'Alaska', 'Young', 7428731999, 'abcdef123');

-- CONSTRAINT DEMOSTRATION - Gives error as email is same
INSERT INTO users (user_email, first_name, last_name, phno, pswd) VALUES 
('alaska345@gmail.com', 'Beatrice', 'Dou', 7428731349, 'qwerty123');

-- CONSTRAINT DEMOSTRATION - Gives error as phone number is same
INSERT INTO users (user_email, first_name, last_name, phno, pswd) VALUES 
('laraj@gmail.com', 'Lara', 'Jean', 7428731999, 'lj@123');

-- Updating user status to ONGOING when in a ride
UPDATE users SET current_status = "ONGOING" WHERE user_email = "berta_magana@gmail.com";

-- Updating user status to IDLE when in a ride finishes
UPDATE users SET current_status = "IDLE" WHERE user_email = "berta_magana@gmail.com";

-- CONSTRAINT DEMOSTRATION - Gives error as phone number is same
INSERT INTO drivers (first_name, last_name, driver_email, phone_number, passkey)
VALUES  ('Richard', 'Sanchez', 'richards2@hotmail.com', 1000000499, 'kEAwSmGJXMhlvlMcXn');

-- CONSTRAINT DEMOSTRATION - Gives error as phone number is less than 10 digits
INSERT INTO drivers (first_name, last_name, driver_email, phone_number, passkey)
VALUES  ('Richard', 'Sanchez', 'richards2@hotmail.com', 10499, 'kEAwSmGJXMhlvlMcXn');

-- Displaying relationship between vehicles and vehicles_type
SELECT reg_no, vname, d_email, vehicles.type_id, vehicle_type, seating,
fuel_type FROM vehicles JOIN vehicle_types ON vehicles.type_id = vehicle_types.type_id;

-- Displaying count of vehicles of each type
SELECT COUNT(*) from vehicles GROUP BY type_id;

-- Displaying the most recent ride of a user
SELECT * from rides where u_email = "berta_magana@gmail.com" ORDER BY pickup_time DESC limit 1;

-- Displaying all ongoing rides 
SELECT * from rides where ongoing IS NOT NULL;

-- Inserting an ongoing ride in rides table
INSERT INTO rides (receipt_no, pickup_time,pickup_loc, drop_time, drop_loc, 
vehicle_no, d_email, u_email, distance, fare, ongoing) VALUES('2#kathleen4@hotmail.com', '2022-01-17 06:00:00', '23 East Princeton Avenue North Tonawanda, NY 14120', '2022-01-17 07:00:00', '8072 Fifth Ave. Odenton, MD 21113', 
'CH14CN1966', 'avis72@hotmail.com', 'kathleen4@hotmail.com', 47, 564, 1);

-- CONSTRAINT DEMOSTRATION - Gives error as same user cannot have another ongoing ride
INSERT INTO rides (receipt_no, pickup_time,pickup_loc, drop_time, drop_loc, 
vehicle_no, d_email, u_email, distance, fare, ongoing) VALUES('3#kathleen4@hotmail.com', '2022-01-17 06:00:00', '23 East Princeton Avenue North Tonawanda, NY 14120', '2022-01-17 07:00:00', '8072 Fifth Ave. Odenton, MD 21113', 
'CH14CN1966', 'avis72@hotmail.com', 'kathleen4@hotmail.com', 47, 564, 1);

-- Updating driver status to UNAVILABLE based on email
UPDATE drivers SET current_status = "UNAVAILABLE" WHERE driver_email = "avis72@hotmail.com";

-- Adding constraint in rides table to ensure unique entries during ongoing trips
ALTER TABLE rides ADD CONSTRAINT unique_driver UNIQUE (d_email, ongoing);
ALTER TABLE rides ADD CONSTRAINT unique_user UNIQUE (u_email, ongoing);
ALTER TABLE rides ADD CONSTRAINT unique_vehicle UNIQUE (vehicle_no, ongoing);

-- CONSTRAINT DEMOSTRATION - Gives error as same user cannot have another ongoing ride
INSERT INTO rides (receipt_no, pickup_time,pickup_loc, drop_time, drop_loc, 
vehicle_no, d_email, u_email, distance, fare, ongoing) VALUES('3#kathleen4@hotmail.com', '2022-01-17 06:00:00', '23 East Princeton Avenue North Tonawanda, NY 14120', '2022-01-17 07:00:00', '8072 Fifth Ave. Odenton, MD 21113', 
'CH14CN1966', 'pbartoletti@hotmail.com', 'kathleen4@hotmail.com', 47, 564, 1);


-- alter table to set default value of ongoing to 0
ALTER TABLE rides ALTER COLUMN ongoing SET default 0;
-- get all the rides of a driver on a particular day
SELECT * FROM rides WHERE d_email = 'cronin.allie@yahoo.com' AND pickup_time > '2022-02-24 00:00:00' AND pickup_time < '2022-02-24 23:59:59';
-- get the drivers net earnings on a particular day
SELECT SUM(fare) FROM rides WHERE d_email = 'cronin.allie@yahoo.com' AND pickup_time > '2022-02-24 00:00:00' AND pickup_time < '2022-02-24 23:59:59';
-- change user's name
UPDATE users
SET first_name = 'Saruru', last_name = "Ruru"
WHERE user_email = 'daniel.mata68@hotmail.com';
-- change user's password
UPDATE users
SET pswd = 'hellomina'
WHERE user_email = 'daniel.mata68@hotmail.com';
-- change user's phone number
UPDATE users
SET phno = 1753405215
WHERE user_email = 'daniel.mata68@hotmail.com';
-- select ongoing trips
SELECT * FROM rides where ongoing = 1;
-- start the current trip
UPDATE rides
SET ongoing = 1
WHERE d_email = 'cronin.allie@yahoo.com' 
AND pickup_time > '2022-02-24 00:00:00' AND pickup_time < '2022-02-24 23:59:59';
SELECT * FROM rides where ongoing = 1;
-- insert into drivers
INSERT INTO drivers (first_name, last_name, driver_email, phone_number, passkey)
VALUE ('Viks', 'Yajeet', 'mehul@hotmail.com', 6969696969, 'vivi123');
-- add constraint that pickup time should be before the drop-off time
ALTER TABLE rides
ADD CONSTRAINT check_time CHECK (pickup_time < drop_time);
-- add constraint that rated_trips should be less than or equal to total trips
ALTER TABLE drivers
ADD CONSTRAINT check_trip_count CHECK (rated_trips <= total_trips);
-- select 1 vehicle for user based on vehicle type from the available vehicle types
SELECT * FROM vehicles WHERE type_id = 5 LIMIT 1;
-- add driver rating
UPDATE drivers
SET net_rating_sum = net_rating_sum + 4
WHERE driver_email = 'mehul@hotmail.com';
-- SELECT * FROM drivers WHERE driver_email = 'mehul@hotmail.com';
-- update total trip count
UPDATE drivers
SET total_trips = total_trips + 2
WHERE driver_email = 'mehul@hotmail.com';
-- update rated trip count
UPDATE drivers
SET rated_trips = rated_trips + 1
WHERE driver_email = 'mehul@hotmail.com';
-- update final rating
UPDATE drivers SET final_rating = net_rating_sum/rated_trips;
-- calculate fare
UPDATE rides SET fare = distance*10;
-- SELECT * FROM drivers;
DESCRIBE drivers;
DESCRIBE rides;
DESCRIBE rides;
DESCRIBE admins;
DESCRIBE users;
DESCRIBE vehicles;
DESCRIBE vehicle_types;


