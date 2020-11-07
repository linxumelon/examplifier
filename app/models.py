from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    identity = db.Column(db.String(16), default="Student")
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        print(password)
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Module(db.Model):
    __tablename__='module'
    code = db.Column(db.String(64), primary_key=True)
    def __repr__(self):
        return '<Module {}>'.format(self.code)

class Teaches(db.Model):
    __tablename__='teache'
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    instructor_name = db.Column(db.String(64), db.ForeignKey('user.username'))
    modcode = db.Column(db.String(64), db.ForeignKey('module.code'))  
    def __repr__(self):
        return '<Teaches {} {}>'.format(self.instructor_name, self.modcode)

class Takes(db.Model):
    __tablename__='take'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student_name = db.Column(db.String(64), db.ForeignKey('user.username'))
    modcode = db.Column(db.String(64), db.ForeignKey('module.code'), index=True)
    def __repr__(self):
        return '<Takes {} {} {}>'.format(self.student_id, self.student_name, self.modcode)


class TestPaper(db.Model):
    __tablename__='testpaper'
    id = db.Column(db.Integer, primary_key=True)
    modcode = db.Column(db.String(64), db.ForeignKey('module.code'), index=True)
    name = db.Column(db.String(64), index=True)
    def set_fileurl(self, url):
        self.fileurl = url
    def __repr__(self):
        return '<Test Paper {}>'.format(self.modcode)


class StudentSubmission(db.Model):
    __tablename__='studentsubmission'
    id = db.Column(db.Integer, primary_key=True)
    modcode = db.Column(db.String(64), db.ForeignKey('module.code'), index=True)
    studentid = db.Column(db.String(64))
    def __repr__(self):
        return '<Student Submission {} {}'.format(self.modcode, self.studentid)

# class NetStatistics(db.Model):
#     __table__ = 'netstatistics'
#     id = db.Column(db.Integer, primary_key=True)
#     studentid = db.Column(db.String(64))
#     occurence = db.Column(db.Time)