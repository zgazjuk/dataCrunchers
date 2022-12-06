from database import db
import datetime


class Task(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(200))
    description = db.Column("description", db.String(200))
    pinned = db.Column("pinned", db.Boolean, default=False)
    section = db.Column("section", db.String(200))
    comments = db.relationship("Comment", backref="comment", cascade="all, delete-orphan", lazy=True)

    def __init__(self, name, description, pinned, section):
        self.name = name
        self.description = description
        self.pinned = pinned
        self.section = section

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    db.relationship("User", backref="userName", cascade="all, delete-orphan", lazy=True)

    def __init__(self, content, task_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.user_id = user_id
        self.task_id = task_id

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log = db.Column("log", db.String(200))

    def __init__(self, log):
        self.log = log
