#Authentication
from flask import Flask,render_template,redirect,url_for,request,session,flash

import bcrypt
import mysql.connector

app=Flask(__name__)
app.secret_key="123"
#MYSQL CONFIG
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Harshad@1234'
MYSQL_DB = "thunder"

# MySQL connection
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)
cursor=conn.cursor()

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET',"POST"])
def login():
    if request.method =="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        
        cursor.execute("select * from auth where email=%s;",(email,))
        user=cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):  
            session['user']=user[1]
            session['id']=user[0]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credential"
    return render_template('login.html')

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method =="POST":
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        
        cursor.execute('insert into auth (name,email,password) values (%s,%s,%s);',(name,email,hashed_password))
        conn.commit()
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user'in session:
        return render_template('dashboard.html',name=session['user'])
    return redirect('/login')
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/profile/<int:id>' ,methods=["GET","POST"])
def profile(id):
    if request.method=="GET":
        cursor.execute("select * from auth where id=%s",(id,))
        data=cursor.fetchone()
        return render_template('profile.html', user_data=data)
    
@app.route('/edit/<int:id>',methods=["GET","POST"])
def edit(id):
    if request.method == "POST":
        new_name = request.form.get("name")
        new_email = request.form.get("email")
        new_password = request.form.get("password")
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("UPDATE auth SET name = %s, email = %s, password = %s WHERE id = %s",(new_name, new_email, hashed_password, id))
        conn.commit()
        return redirect(url_for('dashboard')) 
    else:
        return render_template('edit_data.html',id=id)

@app.route('/target/<int:id>', methods=["GET", "POST"])
def target(id):
    target_count = 0

    # Fetch the count of existing targets for the user
    cursor.execute("SELECT COUNT(*) FROM targets WHERE user_id = %s", (id,))
    result = cursor.fetchone()

    if result:  
        target_count = result[0] 
    if request.method == "POST":
        
        if target_count >= 5:  # Check if the limit is reached
            flash("You have reached the maximum limit of 5 targets!", "error")
        else:
            new_target = request.form.get("target")
            cursor.execute("INSERT INTO targets (user_id, target) VALUES (%s, %s)", (id, new_target))
            conn.commit()
            flash("Target added successfully!", "success")

        return redirect(url_for('target', id=id))

    # Fetch targets for the user
    cursor.execute("SELECT id, target FROM targets WHERE user_id = %s", (id,))
    targets = cursor.fetchall()

    return render_template('target.html', id=id, targets=targets,target_count=target_count) 


# Remove Target
@app.route('/remove_target/<int:user_id>/<int:target_id>', methods=["POST"])
def remove_target(user_id, target_id):
    cursor.execute("DELETE FROM targets WHERE id = %s AND user_id = %s", (target_id, user_id))
    conn.commit()
    
    return redirect(url_for('target', id=user_id))
        
if __name__=='__main__':
    app.run(debug=True)
    