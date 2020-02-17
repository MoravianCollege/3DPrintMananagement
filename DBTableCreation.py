from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/kschmall/Documents/Projects/FullStackDev/SQLAlchemyDBs/fullStackdbs.db'
db = SQLAlchemy(app)


class Workers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_Admin = db.Column(db.Boolean, unique=False, default=False)
    is_Active = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return '<Workers %r>' % self.name

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    general_Link = db.Column(db.String(500), unique=False, nullable=False)
    for_Who = db.Column(db.String(100), unique=False, nullable=False)
    deadline = db.Column(db.DateTime, unique=False, nullable=True)
    status = db.Column(db.String(50), unique=False, nullable=False)
    primary_Person = db.Column(db.String(80), unique=True, nullable=False) 

    def __repr__(self):
        return '<Project %r>' % self.name

# class Status(db.Model):
#     submimtted = db.Column(db.String(80), unique=False, nullable=False)
#     accepted = db.Column(db.String(80), unique=False, nullable=False)
#     designing = db.Column(db.String(80), unique=False, nullable=False)
#     needs_Work = db.Column(db.String(80), unique=False, nullable=False)
#     printing = db.Column(db.String(80), unique=False, nullable=False)
#     post_Processing = db.Column(db.String(80), unique=False, nullable=False)
#     delivered = db.Column(db.String(80), unique=False, nullable=False)

#     def __repr__(self):
#         return '<Status %r>' % self.name
#         # shouldnt return name, what should this return?

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_ID= db.Column(db.Integer, unique=False) # reference project Id
    status = db.Column(db.String(50), unique=False, nullable=False) # ref project status
    count_Needed = db.Column(db.Integer, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Model %r>' % self.id

class Print(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    base_Settings = db.Column(db.String(80), unique=False, nullable=False)
    core1 = db.Column(db.String(80), unique=False, nullable=False)
    core2 = db.Column(db.String(80), unique=False, nullable=False)
    material1 = db.Column(db.String(80), unique=False, nullable=False)
    material2 = db.Column(db.String(80), unique=False, nullable=False)
    est_Time = db.Column(db.Integer, unique=False, nullable=False)
    est_Material = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Print %r>' % self.name


class Print_Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), unique=False, nullable=False)
    when = db.Column(db.DateTime, unique=False, nullable=True)
    who = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Print Events %r>' % self.id

class Print_Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    print_ID = db.Column(db.Integer, unique=False) # reference print Id
    model_ID = db.Column(db.Integer, unique=False) # reference model Id
    setting_ID = db.Column(db.Integer, unique=False) # reference setting Id?
    core = db.Column(db.Integer, unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Print Settings %r>' % self.id

class Print_Models(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    print_ID = db.Column(db.Integer, unique=False) # reference print Id
    model_ID = db.Column(db.Integer, unique=False) # reference model Id
    
    def __repr__(self):
        return '<Print Models %r>' % self.id

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Settings %r>' % self.name

class Print_Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    print_ID = db.Column(db.Integer, unique=False) # reference print Id
    workers_ID = db.Column(db.Integer, unique=False) # reference worker Id
    when = db.Column(db.DateTime, unique=False, nullable=True)
    message = db.Column(db.String(180), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Print Comments %r>' % self.id

class Project_Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_ID = db.Column(db.Integer, unique=False) # reference project Id
    workers_ID = db.Column(db.Integer, unique=False) # reference worker Id
    when = db.Column(db.DateTime, unique=False, nullable=True)
    message = db.Column(db.String(180), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Project Comments %r>' % self.id

class Model_Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_ID = db.Column(db.Integer, unique=False) # reference model Id
    workers_ID = db.Column(db.Integer, unique=False) # reference worker Id
    when = db.Column(db.DateTime, unique=False, nullable=True)
    message = db.Column(db.String(180), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Model Comments %r>' % self.id

