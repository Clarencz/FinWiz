from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from data.data_models import Trade,Investment,Portfolio

class TradeViewer(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.portfolio_label = QLabel("Current Portfolio: None")
        self.layout.addWidget(self.portfolio_label)
        
        self.trade_table = QTableWidget()
        self.trade_table.setColumnCount(7)
        self.trade_table.setHorizontalHeaderLabels(["Trade ID", "Symbol", "Type","Quantity","Price","Commission"])
        self.trade_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.trade_table)
        
        self.investment_table = QTableWidget()
        self.investment_table.setColumnCount(6)
        self.investment_table.setHorizontalHeaderLabels([
            "Investment ID", "Name", "Asset Type", "Current Type", "Quantity Held", "Purchase Price"
        ])
        self.investment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.investment_table)
        
        self.summary_label = QLabel("Summary: ")
        self.layout.addWidget(self.summary_label)
        
    def display_portfolio(self,portfolio:Portfolio):
        self.portfolio_label.setText(f"current portfolio: {portfolio.name}")
        self._populate_trade_table(portfolio.trades)
        self._populate_investment_table(portfolio.investments)
        self._update_summary(portfolio)
        
    def _populate_trade_table(self,trades: list[Trade]):
        self.trade_table.setRowCount(len(trades))
        for row, trade in enumerate(trades):
            self.trade_table.setItem(row, 0, QTableWidgetItem(trade.trade_id))
            self.trade_table.setItem(row, 1, QTableWidgetItem(trade.symbol))
            self.trade_table.setItem(row, 2, QTableWidgetItem(trade.trade_type))
            self.trade_table.setItem(row, 3, QTableWidgetItem(str(trade.quantity)))
            self.trade_table.setItem(row, 4, QTableWidgetItem(str(trade.price)))
            self.trade_table.setItem(row, 5, QTableWidgetItem(trade.trade_date.strftime("%Y-%m-%d")))
            self.trade_table.setItem(row, 6, QTableWidgetItem(str(trade.commission)))
            
    def _populate_investment_table(self,investments: list[Investment]):
        self.investment_table.setRowCount(len(investments))
        for row, investment in enumerate (investments):
            self.investment_table.setItem(row, 0, QTableWidgetItem(investment.investment_id))
            self.investment_table.setItem(row, 1, QTableWidgetItem(investment.name))
            self.investment_table.setItem(row, 2, QTableWidgetItem(investment.asset_type))
            self.investment_table.setItem(row, 3, QTableWidgetItem(str(investment.current_price)))
            self.investment_table.setItem(row, 4, QTableWidgetItem(str(investment.quantity_held)))
            self.investment_table.setItem(row,5, QTableWidgetItem(str(investment.purchase_price) if investment.purchase_price else "N/A"))
            
    def _update_summary(self,portfolio:Portfolio):
        total_value = portfolio.total_value()
        total_commission = portfolio.total_commission()
        summary_text = f"Summary: Total Portfolio Value:: ${total_value:.2f} | Total Commission : {total_commission:.2f}"
        
        self.summary_label.setText(summary_text)