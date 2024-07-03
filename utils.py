import os

def read_directories_from_file(file_path):
    directories = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                directory = line.strip()
                if os.path.isdir(directory):
                    directories.append(directory)
                else:
                    print(f"Directorio no válido: {directory}")
    except FileNotFoundError:
        print(f"Archivo no encontrado: {file_path}")
    return directories

def get_serial_number(file_path):
    try:
        with open(file_path, 'r') as f:
            serial = f.read().strip()
            return serial
    except FileNotFoundError:
        print(f"Archivo de número de serie no encontrado: {file_path}")
        return None

# Otras funciones de utilidades según sea necesario
