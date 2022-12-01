
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
from forms import LoginForm


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

    return render_template('create_account.html', form=form)

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


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
