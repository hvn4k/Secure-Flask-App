import sqlite3
import hashlib
import base64
from flask import Flask,session,render_template,request, url_for ,flash , redirect ,abort
from flask_session import Session
from datetime import timedelta
from flask import request
import secrets
import time
from datetime import datetime


app = Flask(__name__)
secret_key = secrets.token_hex(16)
print(secret_key)   
app.config['SECRET_KEY'] = secret_key
app.config['SESSION_PERMANENT'] = False   
app.config['SESSION_USE_SIGNER'] = True    
app.config['SESSION_COOKIE_SECURE'] = True  
app.config['SESSION_COOKIE_HTTPONLY'] = True  
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  
app.permanent_session_lifetime = timedelta(minutes=1)
Session(app)

phone=0

def start():
    global start_time
    start_time=0
    start_time=time.time()
    
def timeout():
        end_time=0
        total=0
        end_time =time.time() 
        total=end_time-start_time
        print(start_time)
        print(end_time)
        print(total)
        return total
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM STATUS WHERE CNIC = ?',(post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

    
@app.route('/Monthly')
def Monthly():
   new7=timeout()
   if(new7 >10):
        return redirect(url_for('Login'))
   
   conn = get_db_connection()
   global Total
   Total=0
   STATUS = conn.execute('SELECT * from STATUS').fetchall()
   conn.execute('Delete from Sales')
   conn.commit()
   with get_db_connection() as conn:
        cursor = conn.cursor()
        # Fetch all rows from the 'Information' table
        cursor.execute('SELECT Bill FROM STATUS')
        rows = cursor.fetchall()
   for row in rows:  
       Total=Total+row['Bill']
         
   conn.execute('Insert into Sales(Billing) values(?)',(Total,))
   conn.commit()
   Total=0
   Sales = conn.execute('SELECT * from Sales').fetchall()
   conn.close()
   start()
   return render_template('Monthly.html',STATUS=STATUS,Sales=Sales)

@app.route('/Monthly',methods=['POST'])
def Monthly1():
   new6=timeout()
   if(new6 >10):
        return redirect(url_for('Login'))
   start()
   conn = get_db_connection()
   conn.execute('Delete from STATUS')
   conn.commit()
   start()
   return redirect(url_for('admins')) 

  

@app.route('/bill')
def bill():
    new2=timeout()
    if(new2 >10):
        return redirect(url_for('Login'))
    start()
   
    return render_template('rentdays.html')

@app.route('/bill',methods=['POST'])
def bill1():
    global rentdate
    global bill
    if request.method=='POST':
        new3=timeout()
        if(new3 >10):
            return redirect(url_for('Login'))
        
        rentday=request.form['d']
        rentdate=request.form['dd']
        bill=3500*int(rentday)
        bill=int(bill)
        print( phone)
        print(rentday)
        total=0
        start()
        return redirect(url_for('invoice')) 
  
@app.route('/customer')
def customer():
   conn = get_db_connection()
   Information = conn.execute('SELECT * from Information').fetchall()
   conn.close()
   return render_template('customer.html',Information=Information)

@app.route('/<string:id>/deletecustomer/', methods=('GET', 'POST'))
def deletecustomer(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Information WHERE CNIC = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('customer'))

@app.route('/status')
def status():
   conn = get_db_connection()
   STATUS = conn.execute('SELECT * from STATUS').fetchall()
   conn.close()
   return render_template('status.html',STATUS=STATUS)

@app.route('/<string:id>/delete/', methods=('GET', 'POST'))
def delete(id):
    print(id)
    shehzil = get_post(id)
    print(shehzil)
    conn = get_db_connection()
    conn.execute('DELETE FROM STATUS WHERE CNIC = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('status'))
    
@app.route('/contact')
def contact():
   
   return render_template('contact.html')


@app.route('/')
def index():
    return render_template('Home.html')
    
@app.route('/admins')
def admins():
   new9=timeout()
   if(new9 >10):
        return redirect(url_for('Login'))
   start()
   return render_template('admin_interface.html')
@app.route('/admins',methods=['POST'])
def create3():
    if request.method=='POST':
        new10=timeout()
        if(new10 >10):
            return redirect(url_for('Login'))
        start()
        return redirect(url_for('admins'))
        
@app.route('/Login')
def Login():
    start_time=0
    return render_template('new login.html')    
@app.route('/Login',methods=['POST'])
def create():
        global usr
        global passwordd
        global cnic    
        if request.method == 'POST':
            usr = request.form['usrname']
            passwordd = request.form['passwrd']
            hashed_name = base64.b64encode(usr.encode()).decode()
            hashed_password = base64.b64encode(passwordd.encode()).decode()
            
            
            with get_db_connection() as conn:
             cursor = conn.cursor()
             cursor.execute('SELECT Name, Password,CNIC FROM Information')
             rows = cursor.fetchall()

            for row in rows:
                # Compare hashed values with user input
                if row['Name'] == usr and base64.b64decode(row['Password']).decode()== passwordd:
                    
                    if(usr=='admin'):
                        print(usr)
                        start()
                        return redirect(url_for('admins'))   
                  

                    hashcnic= row['CNIC']
                    cnic = base64.b64decode(hashcnic).decode()
                    print(cnic)
                    start()
                    return redirect(url_for('Service'))
               
                        
            return render_template('new login.html')

@app.route('/Service')
def Service():
    new=timeout()
    if(new >10):
        return redirect(url_for('Login'))
    start()
    return render_template('Service.html')


@app.route('/Service',methods=['POST'])
def create1():
    if request.method=='POST':
        new1=timeout()
        if(new1 >10):
            return redirect(url_for('Login'))
        start()
        return redirect(url_for('bill'))


@app.route('/INVOICE')
def invoice():
   new4=timeout()
   if(new4 >10):
       return redirect(url_for('Login'))
   
   
   print (usr)
   print (cnic)
   print (rentdate)
   print(bill)
   conn = get_db_connection()
   conn.execute('Insert into STATUS(NAME,CNIC,MOBILE,Date,Bill) values(?,?,?,?,?)',(usr,cnic,"03143537644",rentdate,bill))
   conn.commit()
   STATUS = conn.execute('SELECT * from STATUS').fetchall()
   conn.close()
   start()
   return render_template('index.html',STATUS=STATUS)


@app.route('/INVOICE',methods=['POST'])
def invoice1():
   new5=timeout()
   if(new5 >10):
       return redirect(url_for('Login'))
   start()
   return redirect(url_for('Service'))     
@app.route('/registration')
def registration():
   
   return render_template('registration.html')

@app.route('/registration',methods=('GET','POST'))
def registration1():
        
        
        n=request.form['typefull']
        password=request.form['pass'] 
        cnic=request.form['nic']
        usr=n
        passwordd=password
        
        email=0
        hashed_name = base64.b64encode(n.encode()).decode()
        hashed_password = base64.b64encode(password.encode()).decode()
        hashed_cnic = base64.b64encode(cnic.encode()).decode()
        conn = get_db_connection()
        conn.execute('INSERT INTO Information(Name,Password,CNIC,Email) VALUES (?,?,?,?)',(n,hashed_password,hashed_cnic,email))
        conn.commit()
        conn.close() 
        return redirect(url_for('Login'))    
@app.route('/logout')            
def logout():
    session.pop('user', None)
    return render_template('new login.html')
          
       
   
       
                
               
            
        
