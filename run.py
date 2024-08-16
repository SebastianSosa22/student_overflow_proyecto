from app import create_app
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde .env
load_dotenv()

# Configurar la aplicación para usar el entorno de desarrollo o producción
env = os.getenv('FLASK_ENV', 'development')

if env == 'development':
    app = create_app()
    app.config['DEBUG'] = True
else:
    app = create_app()
    app.config['DEBUG'] = False

if __name__ == '__main__':
    app.run()
