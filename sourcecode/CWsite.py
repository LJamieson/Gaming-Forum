import bcrypt
import sqlite3
from functools import wraps
from flask import Flask, redirect, render_template, request, session, url_for, g

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db_location = 'var/database.db'

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
      user = request.form['user']
      pw = request.form['password']
      pw = pw.encode('utf-8')
      spw = bcrypt.hashpw(pw, bcrypt.gensalt())
      if(user is not None and pw is not None):
		  db = get_db()
		  db.cursor().execute("INSERT INTO accounts(user,password,Avatar) VALUES (?,?,?)", (user,spw,default_Avatar))
		  db.commit()
		  return redirect(url_for('.login'))
    
   return render_template('register.html')

@app.route("/debug/")
def debugList():
   db = get_db()
   page = []
   page.append('<html><ul>')
   sql = "SELECT * FROM accounts"
   for row in db.cursor().execute(sql):
       page.append('<li>')
       page.append(str(row))
       page.append('<li>')
       
   sql2 = "SELECT * FROM messages"
   for row in db.cursor().execute(sql2):
       page.append('<li>')
       page.append(str(row))
       page.append('<li>')

   page.append('</ul><html>')
   data = db.cursor().execute('''SELECT user,password From accounts''')
   data = data.fetchall()
   for value in (data):
        print(value[0])
	
   for value in (data):
        print(value[1])
	
   return ''.join(page)

default_Avatar="https://via.placeholder.com/128"


def check_auth(user, password):
	db = get_db()
	data = db.cursor().execute('''SELECT user,password From accounts''')
	data = data.fetchall()
	password = password.encode('utf-8')
	for value in (data):
	    if(user == value[0] and value[1].encode('utf-8') == bcrypt.hashpw(password, value[1].encode('utf-8'))):
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
    session['current_user'] = None
    return redirect(url_for('.home'))

@app.route("/profile/", methods=['POST','GET'])
@requires_login
def profile():
	db = get_db()
	name = session['current_user']
	data = db.cursor().execute('SELECT * FROM accounts WHERE user = "'+name+'"')
	mRows = data.fetchall()
	if request.method == 'POST':
		user = request.form['user']
		pw = request.form['password']
		pw = pw.encode('utf-8')
		spw = bcrypt.hashpw(pw, bcrypt.gensalt())
		if(user is not None and pw is not None):
			db = get_db()
			db.cursor().execute('UPDATE accounts SET user="'+user+'" WHERE user ="'+name+'"')
			db.cursor().execute('UPDATE accounts SET password="'+spw+'" WHERE user ="'+name+'"')
			db.commit()
			return redirect(url_for('.home'))
		
	return render_template('profile.html', mRows = mRows)

@app.route("/")
def home():
    return render_template('home.html')
    
@app.errorhandler(404)
def page_not_found(error):
   return render_template('error.html'), 404

@app.route("/other/", methods=['POST','GET'])
def other():
	group = "other"
	db = get_db()
	data = db.cursor().execute('''SELECT * FROM messages WHERE board="other"''')
	mRows = data.fetchall()
	if session['current_user'] is not None:
		if request.method == 'POST':
			mbody = request.form['messagebody']
			db.cursor().execute("INSERT INTO messages(user,board,body) VALUES (?,?,?)", (session['current_user'],group,mbody))
			db.commit()
			return redirect(url_for('.other'))
		
	return render_template('messageboard.html', group = group, mRows = mRows)
	
@app.route("/bethesda/", methods=['POST','GET'])
def bethesda():
	group = "bethesda"
	db = get_db()
	data = db.cursor().execute('''SELECT * FROM messages WHERE board="bethesda"''')
	mRows = data.fetchall()
	if request.method == 'POST':
			mbody = request.form['messagebody']
			db.cursor().execute("INSERT INTO messages(user,board,body) VALUES (?,?,?)", (session['current_user'],group,mbody))
			db.commit()
			return redirect(url_for('.other'))
		
	return render_template('messageboard.html', group = group, mRows = mRows)

@app.route("/microsoft/", methods=['POST','GET'])
def microsoft():
	group = "microsoft"
	db = get_db()
	data = db.cursor().execute('''SELECT * FROM messages WHERE board="microsoft"''')
	mRows = data.fetchall()
	if request.method == 'POST':
			mbody = request.form['messagebody']
			db.cursor().execute("INSERT INTO messages(user,board,body) VALUES (?,?,?)", (session['current_user'],group,mbody))
			db.commit()
			return redirect(url_for('.other'))
		
	return render_template('messageboard.html', group = group, mRows = mRows)
    
@app.route("/nintendo/", methods=['POST','GET'])
def nintendo():
	group = "nintendo"
	db = get_db()
	data = db.cursor().execute('''SELECT * FROM messages WHERE board="nintendo"''')
	mRows = data.fetchall()
	if request.method == 'POST':
			mbody = request.form['messagebody']
			db.cursor().execute("INSERT INTO messages(user,board,body) VALUES (?,?,?)", (session['current_user'],group,mbody))
			db.commit()
			return redirect(url_for('.other'))
		
	return render_template('messageboard.html', group = group, mRows = mRows)
    
@app.route("/sony/", methods=['POST','GET'])
def sony():
	group = "sony"
	db = get_db()
	data = db.cursor().execute('''SELECT * FROM messages WHERE board="sony"''')
	mRows = data.fetchall()
	if request.method == 'POST':
			mbody = request.form['messagebody']
			db.cursor().execute("INSERT INTO messages(user,board,body) VALUES (?,?,?)", (session['current_user'],group,mbody))
			db.commit()
			return redirect(url_for('.other'))
		
	return render_template('messageboard.html', group = group, mRows = mRows)
    
@app.route("/pc/", methods=['POST','GET'])
def pc():
	group = "pc"
	db = get_db()
	data = db.cursor().execute('''SELECT * FROM messages WHERE board="pc"''')
	mRows = data.fetchall()
	if request.method == 'POST':
			mbody = request.form['messagebody']
			db.cursor().execute("INSERT INTO messages(user,board,body) VALUES (?,?,?)", (session['current_user'],group,mbody))
			db.commit()
			return redirect(url_for('.other'))
		
	return render_template('messageboard.html', group = group, mRows = mRows)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        pw = request.form['password']

        if check_auth(request.form['user'], request.form['password']):
            session['logged_in'] = True
            session['current_user'] = user
            return redirect(url_for('.home'))
    return render_template('login.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
