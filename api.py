import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [800, 600]


class Example(QWidget):
    def __init__(self, lon, lat):
        super().__init__()
        self.lon = f'{lat}'
        self.lat = f'{lon}'
        self.getImage()
        self.initUI()

    def getImage(self):
        import requests
        api_server = "http://static-maps.yandex.ru/1.x/"

        lon = self.lon
        lat = self.lat
        delta = "0.2"

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coords = [float(elem) for elem in input().split(', ')]

    ex = Example(coords[0], coords[1])
    ex.show()
    sys.exit(app.exec())
