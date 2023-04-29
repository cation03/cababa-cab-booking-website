from flask import Flask, render_template, request
import mysql.connector as mc
import random
import datetime
mydb=mc.connect(host="localhost",user="root",passwd="astronaut",database="cababa")

app = Flask(__name__)

current_user = 'anamaria.griego@gmail.com'
def ratings_mysql(rating):
    global current_user
    mycursor=mydb.cursor()
    data=(rating,current_user)
    try:
        sql=("UPDATE rides SET rating = %s where u_email = %s")
        mycursor.execute(sql,data)
        mycursor.execute("commit")
        current_user = ''
        mycursor.close()
        return 1
    except:
        mycursor.close()
        return 0
    
@app.route('/')
def index():
    return render_template('review.html')

@app.route('/ratings', methods=['POST'])
def ratings():
    rating = request.form['rating']
    ret_val = ratings_mysql(rating)
    if ret_val == 1:
        return '<html><body><h1>Thank for the review!</h1>body></html>'
    else:
        return '<html><body><h1>ERROR!</h1><p>Something went wrong. Try again later<p></body></html>'

if __name__ == '__main__':
    app.run(debug=True)
