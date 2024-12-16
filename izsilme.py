import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor


class PrivacyTool(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Golge Linux İz Silme Aracı")
        self.setGeometry(100, 100, 700, 500)

        # Arayüz elemanları
        self.initUI()

    def initUI(self):
        # Ana Layout
        main_layout = QVBoxLayout()

        # Log alanı
        self.log_text_edit = CustomQTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        main_layout.addWidget(self.log_text_edit)

        # Sonuç label'ı
        self.result_label = QLabel(self)
        main_layout.addWidget(self.result_label)

        # İlerleme çubuğu
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # Temizleme butonu
        self.clear_button = QPushButton("İzleri Temizle", self)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #6A1B9A; 
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #9C4D97;
            }
            QPushButton:pressed {
                background-color: #4A148C;
            }
        """)
        self.clear_button.clicked.connect(self.on_clear_button_click)
        main_layout.addWidget(self.clear_button)

        # Uygulama işleme arka planı
        self.worker = PrivacyWorker(self.log_text_edit, self.result_label, self.progress_bar)

        self.setLayout(main_layout)

    def on_clear_button_click(self):
        """İz silme butonuna tıklayınca çalışacak fonksiyon"""
        self.clear_button.setEnabled(False)  # Butonu devre dışı bırak
        self.worker.start()  # Arka planda işlemi başlat


class PrivacyWorker(QThread):
    progress_signal = pyqtSignal(int)  # İlerleme için sinyal
    log_signal = pyqtSignal(str)  # Log için sinyal
    result_signal = pyqtSignal(str)  # Sonuç için sinyal

    def __init__(self, log_text_edit, result_label, progress_bar):
        super().__init__()
        self.log_text_edit = log_text_edit
        self.result_label = result_label
        self.progress_bar = progress_bar

    def run(self):
        """Arka planda çalışacak iz silme işlemi"""
        self.clear_browser_history()
        self.clear_tor_history()
        self.clear_temp_files()

        self.result_signal.emit("İz silme işlemi tamamlandı.")
        self.progress_signal.emit(100)  # Tamamlandı

    def clear_browser_history(self):
        """Chromium ve Brave tarayıcı geçmişlerini temizler"""
        try:
            # Chromium geçmişi
            chromium_cache = os.path.expanduser("~/.cache/chromium/")
            if os.path.exists(chromium_cache):
                shutil.rmtree(chromium_cache)
                self.log_signal.emit("Chromium geçmişi silindi.")
                self.progress_signal.emit(33)

            # Brave geçmişi
            brave_cache = os.path.expanduser("~/.cache/brave-browser/")
            if os.path.exists(brave_cache):
                shutil.rmtree(brave_cache)
                self.log_signal.emit("Brave geçmişi silindi.")
                self.progress_signal.emit(66)

        except Exception as e:
            self.log_signal.emit(f"Tarayıcı geçmişi silinemedi: {e}")

    def clear_tor_history(self):
        """Tor geçmişini temizler"""
        try:
            tor_data_path = os.path.expanduser("~/.tor")
            tor_browser_path = os.path.expanduser("~/.local/share/torbrowser")

            if os.path.exists(tor_data_path):
                shutil.rmtree(tor_data_path)
                self.log_signal.emit(f"Tor geçmişi silindi: {tor_data_path}")
                self.progress_signal.emit(50)

            if os.path.exists(tor_browser_path):
                shutil.rmtree(tor_browser_path)
                self.log_signal.emit(f"Tor Browser geçmişi silindi: {tor_browser_path}")
                self.progress_signal.emit(75)

        except Exception as e:
            self.log_signal.emit(f"Tor geçmişi silinemedi: {e}")

    def clear_temp_files(self):
        """Geçici dosyaları temizler"""
        try:
            temp_dir = "/tmp"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                self.log_signal.emit(f"Sistem geçici dosyaları silindi: {temp_dir}")
                self.progress_signal.emit(100)
        except Exception as e:
            self.log_signal.emit(f"Sistem geçici dosyaları silinemedi: {e}")


class CustomQTextEdit(QTextEdit):
    """Logları daha düzenli gösterebilmek için özel QTextEdit"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #2C003E; color: white; font-family: Arial, sans-serif; font-size: 12px;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PrivacyTool()
    window.show()
    sys.exit(app.exec_())
