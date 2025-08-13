from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
# from data.data_models import Trade,Investment,Portfolio

class TradeViewer(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.setLayout)
        
        self.portfolio_label = QLabel("Current Portfolio: None")
        self.layout.addWidget(self.portfolio_label)
        
        self.trade_table = QTableWidget()
        self.trade_table.setColumnCount(7)
        self.trade_table.setHorizontalHeaderLabels(["Trade ID", "Symbol", "Type","Quantity","Price","Commission"])
        self.trade_table.horizontalHeader().setSectionResizeMode(QHeaderView.stretch)
        self.layout.addWidget(self.trade_table)
        
        