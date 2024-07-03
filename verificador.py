# verificador.py

import os
import hashlib
import json
from db import DatabaseManager
from alert_manager import AlertManager
from utils import read_directories_from_file, get_serial_number

# Cargar configuraciones
with open('config/db_config.json', 'r') as f:
    config = json.load(f)

# Configuración de la base de datos
db_manager = DatabaseManager(config)

# Inicializar gestor de alertas
alert_manager = AlertManager(db_manager)

# Leer directorios a verificar
directories_to_check = read_directories_from_file('config/directories.txt')

# Obtener número de serie del equipo
serial_number = get_serial_number('C:/bios_serial.txt')

# Función principal de verificación
def verificar_archivos():
    for directory in directories_to_check:
        try:
            # Verificar archivos en el directorio
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calcular hash del archivo
                    file_hash = hashlib.sha256()
                    with open(file_path, 'rb') as f:
                        while chunk := f.read(4096):
                            file_hash.update(chunk)
                    file_hash = file_hash.hexdigest()

                    # Registrar archivo en la base de datos y gestionar alertas
                    alert_manager.check_file(directory, file, file_hash, serial_number)

        except Exception as e:
            print(f"Error al verificar archivos en {directory}: {e}")

# Ejecutar verificación al iniciar
if __name__ == "__main__":
    verificar_archivos()
