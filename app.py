from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = 'stu'
    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String)
    name = db.Column(db.String)
    sem = db.Column(db.String)
    branch = db.Column(db.String)


    def __init__(self, usn, name, sem, branch):
        self.usn = usn
        self.name = name
        self.sem = sem
        self.branch = branch

class AddRecord(FlaskForm):
    
    id_field = HiddenField() 
    usn = StringField('usn')
    name = StringField('name')
    sem = SelectField('Choose the semester',
        choices=[ (''), ('1'),
        ('2'),
        ('3'),
        ('4'),('5'),('6'),('7'),('8') ])
    branch = StringField('branch')
    updated = HiddenField()
    submit = SubmitField('Add/Update Record')

@app.route('/')
def index():
    # get a list of unique values in the style column
    sem = Student.query.with_entities(Student.sem).distinct()
    return render_template('index.html', sem=sem)

@app.route('/inventory/<sem>')
def inventory(sem):
    new = Student.query.filter_by(sem=sem).order_by(Student.name).all()
    return render_template('list.html', new = new, sem=sem)

@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form1 = AddRecord()
    if form1.validate_on_submit():
        usn = request.form['usn']
        name = request.form['name']
        sem = request.form['sem']
        branch = request.form['branch']
        record = Student( usn, name, sem, branch)
        db.session.add(record)
        db.session.commit()
        message = f"The data for Student {name} has been submitted."
        return render_template('add_record.html', message=message)
    else:
        return render_template('add_record.html', form1=form1)


if __name__=="__main__":
    app.run(debug = True)
        