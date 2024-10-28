import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QLabel, QVBoxLayout, QWidget, \
    QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from gif_reader import GIFReader
from data_manager import load_gif_data, save_gif_data


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIF Data Extractor")
        self.setGeometry(100, 100, 800, 600)

        # Datos cargados de GIF
        self.gif_data = load_gif_data()
        self.current_gif_path = None  # Ruta del GIF actualmente seleccionado

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Botón para seleccionar archivos GIF
        self.select_files_button = QPushButton("Seleccionar Archivos GIF")
        self.select_files_button.clicked.connect(self.select_files)
        layout.addWidget(self.select_files_button)

        # Lista de archivos GIF seleccionados
        self.gif_list = QListWidget()
        layout.addWidget(self.gif_list)

        # Botón para analizar el archivo GIF seleccionado
        self.analyze_button = QPushButton("Analizar GIF")
        self.analyze_button.clicked.connect(self.analyze_gif)
        layout.addWidget(self.analyze_button)

        # Área para mostrar el GIF seleccionado
        self.gif_display = QLabel("Vista previa del GIF")
        self.gif_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.gif_display)

        # Etiqueta para mostrar la información del GIF
        self.gif_info_label = QLabel("Información del GIF")
        self.gif_info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.gif_info_label)

        # Campos para editar información
        edit_layout = QHBoxLayout()
        self.edit_comment = QLineEdit()
        self.edit_comment.setPlaceholderText("Editar comentario")
        self.save_button = QPushButton("Guardar Cambios")
        self.save_button.clicked.connect(self.save_changes)
        edit_layout.addWidget(self.edit_comment)
        edit_layout.addWidget(self.save_button)
        layout.addLayout(edit_layout)

        # Configuración del layout en el widget principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_files(self):
        # Permite seleccionar múltiples archivos GIF desde el explorador de archivos
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos GIF", "", "GIF Files (*.gif)")
        if file_paths:
            self.load_gif_files(file_paths)

    def load_gif_files(self, file_paths):
        self.gif_list.clear()  # Limpiamos la lista antes de cargar nuevos archivos
        for file_path in file_paths:
            if file_path.lower().endswith('.gif'):
                self.gif_list.addItem(file_path)

    def analyze_gif(self):
        # Verifica si hay un archivo seleccionado en la lista
        selected_item = self.gif_list.currentItem()
        if selected_item:
            file_path = selected_item.text()
            reader = GIFReader(file_path)
            reader.read_gif()
            data = reader.get_data()
            self.current_gif_path = file_path
            self.gif_data[file_path] = data

            # Mostrar el GIF en la interfaz
            self.display_gif(file_path)

            # Muestra la información en la etiqueta
            gif_info = (
                f"Archivo: {os.path.basename(file_path)}\n"
                f"Versión: {data['version']}\n"
                f"Ancho: {data['width']} px\n"
                f"Alto: {data['height']} px\n"
                f"Color de Fondo: {data['background_color_index']}\n"
                f"Resolución de Color: {data['color_resolution']}\n"
                f"Tamaño Tabla de Color: {data['size_of_global_color_table']} colores\n"
                f"Comentarios: {data['comments']}\n"
            )
            self.gif_info_label.setText(gif_info)
            self.edit_comment.setText(data['comments'])
        else:
            self.gif_info_label.setText("Por favor, selecciona un archivo GIF para analizar.")

    def display_gif(self, file_path):
        # Cargar y mostrar la imagen GIF en el QLabel
        pixmap = QPixmap(file_path)
        self.gif_display.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))

    def save_changes(self):
        # Guarda los comentarios editados
        if self.current_gif_path in self.gif_data:
            self.gif_data[self.current_gif_path]['comments'] = self.edit_comment.text()
            save_gif_data(self.gif_data)
            self.gif_info_label.setText("Cambios guardados correctamente.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
