#===========MYBLOG Backend=========
# language:python(2.7)           ==
# framework:flask(0.12)          ==
# author : venkatesh bellale     ==
# last-updated:3:56 PM 10-Apr-18 ==
# version: 1.1                   ==
# host: http://localhost:80      ==
# license: MIT                   ==
#==================================

#------------ importing modules----

from flask import Flask, render_template, request, redirect, g, flash, abort, url_for, session
from werkzeug.utils import secure_filename
import sqlite3
import os
import random
import string
import time
import psycopg2

#--------- App configuration & declaration ---------------------------------
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
database = 'postgres://thhzvmrynenrbn:7936173332181f998242116d8045d1c868352b12e4b2fdf6332b10962e14a3aa@ec2-23-21-171-25.compute-1.amazonaws.com:5432/d9ql13d83ao9t9',
SECRET_KEY = '\x07-\x98\xdf\xf2\xa6\x97\xebT\x13\x92\xa8\xa8h\xb1k',
username = 'test',
password = 'test',
debug = False,
ftp = os.path.join(app.root_path, 'static/ftp'),
upload = os.path.join(app.root_path, 'static/user_upload'),
allowed_extension = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' , 'mp4' , 'exe' , 'mp3' ,'xml' , 'config' , 'py'])
))
app.config.from_envvar('flaskr_setting' , silent=True)
#----------------------- database connections --------------------------------

def connect_db():
    """Connects to the specific database."""
    db = psycopg2.connect(app.config['database'])
    rv = db.cursor()
    return rv


def init_db():
    """Initializes the database."""
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db
    print('Initialized the database.')
"""Initializes the database."""

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """closes database connection """
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()


#--------------------- functions ------------------------------------------------

# checks for extensions of uploaded files
def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1].lower() in app.config['allowed_extension']

"""
function to generate post_ids
"""
    #post_id = []
    #ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    #get_nums = str(random.sample(xrange(0,10),3))
    #get_string = random.choice(ALPHABET)

def gen():
    return (string.digits + string.letters)

def id():
    key = [random.choice(gen()) for i in range(5)]
    return (''.join(key))









#----------------------- app routing ------------------------------------


# landing page
@app.route('/')
def show_entries():
    db = connect_db()
    fetch_entries = db.execute('select title, sub_title, description, date, tag, content, image from post').fetchall()
    return render_template('index.html', fetch_entries=fetch_entries)

# route to add posts


# handling publishing posts
@app.route('/post')
def post():
    if not session.get('logged_in'):
        abort(400)
    timestamp = time.asctime()
    title = request.form['title']
    sub_title = request.form['description']
    tags = request.form['tags']
    body = request.form['body']

    #----image upload----
    cover_img  = request

    return render_template('post.html')


# handling login
@app.route('/login' , methods=['GET', 'POST'])
def login():
    db = connect_db()
    get_auth = db.execute('SELECT username , password FROM AUTH').fetchall()
    convert = dict(get_auth)

    error = None

    if request.method == 'POST':
        for key,value in convert.iteritems(): # key -> username,value -> password.

            get_username = request.form['username']
            get_password = request.form['password']
            if key != get_username:
                error = "Invalid username or password"
            if  value != get_password:
                error = "Invalid username or password"

            else:
                session['logged_in'] = True
                flash('You are logged in')
                return redirect(url_for('post'))
    return render_template('login.html', error=error)

# handling logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('<h1>You are logged out</h1>')
    return redirect(url_for('show_entries'))

@app.route('/signup' , methods=['POST', 'GET'])
#"""signup form"""
def new_user():
    db = connect_db()
    if request.method == "POST":
        db = get_db()
        db.execute('insert into auth (username , password) values (?,?)' , [request.form['username'] , request.form['password']])
        db.commit()
        flash('signup Successfully')
        return redirect(url_for('login'))

    return render_template('signup.html')


# about page route
@app.route('/about')
def about():
    return render_template('about.html')
#----------------- Custom error handler----------------------------
@app.errorhandler(404)
def error_404(error):
    #custom page for 404 error
    return render_template("404.html") , 404

@app.errorhandler(500)
def error_500(error):
    #custom page for 500 error
    return render_template("500.html") , 500

@app.errorhandler(400)
def error_400(error):
    #custom page for 400 error
    return render_template("400.html") , 400

#----------------- ftp like shareit ---------------------------------------------------
@app.route('/upload')
def send():
    return render_template('upload.html')

@app.route('/get_upload')
def get_upload():
    db = get_db()
    file = request.files['photo']
    if file or allowed_file(file.filename):
        filename = secure_filename(file.filename)
        db.execute('insert into files values (?)' , [filename])
        file.save(os.path.join(app.config['ftp'], filename ))
        db.commit()
    return redirect(url_for('send'))
"""
@app.route('/img')
def get_img():
    img = request.files['photo']
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
