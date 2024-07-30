from app import create_app
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
