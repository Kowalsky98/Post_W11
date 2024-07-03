from flask import Flask, request, jsonify
import json
from db import DatabaseManager

app = Flask(__name__)

# Cargar configuraciones
with open('config/db_config.json', 'r') as f:
    config = json.load(f)

# Configuración de la base de datos
db_manager = DatabaseManager(config)

@app.route('/alerts', methods=['POST'])
def create_alert():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        directory = data.get('directory')
        file_name = data.get('file_name')
        file_hash = data.get('file_hash')
        serial = data.get('serial')

        if not directory or not file_name or not file_hash or not serial:
            return jsonify({"error": "Missing data"}), 400

        db_manager.insert_alert(directory, file_name, file_hash, serial)
        return jsonify({"message": "Alert created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
