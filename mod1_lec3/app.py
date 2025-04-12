from flask import Flask, request, jsonify
import json

app = Flask(__name__)

with open('estructura_datos.json', 'r') as f:
    datos = json.load(f)

usuarios = datos['usuarios']

# Ruta GET /info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'app': 'Gestor de Usuarios',
        'versión': '1.0',
        'autor': 'Saul Medina'
    })

# Ruta POST /crear_usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No se envió ningún dato'}), 400

    nombre = data.get('nombre')
    correo = data.get('correo')

    if not nombre or not correo:
        return jsonify({'error': 'Se requieren los campos "nombre" y "correo"'}), 400

    nuevo_usuario = {
        'id': usuarios[-1]['id'] + 1 if usuarios else 1,
        'nombre': nombre,
        'correo': correo
    }
    usuarios.append(nuevo_usuario)

    datos['usuarios'] = usuarios
    with open('estructura_datos.json', 'w') as f:
        json.dump(datos, f, indent=2)

    return jsonify({'mensaje': 'Usuario creado exitosamente', 'usuario': nuevo_usuario}), 201

# Ruta GET /usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({'usuarios': usuarios})

if __name__ == '__main__':
    app.run(debug=True)
