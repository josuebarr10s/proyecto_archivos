import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QColor, QPalette
from gif_reader import GIFReader
from data_manager import load_gif_data, save_gif_data

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenida")
        self.setGeometry(100, 100, 800, 600)  # Tamaño igual que la ventana principal

        # Layout principal
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Colores y estilo
        self.setStyleSheet("background-color: #f5f5f5;")

        # Título de la aplicación
        title_label = QLabel("ANALIZADOR DE GIF")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #333333;")
        layout.addWidget(title_label)

        # Nombres de los integrantes
        members_label = QLabel("Integrantes del Grupo:\nJosue Barrios\nJulio Caceres")
        members_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        members_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        members_label.setStyleSheet("color: #666666; margin: 20px;")
        layout.addWidget(members_label)

        # Botón para continuar
        continue_button = QPushButton("Continuar")
        continue_button.clicked.connect(self.continue_to_main)
        continue_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(continue_button)

    def continue_to_main(self):
        self.main_window = MainWindow()  # Crea la ventana principal
        self.main_window.show()  # Muestra la ventana principal
        self.close()  # Cierra la ventana de bienvenida

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIF Data Extractor")
        self.setGeometry(100, 100, 800, 600)  # Tamaño igual que la ventana de bienvenida

        # Datos cargados de GIF
        self.gif_data = load_gif_data()
        self.current_gif_path = None  # Ruta del GIF actualmente seleccionado

        self.initUI()

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStyleSheet("background-color: #fafafa;")

        # Botón para seleccionar archivos GIF
        self.select_files_button = QPushButton("Seleccionar Archivos GIF")
        self.select_files_button.clicked.connect(self.select_files)
        self.select_files_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(self.select_files_button)

        # Lista de archivos GIF seleccionados
        self.gif_list = QListWidget()
        self.gif_list.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #ddd;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.gif_list)

        # Botón para analizar el archivo GIF seleccionado
        self.analyze_button = QPushButton("Analizar GIF")
        self.analyze_button.clicked.connect(self.analyze_gif)
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #17A2B8;
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        layout.addWidget(self.analyze_button)

        # Área para mostrar el GIF seleccionado
        self.gif_display = QLabel("Vista previa del GIF")
        self.gif_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gif_display.setStyleSheet("background-color: #EEEEEE; border: 1px solid #ccc; padding: 20px;")
        layout.addWidget(self.gif_display)

        # Etiqueta para mostrar la información del GIF
        self.gif_info_label = QLabel("Información del GIF")
        self.gif_info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.gif_info_label.setStyleSheet("color: #333333; font-size: 14px; margin: 10px;")
        layout.addWidget(self.gif_info_label)

        # Campos para editar información
        edit_layout = QHBoxLayout()
        self.edit_comment = QLineEdit()
        self.edit_comment.setPlaceholderText("Editar comentario")
        self.edit_comment.setStyleSheet("padding: 5px; border: 1px solid #ddd; font-size: 14px;")
        self.save_button = QPushButton("Guardar Cambios")
        self.save_button.clicked.connect(self.save_changes)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        edit_layout.addWidget(self.edit_comment)
        edit_layout.addWidget(self.save_button)
        layout.addLayout(edit_layout)

    def select_files(self):
        # Permite seleccionar múltiples archivos GIF desde el explorador de archivos
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos GIF", "", "GIF Files (*.gif)")
        if file_paths:
            self.load_gif_files(file_paths)

    def load_gif_files(self, file_paths):
        # Limpiamos la lista antes de cargar nuevos archivos
        self.gif_list.clear()
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
    welcome_window = WelcomeWindow()  # Muestra la ventana de bienvenida
    welcome_window.show()
    sys.exit(app.exec())
