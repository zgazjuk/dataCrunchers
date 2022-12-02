
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for, flash
from database import db
from models import Task as Task
from flask import session
import bcrypt
from models import User as User
from forms import LoginForm, NewTaskForm, RegisterForm
import re


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_task_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    if session.get('user'):
        current_user = session['user']
        tasks = db.session.query(Task).all()
        return render_template('dashboard.html', tasks = tasks, user=current_user)
    else:
        return redirect(url_for('user_login'))
    

@app.route('/<task_id>')
def get_task(task_id):
    task = db.session.query(Task).filter_by(id=task_id).one()
    return render_template('task-details.html', task = task, user=session['user'])

@app.route('/new', methods=['GET', 'POST'])
def new_task():
    new_task_form = NewTaskForm()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        # check to ensure that Title and Description fields are filled out properly;
        # if not, flash a message to the user to fix the issue and render the new.html template again
        if not (re.search('^.{6,}$', description) or re.search('^.{6,}$', name)):
            flash('Title and Details fields must not be empty, and must contain more than just whitespace. Please check your input and try again.')
            return render_template('new.html', flash=flash, user=session['user'])

        section = request.form['task-details-moveto']

        new_record = Task(name, description, False, section)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('dashboard'))
    else:
        return render_template('new.html', user=session['user'])

@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        section = request.form['task-details-moveto']
        task = db.session.query(Task).filter_by(id=task_id).one()
        task.name = name
        task.description = description
        task.section = section

        db.session.add(task)
        db.session.commit()

        return redirect(url_for('dashboard'))
    else:
        task = db.session.query(Task).filter_by(id=task_id).one()
        return render_template('new.html', task = task, user=session['user'])

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    task = db.session.query(Task).filter_by(id=task_id).one()

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/signup', methods=['POST', 'GET'])
def create_account():
    form = RegisterForm() # getting a reference to the RegisterForm from forms.py
    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        hash_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # getting entered user data
        first_name = request.form['firstname']
        print(first_name)
        last_name = request.form['lastname']
        print(last_name)
        email = request.form['email']
        print(email)
        print(hash_password)
        # create user model
        new_user = User(first_name, last_name, email, hash_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        # session['user'] = first_name
        # session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('dashboard'))

    return render_template('create_account.html', form=form, user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    login_form = LoginForm() # Getting refernece to the LoginForm from forms.py
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('dashboard'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("user_login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("user_login.html", form=login_form)

@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    
    return redirect(url_for('user_login'))


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
