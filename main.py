import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from gif_reader import GIFReader
from data_manager import load_gif_data, save_gif_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIF Data Extractor")
        self.setGeometry(100, 100, 800, 600)

        # Datos cargados de GIF
        self.gif_data = load_gif_data()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Botón para seleccionar carpeta
        self.select_folder_button = QPushButton("Seleccionar Carpeta")
        self.select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_button)

        # Lista de archivos GIF encontrados
        self.gif_list = QListWidget()
        self.gif_list.itemClicked.connect(self.display_gif_data)
        layout.addWidget(self.gif_list)

        # Etiquetas y cuadros de edición
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

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder_path:
            self.load_gif_files(folder_path)

    def load_gif_files(self, folder_path):
        self.gif_list.clear()
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.lower().endswith('.gif'):
                    file_path = os.path.join(root, file_name)
                    self.gif_list.addItem(file_path)

    def display_gif_data(self, item):
        file_path = item.text()
        reader = GIFReader(file_path)
        reader.read_gif()
        data = reader.get_data()
        self.current_gif_path = file_path
        self.gif_data[file_path] = data
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

    def save_changes(self):
        # Guarda los comentarios editados
        if self.current_gif_path in self.gif_data:
            self.gif_data[self.current_gif_path]['comments'] = self.edit_comment.text()
            save_gif_data(self.gif_data)
            self.display_gif_data(QListWidget().item(self.current_gif_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
