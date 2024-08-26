import logging
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_user, login_required, logout_user, current_user
from .models import db, User, Question, Answer
from .forms import LoginForm, SignupForm, AnswerForm
from . import bcrypt

# Definir el blueprint para las rutas principales
main = Blueprint('main', __name__)


def format_time_diff(time_diff):
    """
    Calcula la diferencia de tiempo entre la fecha actual y una dada,
    devolviendo un texto amigable para el usuario.
    """
    days, seconds = time_diff.days, time_diff.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 365:
        return f"hace {days // 365} años"
    if days > 30:
        return f"hace {days // 30} meses"
    if days > 0:
        return f"hace {days} días"
    if hours > 0:
        return f"hace {hours} horas"
    if minutes > 0:
        return f"hace {minutes} minutos"
    return "hace unos segundos"


@main.before_request
def before_request():
    """
    Guarda en la sesión los datos del usuario autenticado antes de cada petición.
    Esto asegura que la sesión contenga la información actualizada del usuario.
    """
    if current_user.is_authenticated:
        session['username'] = current_user.username
        session['email'] = current_user.email
        session['id'] = current_user.id


@main.route('/')
@login_required  # Requiere que el usuario esté autenticado
def home():
    """
    Muestra la página principal con una lista paginada de preguntas.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 10
    questions = Question.query.paginate(page, per_page, error_out=False)
    now = datetime.utcnow()

    # Añadir formato de tiempo y etiquetas a cada pregunta
    for question in questions.items:
        question.time_ago = format_time_diff(
            now - question.created_at) if question.created_at else "Fecha no disponible"
        question.tags = question.tags or []

    return render_template('index.html', questions=questions.items, pagination=questions)


@main.route('/ask_question', methods=['GET', 'POST'])
@login_required  # Requiere que el usuario esté autenticado
def ask_question():
    """
    Permite a los usuarios hacer una nueva pregunta.
    """
    if request.method == 'POST':
        title = request.form.get('titulo')
        content = request.form.get('detalle')
        tags = request.form.get('etiquetas').split(',')

        # Verifica si el título y el contenido cumplen con los requisitos
        if title and len(content) > 20:
            new_question = Question(
                title=title, content=content, creator=current_user, tags=tags)
            db.session.add(new_question)
            db.session.commit()
            return redirect(url_for('main.home'))

    return render_template('ask_question.html')


@main.route('/profile')
@login_required  # Requiere que el usuario esté autenticado
def profile():
    """
    Muestra el perfil del usuario con todas las preguntas realizadas por él.
    """
    return render_template('profile.html', questions=Question.query.filter_by(user_id=current_user.id).all())


@main.route('/settings')
@login_required  # Requiere que el usuario esté autenticado
def settings():
    """
    Muestra la página de configuración del usuario.
    """
    return render_template('settings.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Permite a los usuarios iniciar sesión en la plataforma.
    """
    form = LoginForm()
    if form.validate_on_submit():
        # Buscar al usuario por email o nombre de usuario
        user = User.query.filter((User.email == form.email.data) | (
            User.username == form.email.data)).first()
        # Verificar contraseña
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        error = "Correo o contraseña incorrectos. Por favor, intenta de nuevo."
        return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def signup():
    """
    Permite a nuevos usuarios registrarse en la plataforma.
    """
    form = SignupForm()
    if form.validate_on_submit():
        # Crear un nuevo usuario con contraseña cifrada
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password, role='standard')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/logout')
@login_required  # Requiere que el usuario esté autenticado
def logout():
    """
    Cierra la sesión del usuario actual y redirige a la página de login.
    """
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required  # Requiere que el usuario esté autenticado
def question(question_id):
    """
    Muestra una pregunta específica junto con sus respuestas.
    Permite a los usuarios agregar nuevas respuestas.
    """
    question = Question.query.get_or_404(question_id)

    return render_template('question.html', question=question)


# Configura el logger
logging.basicConfig(level=logging.DEBUG)


@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    """
    Permite a los usuarios responder a una pregunta específica.
    """
    question = Question.query.get_or_404(question_id)
    form = AnswerForm()

    if form.validate_on_submit():
        try:
            new_answer = Answer(content=form.content.data,
                                question=question, author=current_user)
            db.session.add(new_answer)
            db.session.commit()
            return redirect(url_for('main.question', question_id=question.id))
        except Exception as e:
            db.session.rollback()
            # Registra el error
            logging.error(f"Ocurrió un error al guardar la respuesta: {e}")
            error_message = "Ocurrió un error al guardar tu respuesta. Por favor, inténtalo de nuevo."
            return render_template('answer.html', question=question, form=form, error=error_message)

    # Registro de depuración
    logging.debug(f"Formulario enviado: {form.validate_on_submit()}")
    return render_template('answer.html', question=question, form=form)


# @main.route('/tags', methods=['GET'])
# @login_required
# def get_tags():
#     """
#     Devuelve las etiquetas existentes en la base de datos en formato JSON.
#     """
#     tags = Tags.query.all()  # Asegúrate de que el modelo Tag esté importado
#     tag_names = [tag.name for tag in tags]
#     return jsonify(tag_names)
