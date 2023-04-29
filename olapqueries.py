from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector as mc
import random
import datetime
import re

mydb=mc.connect(host="localhost",user="root",passwd="astronaut",database="cababa")

current_user = ''
def signup_mysql(user_email, first_name, last_name, ph, ps):
    mycursor=mydb.cursor()
    data=(user_email, first_name, last_name, ph, ps)
    try:
        sql=("INSERT INTO users (user_email, first_name, last_name, phno, pswd) VALUES (%s, %s, %s, %s, %s)")
        mycursor.execute(sql,data)
        mycursor.execute("commit")
        mycursor.close()
        return 1
    except:
        mycursor.close()
        return 0
    
def display_ride_history(user_email):
    cur = mydb.cursor()
    cur.execute("SELECT * FROM rides WHERE u_email = %s AND ongoing IS NULL ORDER BY drop_time DESC", (user_email,))
    rows = cur.fetchall()
    return rows

def login_mysql(user_email, ps):
    mycursor=mydb.cursor()
    data=(user_email, ps)
    try:
        # check if the user exists in the database
        sql=("SELECT * FROM users WHERE user_email = %s AND pswd = %s")
        mycursor.execute(sql,data)
        # if the user exists, enter the user's email in the current_user dictionary and redirect to the request ride page
        if mycursor.fetchone():
            current_user = user_email
            mycursor.close()
            return 1
        else:
            mycursor.close()
            return 0
    except:
        mycursor.close()
        return 0
    
def olap1():
    cur = mydb.cursor()
    cur.execute("SELECT d_email, YEARWEEK(pickup_time) as week, SUM(distance), AVG(final_rating) as rating FROM rides JOIN drivers ON rides.d_email = drivers.driver_email GROUP BY drivers.final_rating, drivers.first_name, drivers.last_name, drivers.driver_email, week, distance ORDER BY week DESC")
    rows = cur.fetchall()
    return rows

def olap2():
    cur = mydb.cursor()
    cur.execute("""
        SELECT DATE(r.pickup_time) AS ride_date, SUM(fare) AS total_earnings
        FROM rides r
        JOIN vehicles v ON r.vehicle_no = v.reg_no
        JOIN vehicle_types vt ON v.type_id = vt.type_id
        WHERE DATE(r.pickup_time) >= DATE_SUB(NOW(), INTERVAL 4 MONTH)
        GROUP BY ride_date
        ORDER BY ride_date DESC;
    """)

    rows = cur.fetchall()
    return rows

def olap3():
    cur = mydb.cursor()
    cur.execute("""
    SELECT YEAR(pickup_time), pickup_loc, SUM(fare) as fare,
    GROUPING(YEAR(pickup_time)) AS grp_year,
    GROUPING(pickup_loc) AS grp_pickup_loc
    FROM rides
    GROUP BY YEAR(pickup_time), pickup_loc WITH ROLLUP;
    """)
    rows = cur.fetchall()
    return rows
    
def olap4():
    cur = mydb.cursor()
    cur.execute("""
        SELECT drivers.driver_email, drivers.first_name, drivers.last_name, YEAR(pickup_time) as year, SUM(fare) as total_fare, final_rating as rating
        FROM rides
        JOIN drivers ON rides.d_email = drivers.driver_email
        GROUP BY drivers.driver_email, drivers.first_name, drivers.last_name, year, final_rating
        ORDER BY total_fare DESC
        LIMIT 3;
    """)
    rows = cur.fetchall()
    return rows

def trigger1():
    cur = mydb.cursor()
    cur.execute("""
        DELIMITER #
        CREATE TRIGGER driver_availibity 
        BEFORE INSERT ON rides 
        FOR EACH ROW 
        BEGIN ATOMIC
        UPDATE drivers SET current_status = "UNAVAILABLE" 
        WHERE driver_email = new.d_email; 
        END#
        DELIMITER
    """)
    rows = cur.fetchall()
    return rows

def trigger2():
    cur = mydb.cursor()
    cur.execute("""
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
        DELIMITER
    """)
    rows = cur.fetchall()
    return rows

def trigger3():
    cur = mydb.cursor()
    cur.execute("""
        DELIMITER #
        CREATE TRIGGER ratings_update
        BEFORE UPDATE ON rides 
        FOR EACH ROW 
        BEGIN
        IF NEW.rating > 0 THEN
        UPDATE drivers 
        SET rated_trips = rated_trips + 1, net_rating_sum = net_rating_sum + NEW.rating
        WHERE driver_email = NEW.d_email; 
        END IF;
        END#
        DELIMITER ;
    """)
    rows = cur.fetchall()
    return rows

def change_password_mysql(user_email, new_password):
    cur = mydb.cursor()
    cur.execute("UPDATE users SET pswd = %s WHERE user_email = %s", (new_password, user_email))
    cur.execute("commit")
    cur.close()
    return 1

def change_phone_mysql(user_email, new_phone):
    cur = mydb.cursor()
    cur.execute("UPDATE users SET phno = %s WHERE user_email = %s", (new_phone, user_email))
    cur.execute("commit")
    cur.close()
    return 1

def ride_history(user_email):
    cur = mydb.cursor()
    cur.execute("SELECT * FROM rides WHERE u_email = %s AND ongoing IS NULL ORDER BY drop_time DESC", (user_email,))
    rows = cur.fetchall()
    return rows

def request_ride_mysql(user_email, pickup_loc, drop_loc, pickup_time, vehicle_type, fare):
    cur = mydb.cursor()
    # drop_time is twenty minutes after pickup_time
    drop_time = pickup_time + datetime.timedelta(minutes=20)
    cur.execute("INSERT INTO rides (u_email, pickup_loc, drop_loc, pickup_time, drop_time, fare, vehicle_no, ongoing) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (user_email, pickup_loc, drop_loc, pickup_time, drop_time, fare, get_vehicle_no(vehicle_type), 1))

def get_vehicle_no(vehicle_type: int):
    cur = mydb.cursor()
    cur.execute("SELECT reg_no FROM vehicles WHERE type_id = %s LIMIT 1", (vehicle_type,))
    rows = cur.fetchall()
    return str(rows[0])

def generate_receipt_number(user_email):
    cur = mydb.cursor()
    cur.execute("SELECT COUNT(*) FROM rides WHERE u_email = %s ORDER BY pickup_time DESC", (user_email,))
    rows = cur.fetchall()
    # add 1 to the number before the # to get the receipt number
    old_receipt_number = str(rows[0])
    new_receipt_number = ''
    for i in range(len(old_receipt_number)):
        if (old_receipt_number[i] == "#"):
            new_receipt_number = int(old_receipt_number[i + 1:]) + 1
            break
        else:
            new_receipt_number += old_receipt_number[i]
    new_receipt_number = int(new_receipt_number)
    new_receipt_number += 1
    new_receipt_number = str(new_receipt_number) + "#" + user_email
    return new_receipt_number

def rate_trip(user_email, receipt_number, rating):
    cur = mydb.cursor()
    cur.execute("UPDATE rides SET rating = %s WHERE u_email = %s AND receipt_no = %s", (rating, user_email, receipt_number))
    cur.execute("commit")
    cur.close()
    return 1

def get_driver_email():
    cur = mydb.cursor()
    cur.execute("SELECT driver_email FROM drivers WHERE current_status = 'AVAILABLE' LIMIT 1")
    rows = cur.fetchall()
    return str(rows[0])



# make command line app for logging in and signing up

input1 = 0
receipt_number = 0

while (input1 != 3):
    print("1. Login")
    print("2. Sign Up")
    print("3. Exit")
    input1 = int(input("Enter your choice: "))

    if (input1 == 1):
        user_email = input("Enter your email: ")
        ps = input("Enter your password: ")
        if (login_mysql(user_email, ps)):
            print("Login successful")

            # create menu to choose between olap queries, settings, ride history, and request ride, and exit

            input3 = 0
            while (input3 != 6):
                print("1. OLAP Queries")
                print("2. Settings")
                print("3. Ride History")
                # print("4. Request Ride")
                # print("5. Rate Trip")
                print("4. Exit")
                input3 = int(input("Enter your choice: "))
                if (input3 == 1):
                    input2 = 0

                    while (input2 != 5):
                        # print menu of olap queries
                        print("1. Show total rider rating by week and distance")
                        print("2. Show total earnings per day for the last four months")
                        print("3. Show groups of the rides by the year and pickup location, and calculate the total fare for each group")
                        print("4. Show top 3 drivers by total ride fare and year")
                        print("5. Exit to main menu")
                        
                        input2 = int(input("Enter your choice: "))
                        if (input2 == 1):
                            rows = olap1()
                            for row in rows:
                                print(row)
                                print("\n")
                        
                        elif (input2 == 2):
                            rows = olap2()
                            for row in rows:
                                print(row)
                                print("\n")

                        elif (input2 == 3):
                            rows = olap3()
                            for row in rows:
                                print(row)
                                print("\n")
                        
                        elif (input2 == 4):
                            rows = olap4()
                            for row in rows:
                                print(row)
                                print("\n")
                        
                        elif (input2 == 5):
                            print("Exiting...")
                            break

                elif (input3 == 2):
                    print("Settings")

                    input4 = 0

                    while (input4 != 3):

                        print("1. Change Password")
                        print("2. Change Phone Number")
                        print("3. Exit to main menu")

                        input4 = int(input("Enter your choice: "))
                        if (input4 == 1):
                            new_password = input("Enter your new password: ")
                            if (change_password_mysql(user_email, new_password)):
                                print("Password changed successfully")
                            else:
                                print("Password change unsuccessful")
                        elif (input4 == 2):
                            new_phone = input("Enter your new phone number: ")
                            if (change_phone_mysql(user_email, new_phone)):
                                print("Phone number changed successfully")
                            else:
                                print("Phone number change unsuccessful")

                        elif (input4 == 3):
                            print("Exiting...")
                            break

                        else:
                            print("Invalid input")

                elif (input3 == 3):
                    print("Ride History")
                    rows = ride_history(user_email)
                    print("Ride ID\t\tPickup Time\t\tDrop Time\t\tPickup Location\t\tDrop Location\t\tFare\t\tDriver Email\t\tRating\t\tOngoing")
                    for row in rows:
                        print(row)
                        print()
                        print()
                
                # elif (input3 == 4):
                #     print("Request Ride")
                #     pickup_location = input("Enter your pickup location: ")
                #     # pickup time is current time in yyyy-mm-dd hh:mm:ss format
                #     pickup_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #     drop_location = input("Enter your drop location: ")
                #     distance = random.randint(1, 100)
                #     vehicle_type = input("Enter your vehicle type: ")
                #     fare = distance*10
                #     if (request_ride_mysql(user_email, pickup_location, pickup_time, drop_location, distance, fare)):
                #         print("Ride request successful")
                #     else:
                #         print("Ride request unsuccessful")

                # elif (input3 == 5):
                #     print("Rate Trip")
                
                elif (input3 == 4):
                    print("Exiting...")
                    break

        else:
            print("Login unsuccessful")
    elif (input1 == 2):
        user_email = input("Enter your email: ")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        ph = input("Enter your phone number: ")
        ps = input("Enter your password: ")
        if (signup_mysql(user_email, first_name, last_name, ph, ps)):
            print("Sign up successful")
        else:
            print("Sign up unsuccessful")
    elif (input1 == 3):
        print("Exiting...")
        break
    else:
        print("Invalid input")
