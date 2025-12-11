from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import markdown # <<< LIBRERÍA DE MARKDOWN

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# --- Modelos de Base de Datos ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # TAMAÑO CORREGIDO A 256
    password_hash = db.Column(db.String(256), nullable=False) 
    notes = db.relationship('Note', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

# --- Funciones de Ayuda (Decoradores) ---

def login_required(f):
    """Decorador para restringir el acceso a usuarios no autenticados."""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# --- Rutas de la Aplicación ---

## Rutas de Autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso. ¡Ahora puedes iniciar sesión!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('login'))

## Rutas de Notas
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_id = session['user_id']
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_note = Note(title=title, content=content, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()
        flash('Nota creada exitosamente.', 'success')
        return redirect(url_for('index'))

    notes = Note.query.filter_by(user_id=user_id).all()
    
    # CONVERSIÓN DE MARKDOWN A HTML
    for note in notes:
        note.html_content = markdown.markdown(note.content)

    return render_template('index.html', notes=notes)

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if note.user_id != session['user_id']:
        flash('No tienes permiso para editar esta nota.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        flash('Nota actualizada exitosamente.', 'success')
        return redirect(url_for('index'))

    return render_template('edit_note.html', note=note)

@app.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    # Seguridad: Asegurarse de que el usuario sea el dueño de la nota
    if note.user_id != session['user_id']:
        flash('No tienes permiso para ver esta nota.', 'danger')
        return redirect(url_for('index'))

    # Convertir el contenido a HTML para la vista detallada
    note.html_content = markdown.markdown(note.content)

    return render_template('view_note.html', note=note)

@app.route('/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if note.user_id != session['user_id']:
        flash('No tienes permiso para eliminar esta nota.', 'danger')
        return redirect(url_for('index'))

    db.session.delete(note)
    db.session.commit()
    flash('Nota eliminada exitosamente.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Línea comentada/modificada para corregir la vulnerabilidad B201 de Bandit
    # app.run(debug=True, host='0.0.0.0') 
    pass