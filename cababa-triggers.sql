DELIMITER #
CREATE TRIGGER driver_availibity 
BEFORE INSERT ON rides 
FOR EACH ROW 
BEGIN 
UPDATE drivers SET current_status = "UNAVAILABLE" 
WHERE driver_email = new.d_email; 
END#
DELIMITER ;

DELIMITER #
CREATE TRIGGER ending_trip
BEFORE UPDATE ON rides 
FOR EACH ROW 
BEGIN
IF NEW.ongoing = 1 THEN
UPDATE drivers 
SET current_status = 'AVAILABLE', total_trips = total_trips + 1 
WHERE driver_email = NEW.d_email; 
END IF;
END#
DELIMITER ;


DELIMITER #
CREATE TRIGGER ratings_update
BEFORE UPDATE ON rides 
FOR EACH ROW 
BEGIN
IF NEW.rating > 0 THEN
UPDATE drivers 
SET rated_trips = rated_trips + 1, net_rating_sum = net_rating_sum + NEW.rating,
final_rating = net_rating_sum/rated_trips, total_trips = total_trips + 1
WHERE driver_email = NEW.d_email; 
END IF;
END#
DELIMITER ;

DELIMITER #
CREATE TRIGGER settings_update
BEFORE UPDATE ON users 
FOR EACH ROW 
BEGIN 
DELETE FROM rides 
WHERE u_email = OLD.user_email; 
END#
DELIMITER ;

