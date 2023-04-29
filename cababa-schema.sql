CREATE DATABASE cababa;
USE cababa;
CREATE TABLE drivers (
	first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    driver_email VARCHAR(255) NOT NULL,
	phone_number BIGINT UNIQUE NOT NULL,
    passkey VARCHAR(50) NOT NULL,
    current_status VARCHAR(50) DEFAULT 'AVAILABLE',
    total_trips INT DEFAULT 1,
    rated_trips INT DEFAULT 1,
    net_rating_sum INT DEFAULT 5,
    final_rating FLOAT DEFAULT 5,
    CONSTRAINT check_status CHECK (current_status = 'AVAILABLE' OR current_status = 'UNAVAILABLE'),
    CONSTRAINT check_phone_number CHECK (phone_number >= 1000000000 AND phone_number <= 9999999999),
    PRIMARY KEY (driver_email)
);

CREATE TABLE admins (
    admin_email VARCHAR(255) NOT NULL,
    admin_passkey VARCHAR(50) NOT NULL,
    username VARCHAR(255) NOT NULL,
    PRIMARY KEY (admin_email)
);

CREATE TABLE vehicle_types (
	type_id INT NOT NULL AUTO_INCREMENT,
	vehicle_type VARCHAR(255) NOT NULL,
	seating INT NOT NULL,
	fuel_type VARCHAR(50) NOT NULL,
	total_vehicle_units INT NOT NULL DEFAULT 20,
	available_vehicle_units INT DEFAULT 20,
	CONSTRAINT check_fuel_type CHECK (fuel_type = 'DIESEL' OR fuel_type = 'PETROL' OR fuel_type = 'CNG' OR fuel_type = 'ELECTRIC'),
	PRIMARY KEY (type_id)
);
CREATE TABLE users(
    user_email VARCHAR(255) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    phno BIGINT NOT NULL UNIQUE,
    pswd VARCHAR(50) NOT NULL,
    current_status VARCHAR(50) DEFAULT 'IDLE',
    CONSTRAINT chk_ph_no check(phno >= 1000000000 and phno <= 9999999999)
);

CREATE TABLE vehicles(
    reg_no VARCHAR(20) PRIMARY KEY,
    vname VARCHAR(50) NOT NULL,
    type_id INT NOT NULL,
    FOREIGN KEY (type_id) REFERENCES vehicle_types(type_id)
);


CREATE TABLE rides(
    receipt_no VARCHAR(255) PRIMARY KEY,
    pickup_time DATETIME NOT NULL,
    pickup_loc VARCHAR(255) NOT NULL,
    drop_time DATETIME NOT NULL,
    drop_loc VARCHAR(255) NOT NULL,
    vehicle_no VARCHAR(20) NOT NULL,
    d_email VARCHAR(255) NOT NULL,
    u_email VARCHAR(255) NOT NULL,
    FOREIGN KEY (vehicle_no) REFERENCES vehicles(reg_no),
    FOREIGN KEY (d_email) REFERENCES drivers(driver_email),
    FOREIGN KEY (u_email) REFERENCES users(user_email),
    distance FLOAT NOT NULL,
    fare INT NOT NULL,
    rating INT DEFAULT 0,
    ongoing INT DEFAULT NULL,
    CONSTRAINT ongoing_trip UNIQUE (d_email,u_email,vehicle_no, ongoing)
);