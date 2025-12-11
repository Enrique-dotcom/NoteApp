# init_db.py

from app import app, db
from app import User, Note # Importa tus modelos si app.py no los importa explícitamente

print("Intentando crear tablas de la base de datos...")
with app.app_context():
    try:
        db.create_all()
        print("Tablas creadas exitosamente o ya existían.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
        print("Asegúrate de que el contenedor de la base de datos esté accesible.")