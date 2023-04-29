# User Guide

1. Homepage
2. Login/Sign Up
3. Request a Ride
4. Settings
5. Ride History
6. End ride
7. Rate and review
8. Log out

## 1. Homepage

- Provides the option to log in or signup.
- Login for an existing user account.
- Sign Up for a new user
![image](https://user-images.githubusercontent.com/78123938/235296779-569e77a4-c7d9-4e66-baef-9ea4d4e1c475.png)

## 2. Log in/Sign up
 - Log in
    a. Login for an existing user. 
    b. Provide your email and password for logging into the database. 
    c. If the entered data is correct and present in the database, you will be redirected to the request ride page; else, you will get an error message.
![image](https://user-images.githubusercontent.com/78123938/235296787-8a1852b6-61fe-4786-9150-5bdf63e8c595.png)

- Sign up
    a. Sign up for a new user.
    b. Provide a unique email, phone number, and other details like first name, last name, and password to create a new account.
    c. A new user is redirected to the request ride page if a unique email and phone number are entered. Else, the user will get an error message.
![image](https://user-images.githubusercontent.com/78123938/235296791-a64f2aec-f936-41f1-8bd8-c9ab2b8b2cf3.png)


## 3. Request a Ride
- The user must enter the pickup location, destination address, and preferred ride type.
- The database will select a ride per the user’s needs and an available driver from the database who can fulfil the driver’s request.
- When the user clicks on the request ride button, they are redirected to the end ride page, where the ride is started, and the user can end the ride at their convenience.
- The user can also view the ride history, go to settings and log out of their account through the buttons provided in the navigation bar of this page.
![image](https://user-images.githubusercontent.com/78123938/235296853-c63080a8-421d-4026-ad7c-202f6cdd77e7.png)

## 4. Settings
- Users can change their email, password and phone number using the settings page. This also involves triggers so that when users change their email address and phone number, their ride history is automatically deleted.
![image](https://user-images.githubusercontent.com/78123938/235296867-57c955a2-26cf-4344-872b-d9c7835327c4.png)

## 5. Ride History
- This page shows the user's ride history through the rides booked through this app.
- It shows various details like the vehicle number, pickup and drop-off date, time and location, driver email, fare, distance, ride status and the rating given by the user.
![image](https://user-images.githubusercontent.com/78123938/235296908-83b3da06-4f41-499f-8f83-ce17a577a792.png)

## 6. End Ride
- This page provides the user with an option to end their current ride. Since it is not possible for us to arrange a physical ride, we have implemented this button where the user can end the ride when they press this button.
![image](https://user-images.githubusercontent.com/78123938/235296881-ae5d3d25-ffcd-4b4c-9d37-bab6d0480b53.png)

## 7. Rate and Review
- Provides the user with an option to rate their driver.
- The ratings are stored in the row of the corresponding driver, and the average of all the ratings over rated trips is taken to calculate the final rating of the driver.
- The user also has the option to visit the request ride page if they do not want to rate their ride.
![image](https://user-images.githubusercontent.com/78123938/235296895-0a5b72dc-7135-46d0-ac62-d4e44f6e7ad5.png)

## 8. Log out
- Logs the user out of their account and redirects to the homepage.
![image](https://user-images.githubusercontent.com/78123938/235296922-01bb8765-0af8-4d06-b424-fec3d6fc4157.png)

# How to use

1. Clone the repository.
2. Run cababa-schema.sql
3. Run cababa-data.sql (run everything except the lines that insert into the rides and vehicle table)
4. Run vehicle data.sql
5. Run rides data.sql
6. Run cababa-queries.sql (the ones without the constraint demonstration comment)
7. Run cababa-triggers.sql
8. Navigate to the website folder
9. Change the password in line 5 of app.py to your MySQL password
10. `mydb=mc.connect(host="localhost",user="root",passwd="your-password-here",database="cababa")`
11. Run app.py
12. Go to http://127.0.0.1:5000 or localhost:5000[localhost:5000] to use the website.
