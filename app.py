
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Task as Task
from forms import RegisterForm
from flask import session
import bcrypt
from models import User as User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_task_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    tasks = db.session.query(Task).all()
    return render_template('dashboard.html', tasks = tasks)

@app.route('/<task_id>')
def get_task(task_id):
    task = db.session.query(Task).filter_by(id=task_id).one()
    return render_template('task-details.html', task = task)

@app.route('/new', methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        new_record = Task(name, description, False, "")
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('dashboard'))
    else:
        return render_template('new.html')

@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        task = db.session.query(Task).filter_by(id=task_id).one()
        task.name = name
        task.description = description

        db.session.add(task)
        db.session.commit()

        return redirect(url_for('dashboard'))
    else:
        task = db.session.query(Task).filter_by(id=task_id).one()
        return render_template('new.html', task = task)

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    task = db.session.query(Task).filter_by(id=task_id).one()

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/signup', methods=['POST', 'GET'])
def create_account():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        hash_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
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

    return render_template('create_account.html', form=form)

@app.route('/login')
def user_login():
    return render_template('user_login.html')

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
