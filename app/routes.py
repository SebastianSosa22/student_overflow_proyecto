from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, Question, Answer
from .forms import LoginForm, SignupForm, QuestionForm, AnswerForm


from . import create_app
app = create_app()

@app.route('/')
def home():
    print("Home route accessed")
    questions = Question.query.all()
    return render_template('home.html', questions=questions)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('ask.html', form=form)

@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    question = Question.query.get_or_404(id)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(content=form.content.data, question_id=id, user_id=current_user.id)
        db.session.add(answer)
        db.session.commit()
    answers = Answer.query.filter_by(question_id=id).all()
    return render_template('question.html', question=question, answers=answers, form=form)