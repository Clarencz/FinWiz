from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout,QLabel,QMenuBar,QToolBar,QStatusBar,QTableWidget
from PySide6.QtCore import Qt
from ui.trade_viewer import TradeViewer
from ui.analysis_viewer import AnalysisViewer
from ui.file_importer_widget import FileImporterWidget
from ui.styles import DarkTheme
from terminal.python_terminal import PythonTerminal
from data.data_models import Trade, Investment,Portfolio
from datetime import datetime

class MainWindow (QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financial Wizard")
        self.setGeometry(100,100,1200,800)
        
        #====Apply dark theme====
        self.setStyleSheet(DarkTheme.get_stylesheet())
        
        self._create_menu_bar()
        # self._create_tool_bar()
        # self._create_status_bar()
        # self._create_central_widget()
        # self._load_dummy_data()
        
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        #File menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("&Open..")
        file_menu.addAction("&Save")
        file_menu.addSeparator()
        file_menu.addAction("&Exit")
        
        #Edit Menu
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("&Cut")
        edit_menu.addAction("&Copy")
        edit_menu.addAction("&Paste")
        
        #View Menu
        view_menu= menu_bar.addMenu("&View")
        view_menu.addAction("&Toolbar")
        view_menu.addAction("&Status Bar")
        
        #Tools Menu 
        tool_menu = menu_bar.addMenu("&Tools")
        tool_menu.addAction("&Terminal")
        tool_menu.addAction("&Settings")
        
        #Help Menu
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction("&About")
        
    def _create_tool_bar(self):
        tool_bar = QToolBar("Main Toolbar")
        self.addToolBar(tool_bar)
        
        tool_bar.addAction("Open")
        tool_bar.addAction("Save")
        tool_bar.addSeparator()
        tool_bar.addAction("Run Terminal")
        
    def _create_central_widget(self):
        self.tab_widget = QTableWidget()
        self.setCentralWidget(self.tab_widget)
        
        #Tabs
        self.trade_analysis_tab = TradeViewer()
        self.investment_styles_tab = AnalysisViewer()
        self.file_importer_tab = FileImporterWidget()
        self.terminal_tab = PythonTerminal()
        
        self.tab_widget.addTab(self.trade_analysis_tab, "Trade Analysis")
        self.tab_widget.addTab(self.investment_styles_tab, "Investment & Math Tools")
        self.tab_widget.addTab(self.file_importer_tab, "Import Data")
        self.tab_widget.addTab(self.terminal_tab,"Terminal")
        
    def _load_dummy_data(self):
        # Create dummy trades
        trade1 = Trade("T001", "AAPL", "BUY", 10, 150.00, datetime(2023, 1, 10), 5.00)
        trade2 = Trade("T002", "GOOGL", "SELL", 5, 100.00, datetime(2023, 2, 15), 3.50)
        trade3 = Trade("T003", "MSFT", "BUY", 20, 250.00, datetime(2023, 3, 20), 7.00)

        # Create dummy investments
        inv1 = Investment("I001", "Apple Inc.", "Stock", 155.00, 10, datetime(2023, 1, 10), 150.00)
        inv2 = Investment("I002", "Alphabet Inc.", "Stock", 102.00, 5, datetime(2023, 2, 15), 100.00)
        inv3 = Investment("I003", "Microsoft Corp.", "Stock", 255.00, 20, datetime(2023, 3, 20), 250.00)
        
    #     #create a dummy portfolio
        my_portfolio = Portfolio("P001","My firs