from typing import Optional
from PySide6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        # Layout vertical principal
        self.cw = QWidget()
        self.vLayout = QVBoxLayout(self.cw)
        self.setCentralWidget(self.cw)

        # Título da janela
        self.setWindowTitle('Calculadora')

    def adjustFixedSize(self):
        # Impede redimensionamento da janela
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    def makeMsgBox(self) -> QMessageBox:
        return QMessageBox(self)

