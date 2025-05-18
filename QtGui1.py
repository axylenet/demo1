import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from database import Database
from mainwindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)

        self.user_id = user_id
        self.db = Database()
        self.current_products = []

        self.setup_ui()
        self.load_products()
        self.load_types()

        self.pushButton.clicked.connect(self.open_cart)
        self.pushButton_2.clicked.connect(self.add_to_cart)
        self.comboBox.currentIndexChanged.connect(self.filter_by_type)

    def setup_ui(self):
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(60, 30, 681, 371))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Название продукта", "Тип продукта"])
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

    def load_products(self):
        products = self.db.get_products_with_types()
        self.current_products = products
        self.tableWidget.setRowCount(len(products))

        for row, product in enumerate(products):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(product['product_name']))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(product['type_name']))

    def load_types(self):
        types = self.db.get_product_types()
        self.comboBox.clear()
        self.comboBox.addItem("Все типы", 0)

        for type_item in types:
            self.comboBox.addItem(type_item['name'], type_item['id'])

    def filter_by_type(self):
        type_id = self.comboBox.currentData()
        if type_id == 0:
            self.load_products()
        else:
            filtered_products = [p for p in self.current_products
                                 if p['type_name'] == self.comboBox.currentText()]
            self.display_filtered_products(filtered_products)

    def display_filtered_products(self, products):
        self.tableWidget.setRowCount(len(products))
        for row, product in enumerate(products):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(product['product_name']))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(product['type_name']))

    def add_to_cart(self):
        selected_rows = {item.row() for item in self.tableWidget.selectedItems()}


        row = selected_rows.pop()
        product_name = self.tableWidget.item(row, 0).text()
        quantity = self.spinBox.value()



        product_id = self.db.get_product_id_by_name(product_name)


        if self.db.add_to_cart(self.user_id, product_id, quantity):
            QMessageBox.information(self, "Успех", "Товар добавлен в корзину!")


    def open_cart(self):
        from corzina_main1 import CartWindow
        self.cart_window = CartWindow(self.user_id)
        self.cart_window.show()

    def closeEvent(self, event):
        self.db.close()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


import pymysql
from pymysql import Error


class Database:
    def __init__(self):
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                database='',
                cursorclass=pymysql.cursors.DictCursor
            )

    def get_products_with_types(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                       SELECT 
                           p.name AS product_name, 
                           t.name AS type_name
                       FROM 
                           product p
                       JOIN 
                           type t ON p.id_type_product = t.id
                       ORDER BY 
                           p.name
                   """)
            return cursor.fetchall()

    def get_product_types(self):
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT id, name FROM type")
                return cursor.fetchall()

    def add_to_cart(self, user_id, product_id, quantity):
        try:
            with self.connection.cursor() as cursor:

                cursor.execute(
                    "SELECT id, count FROM corzina WHERE id_user = %s AND id_product = %s",
                    (user_id, product_id)
                )
                result = cursor.fetchone()

                if result:

                    new_quantity = result['count'] + quantity
                    cursor.execute(
                        "UPDATE corzina SET count = %s WHERE id = %s",
                        (new_quantity, result['id'])
                    )
                else:

                    cursor.execute(
                        "INSERT INTO corzina (id_product, count, id_user) VALUES (%s, %s, %s)",
                        (product_id, quantity, user_id)
                    )

                self.connection.commit()
                return True
        except Error as e:
            print(f"Ошибка при добавлении в корзину: {e}")
            self.connection.rollback()
            return False

    def get_product_id_by_name(self, product_name):
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM product WHERE name = %s",
                    (product_name,)
                )
                result = cursor.fetchone()
                return result['id'] if result else None

    def close(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    def authenticate_user(self, login, password):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name FROM users WHERE login = %s AND password = %s",
                    (login, password)
                )
                return cursor.fetchone()
        except Error as e:
            print(f"Ошибка fdnjhbpfwbb: {e}")
            return None



from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from database import Database
from corzina_main import Ui_Form


class CartWindow(QtWidgets.QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)


        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.user_id = user_id
        self.db = Database()


        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 360, 200))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Название продукта", "Тип", "Количество"])
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)


        self.ui.pushButton.clicked.connect(self.go_back)
        self.ui.pushButton_2.clicked.connect(self.delete_selected)


        self.load_cart()

    def load_cart(self):
        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.name as product_name, t.name as type_name, c.count, c.id
                    FROM corzina c
                    JOIN product p ON c.id_product = p.id
                    JOIN type t ON p.id_type_product = t.id
                    WHERE c.id_user = %s
                """, (self.user_id,))

                cart_items = cursor.fetchall()
                self.tableWidget.setRowCount(len(cart_items))

                for row, item in enumerate(cart_items):
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(item['product_name']))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(item['type_name']))
                    self.tableWidget.setItem(row, 2, QTableWidgetItem(str(item['count'])))

                    self.tableWidget.setItem(row, 3, QTableWidgetItem(str(item['id'])))


                self.tableWidget.setColumnHidden(3, True)

        except Exception as e:
            QMessageBox.critical(self, "Не удалось загрузить корзину: {str(e)}")

    def delete_selected(self):
        selected_rows = {item.row() for item in self.tableWidget.selectedItems()}

        row = selected_rows.pop()
        cart_item_id = int(self.tableWidget.item(row, 3).text())

        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM corzina WHERE id = %s AND id_user = %s",
                    (cart_item_id, self.user_id)
                )
                self.db.connection.commit()
                self.load_cart()
                QMessageBox.information(self, "Товар удален из корзины!")
        except Exception as e:
            self.db.connection.rollback()

    def go_back(self):
        self.close()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from database import Database
from main import MainWindow
from auth import Ui_Form
import sys


class AuthWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.authenticate)

        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.db = Database()

    def authenticate(self):
        login = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()


        user = self.db.authenticate_user(login, password)

        if user:

            self.close()

            self.main_window = MainWindow(user['id'])
            self.main_window.show()
        else:
            QMessageBox.critical(self, "Неверный что то")

    def closeEvent(self, event):
        self.db.close()
        event.accept()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())