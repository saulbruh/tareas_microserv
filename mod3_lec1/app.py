from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Necesaria para sesiones

usuarios = {
    'admin': {'password': 'admin123', 'rol': 'Administrador'},
    'juan': {'password': 'juanpass', 'rol': 'Usuario'},
    'maria': {'password': 'mariapass', 'rol': 'Editor'}
}

@app.route('/')
def dashboard():
    if 'usuario' in session:
        return render_template('index.html', usuario=session['usuario'], rol=session['rol'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = usuarios.get(username)
        if user and user['password'] == password:
            session['usuario'] = username
            session['rol'] = user['rol']
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)