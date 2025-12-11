import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_muy_dificil'
    
    # Configuración de la base de datos
    # Por defecto SQLite (más fácil para desarrollo local)
    # En Docker usaremos la variable de entorno para PostgreSQL/MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///notes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False