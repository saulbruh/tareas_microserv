from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class RegisterForm(FlaskForm):
    username = StringField("Nombre de Usuario", validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, message="El nombre debe tener al menos 3 caracteres.")
    ])
    email = StringField("Correo Electrónico", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Debe ser un correo válido.")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="Debe tener al menos 6 caracteres.")
    ])
    confirm_password = PasswordField("Confirmar Contraseña", validators=[
        DataRequired(message="Debes confirmar tu contraseña."),
        EqualTo("password", message="Las contraseñas deben coincidir.")
    ])
    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    email = StringField("Correo Electrónico", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Debe ser un correo válido.")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria.")
    ])
    submit = SubmitField("Iniciar Sesión")

class PostForm(FlaskForm):
    title = StringField("Título", validators=[
        DataRequired(message="El título es obligatorio."),
        Length(min=5, message="El título debe tener al menos 5 caracteres.")
    ])
    content = TextAreaField("Contenido", validators=[
        DataRequired(message="El contenido no puede estar vacío.")
    ])
    submit = SubmitField("Publicar")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Cuenta creada con éxito!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Inicio de sesión exitoso!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Publicación creada con éxito!', 'success')
        return redirect(url_for('home'))
    return render_template('post.html', form=form)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
