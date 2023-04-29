import mysql.connector as mc
mydb=mc.connect(host="localhost",user="root",passwd="astronaut",database="cababa")

def driver_details():
    cur=mydb.cursor()
    cur.execute("SELECT reg_no, vname, type_id, driver_email, first_name, last_name, phone_number, passkey, current_status, total_trips, rated_trips, net_rating_sum, final_rating FROM vehicles JOIN drivers ON drivers.driver_email = vehicles.d_email")
    rows=cur.fetchall()
    for records in rows:
        for i in records:
            print(i, end = " ")
        print()
    print()
    cur.close()

def record_delete():
    mycursor=mydb.cursor()
    user_email = input("Enter email id to delete from users: ")
    sql = "delete from users where user_email = %s"
    mycursor.execute(sql, (user_email,))
    mycursor.execute('commit')
    print("Record deleted successfully\n")
    mycursor.close()

def update_status_to_idle():
    mycursor=mydb.cursor()
    #email-sample = berta_magana@gmail.com
    user_email = input("Enter email id to update status: ")
    status = "IDLE"
    cmd = "UPDATE users SET current_status = %s WHERE user_email = %s"
    data=(status,user_email)
    mycursor.execute(cmd, data)
    mycursor.execute('commit')
    print("Record updated successfully\n")
    mycursor.close()

driver_details()
record_delete() 
update_status_to_idle()
