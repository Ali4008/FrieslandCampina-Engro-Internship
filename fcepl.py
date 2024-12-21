import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtWidgets import QApplication, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTabWidget, QFileDialog
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class MilkSalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Milk Sales Form')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        self.button = QPushButton('Enter Milk Sales Data', self)
        self.button.clicked.connect(self.collectData)
        
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def collectData(self):
        farmers_data = []
        while True:
            farmer, okPressed = QInputDialog.getText(self, "Farmer's Name", "Enter farmer's name:")
            if not okPressed or not farmer:
                break
                
            date, okPressed = QInputDialog.getText(self, "Date of Sale", "Enter the date of sale (YYYY-MM-DD):")
            if not okPressed or not date:
                break
                
            litres, okPressed = QInputDialog.getDouble(self, "Amount of Milk", "Enter the amount of milk sold (in litres):", 0, 0, 10000, 2)
            if not okPressed:
                break
                
            farmers_data.append((farmer, date, litres))
            
        self.displayData(farmers_data)
    
    def displayData(self, farmers_data):
        if farmers_data:
            message = "Collected Data:\n"
            for data in farmers_data:
                message += f"Farmer: {data[0]}, Date: {data[1]}, Litres: {data[2]}\n"
        else:
            message = "No data collected."
            
        QMessageBox.information(self, "Milk Sales Data", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MilkSalesForm()
    form.show()
    sys.exit(app.exec_())
