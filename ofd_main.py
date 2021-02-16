import sqlite3
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PyQt5.QtCore import QSettings


# ======================================================

# виджеты
form_class = uic.loadUiType('qt.ui')[0]
find_class = uic.loadUiType('find.ui')[0]
way_class = uic.loadUiType('dbway.ui')[0]

# =====================================================
dbway = ''


# ====================================================


# Функция запуска браузера и входа в лк
def login_OFD(logn, pas):
    driver = webdriver.Chrome()

    driver.get("https://lk.platformaofd.ru/web/login")
    login = driver.find_element_by_name("j_username")
    login.clear()
    login.send_keys(logn)
    pwd = driver.find_element_by_name("j_password")
    pwd.send_keys(pas)
    pwd.send_keys(Keys.RETURN)


# Основное окно
class MainWindowClass(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        global dbway
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.AddBtn.clicked.connect(self.add_Btn)
        self.FndBtn.clicked.connect(self.find_Btn)
        self.stButton.clicked.connect(self.stng_Btn)

        # Загружаем путь к базе
        s = QSettings('settings.ini', QSettings.IniFormat) # Обозначаем название файла с настройками
        dbway = s.value('way_to_db', type=str) # Принимаем значение way_to_db из ini файла в переменную
        print(dbway)

    def stng_Btn(self):
        DbWay(self).show()

    # кнопка добавления данных в бд
    def add_Btn(self):
        global dbway
        if self.OrgLine.text() == '':
            self.sucsLabel.setText('Error org')
        elif self.LoginLine.text() == '()':
            self.sucsLabel.setText('Error login')
        elif self.PassLine.text() == '':
            self.sucsLabel.setText('Error pass')
        else:
            line = [self.OrgLine.text(), self.LoginLine.text(), self.PassLine.text()]
            print(line)
            db = sqlite3.connect(dbway)
            cur = db.cursor()
            try:
                cur.execute('''INSERT INTO ofd VALUES (?,?,?)''', line)
            except sqlite3.ProgrammingError:
                QtWidgets.QMessageBox.critical(self,
                                               "Ошибка",
                                               "Error",
                                               QtWidgets.QMessageBox.Ok)
            except sqlite3.OperationalError:
                QtWidgets.QMessageBox.critical(self,
                                               "Ошибка",
                                               "База данных не найдена!",
                                               QtWidgets.QMessageBox.Ok)
            except sqlite3.DatabaseError:
                QtWidgets.QMessageBox.critical(self,
                                               "Ошибка",
                                               "Файл не является базой",
                                               QtWidgets.QMessageBox.Ok)
            else:
                db.commit()
                self.OrgLine.setText('')
                self.LoginLine.setText('')
                self.PassLine.setText('')
                self.sucsLabel.setText('')
                db.close()

    def find_Btn(self):
        global dbway
        FindClass(self).show()


class DbWay(QtWidgets.QMainWindow, way_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.acceptB.clicked.connect(self.accept_Btn)
        self.okBtn.clicked.connect(self.ok)
        self.browseBtn.clicked.connect(self.browse_Btn)
        self.lineWay.setText(dbway)

    def accept_Btn(self):
        global dbway
        dbway = self.lineWay.text()
        # Сохраняем путь к базе
        s = QSettings('settings.ini', QSettings.IniFormat)
        s.setValue('way_to_db', dbway)

    def browse_Btn(self):
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.lineWay.setText(path)

    def ok(self):
        self.hide()


# описание кнопки поиска
class FindClass(QtWidgets.QMainWindow, find_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.FndBtn.clicked.connect(self.find_Btn)
        self.lineFnd.returnPressed.connect(self.find_Btn)

    def selenium(self):
        # тут передаем значение текущей строки кнопки
        i = self.tableWidget.currentRow()
        # берем в переменные текст логина и пароля
        login = self.tableWidget.item(i, 1).text()
        pwd = self.tableWidget.item(i, 2).text()
        # юзаем функцию для перехода в лк с подстановкой логина и пароля
        login_OFD(login, pwd)

    def find_Btn(self):
        global dbway
        # поиск информации в бд
        db = sqlite3.connect(dbway)
        if self.lineFnd.text() == "":
            QtWidgets.QMessageBox.information(self,
                                              "Поиск",
                                              "Введите значение",
                                              QtWidgets.QMessageBox.Ok)
        else:
            try:
                w = str(self.lineFnd.text())
                w = ('%' + w + '%',)
                result = db.execute('SELECT * FROM ofd WHERE org LIKE ?', w)
                self.tableWidget.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.tableWidget.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        button = QtWidgets.QPushButton()
                        button.clicked.connect(self.selenium)
                        button.setText('ЛК ОФД')
                        self.tableWidget.setCellWidget(row_number, 3, button)
                        self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

            except sqlite3.ProgrammingError:
                QtWidgets.QMessageBox.critical(self,
                                               "Ошибка",
                                               "Error",
                                               QtWidgets.QMessageBox.Ok)
            except sqlite3.OperationalError:
                QtWidgets.QMessageBox.critical(self,
                                               "Ошибка",
                                               "База данных не найдена!",
                                               QtWidgets.QMessageBox.Ok)
            db.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MainWindowClass()
    myWindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
