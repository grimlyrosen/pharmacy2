from operator import imod
import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

def load_map( x=37.597784, y=54.193923, zoom=17, type='map'):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={x},{y}&z={z}&l={type}".format(x=x, y=y,type=type, z=zoom)
    print(map_request)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запись полученного изображения в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.x = QLineEdit(self)
        self.y = QLineEdit(self)
        self.zoom = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("x", self.x)
        layout.addRow("y", self.y)
        layout.addRow("Масштаб", self.zoom)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        load_map( x=float(self.x.text()), y=float(self.y.text()), zoom=int(self.zoom.text()), type='map')
        return (self.x.text(), self.y.text(), self.zoom.text())
    
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Вывод карты'
        self.left = 200
        self.top = 200
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('map.png')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    while True:
        dialog = InputDialog()
        dialog_result = dialog.exec()
        if dialog_result:
            print(dialog.getInputs())
        else:
            sys.exit()            
        ex = App()
        print(app.exec_())
        