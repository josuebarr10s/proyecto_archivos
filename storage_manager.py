import json
import os


def guardar_informacion(info, archivo_salida):
    try:
        with open(archivo_salida, 'w') as archivo:
            json.dump(info, archivo, indent=4)
    except Exception as e:
        print(f"Error guardando la información: {e}")


def cargar_informacion(archivo_salida):
    if os.path.isfile(archivo_salida):
        try:
            with open(archivo_salida, 'r') as archivo:
                return json.load(archivo)
        except Exception as e:
            print(f"Error cargando la información: {e}")
    return {}
