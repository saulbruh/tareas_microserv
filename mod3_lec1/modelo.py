from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simulación de base de datos de usuarios en memoria
usuarios = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'role': 'admin'
    },
    'juan': {
        'password': generate_password_hash('juan456'),
        'role': 'user'
    }
}

# Clase Usuario compatible con Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = usuarios[username]['role']

    def get_role(self):
        return self.role

@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return User(user_id)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and check_password_hash(usuarios[username]['password'], password):
            user = User(username)
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Bienvenido, {current_user.id}! Tu rol es: {current_user.get_role()}'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)