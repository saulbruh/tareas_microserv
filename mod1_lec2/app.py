from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta GET /info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'app': 'Servidor de Mensajes',
        'versión': '1.0',
        'autor': 'Tu Nombre'
    })

# Ruta POST /mensaje
@app.route('/mensaje', methods=['POST'])
def mensaje():
    data = request.get_json()
    
    if not data or 'mensaje' not in data:
        return jsonify({'error': 'Falta el campo "mensaje"'}), 400
    
    mensaje_usuario = data['mensaje']
    respuesta = f"Mensaje recibido: '{mensaje_usuario}'"
    
    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    app.run(debug=True)