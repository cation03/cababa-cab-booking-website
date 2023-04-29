import mysql.connector as mc
mydb = mc.connect(host = "localhost",
                  user = "root",
                  passwd = "astronaut",
                  database = "cababa")
def signup():
    mycursor=mydb.cursor()
    user_email = input("Enter Email: ")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    ph = int(input("Enter Phone Number: "))
    ps = input("Enter Password: ")
    data=(user_email, first_name, last_name, ph, ps)
    try:
        sql=("INSERT INTO users (user_email, first_name, last_name, phno, pswd) VALUES (%s, %s, %s, %s, %s)")
        mycursor.execute(sql,data)
        mycursor.execute("commit")
        print("Account created!\n")
    except:
        print("ERROR: Email or Phone Number already exists\n")
    mycursor.close()

def display_ride_history():
    cur = mydb.cursor()
    print("Displaying the ride history of a particular user by taking email id as input\n")
    #email-sample = berta_magana@gmail.com
    user_email = input("Enter email id to see ride history: ")
    cur.execute("SELECT * FROM rides WHERE u_email = %s AND ongoing IS NULL ORDER BY drop_time DESC", (user_email,))
    rows = cur.fetchall()
    for records in rows:
        for i in records:
            print(i, end = " ")
        print()
        print("\n")
        
def update_status_to_ongoing():
    mycursor=mydb.cursor()
    #email-sample = berta_magana@gmail.com
    user_email = input("Enter email id to update status: ")
    status = "ONGOING"
    cmd = "UPDATE users SET current_status = %s WHERE user_email = %s"
    data=(status,user_email)
    mycursor.execute(cmd, data)
    mycursor.execute('commit')
    print("Record updated successfully\n")
    mycursor.close()
    
signup()
display_ride_history()
update_status_to_ongoing()
