from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xaagfwyhzyjsie:06b98075fe92384fad58910290d15b278f986113004378844026f7ea6a5b92ae@ec2-52-73-199-211.compute-1.amazonaws.com:5432/d63cpvol791v98'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String(200), unique=True)
    professor = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, student, professor, rating, comments):
        self.student = student
        self.professor = professor
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        student = request.form['student']
        professor = request.form['professor']
        rating = request.form['rating']
        comments = request.form['comments']

        if student == '' or professor == '':
            return render_template('index.html', message='Please enter required fields')

        if db.session.query(Feedback).filter(Feedback.student == student).count() == 0:
            data = Feedback(student, professor, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')

if __name__ == '__main__':
    
    app.run()