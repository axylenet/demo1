import sys

from PyQt6.QtWidgets import QApplication

from LLogin import LoginTipo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginTipo()
    win.show()
    sys.exit(app.exec())


import pymysql


def db():
    return pymysql.connect(
        host = 'localhost',
        user='root',
        password='',
        database='tipografia',
        cursorclass=pymysql.cursors.DictCursor

    )


from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QMessageBox, QPushButton, QLabel, QApplication

from db import db


class LoginTipo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        self.setGeometry(0, 0, 600, 500)
        self.setStyleSheet('background-color: #ffdcc2; color: black; font-family: Sitka Text;')
        self.setWindowIcon(QIcon('icon.png'))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        photo = QLabel()
        pixmap = QPixmap('icon.png')
        pixmap = pixmap.scaled(200,200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        photo.setPixmap(pixmap)
        self.layout.addWidget(photo,alignment=Qt.AlignmentFlag.AlignCenter )
        logo = QLabel('Добро пожаловать')
        self.layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.username = QLineEdit()
        self.username.setPlaceholderText('Логин')
        self.password = QLineEdit()
        self.password.setPlaceholderText('Пароль')
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password)


        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.login)
        self.layout.addWidget(self.login_btn)

        self.exit_btn = QPushButton("Выйти")
        self.exit_btn.clicked.connect(self.exit)
        self.layout.addWidget(self.exit_btn)

    def login(self):
        u = self.username.text()
        p = self.password.text()

        try:
            conn = db()
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, role_id  FROM Users WHERE password = %s AND login = %s', (p,u))
                user = cursor.fetchone()
                if user:
                    self.close()
                    if user ['role_id'] == 1:
                        from PlayerWindow import Player
                        self.wink = Player(user['id'])
                        self.wink.show()
                    elif user ['role_id'] == 2:
                        from MenegerWindow import Men
                        self.winkkk = Men(user['id'])
                        self.winkkk.show()
                else:
                    QMessageBox.critical(self, 'Сообщение', 'еверные учетные данные')
        except Exception as e:
            QMessageBox.critical(self, 'Сообщение', f'Ошибка подключения {str(e)}')

    def exit(self):
        QApplication.instance().quit()


import sys

from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QApplication, \
    QHBoxLayout, QLineEdit, QLabel, QPushButton, QDialog, QComboBox, QFormLayout

from LLogin import LoginTipo
from db import db


class Men(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle('Мои заявки')
        self.setGeometry(0, 0, 600, 500)
        self.setStyleSheet('background-color: #ffdcc2; color: black; font-family: Sitka Text;')
        self.setWindowIcon(QIcon('icon.png'))
        self.user_id = user_id

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.exit_but_zav = QPushButton("Выйти")
        self.exit_but_zav.clicked.connect(self.exit_zav)
        self.exit_but_zav.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.exit_but_zav)

        self.black_but_zav = QPushButton("Вернуться")
        self.black_but_zav.clicked.connect(self.back)
        self.black_but_zav.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.black_but_zav)

        self.dell_but_zav = QPushButton("Удалить")
        self.dell_but_zav.clicked.connect(self.dilete_zav)
        self.dell_but_zav.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.dell_but_zav)

        self.edit_but_zav = QPushButton("Изменить количество")
        self.edit_but_zav.clicked.connect(self.edit_zav)
        self.edit_but_zav.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.edit_but_zav)

        self.add_but_zav = QPushButton("Добавить заявку ")
        self.add_but_zav.clicked.connect(self.add_zav)
        self.add_but_zav.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.add_but_zav)


        self.table_zav = QTableWidget()
        self.table_zav.setColumnCount(6)
        self.table_zav.setHorizontalHeaderLabels(
            ['Наименование продукта', 'Клиент', 'Количество', 'Цена', 'Статус', 'Артикул'])
        self.layout.addWidget(self.table_zav)

        self.my_load_zav()

    def my_load_zav(self):
        try:
            self.table_zav.setRowCount(0)

            conn = db()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT z.id, p.name, u.name as client, p.price, z.count,z.status  
                   FROM Zayvka z
                   JOIN Users u ON z.id_user = u.id
                   JOIN  Product p ON z.id_product = p.id
                   WHERE u.id = %s""", (self.user_id,))

                prod = cursor.fetchall()
                for row, p in enumerate(prod):
                    self.table_zav.insertRow(row)
                    self.table_zav.setItem(row, 0, QTableWidgetItem(p['name']))
                    self.table_zav.setItem(row, 1, QTableWidgetItem(p['client']))
                    self.table_zav.setItem(row, 2, QTableWidgetItem(str(p['count'])))
                    self.table_zav.setItem(row, 3, QTableWidgetItem(str(p['price'])))
                    self.table_zav.setItem(row, 4, QTableWidgetItem(p['status']))
                    self.table_zav.setItem(row, 5, QTableWidgetItem(str(p['id'])))
                    self.table_zav.resizeColumnsToContents()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось выгрузить данные в таблицу {str(e)}')

    def dilete_zav(self):
        select_row = self.table_zav.currentRow()
        namee = self.table_zav.item(select_row, 0).text()
        id_p = self.table_zav.item(select_row, 5).text()

        user = QMessageBox.question(self, 'Сообщение',
                                    f"Вы уверены, что хотите удалить заявку на товар '{namee}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if user == QMessageBox.StandardButton.Yes:
            try:
                conn = db()
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM Zayvka WHERE id = %s', (id_p,))
                    conn.commit()
                    self.table_zav.setRowCount(0)
                    self.my_load_zav()
                conn.close()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось внести ихменения  {str(e)}')

    def exit_zav(self):
        QApplication.instance().quit()

    def back(self):
        self.close()
        self.winn = LoginTipo()
        self.winn.show()

    def edit_zav(self):
        select_row = self.table_zav.currentRow()
        old_count = self.table_zav.item(select_row, 2).text()

        dialog_edit = QDialog()
        dialog_edit.setWindowTitle('Изменение количества')
        dialog_edit.setGeometry(0, 0, 300, 200)
        dialog_edit.setStyleSheet('background-color: #ffdcc2; color: black; font-family: Sitka Text;')
        dialog_edit.setWindowIcon(QIcon('icon.png'))

        layot = QVBoxLayout(dialog_edit)

        layot.addWidget(QLabel('Количество'))
        cou = QLineEdit()
        cou.setText(old_count)
        layot.addWidget(cou)

        save_edit_but = QPushButton("Сохранить")
        save_edit_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        layot.addWidget(save_edit_but)

        def save_edit():
            select_row = self.table_zav.currentRow()
            old_count = self.table_zav.item(select_row, 2).text()
            namee = self.table_zav.item(select_row, 0).text()
            id_p = self.table_zav.item(select_row, 5).text()
            coun =  cou.text()

            user = QMessageBox.question(self, 'Сообщение', f"Вы уверены, что хотите изменить у товара '{namee}' количество '{old_count}'?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if user == QMessageBox.StandardButton.Yes:
                try:
                    conn = db()
                    with conn.cursor() as cursor:
                        cursor.execute('UPDATE Zayvka SET count = %s WHERE id = %s',(coun, id_p))
                        conn.commit()
                        self.table_zav.setRowCount(0)
                        self.my_load_zav()
                    dialog_edit.accept()
                    conn.close()
                except Exception as e:
                    QMessageBox.critical(dialog_edit, 'Ошибка', f'Не удалось внести изменения  {str(e)}')
                else:
                    QMessageBox.information(dialog_edit, 'Сообщение', 'Количество изменено')

        save_edit_but.clicked.connect(save_edit)
        dialog_edit.exec()

    def add_zav(self):
        dialog_add = QDialog()
        dialog_add.setWindowTitle('Добавление заявки')
        dialog_add.setGeometry(0, 0, 300, 200)
        dialog_add.setStyleSheet('background-color: #ffdcc2; color: black; font-family: Sitka Text;')
        dialog_add.setWindowIcon(QIcon('icon.png'))

        layout = QVBoxLayout(dialog_add)

        # Загрузка товаров из БД
        conn = db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM Product")
        products = cursor.fetchall()
        conn.close()

        # Надпись и выпадающий список продуктов
        layout.addWidget(QLabel("Выберите товар:"))
        product_combo = QComboBox()
        for p in products:
            product_combo.addItem(f"{p['name']} - {p['price']} руб.")
        layout.addWidget(product_combo)

        # Поле ввода количества
        layout.addWidget(QLabel("Количество:"))
        count_input = QLineEdit()
        count_input.setPlaceholderText("Введите количество")
        layout.addWidget(count_input)

        # Кнопка "Сохранить"
        save_btn = QPushButton("Сохранить")
        save_btn.setStyleSheet('background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        layout.addWidget(save_btn)

        def save_zav():
            count = count_input.text()
            if not count.isdigit() or int(count) <= 0:
                QMessageBox.warning(dialog_add, "Ошибка", "Введите корректное количество")
                return

            try:
                conn = db()
                cursor = conn.cursor()
                product_id = products[product_combo.currentIndex()]['id']
                cursor.execute(
                    "INSERT INTO Zayvka (id_user, id_product, count, status) VALUES (%s, %s, %s, 'в обработке')",
                    (self.user_id, product_id, count)
                )
                conn.commit()
                conn.close()
                QMessageBox.information(dialog_add, "Успех", "Заявка успешно добавлена")
                self.my_load_zav()
                dialog_add.accept()
            except Exception as e:
                QMessageBox.critical(dialog_add, "Ошибка", f"Не удалось добавить заявку: {str(e)}")

        save_btn.clicked.connect(save_zav)
        dialog_add.exec()



import sys

from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QApplication, \
    QHBoxLayout, QLineEdit, QLabel, QPushButton, QDialog, QComboBox

from LLogin import LoginTipo
from db import db

class Zavki(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle('Заявки на заказ')
        self.setGeometry(0, 0, 600, 500)
        self.setStyleSheet('background-color: #ffdcc2; color: black; font-family: Sitka Text;')
        self.setWindowIcon(QIcon('icon.png'))
        self.user_id = user_id

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.f_layout = QHBoxLayout()
        self.layout.addLayout(self.f_layout)

        self.f_label = QLabel('По статусу')
        self.f_combo = QComboBox()
        self.f_combo.addItems(['отменен','подтвержден', 'в обработке'])
        self.f_combo.currentIndexChanged.connect(self.load_table_zav)

        self.f_layout.addWidget(self.f_label)
        self.f_layout.addWidget(self.f_combo)

        self.up_but_zav = QPushButton("Обновить")
        self.up_but_zav.clicked.connect(self.upgrate_load_zav)
        self.up_but_zav.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.f_layout.addWidget(self.up_but_zav)

        self.back_but = QPushButton("Вернуться")
        self.back_but.clicked.connect(self.back)
        self.back_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.f_layout.addWidget(self.back_but)

        self.back_but_login = QPushButton("Вернуться к авторизации")
        self.back_but_login.clicked.connect(self.back_login)
        self.back_but_login.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.f_layout.addWidget(self.back_but_login)

        self.exit_but_zav = QPushButton("Выйти")
        self.exit_but_zav.clicked.connect(self.exit_zav)
        self.exit_but_zav.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.f_layout.addWidget(self.exit_but_zav)

        self.podtverd_zav_but = QPushButton("Подтвердить")
        self.podtverd_zav_but.clicked.connect(self.podtver_zav)
        self.podtverd_zav_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.podtverd_zav_but)

        self.otmena_zav_but = QPushButton("Отменить")
        self.otmena_zav_but.clicked.connect(self.otmena_zav)
        self.otmena_zav_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.otmena_zav_but)

        self.table_zav = QTableWidget()
        self.table_zav.setColumnCount(6)
        self.table_zav.setHorizontalHeaderLabels(['Наименование продукта', 'Клиент', 'Количество', 'Цена', 'Статус', 'Артикул'])
        self.layout.addWidget(self.table_zav)

        self.load_table_zav()

    def load_table_zav(self):
        try:
            self.table_zav.setRowCount(0)
            f_combo_text = self.f_combo.currentText()

            conn = db()
            with conn.cursor() as cursor:
                query = """SELECT z.id, p.name, u.name as client, p.price, z.count,z.status  
                FROM Zayvka z
                JOIN Users u ON z.id_user = u.id
                JOIN  Product p ON z.id_product = p.id"""
                if f_combo_text:
                    if f_combo_text == 'отменен':
                        query += ' WHERE z.status LIKE %s'
                        cursor.execute(query, (f'%{f_combo_text}%',))
                    elif f_combo_text == 'подтвержден':
                        query += ' WHERE z.status LIKE %s'
                        cursor.execute(query, (f'%{f_combo_text}%',))
                    elif f_combo_text == 'в обработке':
                        query += ' WHERE z.status LIKE %s'
                        cursor.execute(query, (f'%{f_combo_text}%',))
                else:
                    cursor.execute(query)
                prod = cursor.fetchall()
                for row, p in enumerate(prod):
                    self.table_zav.insertRow(row)
                    self.table_zav.setItem(row, 0, QTableWidgetItem(p['name']))
                    self.table_zav.setItem(row, 1, QTableWidgetItem(p['client']))
                    self.table_zav.setItem(row, 2, QTableWidgetItem(str(p['count'])))
                    self.table_zav.setItem(row, 3, QTableWidgetItem(str(p['price'])))
                    self.table_zav.setItem(row, 4, QTableWidgetItem(p['status']))
                    self.table_zav.setItem(row, 5, QTableWidgetItem(str(p['id'])))
                    self.table_zav.resizeColumnsToContents()

            conn.close()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось выгрузить данные в таблицу {str(e)}')
    def upgrate_load_zav(self):
        try:
            self.table_zav.setRowCount(0)

            conn = db()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT z.id, p.name, u.name as client, p.price, z.count,z.status  
                FROM Zayvka z
                JOIN Users u ON z.id_user = u.id
                JOIN  Product p ON z.id_product = p.id""")

                prod = cursor.fetchall()
                for row, p in enumerate(prod):
                    self.table_zav.insertRow(row)
                    self.table_zav.setItem(row, 0, QTableWidgetItem(p['name']))
                    self.table_zav.setItem(row, 1, QTableWidgetItem(p['client']))
                    self.table_zav.setItem(row, 2, QTableWidgetItem(str(p['count'])))
                    self.table_zav.setItem(row, 3, QTableWidgetItem(str(p['price'])))
                    self.table_zav.setItem(row, 4, QTableWidgetItem(p['status']))
                    self.table_zav.setItem(row, 5, QTableWidgetItem(str(p['id'])))
                    self.table_zav.resizeColumnsToContents()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось выгрузить данные в таблицу {str(e)}')

    def exit_zav(self):
        QApplication.instance().quit()

    def back(self):
        self.close()
        self.winn = Player(self.user_id)
        self.winn.show()

    def back_login(self):
        self.close()
        self.winn = LoginTipo()
        self.winn.show()


    def podtver_zav(self):
        select_row = self.table_zav.currentRow()
        namee = self.table_zav.item(select_row, 1).text()
        id_p = self.table_zav.item(select_row, 5).text()

        user = QMessageBox.question(self, 'Сообщение',
                                    f"Вы уверены, что хотите подтвердить заявку номер '{id_p}' клиента '{namee}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if user == QMessageBox.StandardButton.Yes:
            try:
                conn = db()
                with conn.cursor() as cursor:
                    cursor.execute('UPDATE Zayvka SET status = %s WHERE id = %s', ('подтвержден', id_p))
                    conn.commit()
                    self.table_zav.setRowCount(0)
                    self.load_table_zav()
                conn.close()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось подтвердить  {str(e)}')
            else:
                QMessageBox.information(self, 'Сообщение', 'Успешно подтверждена заявка')

    def otmena_zav(self):
        select_row = self.table_zav.currentRow()
        namee = self.table_zav.item(select_row, 1).text()
        id_p = self.table_zav.item(select_row, 5).text()

        user = QMessageBox.question(self, 'Сообщение',
                                    f"Вы уверены, что хотите отменить заявку номер '{id_p}' клиента '{namee}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if user == QMessageBox.StandardButton.Yes:
            try:
                conn = db()
                with conn.cursor() as cursor:
                    cursor.execute('UPDATE Zayvka SET status = %s WHERE id = %s', ('отменен', id_p))
                    conn.commit()
                    self.table_zav.setRowCount(0)
                    self.load_table_zav()
                conn.close()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось отменить  {str(e)}')
            else:
                QMessageBox.information(self, 'Сообщение', 'Успешно отменена заявка')

class Player(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle('Продукция')
        self.setGeometry(0, 0, 600, 500)
        self.setStyleSheet('background-color: #ffdcc2; color: black; font-family: Sitka Text;')
        self.setWindowIcon(QIcon('icon.png'))
        self.user_id = user_id


        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.f_layout = QHBoxLayout()
        self.layout.addLayout(self.f_layout)

        self.f_label = QLabel('Поиск')
        self.f_input = QLineEdit()
        self.f_input.setPlaceholderText('Введите наименование продукции для поиска')
        self.f_input.textChanged.connect(self.load_table_prod)

        self.f_layout.addWidget(self.f_label)
        self.f_layout.addWidget(self.f_input)

        self.check_but = QPushButton("Просмотр заявок")
        self.check_but.clicked.connect(self.check_zav)
        self.check_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.check_but)

        self.back_but_login = QPushButton("Вернуться")
        self.back_but_login.clicked.connect(self.back_login)
        self.back_but_login.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.f_layout.addWidget(self.back_but_login)

        self.up_but = QPushButton("Обновить")
        self.up_but.clicked.connect(self.upgrate_load)
        self.up_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.f_layout.addWidget(self.up_but)

        self.exit_but = QPushButton("Выйти")
        self.exit_but.clicked.connect(self.exit)
        self.exit_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.f_layout.addWidget(self.exit_but)

        self.add_prod_but = QPushButton("Добавить")
        self.add_prod_but.clicked.connect(self.add_prod)
        self.add_prod_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.add_prod_but)

        self.dilete_prod_but = QPushButton("Удалить")
        self.dilete_prod_but.clicked.connect(self.dilete_prod)
        self.dilete_prod_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.dilete_prod_but)

        self.edit_prod_but = QPushButton("Изменить цену")
        self.edit_prod_but.clicked.connect(self.edit_prod)
        self.edit_prod_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        self.layout.addWidget(self.edit_prod_but)

        self.table_prod = QTableWidget()
        self.table_prod.setColumnCount(5)
        self.table_prod.setHorizontalHeaderLabels(['Наименование','Цена','Описание','Размер','Артикул'])
        self.layout.addWidget(self.table_prod)

        self.load_table_prod()

    def load_table_prod(self):
        try:
            self.table_prod.setRowCount(0)
            f_text = self.f_input.text().strip()

            conn = db()
            with conn.cursor() as cursor:
                query ='SELECT id, name, price,opisania,size_cm FROM Product p '
                if f_text:
                    query += ' WHERE p.name LIKE %s'
                    cursor.execute(query, (f'%{f_text}%',))

                else:
                    cursor.execute(query,)
                prod = cursor.fetchall()
                for row, p in enumerate(prod):
                    self.table_prod.insertRow(row)
                    self.table_prod.setItem(row, 0, QTableWidgetItem(p['name']))
                    self.table_prod.setItem(row, 1, QTableWidgetItem(str(p['price'])))
                    self.table_prod.setItem(row, 2, QTableWidgetItem(p['opisania']))
                    self.table_prod.setItem(row, 3, QTableWidgetItem(str(p['size_cm'])))
                    self.table_prod.setItem(row, 4, QTableWidgetItem(str(p['id'])))

            conn.close()
            self.table_prod.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось выгрузить данные в таблицу {str(e)}')

    def upgrate_load(self):
        self.f_input.clear()
        self.load_table_prod()

    def exit(self):
        QApplication.instance().quit()

    def add_prod(self):
        dialog_add = QDialog()
        dialog_add.setWindowTitle('Добавление нового товара')
        dialog_add.setGeometry(0, 0, 300, 200)
        dialog_add.setStyleSheet('background-color: #ffdcc2; color: black; font-family: Sitka Text;')
        dialog_add.setWindowIcon(QIcon('icon.png'))

        layot = QVBoxLayout(dialog_add)

        layot.addWidget(QLabel('Наименование'))
        name = QLineEdit()
        layot.addWidget(name)

        layot.addWidget(QLabel('Цена'))
        pr = QLineEdit()
        layot.addWidget(pr)

        layot.addWidget(QLabel('Описание'))
        opi = QLineEdit()
        layot.addWidget(opi)

        layot.addWidget(QLabel('Размер'))
        size = QLineEdit()
        layot.addWidget(size)

        save_add_but = QPushButton("Сохранить")
        save_add_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        layot.addWidget(save_add_but)

        def save_add():
            n = name.text()
            p = pr.text()
            o  = opi.text()
            s = size.text()

            user = QMessageBox.question(self, 'Сообщение', 'Вы добавляете новый товар?',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if user == QMessageBox.StandardButton.Yes:
                try:
                    conn = db()
                    with conn.cursor() as cursor:
                        cursor.execute('INSERT INTO Product (name, price,opisania,size_cm) VALUES (%s,%s,%s,%s)', (n,p,o,s))
                        conn.commit()
                        self.table_prod.setRowCount(0)
                        self.load_table_prod()
                    dialog_add.accept()
                    conn.close()
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить новые данные {str(e)}')
        save_add_but.clicked.connect(save_add)
        dialog_add.exec()

    def edit_prod(self):
        select_row = self.table_prod.currentRow()
        old_price = self.table_prod.item(select_row, 1).text()

        dialog_edit = QDialog()
        dialog_edit.setWindowTitle('Изменение цены')
        dialog_edit.setGeometry(0, 0, 300, 200)
        dialog_edit.setStyleSheet('background-color: #ffdcc2; color: black; font-family: Sitka Text;')
        dialog_edit.setWindowIcon(QIcon('icon.png'))

        layot = QVBoxLayout(dialog_edit)

        layot.addWidget(QLabel('Цена'))
        pr = QLineEdit()
        pr.setText(old_price)
        layot.addWidget(pr)

        save_edit_but = QPushButton("Сохранить")
        save_edit_but.setStyleSheet(
            'background-color: #fff4ea; color: black; font-family: Sitka Text; padding: 2px;')
        layot.addWidget(save_edit_but)

        def save_edit():
            select_row = self.table_prod.currentRow()
            old_price = self.table_prod.item(select_row, 1).text()
            namee = self.table_prod.item(select_row, 0).text()
            id_p = self.table_prod.item(select_row, 4).text()
            p = pr.text()

            user = QMessageBox.question(self, 'Сообщение', f"Вы уверены, что хотите изменить у  товара '{namee}' цену '{old_price}'?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if user == QMessageBox.StandardButton.Yes:
                try:
                    conn = db()
                    with conn.cursor() as cursor:
                        cursor.execute('UPDATE Product SET  price = %s WHERE id = %s',(p, id_p))
                        conn.commit()
                        self.table_prod.setRowCount(0)
                        self.load_table_prod()
                    dialog_edit.accept()
                    conn.close()
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось внести ихменения  {str(e)}')

        save_edit_but.clicked.connect(save_edit)
        dialog_edit.exec()

    def dilete_prod(self):
        select_row = self.table_prod.currentRow()
        namee = self.table_prod.item(select_row, 0).text()
        id_p = self.table_prod.item(select_row, 4).text()

        user = QMessageBox.question(self, 'Сообщение',
                                    f"Вы уверены, что хотите удалить товар '{namee}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if user == QMessageBox.StandardButton.Yes:
            try:
                conn = db()
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM Product WHERE name = %s AND id = %s', (namee, id_p))
                    conn.commit()
                    self.table_prod.setRowCount(0)
                    self.load_table_prod()
                conn.close()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось внести ихменения  {str(e)}')

    def check_zav(self):
        self.window = Zavki(self.user_id)
        self.window.show()

    def back_login(self):
        self.close()
        self.winn = LoginTipo()
        self.winn.show()


'''
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: MySQL-8.2
-- Время создания: Май 18 2025 г., 22:27
-- Версия сервера: 8.2.0
-- Версия PHP: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `tipografia`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Product`
--

CREATE TABLE `Product` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` int NOT NULL,
  `opisania` text NOT NULL,
  `size_cm` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Product`
--

INSERT INTO `Product` (`id`, `name`, `price`, `opisania`, `size_cm`) VALUES
(1, 'тетрадь', 100, 'для прописи', '20'),
(2, 'плакат', 200, 'для разных целей', '100'),
(3, 'папка', 130, 'для хранения', '60'),
(5, 'aaaaaaaaaa', 180, '345T6YU', '45'),
(6, 'qqqqqqq', 123, 'wdfdew', '1'),
(7, 'qqqqqqqqqqqqqq', 145, '23wertyui', '2'),
(8, 'ddddddddddddd', 120, 'qwsedfgh', '23'),
(9, 'qqqqqqqqqqqqqqqq', 12222, 'qwerftyhujk', '12'),
(12, 'AAA', 1230, 'AAA', '98'),
(15, 'книга', 1900, 'для записей', '40');

-- --------------------------------------------------------

--
-- Структура таблицы `Role`
--

CREATE TABLE `Role` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Role`
--

INSERT INTO `Role` (`id`, `name`) VALUES
(1, 'Админ'),
(2, 'Клиент');

-- --------------------------------------------------------

--
-- Структура таблицы `Users`
--

CREATE TABLE `Users` (
  `id` int NOT NULL,
  `role_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `login` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Users`
--

INSERT INTO `Users` (`id`, `role_id`, `name`, `password`, `login`) VALUES
(1, 1, 'саша', '111', '1111'),
(2, 2, 'карина', '3333', '3333'),
(3, 2, 'виктор', '2222', '2222');

-- --------------------------------------------------------

--
-- Структура таблицы `Zayvka`
--

CREATE TABLE `Zayvka` (
  `id` int NOT NULL,
  `id_product` int DEFAULT NULL,
  `id_user` int NOT NULL,
  `count` int NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Zayvka`
--

INSERT INTO `Zayvka` (`id`, `id_product`, `id_user`, `count`, `status`) VALUES
(3, 3, 3, 80, 'подтвержден'),
(8, 2, 3, 12, 'подтвержден'),
(9, 7, 3, 12, 'отменен'),
(10, 5, 3, 9, 'в обработке'),
(11, 15, 3, 56, 'в обработке'),
(12, 5, 3, 12, 'в обработке');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Product`
--
ALTER TABLE `Product`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Role`
--
ALTER TABLE `Role`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `role_id` (`role_id`);

--
-- Индексы таблицы `Zayvka`
--
ALTER TABLE `Zayvka`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_product` (`id_product`,`id_user`),
  ADD KEY `id_user` (`id_user`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Product`
--
ALTER TABLE `Product`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT для таблицы `Role`
--
ALTER TABLE `Role`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `Users`
--
ALTER TABLE `Users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `Zayvka`
--
ALTER TABLE `Zayvka`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Users`
--
ALTER TABLE `Users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `Role` (`id`);

--
-- Ограничения внешнего ключа таблицы `Zayvka`
--
ALTER TABLE `Zayvka`
  ADD CONSTRAINT `zayvka_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `Users` (`id`),
  ADD CONSTRAINT `zayvka_ibfk_2` FOREIGN KEY (`id_product`) REFERENCES `Product` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
'''