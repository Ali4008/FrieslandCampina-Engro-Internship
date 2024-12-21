import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QInputDialog, QMessageBox, QLabel, QDateEdit, QHBoxLayout, QDialog, 
                             QDialogButtonBox, QLineEdit, QTabWidget, QTextEdit)
from PyQt5.QtCore import Qt, QDate
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials

# Set the environment variable for credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Hp/Desktop/FCEPL/serviceAccountKey.json"

# Initialize Firebase
cred = credentials.Certificate("C:/Users/Hp/Desktop/FCEPL/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.Client()

class MilkSalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.updateAvailableMilk()  # Update available milk when the app starts
        self.updateAvailableProducts()  # Update available products when the app starts
        
    def initUI(self):
        self.setWindowTitle('Milk Management System')
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: #f0f0f0;")
        
        # Create tabs
        self.tabs = QTabWidget()
        
        # Milk Sales tab
        self.sales_tab = QWidget()
        self.tabs.addTab(self.sales_tab, "Milk Sales")
        self.initSalesTab()
        
        # Milk Collection tab
        self.collection_tab = QWidget()
        self.tabs.addTab(self.collection_tab, "Milk Collection")
        self.initCollectionTab()

        # Milk Production tab
        self.production_tab = QWidget()
        self.tabs.addTab(self.production_tab, "Milk Production")
        self.initProductionTab()

        # Production Overview tab
        self.production_overview_tab = QWidget()
        self.tabs.addTab(self.production_overview_tab, "Production Overview")
        self.initProductionOverviewTab()

        # Primary Sales tab (Distributor)
        self.primary_sales_tab = QWidget()
        self.tabs.addTab(self.primary_sales_tab, "Primary Sales")
        self.initPrimarySalesTab()

        # Final Overview tab
        self.final_overview_tab = QWidget()
        self.tabs.addTab(self.final_overview_tab, "Final Overview")
        self.initFinalOverviewTab()
        
        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        
    def initSalesTab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Milk Sales Data Collection', self.sales_tab)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Instructions
        instructions = QLabel('Please enter the details of each farmer\'s milk sales:', self.sales_tab)
        instructions.setStyleSheet("font-size: 14px; color: #34495e;")
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Available milk display
        self.available_milk_sales_label = QLabel('Total available milk: Calculating...', self.sales_tab)
        self.available_milk_sales_label.setStyleSheet("font-size: 14px; color: #34495e;")
        layout.addWidget(self.available_milk_sales_label)
        
        # Refresh button to update available milk
        self.refresh_sales_button = QPushButton('Refresh Available Milk', self.sales_tab)
        self.refresh_sales_button.setStyleSheet("font-size: 16px; background-color: #3498db; color: white; border-radius: 5px; padding: 10px;")
        self.refresh_sales_button.clicked.connect(self.updateAvailableMilkInSalesTab)
        layout.addWidget(self.refresh_sales_button)
        
        # Collect data button
        self.button = QPushButton('Enter Milk Sales Data', self.sales_tab)
        self.button.setStyleSheet("font-size: 16px; background-color: #3498db; color: white; border-radius: 5px; padding: 10px;")
        self.button.clicked.connect(self.collectData)
        layout.addWidget(self.button)
        
        self.sales_tab.setLayout(layout)
    
    def initCollectionTab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Milk Collection', self.collection_tab)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Date input
        self.collection_date_edit = QDateEdit(self.collection_tab)
        self.collection_date_edit.setCalendarPopup(True)
        self.collection_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.collection_date_edit)
        
        # View button
        self.view_collection_button = QPushButton('View Milk Collection', self.collection_tab)
        self.view_collection_button.setStyleSheet("font-size: 16px; background-color: #3498db; color: white; border-radius: 5px; padding: 10px;")
        self.view_collection_button.clicked.connect(self.viewMilkCollection)
        layout.addWidget(self.view_collection_button)
        
        # Collection display
        self.collection_display = QTextEdit(self.collection_tab)
        self.collection_display.setReadOnly(True)
        self.collection_display.setStyleSheet("font-size: 14px; color: #34495e;")
        layout.addWidget(self.collection_display)
        
        self.collection_tab.setLayout(layout)
    
    def viewMilkCollection(self):
        selected_date = self.collection_date_edit.date().toString("yyyy-MM-dd")
        sales_docs = db.collection('milk_sales').where('date', '==', selected_date).stream()
        
        collection_text = f"Milk Collection on {selected_date}:\n"
        for doc in sales_docs:
            data = doc.to_dict()
            collection_text += f"Farmer: {data.get('farmer', 'N/A')}, Amount: {data.get('litres', 0)} litres\n"
        
        self.collection_display.setText(collection_text)
        
    def initProductionTab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Milk Production', self.production_tab)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Date input
        self.production_date_edit = QDateEdit(self.production_tab)
        self.production_date_edit.setCalendarPopup(True)
        self.production_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.production_date_edit)

        # Available milk display
        self.available_milk_label = QLabel('Calculating available milk...', self.production_tab)
        self.available_milk_label.setStyleSheet("font-size: 14px; color: #34495e;")
        layout.addWidget(self.available_milk_label)
        
        # Refresh button to update available milk
        self.refresh_button = QPushButton('Refresh Available Milk', self.production_tab)
        self.refresh_button.setStyleSheet("font-size: 16px; background-color: #3498db; color: white; border-radius: 5px; padding: 10px;")
        self.refresh_button.clicked.connect(self.updateAvailableMilk)
        layout.addWidget(self.refresh_button)
        
        # Input fields for production quantities
        self.olpers_input = QLineEdit(self.production_tab)
        self.olpers_input.setPlaceholderText('Enter quantity for Olpers (litres)')
        layout.addWidget(self.olpers_input)
        
        self.cream_input = QLineEdit(self.production_tab)
        self.cream_input.setPlaceholderText('Enter quantity for Cream (litres)')
        layout.addWidget(self.cream_input)
        
        self.powder_input = QLineEdit(self.production_tab)
        self.powder_input.setPlaceholderText('Enter quantity for Powder (litres)')
        layout.addWidget(self.powder_input)
        
        self.tarang_input = QLineEdit(self.production_tab)
        self.tarang_input.setPlaceholderText('Enter quantity for Tarang (litres)')
        layout.addWidget(self.tarang_input)
        
        # Produce button
        self.produce_button = QPushButton('Produce Products', self.production_tab)
        self.produce_button.setStyleSheet("font-size: 16px; background-color: #3498db; color: white; border-radius: 5px; padding: 10px;")
        self.produce_button.clicked.connect(self.produceProducts)
        layout.addWidget(self.produce_button)
        
        self.production_tab.setLayout(layout)
    
    def initProductionOverviewTab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Production Overview', self.production_overview_tab)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Date input
        self.production_overview_date_edit = QDateEdit(self.production_overview_tab)
        self.production_overview_date_edit.setCalendarPopup(True)
        self.production_overview_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.production_overview_date_edit)
        
        # View button
        self.view_production_overview_button = QPushButton('View Production Overview', self.production_overview_tab)
        self.view_production_overview_button.setStyleSheet("font-size: 16px; background-color: #3498db; color: white; border-radius: 5px; padding: 10px;")
        self.view_production_overview_button.clicked.connect(self.viewProductionOverview)
        layout.addWidget(self.view_production_overview_button)
        
        # Production overview display
        self.production_overview_display = QTextEdit(self.production_overview_tab)
        self.production_overview_display.setReadOnly(True)
        self.production_overview_display.setStyleSheet("font-size: 14px; color: #34495e;")
        layout.addWidget(self.production_overview_display)
        
        self.production_overview_tab.setLayout(layout)
    
    def viewProductionOverview(self):
        selected_date = self.production_overview_date_edit.date().toString("yyyy-MM-dd")
        production_docs = db.collection('milk_production').where('date', '==', selected_date).stream()
        
        total_production = {
            'olpers': 0,
            'cream': 0,
            'powder': 0,
            'tarang': 0
        }

        for doc in production_docs:
            data = doc.to_dict()
            total_production['olpers'] += data.get('olpers', 0)
            total_production['cream'] += data.get('cream', 0)
            total_production['powder'] += data.get('powder', 0)
            total_production['tarang'] += data.get('tarang', 0)
        
        production_text = (
            f"Production Overview on {selected_date}:\n"
            f"Olpers: {total_production['olpers']} litres\n"
            f"Cream: {total_production['cream']} litres\n"
            f"Powder: {total_production['powder']} litres\n"
            f"Tarang: {total_production['tarang']} litres\n"
            f"Total: {sum(total_production.values())} litres"
        )
        
        self.production_overview_display.setText(production_text)

    def initPrimarySalesTab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Primary Sales (Distributor)', self.primary_sales_tab)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Date input
        self.primary_sales_date_edit = QDateEdit(self.primary_sales_tab)
        self.primary_sales_date_edit.setCalendarPopup(True)
        self.primary_sales_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.primary_sales_date_edit)
        
        # Available products display
        self.available_products_label = QLabel('Calculating available products...', self.primary_sales_tab)
        self.available_products_label.setStyleSheet("font-size: 14px; color: #34495e;")
        layout.addWidget(self.available_products_label)
        
        # Product input fields
        self.olpers_distributor_input = QLineEdit(self.primary_sales_tab)
        self.olpers_distributor_input.setPlaceholderText('Enter quantity for Olpers (litres)')
        layout.addWidget(self.olpers_distributor_input)
        
        self.cream_distributor_input = QLineEdit(self.primary_sales_tab)
        self.cream_distributor_input.setPlaceholderText('Enter quantity for Cream (litres)')
        layout.addWidget(self.cream_distributor_input)
        
        self.powder_distributor_input = QLineEdit(self.primary_sales_tab)
        self.powder_distributor_input.setPlaceholderText('Enter quantity for Powder (litres)')
        layout.addWidget(self.powder_distributor_input)
        
        self.tarang_distributor_input = QLineEdit(self.primary_sales_tab)
        self.tarang_distributor_input.setPlaceholderText('Enter quantity for Tarang (litres)')
        layout.addWidget(self.tarang_distributor_input)
        
        # Update button
        self.update_sales_button = QPushButton('Update Sales', self.primary_sales_tab)
        self.update_sales_button.setStyleSheet("font-size: 16px; background-color: #3498db; color: white; border-radius: 5px; padding: 10px;")
        self.update_sales_button.clicked.connect(self.processDistributorSales)
        layout.addWidget(self.update_sales_button)
        
        self.primary_sales_tab.setLayout(layout)
        self.updateAvailableProducts()  # Update available products when the tab is initialized

    def initFinalOverviewTab(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Final Overview', self.final_overview_tab)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Date input
        self.date_input_button = QPushButton('Select Date', self.final_overview_tab)
        self.date_input_button.setStyleSheet("font-size: 16px; background-color: #3498db; color: white; border-radius: 5px; padding: 10px;")
        self.date_input_button.clicked.connect(self.selectDate)
        layout.addWidget(self.date_input_button)
        
        # Sales display
        self.sales_label = QLabel('Total Milk Sales: N/A', self.final_overview_tab)
        self.sales_label.setStyleSheet("font-size: 14px; color: #34495e;")
        layout.addWidget(self.sales_label)
        
        # Production display
        self.production_label = QLabel('Total Milk Production: N/A', self.final_overview_tab)
        self.production_label.setStyleSheet("font-size: 14px; color: #34495e;")
        layout.addWidget(self.production_label)
        
        # Primary Sales display
        self.primary_sales_label = QLabel('Total Primary Sales: N/A', self.final_overview_tab)
        self.primary_sales_label.setStyleSheet("font-size: 14px; color: #34495e;")
        layout.addWidget(self.primary_sales_label)
        
        self.final_overview_tab.setLayout(layout)

    def selectDate(self):
        dialog = QDialog()
        dialog.setWindowTitle("Select Date")
        
        date_edit = QDateEdit(dialog)
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Date:", dialog))
        layout.addWidget(date_edit)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            selected_date = date_edit.date().toString("yyyy-MM-dd")
            self.updateFinalOverview(selected_date)
    
    def updateFinalOverview(self, selected_date):
        # Calculate total milk sales for the selected date
        total_sales = 0
        sales_docs = db.collection('milk_sales').where('date', '==', selected_date).stream()
        for doc in sales_docs:
            total_sales += doc.to_dict().get('litres', 0)
        self.sales_label.setText(f"Total Milk Sales: {total_sales:.2f} litres")
        
        # Calculate total production for the selected date
        total_production = {
            'olpers': 0,
            'cream': 0,
            'powder': 0,
            'tarang': 0
        }
        production_docs = db.collection('milk_production').where('date', '==', selected_date).stream()
        for doc in production_docs:
            data = doc.to_dict()
            total_production['olpers'] += data.get('olpers', 0)
            total_production['cream'] += data.get('cream', 0)
            total_production['powder'] += data.get('powder', 0)
            total_production['tarang'] += data.get('tarang', 0)
        
        total_production_litres = sum(total_production.values())
        production_text = (
            f"Total: {total_production_litres} litres\n"
            f"Olpers: {total_production['olpers']} litres\n"
            f"Cream: {total_production['cream']} litres\n"
            f"Powder: {total_production['powder']} litres\n"
            f"Tarang: {total_production['tarang']} litres"
        )
        self.production_label.setText(f"Total Milk Production:\n{production_text}")
        
        # Calculate total primary sales for the selected date
        total_primary_sales = {
            'olpers': 0,
            'cream': 0,
            'powder': 0,
            'tarang': 0
        }
        primary_sales_docs = db.collection('distributor_purchases').where('date', '==', selected_date).stream()
        for doc in primary_sales_docs:
            data = doc.to_dict()
            total_primary_sales['olpers'] += data.get('olpers', 0)
            total_primary_sales['cream'] += data.get('cream', 0)
            total_primary_sales['powder'] += data.get('powder', 0)
            total_primary_sales['tarang'] += data.get('tarang', 0)
        
        total_primary_sales_litres = sum(total_primary_sales.values())
        primary_sales_text = (
            f"Total: {total_primary_sales_litres} litres\n"
            f"Olpers: {total_primary_sales['olpers']} litres\n"
            f"Cream: {total_primary_sales['cream']} litres\n"
            f"Powder: {total_primary_sales['powder']} litres\n"
            f"Tarang: {total_primary_sales['tarang']} litres"
        )
        self.primary_sales_label.setText(f"Total Primary Sales:\n{primary_sales_text}")

    def collectData(self):
        while True:
            farmer, okPressed = QInputDialog.getText(self, "Farmer's Name", "Enter farmer's name:")
            if not okPressed or not farmer:
                break

            date, okPressed = self.getDate()
            if not okPressed:
                break

            litres, okPressed = QInputDialog.getDouble(self, "Amount of Milk", "Enter the amount of milk sold (in litres):", 0, 0, 10000, 2)
            if not okPressed:
                break
                
            self.sendDataToFirestore(farmer, date, litres)
            self.updateAvailableMilkOnSale(litres)
    
    def getDate(self):
        dialog = QDialog()
        dialog.setWindowTitle("Select Date")
        
        date_edit = QDateEdit(dialog)
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Date of Sale:", dialog))
        layout.addWidget(date_edit)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            return date_edit.date().toString("yyyy-MM-dd"), True
        else:
            return None, False
    
    def sendDataToFirestore(self, farmer, date, litres):
        doc_ref = db.collection('milk_sales').document()
        doc_ref.set({
            'farmer': farmer,
            'date': date,
            'litres': litres
        })
    
    def updateAvailableMilkOnSale(self, litres_sold):
        # Update the specific date document
        date = QDate.currentDate().toString("yyyy-MM-dd")
        doc_ref = db.collection('milk_available').document(date)
        doc = doc_ref.get()
        if doc.exists:
            current_litres = doc.to_dict().get('litres', 0)
            new_litres = current_litres + litres_sold
        else:
            new_litres = litres_sold
        doc_ref.set({'date': date, 'litres': new_litres})
        
        self.updateTotalAvailableMilk()  # Update the total document
        self.updateAvailableMilkInSalesTab()  # Update the sales tab
        self.updateAvailableMilk()  # Update the production tab
        
    def updateAvailableMilk(self):
        available_milk = self.getTotalAvailableMilk()
        self.available_milk_label.setText(f"Total available milk: {available_milk:.2f} litres")

    def updateAvailableMilkInSalesTab(self):
        available_milk = self.getTotalAvailableMilk()
        self.available_milk_sales_label.setText(f"Total available milk: {available_milk:.2f} litres")
    
    def getTotalAvailableMilk(self):
        total_doc = db.collection('milk_available').document('total').get()
        if total_doc.exists:
            return total_doc.to_dict().get('litres', 0)
        return 0

    def updateMilkAvailableCollection(self, new_amount):
        date = QDate.currentDate().toString("yyyy-MM-dd")
        doc_ref = db.collection('milk_available').document(date)
        doc_ref.set({
            'date': date,
            'litres': new_amount
        })
        self.updateTotalAvailableMilk()
    
    def produceProducts(self):
        try:
            olpers = float(self.olpers_input.text())
            cream = float(self.cream_input.text())
            powder = float(self.powder_input.text())
            tarang = float(self.tarang_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numeric values for all product quantities.")
            return
        
        total_production = olpers + cream + powder + tarang
        available_milk = self.getTotalAvailableMilk()
        
        if total_production > available_milk:
            QMessageBox.warning(self, "Production Error", "Total production exceeds available milk.")
            return
        
        # Get selected date
        date = self.production_date_edit.date().toString("yyyy-MM-dd")
        
        # Save production data to Firestore
        doc_ref = db.collection('milk_production').document()
        doc_ref.set({
            'olpers': olpers,
            'cream': cream,
            'powder': powder,
            'tarang': tarang,
            'date': date
        })
        
        # Update available milk after production
        new_amount = available_milk - total_production
        self.updateMilkAvailableCollection(new_amount)
        self.updateTotalAvailableMilk()
        self.updateAvailableProducts()
        self.updateAvailableMilkInSalesTab()  # Update the sales tab
        self.updateAvailableMilk()  # Update the production tab
        QMessageBox.information(self, "Success", "Production completed successfully.")

    def updateAvailableProducts(self):
        products = {
            'olpers': 0,
            'cream': 0,
            'powder': 0,
            'tarang': 0
        }
        
        production_docs = db.collection('milk_production').stream()
        for doc in production_docs:
            data = doc.to_dict()
            products['olpers'] += data.get('olpers', 0)
            products['cream'] += data.get('cream', 0)
            products['powder'] += data.get('powder', 0)
            products['tarang'] += data.get('tarang', 0)
        
        distributor_sales_docs = db.collection('distributor_purchases').stream()
        for doc in distributor_sales_docs:
            data = doc.to_dict()
            products['olpers'] -= data.get('olpers', 0)
            products['cream'] -= data.get('cream', 0)
            products['powder'] -= data.get('powder', 0)
            products['tarang'] -= data.get('tarang', 0)
        
        available_products_text = (
            f"Olpers: {products['olpers']} litres\n"
            f"Cream: {products['cream']} litres\n"
            f"Powder: {products['powder']} litres\n"
            f"Tarang: {products['tarang']} litres"
        )
        
        self.available_products_label.setText(available_products_text)
    
    def processDistributorSales(self):
        try:
            olpers_qty = float(self.olpers_distributor_input.text())
            cream_qty = float(self.cream_distributor_input.text())
            powder_qty = float(self.powder_distributor_input.text())
            tarang_qty = float(self.tarang_distributor_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numeric values for all quantities.")
            return
        
        # Get selected date
        date = self.primary_sales_date_edit.date().toString("yyyy-MM-dd")
        
        # Get available quantities
        products = {
            'olpers': olpers_qty,
            'cream': cream_qty,
            'powder': powder_qty,
            'tarang': tarang_qty
        }
        
        available_products = self.getAvailableProducts()

        # Check if enough products are available
        for product, qty in products.items():
            if qty > available_products.get(product, 0):
                QMessageBox.warning(self, "Insufficient Stock", f"Not enough {product} available for sale.")
                return

        # Save sales data to Firestore
        doc_ref = db.collection('distributor_purchases').document()
        doc_ref.set({
            'olpers': olpers_qty,
            'cream': cream_qty,
            'powder': powder_qty,
            'tarang': tarang_qty,
            'date': date
        })

        # Update product availability
        self.updateAvailableProducts()
        QMessageBox.information(self, "Success", "Sale processed successfully.")

    def getAvailableProducts(self):
        products = {
            'olpers': 0,
            'cream': 0,
            'powder': 0,
            'tarang': 0
        }
        
        production_docs = db.collection('milk_production').stream()
        for doc in production_docs:
            data = doc.to_dict()
            products['olpers'] += data.get('olpers', 0)
            products['cream'] += data.get('cream', 0)
            products['powder'] += data.get('powder', 0)
            products['tarang'] += data.get('tarang', 0)
        
        distributor_sales_docs = db.collection('distributor_purchases').stream()
        for doc in distributor_sales_docs:
            data = doc.to_dict()
            products['olpers'] -= data.get('olpers', 0)
            products['cream'] -= data.get('cream', 0)
            products['powder'] -= data.get('powder', 0)
            products['tarang'] -= data.get('tarang', 0)
        
        return products

    def updateTotalAvailableMilk(self):
        total_sales_litres = 0
        total_production_litres = 0

        sales_docs = db.collection('milk_sales').stream()
        for doc in sales_docs:
            total_sales_litres += doc.to_dict().get('litres', 0)

        production_docs = db.collection('milk_production').stream()
        for doc in production_docs:
            production_data = doc.to_dict()
            total_production_litres += (
                production_data.get('olpers', 0) +
                production_data.get('cream', 0) +
                production_data.get('powder', 0) +
                production_data.get('tarang', 0)
            )

        available_milk = total_sales_litres - total_production_litres

        total_ref = db.collection('milk_available').document('total')
        total_ref.set({'litres': available_milk})

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MilkSalesForm()
    ex.show()
    sys.exit(app.exec_())
