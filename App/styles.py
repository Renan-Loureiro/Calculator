import qdarkstyle
from variables import (
    PRIMARY_COLOR, DARKER_PRIMARY_COLOR,DARKEST_PRIMARY_COLOR
    )

qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
        border-radius: 5px;
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}"""

def setupTheme(app):
    try:
        print('Carregando qdarkstyle...')
        darkstyle = qdarkstyle.load_stylesheet()
        app.setStyleSheet(darkstyle + qss)
        print('Tema aplicado com sucesso.')
    except Exception as e:
        print(f'Erro ao aplicar tema: {e}')

