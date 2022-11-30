from database import db
import datetime


class Task(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(200))
    description = db.Column("description", db.String(200))
    pinned = db.Column("pinned", db.Boolean, default=False)
    section = db.Column("section", db.String(200))

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

