import bcrypt
import sqlite3
from functools import wraps
from flask import Flask, redirect, render_template, request, session, url_for, g

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db_location = 'var/userAccounts.db'

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
	    db.cursor().executescript(f.read())
        db.commit

@app.route("/register/", methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      user = request.form['email']
      pw = request.form['password']
      if(user is not None and pw is not None):
		  db = get_db()
		  db.cursor().execute("INSERT INTO accounts(email,password) VALUES (?,?)", (user,pw))
		  db.commit()
		  return redirect(url_for('.login'))
    
   return render_template('register.html')

@app.route("/debug/")
def debugList():
   db = get_db()
   page = []
   page.append('<html><ul>')
   sql = "SELECT rowid, * FROM accounts ORDER BY email"
   for row in db.cursor().execute(sql):
       page.append('<li>')
       page.append(str(row))
       page.append('<li>')

   page.append('</ul><html>')
   return ''.join(page)

valid_email ='person@napier.ac.uk'
valid_pwhash=bcrypt.hashpw('secretpass', bcrypt.gensalt())

def check_auth(email, password):
    if(email == valid_email and
        valid_pwhash == bcrypt.hashpw(password.encode('utf-8'), valid_pwhash)):
            return True
    return False

def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect(url_for('.login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('.login'))

@app.route("/secret/")
@requires_login
def secret():
    return "Secret Page"

@app.route("/")
def home():
    return render_template('home.html')
	
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        pw = request.form['password']

        if check_auth(request.form['email'], request.form['password']):
            session['logged_in'] = True
            return redirect(url_for('.secret'))
    return render_template('login.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
