# MainWindowEx.py
import os, glob, joblib, numpy as np
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt6.QtGui import QDoubleValidator
from MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("House Price Prediction (PyQt6)")
        self.pushButton.setText("Predict")
        self.lineEdit_predict.setReadOnly(True)

        dv = QDoubleValidator(-1e12, 1e12, 8)
        for w in (self.lineEdit_incom, self.lineEdit_age,
                  self.lineEdit_rooms, self.lineEdit_bedrooms,
                  self.lineEdit_population):
            w.setValidator(dv)
            w.setPlaceholderText("0")

        self.pushButton.clicked.connect(self.on_predict)

        self.model = None
        self._load_model_auto()

    # --------- helpers ----------
    def _load_model_auto(self):
        """Ưu tiên nạp ./model/housingmodel.zip; sau đó là .zip mới nhất; cuối cùng hỏi chọn."""
        here = os.path.abspath(os.path.dirname(__file__))
        model_dir = os.path.join(here, "model")                # ví dụ D:/.../model
        os.makedirs(model_dir, exist_ok=True)

        # 1) Ưu tiên tên cố định
        preferred = os.path.join(model_dir, "housingmodel.zip")
        if os.path.isfile(preferred):
            path = preferred
        else:
            # 2) Nếu không có, lấy file .zip mới nhất trong model/
            zips = sorted(glob.glob(os.path.join(model_dir, "*.zip")))
            path = zips[-1] if zips else None

        # 3) Nếu vẫn không có, hỏi người dùng
        if path is None:
            path, _ = QFileDialog.getOpenFileName(
                self, "Select trained model (.zip)", model_dir, "Model (*.zip)"
            )
            if not path:
                QMessageBox.information(self, "Info", "No model selected.")
                return

        # Load
        try:
            self.model = joblib.load(path)
            self.statusBar().showMessage(f"Loaded model: {os.path.basename(path)}", 4000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model:\n{e}")

    def _f(self, le):
        t = le.text().strip()
        return float(t) if t else 0.0

    # --------- actions ----------
    def on_predict(self):
        if self.model is None:
            QMessageBox.warning(self, "Warning", "Please load/train a model first.")
            self._load_model_auto()
            if self.model is None:
                return

        x = np.array([[
            self._f(self.lineEdit_incom),
            self._f(self.lineEdit_age),
            self._f(self.lineEdit_rooms),
            self._f(self.lineEdit_bedrooms),
            self._f(self.lineEdit_population),
        ]], dtype=float)

        try:
            y = self.model.predict(x)[0]
            self.lineEdit_predict.setText(f"{y:,.2f}")
            self.statusBar().showMessage("Predicted successfully", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Prediction failed:\n{e}")
