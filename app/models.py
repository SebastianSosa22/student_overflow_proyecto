from datetime import datetime  # Importa datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    # Usa un nombre único para evitar conflictos
    questions = db.relationship('Question', backref='creator', lazy=True)
    answers = db.relationship('Answer', backref='author', lazy=True)

    @property
    def is_active(self):
        return True


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_votes = db.Column(db.Integer, default=0)
    total_answers = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship(
        'User', backref=db.backref('user_questions', lazy=True))
    # Usando ARRAY para almacenar tags
    tags = db.Column(ARRAY(db.String), default=list)


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
