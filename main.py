import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QListWidget, QLabel,
    QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QMovie
from PIL import Image, ImageSequence

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenida")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setStyleSheet("background-color: #f5f5f5;")

        title_label = QLabel("ANALIZADOR DE GIF")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #333333;")
        layout.addWidget(title_label)

        members_label = QLabel("Integrantes del Grupo:\nJosue Barrios\nJulio Caceres")
        members_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        members_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        members_label.setStyleSheet("color: #666666; margin: 20px;")
        layout.addWidget(members_label)

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
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIF Data Extractor")
        self.setGeometry(100, 100, 800, 600)

        self.gif_data = self.load_gif_data()
        self.current_gif_path = None

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStyleSheet("background-color: #fafafa;")

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

        self.gif_list = QListWidget()
        self.gif_list.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #ddd;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.gif_list)

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

        self.gif_display = QLabel("Vista previa del GIF")
        self.gif_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gif_display.setStyleSheet("background-color: #EEEEEE; border: 1px solid #ccc; padding: 20px;")
        layout.addWidget(self.gif_display)

        self.gif_info_label = QLabel("Información del GIF")
        self.gif_info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.gif_info_label.setStyleSheet("color: #333333; font-size: 14px; margin: 10px;")
        layout.addWidget(self.gif_info_label)

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
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos GIF", "", "GIF Files (*.gif)")
        if file_paths:
            self.load_gif_files(file_paths)

    def load_gif_files(self, file_paths):
        self.gif_list.clear()
        for file_path in file_paths:
            if file_path.lower().endswith('.gif'):
                self.gif_list.addItem(file_path)

    def analyze_gif(self):
        selected_item = self.gif_list.currentItem()
        if selected_item:
            file_path = selected_item.text()
            self.current_gif_path = file_path
            data = self.read_gif_info(file_path)

            self.display_gif(file_path)

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

    def display_gif(self, file_path):
        movie = QMovie(file_path)
        self.gif_display.setMovie(movie)
        movie.start()

    def save_changes(self):
        if not self.current_gif_path:
            return

        new_comment = self.edit_comment.text()
        self.save_comment_to_gif(self.current_gif_path, new_comment)
        self.gif_info_label.setText("Cambios guardados correctamente.")

    def save_comment_to_gif(self, file_path, comment):
        with Image.open(file_path) as im:
            frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
            im.info['comment'] = comment.encode('utf-8')
            save_path, _ = QFileDialog.getSaveFileName(self, "Guardar GIF Modificado", "", "GIF Files (*.gif)")
            if save_path:
                frames[0].save(save_path, save_all=True, append_images=frames[1:], loop=0, duration=im.info['duration'], comment=comment)

    def load_gif_data(self):
        if os.path.exists("gif_comments.json"):
            with open("gif_comments.json", "r") as file:
                return json.load(file)
        return {}

    def read_gif_info(self, file_path):
        with Image.open(file_path) as im:
            return {
                "version": im.info.get("version", ""),
                "width": im.width,
                "height": im.height,
                "background_color_index": im.info.get("background", -1),
                "color_resolution": im.info.get("color_resolution", -1),
                "size_of_global_color_table": len(im.getpalette()) // 3 if im.getpalette() else 0,
                "comments": im.info.get("comment", b"").decode("utf-8")
            }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec())
