from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask_jwt_extended import create_access_token
from .models import db, User, Question, Answer
from .forms import LoginForm, SignupForm, QuestionForm, AnswerForm
from . import bcrypt


main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    questions = Question.query.all()
    return render_template('home.html', questions=questions)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(form)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            access_token = create_access_token(
                identity={'username': user.username, 'role': user.role})
            print(access_token)
            return redirect(url_for('main.home'))
        # jsonify(access_token=access_token), 200
        return jsonify({"msg": "Bad username or password"}), 401
    return render_template('login.html', form=form)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password, role='standard')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = QuestionForm()
    if form.validate_on_submit():
        new_question = Question(title=form.title.data,
                                content=form.content.data, author=current_user)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('ask.html', form=form)


@main.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question(question_id):
    question = Question.query.get_or_404(question_id)
    form = AnswerForm()
    if form.validate_on_submit():
        new_answer = Answer(content=form.content.data,
                            question=question, author=current_user)
        db.session.add(new_answer)
        db.session.commit()
        return redirect(url_for('main.question', question_id=question.id))
    return render_template('question.html', question=question, form=form)
