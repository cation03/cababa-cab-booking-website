from flask import Flask, render_template, request, redirect
import mysql.connector as mc
import random
import datetime
mydb=mc.connect(host="localhost",user="root",passwd="ananya",database="cababa")
rideHistory = set()
current_user = ''
def signup_mysql(user_email, first_name, last_name, ph, ps):
    global current_user
    mycursor=mydb.cursor()
    data=(user_email, first_name, last_name, ph, ps)
    try:
        sql1 = ("START TRANSACTION;")
        mycursor.execute(sql1)
        mycursor.close()
        mycursor=mydb.cursor()
        sql=("INSERT INTO users (user_email, first_name, phno, pswd) VALUES (%s, %s, %s, %s)")
        mycursor.execute(sql,data)
        mycursor.execute("commit")
        current_user = user_email
        mycursor.close()
        return 1
    except:
        mycursor.close()
        return 0

def settings_mysql(user_email, ph, ps):
    global current_user
    mycursor=mydb.cursor()
    data=(user_email, ph, ps, current_user)
    try:
        sql1 = ("START TRANSACTION;")
        mycursor.execute(sql1)
        mycursor.close()
        mycursor=mydb.cursor()
        sql=("UPDATE users SET user_email = %s, phno = %s, pswd = %s where user_email = %s")
        mycursor.execute(sql,data)
        mycursor.execute("commit")
        mycursor.close()
        current_user = ''
        return 1
    except:
        mycursor.close()
        return 0

def endride_mysql():
    global current_user
    mycursor = mydb.cursor()
    data = (current_user,)
    sql1 = ("START TRANSACTION;")
    mycursor.execute(sql1)
    mycursor.close()
    mycursor=mydb.cursor()
    sql = '''update rides set ongoing = NULL where u_email = %s'''
    mycursor.execute(sql, data)
    mycursor.execute("commit")
    mycursor.close()
    return
          
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/requestride')
def request_ride():
    return render_template('requestride.html')

@app.route('/signup')
def redirect_signup():
    return render_template('signup.html')

@app.route('/login')
def redirect_login():
    return render_template('login.html')

@app.route('/settings')
def redirect_settings():
    return render_template('settings.html')

@app.route('/settings', methods=['POST'])
def settings():
    global current_user
    user_email = request.form['username']
    ph = request.form['phone']
    ps = request.form['password']
    ret_val = settings_mysql(user_email, ph, ps)
    
    if ret_val == 1:
        return render_template('homepage.html')
    else:
        return '<html><body><h1>ERROR!</h1><p>Something went wrong. Try again later<p></body></html>'
    
    
@app.route('/signup', methods=['POST'])
def signup():
    global current_user
    user_email = request.form['email']
    first_name = request.form['fname']
    last_name = request.form['lname']
    ph = request.form['phno']
    ps = request.form['pswd']
    ret_val = signup_mysql(user_email, first_name, last_name, ph, ps)
    if ret_val == 1:
        return redirect('/requestride')
    else:
        return '<html><body><h1>ERROR!</h1><p>Something went wrong. Try again later<p></body></html>'

@app.route('/logout')
def logout():
    global current_user
    global rideHistory
    current_user = ""
    rideHistory = set()
    return render_template('homepage.html')

@app.route('/review')
def redirect_review():
    endride_mysql()
    return render_template('review.html')

@app.route('/endride')
def redirect_endride():
    return render_template('endride.html')

def login_mysql(user_email, ps):
    global current_user
    mycursor=mydb.cursor()
    data=(user_email, ps)
    try:
        
        sql=("SELECT * FROM users WHERE user_email = %s AND pswd = %s")
        mycursor.execute(sql,data)
        if mycursor.fetchone():
            current_user = user_email
            mycursor.close()
            return 1
        else:
            mycursor.close()
            return 0
    except Exception as e:
        print(e)
        mycursor.close()
        return 0
    
@app.route('/login', methods=['POST'])
def login():
    global current_user
    user_email = request.form['email']
    ps = request.form['pswd']
    ret_val = login_mysql(user_email, ps)
    if ret_val == 1:
        return redirect('/requestride')

    else:
        return '<html><body><h1>ERROR!</h1><p>Something went wrong. Try again later<p></body></html>'

def request_ride_mysql(user_email, source, destination, vt):
    global current_user
    mycursor=mydb.cursor(buffered=True)
    receipt_no = ""
    mycursor.execute("SELECT receipt_no FROM rides WHERE u_email = %s ORDER BY receipt_no DESC LIMIT 1", (user_email,))
    last_receipt_no = mycursor.fetchone()

    if last_receipt_no == None:
        receipt_no = "1#" + str(current_user)
    else:
        last_receipt_no = str(last_receipt_no[0])
        for i in range(len(last_receipt_no)):
            if last_receipt_no[i] == '#':
                break
            else:
                receipt_no += last_receipt_no[i]
        receipt_no = int(receipt_no)
        receipt_no += 1
        receipt_no = str(receipt_no) + "#" + str(current_user)
        
    
    pickup_time = datetime.datetime.now()
    drop_time = pickup_time + datetime.timedelta(minutes=5)
    vt = int(vt)
    mycursor.execute("commit")
    mycursor.close()
    mycursor = mydb.cursor(buffered = True)
    mycursor.execute("BEGIN")
    mycursor.close()
    mycursor = mydb.cursor()
    mycursor.execute("LOCK TABLES vehicles WRITE")
    mycursor.close()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT reg_no FROM vehicles WHERE type_id = %s order by rand() limit 1", (vt,))
    vehicle_no = mycursor.fetchone()[0]
    vehicle_no = str(vehicle_no)
    mycursor.execute("commit")
    mycursor.close()
    mycursor = mydb.cursor()
    mycursor.execute("UNLOCK TABLES")
    mycursor.close()

    driver_cursor = mydb.cursor(buffered = True)
    driver_cursor.execute("SELECT driver_email FROM drivers where current_status = 'AVAILABLE' ORDER BY RAND() LIMIT 1")
    driver_email = driver_cursor.fetchone()[0]
    driver_cursor.execute("commit")
    driver_email = str(driver_email)
    driver_cursor.execute("commit")
    driver_cursor.close()

    mycursor = mydb.cursor(buffered = True)
    distance = random.randint(1, 500)
    fare = distance*10
    data=(receipt_no, pickup_time, source, drop_time, destination, vehicle_no, driver_email, user_email, distance, fare, 0, 1)
    d = list(data)
    lst = []
    for i in d:
        lst.append(str(i))
    lst = " ".join(lst)
    lst = str(lst)
    
    
    try:
        sql1 = ("START TRANSACTION;")
        mycursor.execute(sql1)
        mycursor.close()
        mycursor=mydb.cursor()
        sql=("INSERT INTO rides (receipt_no, pickup_time, pickup_loc, drop_time, drop_loc, vehicle_no, d_email, u_email, distance, fare, rating, ongoing) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        mycursor.execute(sql,data)
        mycursor.execute("commit")
        mycursor.close()
        return 1, lst
    except:
        mycursor.close()
        return 0, lst

@app.route('/requestride', methods=['POST'])
def requestride():
    global current_user
    user_email = current_user
    source = request.form['source']
    destination = request.form['destination']
    vehicle_type = request.form['vehicle_type']
    ret_val,d = request_ride_mysql(user_email, source, destination, vehicle_type)
    
    if ret_val == 1:
        return redirect_endride()
    else:
        return '<html><body><h1>donee!</h1><p>{d}<p></body></html>'.format(d=d)

def ridehistory_mysql():
    global current_user
    global rideHistory
    user_email = current_user
    mycursor = mydb.cursor(buffered = True)
    mycursor.execute("SELECT * FROM rides WHERE u_email = %s", (user_email,))
    rides = mycursor.fetchall()
    mycursor.execute("commit")
    mycursor.close()
    return rides
    

@app.route('/ridehistory')
def ridehistory():
    global rideHistory
    rides = ridehistory_mysql()
    for ride in rides:
        rideHistory.add(ride)
    return render_template('ridehistory.html',rideHistory = rideHistory)

def ratings_mysql(rating):
    global current_user
    mycursor=mydb.cursor()
    data=(rating,current_user)
    try:
        sql=("UPDATE rides SET rating = %s where u_email = %s ORDER BY drop_time DESC LIMIT 1")
        mycursor.execute(sql,data)
        mycursor.execute("commit")
        mycursor.close()
        return 1
    except:
        mycursor.close()
        return 0
    

@app.route('/review', methods=['POST'])
def review():
    rating = request.form['rating']
    ret_val = ratings_mysql(rating)
    if ret_val == 1:
        return redirect('/requestride')
    
    else:
        return '<html><body><h1>ERROR!</h1><p>Something went wrong. Try again later<p></body></html>'

if __name__ == '__main__':
    app.run(debug=True)
