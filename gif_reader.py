import struct
import os
import datetime

class GIFReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}

    def read_gif(self):
        with open(self.file_path, 'rb') as file:
            # Lee la versión
            self.data['version'] = file.read(6).decode('ascii')

            # Lee el ancho y alto de la imagen
            self.data['width'], self.data['height'] = struct.unpack('<HH', file.read(4))

            # Lee el campo de Packed para obtener la información de colores
            packed_byte = ord(file.read(1))
            self.data['global_color_table_flag'] = (packed_byte & 0b10000000) >> 7
            self.data['color_resolution'] = ((packed_byte & 0b01110000) >> 4) + 1
            self.data['sort_flag'] = (packed_byte & 0b00001000) >> 3
            self.data['size_of_global_color_table'] = 2 ** ((packed_byte & 0b00000111) + 1)

            # Lee el color de fondo y el ratio de aspecto
            self.data['background_color_index'] = ord(file.read(1))
            self.data['pixel_aspect_ratio'] = ord(file.read(1))

            # Obtiene la cantidad de colores, asumiendo que hay una tabla de color global
            if self.data['global_color_table_flag']:
                self.data['color_count'] = self.data['size_of_global_color_table']
            else:
                self.data['color_count'] = 0

            # Obtiene fechas del sistema de archivos (creación y modificación)
            file_stats = os.stat(self.file_path)
            self.data['creation_date'] = datetime.datetime.fromtimestamp(file_stats.st_ctime).strftime('%d-%m-%Y')
            self.data['modification_date'] = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%d-%m-%Y')

            # Simulación de cantidad de imágenes y comentarios (mejora en próximos pasos)
            self.data['image_count'] = 1  # Valor base, puede cambiar
            self.data['comments'] = "No comments"

    def get_data(self):
        return self.data
