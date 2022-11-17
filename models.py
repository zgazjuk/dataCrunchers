from database import db

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
