import math
from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import isEmpty, isNumOrDot, isValidNumber
from variables import MEDIUM_FONT_SIZE

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow


class Button(QPushButton): 
    def __init__(self, text: str):
        super().__init__(text) 
        self.configStyle()


    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow') -> None:
        super().__init__() 

        self._gridMask = [
            ['C', '⌫', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            [' ',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        for rowNumber, rowData in enumerate(self._gridMask):
            for colNumber, buttonText in enumerate(rowData):
                if isEmpty(buttonText):
                    continue

                button = Button(buttonText)

                if isNumOrDot(buttonText):
                    button.setProperty('cssClass', 'numberButton')
                    slot = self._makeSlot(self._insertButtonTextToDisplay, button)
                    self._connectButtonClicked(button, slot)
                else:
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                button.style().unpolish(button)
                button.style().polish(button)

                self.addWidget(button, rowNumber, colNumber)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)  # type: ignore

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        elif text == '⌫':
            if hasattr(self.display, 'backspace'):
                self._connectButtonClicked(button, self.display.backspace)

        elif text in '+-/*^':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._operatorClicked, button)
            )

        elif text == '=':
            self._connectButtonClicked(button, self._eq)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()

    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada.')
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = buttonText
        self.equation = f'{self._left} {self._op} ??'

    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showError('Conta incompleta.')
            return

        self._right = float(displayText)
        result = 'error'

        try:
            if self._op == '^':
                result = math.pow(self._left, self._right)
            else:
                expression = f'{self._left} {self._op} {self._right}'
                result = eval(expression)

        except ZeroDivisionError:
            self._showError('Divisão por zero.')
            result = 'error'
        except OverflowError:
            self._showError('Essa conta não pode ser realizada.')
            result = 'error'
        except Exception:
            self._showError('Erro desconhecido.')
            result = 'error'

        self.display.clear()

        if result == 'error':
            self._left = None
            self._op = None
            self.equation = self._equationInitialValue
            return

        self.info.setText(f'{self._left} {self._op} {self._right} = {result}')
        self._left = result
        self._right = None
        self._op = None

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
