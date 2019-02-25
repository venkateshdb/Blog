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
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import os
import random
import string
import time


#--------- App configuration & declaration ---------------------------------
app = Flask(__name__)
heroku = Heroku(app)
app.config.from_object(__name__)
db = SQLAlchemy(app)


app.config.update(dict(
SQLALCHEMY_TRACK_MODIFICATION = False,
SECRET_KEY = '\x07-\x98\xdf\xf2\xa6\x97\xebT\x13\x92\xa8\xa8h\xb1k',
ftp = os.path.join(app.root_path, 'static/ftp'),
upload = os.path.join(app.root_path, 'static/user_upload'),
allowed_extension = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' , 'mp4' , 'exe' , 'mp3' ,'xml' , 'config' , 'py'])
))
app.config.from_envvar('flaskr_setting' , silent=True)
#----------------------- database --------------------------------
class Posts(db.Model):
    """
    content to be posted
    """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())
    title = db.Column(db.String(), nullable=False)
    sub_title = db.Column(db.String())
    content = db.Column(db.String(), nullable=False)

    def __init__(self,date,title,sub_title,content):
        self.date = date
        self.title = title
        self.sub_title = sub_title
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

class auth(db.Model):
    """
    user auth
    """
    __tablename__ = "auth"

    user_id = db.Column(db.String(), primary_key=True, nullable=False)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self,user_id,username,password):

        self.user_id = user_id
        self.username = username
        self.password = password

    def __repr__(self):
        return "<user_id {}>".format(self.user_id)


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
    return (string.digits + string.ascii_letters)

def id():
    key = [random.choice(gen()) for i in range(5)]
    return (''.join(key))









#----------------------- app routing ------------------------------------


# landing page
@app.route('/')
def show_entries():

    fetch_entries = Posts.query.all()
    return render_template('index.html', fetch_entries=fetch_entries)

# route to add posts


# handling publishing posts
@app.route('/post', methods=['GET', 'POST'])
def post():
    if not session.get('logged_in'):
        abort(400)

    return render_template('post.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    timestamp = time.asctime()
    title = request.form['title']
    sub_title = request.form['description']
    body = request.form['content']

    #----image upload----

    post = Posts(timestamp,title,sub_title,body)

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('show_entries'))


# handling login
@app.route('/login' , methods=['GET', 'POST'])
def login():


    error = None
    if request.method == 'POST':

        get_username = request.form['username']
        get_password = request.form['password']

        if not auth.query.filter_by(username = get_username,password=get_password).all():
            error = "Invalid Credentials"

        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('post'))
    return render_template('login.html', error=error)

# handling logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('<h1 class="flash">You are logged out</h1>')
    return redirect(url_for('show_entries'))

@app.route('/signup' , methods=['POST', 'GET'])
#"""signup form"""
def new_user():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        signup = auth(id(),username,password)
        db.session.add(signup)
        db.session.commit()
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
"""
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

@app.route('/img')
def get_img():
    img = request.files['photo']
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
