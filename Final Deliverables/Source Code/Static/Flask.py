from flask import Flask, render_template, request, session
import ibm_db
import re, sqlite3



app = Flask(__name__)
  
app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=Certificate.crt;UID=bfc78863;PWD=asffv3iXKrFIBru6",'','')

@app.route('/')

def homer():
    return render_template('home.html')


@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE email =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['EMAIL']
            userid=  account['EMAIL']
            session['EMAIL'] = account['EMAIL']
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

        

   
@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  user VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('login', msg = msg)

@app.route('/dashboard')
def dash():
    
    return render_template('dashboard.html')

@app.route('/apply',methods =['GET', 'POST'])
def apply():
     msg = ''
     if request.method == 'POST' :
         f_name = request.form['f_name']
         l_name = request.form['l_name']
         address_1=request.form['address_1']
         address_2=request.form['address_2']
         city=request.form['city']
         dist=request.form['dist']
         postal=request.form['postal']
         state=request.form['state']
         area_code=request.form['area_code']
         ph_no=request.form['ph_no']
         email = request.form['email']
         aoi=request.form['aoi']
         skill_level=request.form['skill_level']
         cl=request.form['cl']
         resume=request.form['resume']
         
         sql = "SELECT * FROM user WHERE name =?"
         
         '''stmt = ibm_db.prepare(conn, sql)
         #ibm_db.bind_param(stmt,1,username)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)
         #if account:
           # msg = 'there is only 1 job position! for you'
           # return render_template('apply.html', msg = msg)'''

         
         
         insert_sql = "INSERT INTO resume VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
         prep_stmt = ibm_db.prepare(conn, insert_sql)
         ibm_db.bind_param(prep_stmt, 1, f_name)
         ibm_db.bind_param(prep_stmt, 2, l_name)
         ibm_db.bind_param(prep_stmt, 3, address_1)
         ibm_db.bind_param(prep_stmt, 4, address_2)
         ibm_db.bind_param(prep_stmt, 5, city)
         ibm_db.bind_param(prep_stmt, 6, dist)
         ibm_db.bind_param(prep_stmt, 7, postal)
         ibm_db.bind_param(prep_stmt, 8, state)
         ibm_db.bind_param(prep_stmt, 9, area_code)
         ibm_db.bind_param(prep_stmt, 10, ph_no)
         ibm_db.bind_param(prep_stmt, 11, email)
         ibm_db.bind_param(prep_stmt, 12, aoi)
         ibm_db.bind_param(prep_stmt, 13, skill_level)
         ibm_db.bind_param(prep_stmt, 14, cl)
         ibm_db.bind_param(prep_stmt, 15, resume)
         ibm_db.execute(prep_stmt)
         msg = 'You have successfully applied for job !'
         session['loggedin'] = True
         TEXT = "Hello sandeep,a new appliaction for job position" +aoi+"is requested"
         
         #sendmail(TEXT,"sandeep@thesmartbridge.com")
        #
        #  sendgridmail("sandeep@thesmartbridge.com",TEXT)
         
         
         
     elif request.method == 'POST':
         msg = 'Please fill out the form !'
     return render_template('apply.html', msg = msg)

@app.route('/display')
def display():
    print(session["name"],session['id'])
    
    cursor = sqlite3.connection.cursor()
    cursor.execute('SELECT * FROM resume WHERE userid = % s', (session['id'],))
    account = cursor.fetchone()
    print("accountdislay",account)

    
    return render_template('display.html',account = account)

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')


    
if __name__ == '_main_':
   app.run(host='0.0.0.0')