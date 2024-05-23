import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDialog, QLineEdit, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} - {self.price} TL - Stok: {self.stock}"

    def reduce_stock(self, amount=1):
        if self.stock >= amount:
            self.stock -= amount
            return True
        else:
            return False

class Order:
    order_counter = 0

    def __init__(self, content):
        Order.order_counter += 1
        self.order_number = Order.order_counter
        self.content = content

    def __str__(self):
        return f"Sipariş Numarası: {self.order_number}\nİçerik: {self.content}\n"

class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def __str__(self):
        customer_info = f"Müşteri Adı: {self.name}\nAdres: {self.address}\n"
        order_info = "\n".join(str(order) for order in self.orders)
        return customer_info + order_info + "\n"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Restoran Sipariş ve Yönetim Sistemi")
        self.setGeometry(800, 250, 400, 300)

        self.setStyleSheet("background-color: #e6f7ff;")

        self.label = QLabel("Hoş Geldiniz!", self)
        self.label.setStyleSheet("font-size: 42px;")
        self.label.setAlignment(Qt.AlignCenter)

        self.order_button = QPushButton("Sipariş Ver", self)
        self.order_button.setStyleSheet(
            "QPushButton { background-color: #007bff; color: white; border: none; border-radius: 5px; padding: 18px; } QPushButton:hover { background-color: #0056b3; }")
        self.order_button.clicked.connect(self.get_customer_info_and_show_menu)

        self.customer_button = QPushButton("Müşteri Bilgileri ve Sipariş Geçmişi", self)
        self.customer_button.setStyleSheet(
            "QPushButton { background-color: #28a745; color: white; border: none; border-radius: 5px; padding: 18px; } QPushButton:hover { background-color: #218838; }")
        self.customer_button.clicked.connect(self.show_customer_info)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.order_button)
        self.layout.addWidget(self.customer_button)

        self.setLayout(self.layout)

        self.products = []
        self.add_sample_products()

        self.customers = []

        self.checkboxes = []

    def add_sample_products(self):
        self.products.append(Product("Köfte", 20, 50))
        self.products.append(Product("Pizza", 30, 30))
        self.products.append(Product("Salata", 15, 20))
        self.products.append(Product("Çorba", 10, 40))
        self.products.append(Product("Kebap", 25, 35))
        self.products.append(Product("Lahmacun", 8, 60))
        self.products.append(Product("Pilav", 12, 45))
        self.products.append(Product("Tavuk", 18, 25))
        self.products.append(Product("Balık", 35, 20))
        self.products.append(Product("Makarna", 14, 30))
        self.products.append(Product("Kahve", 5, 50))
        self.products.append(Product("Çay", 3, 55))
        self.products.append(Product("Su", 1, 100))
        self.products.append(Product("Kola", 4, 40))
        self.products.append(Product("Meyve Suyu", 6, 30))
        self.products.append(Product("Bira", 7, 25))
        self.products.append(Product("Şarap", 15, 20))
        self.products.append(Product("Margarita", 20, 15))
        self.products.append(Product("Pasta", 18, 25))
        self.products.append(Product("Dondurma", 10, 30))
        self.products.append(Product("Waffle", 12, 20))
        self.products.append(Product("Cheesecake", 15, 15))
        self.products.append(Product("Tiramisu", 16, 15))
        self.products.append(Product("Kumpir", 18, 20))

    def get_customer_info_and_show_menu(self):
        customer_dialog = QDialog(self)
        customer_dialog.setWindowTitle("Müşteri Bilgileri")
        layout = QVBoxLayout()

        name_label = QLabel("Adınız ve Soyadınız:")
        self.name_input = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        address_label = QLabel("Adresiniz:")
        self.address_input = QLineEdit()
        layout.addWidget(address_label)
        layout.addWidget(self.address_input)

        layout.addSpacing(20)

        product_label = QLabel("Ürünler:")
        layout.addWidget(product_label)

        self.checkboxes = []

        for product in self.products:
            checkbox = QCheckBox(str(product))
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        confirm_button = QPushButton("Onayla")
        confirm_button.clicked.connect(self.show_menu)
        layout.addWidget(confirm_button)

        customer_dialog.setLayout(layout)
        customer_dialog.exec_()

    def show_menu(self):
        selected_products = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                selected_products.append(checkbox.text())

        if selected_products:
            menu_dialog = QDialog(self)
            menu_dialog.setWindowTitle("Menü")
            layout = QVBoxLayout()

            for product in selected_products:
                label = QLabel(product)
                layout.addWidget(label)

            confirm_button = QPushButton("Sipariş Ver")
            confirm_button.clicked.connect(self.place_order)
            layout.addWidget(confirm_button)

            menu_dialog.setLayout(layout)
            menu_dialog.exec_()
        else:
            QMessageBox.information(self, "Bilgi", "Lütfen en az bir ürün seçin.")

    def place_order(self):
        name = self.name_input.text()
        address = self.address_input.text()

        if name.strip() and address.strip():
            selected_products = []

            for checkbox in self.checkboxes:
                if checkbox.isChecked():
                    selected_products.append(checkbox.text())

            if selected_products:
                customer = Customer(name=name, address=address)
                order_content = ", ".join(selected_products)
                new_order = Order(content=order_content)
                customer.add_order(new_order)
                self.customers.append(customer)
                print(new_order)

                for product_name in selected_products:
                    for product in self.products:
                        if product_name.startswith(product.name):
                            product.reduce_stock()
                            break

            else:
                QMessageBox.information(self, "Bilgi", "Lütfen en az bir ürün seçin.")
        else:
            QMessageBox.information(self, "Bilgi", "Lütfen adınızı, soyadınızı ve adresinizi girin.")

    def show_customer_info(self):
        if self.customers:
            customer_dialog = QDialog(self)
            customer_dialog.setWindowTitle("Müşteri Bilgileri ve Sipariş Geçmişi")
            layout = QVBoxLayout()

            for customer in self.customers:
                customer_info_label = QLabel(str(customer))
                layout.addWidget(customer_info_label)
                layout.addSpacing(20)

            customer_dialog.setLayout(layout)
            customer_dialog.exec_()
        else:
            QMessageBox.information(self, "Bilgi", "Henüz bir sipariş verilmemiş.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
