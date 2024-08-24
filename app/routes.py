from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_user, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token
from .models import db, User, Question, Answer
from .forms import LoginForm, SignupForm, QuestionForm, AnswerForm
from . import bcrypt

main = Blueprint('main', __name__)


def format_time_diff(time_diff):
    days = time_diff.days
    seconds = time_diff.seconds

    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        if days == 1:
            return "hace 1 día"
        elif days < 30:
            return f"hace {days} días"
        elif days < 365:
            return f"hace {days // 30} meses"
        else:
            return f"hace {days // 365} años"
    elif hours > 0:
        return f"hace {hours} horas"
    elif minutes > 0:
        return f"hace {minutes} minutos"
    else:
        return "hace unos segundos"


@main.before_request
def before_request():
    if current_user.is_authenticated:
        session['username'] = current_user.username
        session['email'] = current_user.email


@main.route('/')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Número de preguntas por página
    questions = Question.query.paginate(page, per_page, error_out=False)
    now = datetime.utcnow()
    for question in questions.items:
        if question.created_at:
            time_diff = now - question.created_at
            print(f"Pregunta ID: {question.id}, Created At: {
                  question.created_at}, Time Diff: {time_diff}")
            question.time_ago = format_time_diff(time_diff)
        else:
            question.time_ago = "Fecha no disponible"

        # Asegúrate de que 'tags' es una lista
        if question.tags is None:
            question.tags = []

    return render_template('index.html', questions=questions.items, pagination=questions)


@main.route('/ask_question', methods=['GET', 'POST'])
@login_required
def ask_question():
    if request.method == 'POST':
        title = request.form.get('titulo')
        content = request.form.get('detalle')
        tags = request.form.get('etiquetas').split(
            ',')  # Convertir las etiquetas en una lista

        if len(title) > 0 and len(content) > 20:  # Validaciones básicas
            new_question = Question(
                title=title,
                content=content,
                creator=current_user,
                tags=tags
            )
            db.session.add(new_question)
            db.session.commit()
            # Redirigir a la página principal o a otra página
            return redirect(url_for('main.home'))

    # Asegúrate de que el nombre del template es correcto
    return render_template('ask_question.html')


@main.route('/answer')
@login_required
def answer():
    questions = Question.query.all()
    return render_template('answer.html', questions=questions)


@main.route('/profile')
@login_required
def profile():
    questions = Question.query.all()
    return render_template('profile.html', questions=questions)


@main.route('/settings')
@login_required
def settings():
    questions = Question.query.all()
    return render_template('settings.html', questions=questions)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first(
        ) or User.query.filter_by(username=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            access_token = create_access_token(
                identity={'username': user.username, 'role': user.role})
            return redirect(url_for('main.home'))
        else:
            error = "Correo o contraseña incorrectos. Por favor, intenta de nuevo."
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
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
    return render_template('register.html', form=form)


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
                                content=form.content.data, creator=current_user)
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
