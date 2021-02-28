import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QTableWidgetItem


class Login(QWidget):
    """ Класс отвечающий за вход пользователя в приложение """

    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)

        self.open = 1
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.showButton.clicked.connect(self.shw)
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)
        self.exitButton.clicked.connect(self.exit)

    def shw(self):
        if self.open:
            self.passwordEdit.setEchoMode(QLineEdit.Normal)
            self.open = 1 - self.open
        else:
            self.passwordEdit.setEchoMode(QLineEdit.Password)
            self.open = 1 - self.open

    def login(self):
        if self.loginEdit.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Логин не введён</span></p></body></html>')
            return

        if self.passwordEdit.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пароль не введён</span></p></body></html>')
            return

        logins = [login[0] for login in cur.execute("""SELECT login FROM users""").fetchall()]

        if self.loginEdit.text() not in logins:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Данного пользователя не существует</span></p></body></html>')
            return

        if self.passwordEdit.text() != cur.execute("""SELECT password FROM users
                                                WHERE login = ?""", (self.loginEdit.text(),)).fetchone()[0]:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Введён неверный пароль</span></p></body></html>')
            return

        global user
        user = self.loginEdit.text()
        self.close()
        cur.execute('UPDATE cur_user SET user = ?', (user,))
        data_base.commit()

        global mw
        mw = MainWidget()
        mw.show()

    def register(self):
        self.close()
        reg.show()

    def exit(self):
        out.show()


class Register(QWidget):
    """ Класс отвечающий за регистрацию польвзователя """

    def __init__(self):
        super().__init__()
        uic.loadUi('register.ui', self)

        self.open = 1
        self.open_2 = 1
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit_2.setEchoMode(QLineEdit.Password)

        self.showButton.clicked.connect(self.shw)
        self.showButton_2.clicked.connect(self.shw_2)
        self.registerButton.clicked.connect(self.register)
        self.backButton.clicked.connect(self.back)

    def shw(self):
        if self.open:
            self.passwordEdit.setEchoMode(QLineEdit.Normal)
            self.open = 1 - self.open
        else:
            self.passwordEdit.setEchoMode(QLineEdit.Password)
            self.open = 1 - self.open

    def shw_2(self):
        if self.open_2:
            self.passwordEdit_2.setEchoMode(QLineEdit.Normal)
            self.open_2 = 1 - self.open_2
        else:
            self.passwordEdit_2.setEchoMode(QLineEdit.Password)
            self.open_2 = 1 - self.open_2

    def back(self):
        self.close()
        log.show()

    def register(self):
        if self.loginEdit.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Логин не введён</span></p></body></html>')
            return

        if self.passwordEdit.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пароль не введён</span></p></body></html>')
            return

        if self.passwordEdit_2.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пожалуйста, подтвердите пароль</span></p></body></html>')
            return

        if len(self.loginEdit.text()) < 3:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Логин должен содержать хотя бы 3 символа</span></p></body></html>')
            return

        if len(self.passwordEdit.text()) < 8:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пароль должен содержать хотя бы 8 символов</span></p></body></html>')
            return

        if self.passwordEdit.text() != self.passwordEdit_2.text():
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пароли не совпадают</span></p></body></html>')
            return

        logins = [login[0] for login in cur.execute("""SELECT login FROM users""").fetchall()]

        if self.loginEdit.text() in logins:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Данный логин уже занят</span></p></body></html>')
            return

        cur.execute('INSERT INTO users(login,password,level,coins,car1,car2,car3,car4) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                    (self.loginEdit.text(), self.passwordEdit.text(), 1, 0, 2, 0, 0, 0))
        data_base.commit()
        self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#17e517;">'
                           'Вы успешно зарегистрированы</span></p></body></html>')


class Exit(QWidget):
    """ Класс отвечающий за выход из приложения """

    def __init__(self):
        super().__init__()
        uic.loadUi('exit.ui', self)

        self.yesButton.clicked.connect(self.exit)
        self.noButton.clicked.connect(self.back)

    def exit(self):
        self.close()
        log.close()

    def back(self):
        self.close()


class Top(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('top.ui', self)

        self.pushButton.clicked.connect(self.back)

        result = cur.execute('SELECT login, level FROM users ORDER BY level').fetchall()

        self.tableWidget.setRowCount(len(result))

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if j % 2 == 1:
                    self.tableWidget.setItem(len(result) - i - 1, j, QTableWidgetItem(str(val - 1)))
                else:
                    self.tableWidget.setItem(len(result) - i - 1, j, QTableWidgetItem(str(val)))

    def back(self):
        self.close()
        mw.show()


class Skins(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('skins.ui', self)

        pixmap = QPixmap('car4.png')

        self.car1.setPixmap(pixmap)
        self.car1.resize(pixmap.width(), pixmap.height())

        pixmap = QPixmap('car5.png')

        self.car2.setPixmap(pixmap)
        self.car2.resize(pixmap.width(), pixmap.height())

        pixmap = QPixmap('car6.png')

        self.car3.setPixmap(pixmap)
        self.car3.resize(pixmap.width(), pixmap.height())

        pixmap = QPixmap('car7.png')

        self.car4.setPixmap(pixmap)
        self.car4.resize(pixmap.width(), pixmap.height())

        self.backButton.clicked.connect(self.back)

        self.coins = cur.execute('SELECT coins FROM users WHERE login = ?', (user,)).fetchone()[0]
        self.coinsLabel.setText('Coins: ' + str(self.coins))

        self.car_1 = cur.execute('SELECT car1 FROM users WHERE login = ?', (user,)).fetchall()[0][0]
        self.car_2 = cur.execute('SELECT car2 FROM users WHERE login = ?', (user,)).fetchall()[0][0]
        self.car_3 = cur.execute('SELECT car3 FROM users WHERE login = ?', (user,)).fetchall()[0][0]
        self.car_4 = cur.execute('SELECT car4 FROM users WHERE login = ?', (user,)).fetchall()[0][0]

        if self.car_1 == 2:
            self.car1Button.setText('Выбрано')

        if self.car_1 == 0:
            self.car1Button.setText('Купить за 150')

        if self.car_1 == 1:
            self.car1Button.setText('Выбрать')

        if self.car_2 == 2:
            self.car2Button.setText('Выбрано')

        if self.car_2 == 0:
            self.car2Button.setText('Купить за 150')

        if self.car_2 == 1:
            self.car2Button.setText('Выбрать')

        if self.car_3 == 2:
            self.car3Button.setText('Выбрано')

        if self.car_3 == 0:
            self.car3Button.setText('Купить за 150')

        if self.car_3 == 1:
            self.car3Button.setText('Выбрать')

        if self.car_4 == 2:
            self.car4Button.setText('Выбрано')

        if self.car_4 == 0:
            self.car4Button.setText('Купить за 500')

        if self.car_4 == 1:
            self.car4Button.setText('Выбрать')

        self.car1Button.clicked.connect(self.do_car1)
        self.car2Button.clicked.connect(self.do_car2)
        self.car3Button.clicked.connect(self.do_car3)
        self.car4Button.clicked.connect(self.do_car4)

    def back(self):
        self.close()
        mw.show()

    def do_car1(self):
        if self.car_1 == 0:
            if self.coins >= 150:
                self.coins -= 150
                self.coinsLabel.setText('Coins: ' + str(self.coins))
                self.car1Button.setText('Выбрать')
                self.car_1 = 1

                cur.execute('UPDATE users SET car1 = ? WHERE login = ?', (1, user))
                cur.execute('UPDATE users SET coins = ? WHERE login = ?', (self.coins, user))
                data_base.commit()
            else:
                self.errorLabel.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                                        'Недостаточно средств</span></p></body></html>')
        elif self.car_1 == 1:
            if self.car_1 == 2:
                self.car_1 = 1
                cur.execute('UPDATE users SET car1 = ? WHERE login = ?', (1, user))
                self.car1Button.setText('Выбрать')

            if self.car_2 == 2:
                self.car_2 = 1
                cur.execute('UPDATE users SET car2 = ? WHERE login = ?', (1, user))
                self.car2Button.setText('Выбрать')

            if self.car_3 == 2:
                self.car_3 = 1
                cur.execute('UPDATE users SET car3 = ? WHERE login = ?', (1, user))
                self.car3Button.setText('Выбрать')

            if self.car_4 == 2:
                self.car_4 = 1
                cur.execute('UPDATE users SET car4 = ? WHERE login = ?', (1, user))
                self.car4Button.setText('Выбрать')

            self.car_1 = 2
            cur.execute('UPDATE users SET car1 = ? WHERE login = ?', (2, user))
            cur.execute('UPDATE users SET select_car = ? WHERE login = ?', (1, user))
            data_base.commit()
            self.car1Button.setText('Выбрано')

    def do_car2(self):
        if self.car_2 == 0:
            if self.coins >= 150:
                self.coins -= 150
                self.coinsLabel.setText('Coins: ' + str(self.coins))
                self.car2Button.setText('Выбрать')
                self.car_2 = 1

                cur.execute('UPDATE users SET car2 = ? WHERE login = ?', (1, user))
                cur.execute('UPDATE users SET coins = ? WHERE login = ?', (self.coins, user))
                data_base.commit()
            else:
                self.errorLabel.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                                        'Недостаточно средств</span></p></body></html>')
        elif self.car_2 == 1:
            if self.car_1 == 2:
                self.car_1 = 1
                cur.execute('UPDATE users SET car1 = ? WHERE login = ?', (1, user))
                self.car1Button.setText('Выбрать')

            if self.car_2 == 2:
                self.car_2 = 1
                cur.execute('UPDATE users SET car2 = ? WHERE login = ?', (1, user))
                self.car2Button.setText('Выбрать')

            if self.car_3 == 2:
                self.car_3 = 1
                cur.execute('UPDATE users SET car3 = ? WHERE login = ?', (1, user))
                self.car3Button.setText('Выбрать')

            if self.car_4 == 2:
                self.car_4 = 1
                cur.execute('UPDATE users SET car4 = ? WHERE login = ?', (1, user))
                self.car4Button.setText('Выбрать')

            self.car_2 = 2
            cur.execute('UPDATE users SET car2 = ? WHERE login = ?', (2, user))
            cur.execute('UPDATE users SET select_car = ? WHERE login = ?', (2, user))
            data_base.commit()
            self.car2Button.setText('Выбрано')

    def do_car3(self):
        if self.car_3 == 0:
            if self.coins >= 150:
                self.coins -= 150
                self.coinsLabel.setText('Coins: ' + str(self.coins))
                self.car3Button.setText('Выбрать')
                self.car_3 = 1

                cur.execute('UPDATE users SET car3 = ? WHERE login = ?', (1, user))
                cur.execute('UPDATE users SET coins = ? WHERE login = ?', (self.coins, user))
                data_base.commit()
            else:
                self.errorLabel.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                                        'Недостаточно средств</span></p></body></html>')
        elif self.car_3 == 1:
            if self.car_1 == 2:
                self.car_1 = 1
                cur.execute('UPDATE users SET car1 = ? WHERE login = ?', (1, user))
                self.car1Button.setText('Выбрать')

            if self.car_2 == 2:
                self.car_2 = 1
                cur.execute('UPDATE users SET car2 = ? WHERE login = ?', (1, user))
                self.car2Button.setText('Выбрать')

            if self.car_3 == 2:
                self.car_3 = 1
                cur.execute('UPDATE users SET car3 = ? WHERE login = ?', (1, user))
                self.car3Button.setText('Выбрать')

            if self.car_4 == 2:
                self.car_4 = 1
                cur.execute('UPDATE users SET car4 = ? WHERE login = ?', (1, user))
                self.car4Button.setText('Выбрать')

            self.car_3 = 2
            cur.execute('UPDATE users SET car3 = ? WHERE login = ?', (2, user))
            cur.execute('UPDATE users SET select_car = ? WHERE login = ?', (3, user))
            data_base.commit()
            self.car3Button.setText('Выбрано')

    def do_car4(self):
        if self.car_4 == 0:
            if self.coins >= 500:
                self.coins -= 500
                self.coinsLabel.setText('Coins: ' + str(self.coins))
                self.car4Button.setText('Выбрать')
                self.car_4 = 1

                cur.execute('UPDATE users SET car4 = ? WHERE login = ?', (1, user))
                cur.execute('UPDATE users SET coins = ? WHERE login = ?', (self.coins, user))
                data_base.commit()
            else:
                self.errorLabel.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                                        'Недостаточно средств</span></p></body></html>')
        elif self.car_4 == 1:
            if self.car_1 == 2:
                self.car_1 = 1
                cur.execute('UPDATE users SET car1 = ? WHERE login = ?', (1, user))
                self.car1Button.setText('Выбрать')

            if self.car_2 == 2:
                self.car_2 = 1
                cur.execute('UPDATE users SET car2 = ? WHERE login = ?', (1, user))
                self.car2Button.setText('Выбрать')

            if self.car_3 == 2:
                self.car_3 = 1
                cur.execute('UPDATE users SET car3 = ? WHERE login = ?', (1, user))
                self.car3Button.setText('Выбрать')

            if self.car_4 == 2:
                self.car_4 = 1
                cur.execute('UPDATE users SET car4 = ? WHERE login = ?', (1, user))
                self.car4Button.setText('Выбрать')

            self.car_4 = 2
            cur.execute('UPDATE users SET car4 = ? WHERE login = ?', (2, user))
            cur.execute('UPDATE users SET select_car = ? WHERE login = ?', (4, user))
            data_base.commit()
            self.car4Button.setText('Выбрано')


class MainWidget(QMainWindow):
    """ Класс отвечающий за главное окно программы """

    def __init__(self):
        super().__init__()
        uic.loadUi('Main.ui', self)

        self.playButton.clicked.connect(self.play)
        self.topButton.clicked.connect(self.top)
        self.skinButton.clicked.connect(self.skin)

        level = cur.execute('SELECT level FROM users WHERE login = ?', (user,)).fetchone()[0]
        coins = cur.execute('SELECT coins FROM users WHERE login = ?', (user,)).fetchone()[0]

        self.levelLabel.setText('Level: ' + str(level))
        self.coinsLabel.setText('Coins: ' + str(coins))

        # self.tableWidget.setColumnCount(2)
        # self.tableWidget.setRowCount(0)

    def play(self):
        self.close()

        import game

    def top(self):
        self.close()
        top.show()

    def skin(self):
        self.close()

        global skin
        skin = Skins()
        skin.show()


if __name__ == '__main__':
    data_base = sqlite3.connect("top_db.sqlite")
    cur = data_base.cursor()

    user = ""

    app = QApplication(sys.argv)
    log = Login()
    reg = Register()
    out = Exit()
    top = Top()
    log.show()
    sys.exit(app.exec_())