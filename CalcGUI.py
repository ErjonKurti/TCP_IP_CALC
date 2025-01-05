import sys
import ipaddress
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QStackedWidget, QScrollArea, QScrollBar, QToolTip, QFileDialog

def network_and_broadcast(ip, netmask):
    try:
        network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
        return str(network.network_address), str(network.broadcast_address)
    except ValueError:
        raise ValueError("Adresa IP ose subnet mask nuk jane valide!")

def first_last_ip_and_hosts(ip, netmask):
    try:
        network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
        first_ip = str(network.network_address + 1)
        last_ip = str(network.broadcast_address - 1)
        total_hosts = network.num_addresses - 2
        return first_ip, last_ip, total_hosts
    except ValueError:
        raise ValueError("Adresa IP ose subnet mask nuk jane valide!")

def subnet_info(ip, netmask, subnets):
    try:
        network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
        current_prefix = network.prefixlen
        if subnets <= current_prefix:
            raise ValueError(f"Numri i subneteve duhet te krijohet me prefix me te madh se {current_prefix}")

        subnets_list = list(network.subnets(new_prefix=subnets))
        subnet_info_list = []

        for subnet in subnets_list:
            first_ip = str(subnet.network_address + 1)
            last_ip = str(subnet.broadcast_address - 1)
            total_hosts = subnet.num_addresses - 2
            subnet_info_list.append({
                "Subnet_ID": str(subnet.network_address),
                "Broadcast_ID": str(subnet.broadcast_address),
                "IP_pare": first_ip,
                "IP_Fundit": last_ip,
                "Nr_Hostesh": total_hosts
            })
        return subnet_info_list
    except ValueError:
        raise ValueError("Ka nje gabim ne llogaritjen e subneteve!")

class IP_Calculator_GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Kalkulatori i Adresimit TCP/IP V4')
        self.setGeometry(100, 100, 800, 320)
        self.setStyleSheet("""
            QWidget {background-color: #1e1e1e; font-family: 'Roboto', sans-serif; color: #e5e5e5;}
            QLabel {font-size: 14px; color: #e5e5e5; padding: 5px;}
            QLineEdit {background-color: #2d2d2d; border: 1px solid #444444; color: #e5e5e5; padding: 8px; border-radius: 5px; font-size: 14px; min-width: 250px;}
            QLineEdit:focus {border: 1px solid #7fdb6e;}
            QPushButton {background-color: #4CAF50; color: white; border: none; border-radius: 5px; padding: 10px 16px; font-size: 14px;}
            QPushButton:hover {background-color: #45a049;}
            QPushButton:pressed {background-color: #388E3C;}
            QGroupBox {background-color: #2d2d2d; padding: 20px; border-radius: 10px; border: 1px solid #444444;}
            QGroupBox:title {font-size: 16px; font-weight: bold; color: #7fdb6e;}
        """)

        self.initUI()

    def initUI(self):
        self.stacked_widget = QStackedWidget(self)
        self.page1 = QWidget(self)
        layout1 = QVBoxLayout(self.page1)
        groupBox = QGroupBox('Hyrja e Adreses IP dhe Subnet Mask', self.page1)
        groupBoxLayout = QVBoxLayout()

        self.ip_label = QLabel('Adres IP:', self.page1)
        self.ip_input = QLineEdit(self.page1)
        self.netmask_label = QLabel('Subnet Mask:', self.page1)
        self.netmask_input = QLineEdit(self.page1)

        groupBoxLayout.addWidget(self.ip_label)
        groupBoxLayout.addWidget(self.ip_input)
        groupBoxLayout.addWidget(self.netmask_label)
        groupBoxLayout.addWidget(self.netmask_input)

        groupBox.setLayout(groupBoxLayout)
        self.calculate_button = QPushButton('Llogarit', self.page1)
        self.calculate_button.clicked.connect(self.calculate_results)

        layout1.addWidget(groupBox)
        layout1.addWidget(self.calculate_button)
        self.stacked_widget.addWidget(self.page1)

        self.page2 = QWidget(self)
        layout2 = QVBoxLayout(self.page2)
        self.result_label = QLabel('Rezultatet: ', self.page2)
        layout2.addWidget(self.result_label)

        self.subnets_label = QLabel('Numri i Subneteve (Prefikset):', self.page2)
        self.subnets_input = QLineEdit(self.page2)
        layout2.addWidget(self.subnets_label)
        layout2.addWidget(self.subnets_input)

        self.subnet_button = QPushButton('Llogarit Subnetet', self.page2)
        self.subnet_button.clicked.connect(self.calculate_subnets)
        layout2.addWidget(self.subnet_button)

        self.subnet_result_label = QLabel('Rezultatet per subnete: ', self.page2)
        layout2.addWidget(self.subnet_result_label)
        self.stacked_widget.addWidget(self.page2)

        scroll_area = QScrollArea(self)
        scroll_area.setWidget(self.stacked_widget)
        scroll_area.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def calculate_results(self):
        ip = self.ip_input.text()
        netmask = self.netmask_input.text()

        try:
            network_id, broadcast_id = network_and_broadcast(ip, netmask)
            first_ip, last_ip, total_hosts = first_last_ip_and_hosts(ip, netmask)

            self.result_label.setText(f"Network ID: {network_id}\nBroadcast ID: {broadcast_id}\n"
                                      f"IP e pare: {first_ip}\nIP i fundit: {last_ip}\nNumri i Hosteve te vlefshem: {total_hosts}")
            self.stacked_widget.setCurrentWidget(self.page2)
        except ValueError as e:
            self.result_label.setText(f"Gabim: {e}")

    def calculate_subnets(self):
        ip = self.ip_input.text()
        netmask = self.netmask_input.text()
        subnets = self.subnets_input.text()

        try:
            subnets = int(subnets)
            subnet_info_list = subnet_info(ip, netmask, subnets)
            self.subnet_result_label.setText("Informacionet per subnete: \n")

            for subnet in subnet_info_list:
                self.subnet_result_label.setText(self.subnet_result_label.text() + f"\n\nSubnet_ID: {subnet['Subnet_ID']}\n"
                                                                                  f"Broadcast_ID: {subnet['Broadcast_ID']}\n"
                                                                                  f"IP_pare: {subnet['IP_pare']}\n"
                                                                                  f"IP_Fundit: {subnet['IP_Fundit']}\n"
                                                                                  f"Nr_Hostesh: {subnet['Nr_Hostesh']}")
        except ValueError as e:
            self.subnet_result_label.setText(f"Gabim: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IP_Calculator_GUI()
    window.show()
    sys.exit(app.exec())
