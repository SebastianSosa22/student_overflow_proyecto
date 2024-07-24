# StudentOverflow

StudentOverflow es una aplicación web inspirada en StackOverflow que permite a los usuarios hacer preguntas sobre materias para que otros usuarios de la plataforma puedan ayudarlos.

## Características

- Registro y autenticación de usuarios.
- Publicación y edición de preguntas.
- Publicación y edición de respuestas.
- Votación de preguntas y respuestas.
- Comentarios en preguntas y respuestas.

## Requisitos

- Python 3.7 o superior
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/SebastianSosa22/student_overflow_proyecto.git
   cd studentoverflow
   ```

2.- Crea y activa un entorno virtual:

    python3 -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

3.- Instala las depencencias

    pip install -r requirements.txt

4.- Configura la base de datos:

    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade

## Configuración

Crea un archivo .env en el directorio raíz del proyecto y agrega las siguientes variables de entorno:

SECRET_KEY=tu_clave_secreta
DATABASE_URL=sqlite:///site.db

## Ejecución

Para ejecutar la aplicación localmente usa el siguiente comando:

    flask run

Luego, abre tu navegador y ve a http://localhost:5000.

## Estructura del Proyecto

studentoverflow/
│
├── app/
│ ├── **init**.py
│ ├── routes.py
│ ├── models.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── home.html
│ │ ├── login.html
│ │ ├── signup.html
│ │ ├── ask.html
│ │ └── question.html
│ └── static/
│ ├── styles.css
│ └── scripts.js
│
├── migrations/
│
├── venv/
│
├── .env
├── config.py
├── run.py
└── requirements.txt

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1.- Haz un fork del proyecto.
2.- Crea una nueva rama (git checkout -b feature/nueva-caracteristica).
3.- Haz commit de tus cambios (git commit -am 'Añade una nueva característica').
4.- Haz push a la rama (git push origin feature/nueva-caracteristica).
5.- Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.
