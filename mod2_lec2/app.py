from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"
app.config["TEMPLATES_AUTO_RELOAD"] = True

class RegisterForm(FlaskForm):
    username = StringField("Nombre de Usuario", validators=[
      DataRequired(message="El nombre es obligatorio."),
      Length(min=3, message="El nombre debe tener al menos 3 caracteres.")
    ])
    
    email = EmailField("Correo Electrónico", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Debe ingresar un correo válido.")
    ])
    
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ])
    
    submit = SubmitField("Registrarse")

@app.route("/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return f"Usuario registrado: {form.username.data}, Correo: {form.email.data}"
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
