
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Task as Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_task_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

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
        section = request.form['task-details-moveto']

        new_record = Task(name, description, False, section)
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
        return render_template('new.html', task = task)

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    task = db.session.query(Task).filter_by(id=task_id).one()

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('dashboard'))

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
