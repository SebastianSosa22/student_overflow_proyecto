from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask_jwt_extended import create_access_token
from .models import db, User, Question, Answer
from .forms import LoginForm, SignupForm, QuestionForm, AnswerForm
from . import bcrypt

main = Blueprint('main', __name__)


@main.route('/')
# @login_required
def home():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)


@main.route('/ask_question')
# @login_required
def ask_question():
    questions = Question.query.all()
    return render_template('ask_question.html', questions=questions)


@main.route('/answer')
# @login_required
def answer():
    questions = Question.query.all()
    return render_template('answer.html', questions=questions)


@main.route('/profile')
# @login_required
def profile():
    questions = Question.query.all()
    return render_template('profile.html', questions=questions)


@main.route('/settings')
# @login_required
def settings():
    questions = Question.query.all()
    return render_template('settings.html', questions=questions)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            try:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    access_token = create_access_token(
                        identity={'username': user.username, 'role': user.role})
                    return redirect(url_for('main.home'))
                else:
                    return jsonify({"msg": "Bad username or password"}), 401
            except ValueError as e:
                print(f"Error checking password hash: {e}")
                return jsonify({"msg": "Invalid password hash"}), 500
        else:
            return redirect(url_for('main.login'))
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Generar el hash de la contraseña
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        # Crear un nuevo usuario con el hash de la contraseña
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password, role='standard')

        # Agregar el nuevo usuario a la base de datos
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/ask', methods=['GET', 'POST'])
# @login_required
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
# @login_required
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
