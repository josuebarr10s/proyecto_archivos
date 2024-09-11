def leer_gif(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        # Verificar que se puede leer el archivo correctamente
        if len(data) < 6:
            raise ValueError("El archivo parece estar dañado o incompleto.")


        if data[:6] == b'GIF89a':
            version = 'GIF89a'
        elif data[:6] == b'GIF87a':
            version = 'GIF87a'
        else:
            version = 'Desconocido'

        gif_info = {
            'version': version,
            'tamaño_imagen': (None, None),  # Ejemplo de tamaño
            'cantidad_colores': None,
            'tipo_compresion': None,
            'color_fondo': None,
            'cantidad_imagenes': None,
            'fecha_creacion': None,
            'fecha_modificacion': None,
            'comentarios': None
        }

        return gif_info
    except Exception as e:
        print(f"Error leyendo el archivo {file_path}: {e}")
        return None
