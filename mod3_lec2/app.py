from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity

app = Flask(__name__)
app.secret_key = '1234'

# Login y usuarios
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Principal para permisos
principals = Principal(app)

# Usuarios simulados
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

users = {
    'admin': User('1', 'admin', 'admin'),
    'user': User('2', 'user', 'user')
}

def get_user(username):
    return users.get(username)

# Cargar usuario en sesión
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

# Permisos
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

# Identidad cargada -> asignar roles
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    user = get_user(current_user.username) if current_user.is_authenticated else None
    if user:
        identity.provides.add(RoleNeed(user.role))
        identity.user = user

# Rutas

@app.route('/')
def index():
    return 'Página pública. Usa /login con {"username": "admin"} o {"username": "user"}'

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    user = get_user(username)
    if user:
        login_user(user)
        identity_changed.send(app, identity=Identity(user.id))
        return jsonify({"message": f"{user.username} logueado como {user.role}"}), 200
    return jsonify({"message": "Credenciales inválidas"}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    return jsonify({"message": "Sesión cerrada"}), 200

@app.route('/admin')
@login_required
@admin_permission.require(http_exception=403)
def admin_area():
    return jsonify({"message": f"Bienvenido, Admin {current_user.username}!"})

@app.route('/user')
@login_required
@user_permission.require(http_exception=403)
def user_area():
    return jsonify({"message": f"Bienvenido, Usuario {current_user.username}!"})

if __name__ == '__main__':
    app.run(debug=True)