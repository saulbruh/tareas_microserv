from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de recetas simulada
recetas = [
    {"nombre": "Tacos al Pastor", "descripcion": "Deliciosos tacos de cerdo marinado."},
    {"nombre": "Spaghetti Carbonara", "descripcion": "Pasta italiana con huevo, queso y panceta."},
    {"nombre": "Arepas", "descripcion": "Panecillos de maíz típicos de Venezuela y Colombia."}
]

@app.route("/")
def index():
    return render_template("index.html", recetas=recetas)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        if nombre and descripcion:
            recetas.append({"nombre": nombre, "descripcion": descripcion})
            return redirect(url_for("index"))
    return render_template("agregar.html")

@app.route("/eliminar/<int:indice>", methods=["POST"])
def eliminar(indice):
    if 0 <= indice < len(recetas):
        del recetas[indice]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)