from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from data.data_importer import DataImporter
import pandas as pd

class FileImporterWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.data_importer = DataImporter()
        
        self.import_csv_button = QPushButton("Import CSV")
        self.import_csv_button.clicked.connect(self._import_csv_file)
        self.layout.addWidget(self.import_csv_button)
        
        self.import_pdf_button = QPushButton("Import PDF Text")
        self.import_pdf_button.clicked.connect(self._import_pdf_text_file)
        self.layout.addWidget(self.import_pdf_button)
        
        self.import_pdf_tables_button = QPushButton("Import PDF Tabled (placeholder)")
        self.import_pdf_tables_button.clicked.connect(self._import_pdf_tables_file)
        self.layout.addWidget(self.import_pdf_tables_button)
        
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setPlaceholderText("Imported content will appear here")
        self.layout.addWidget(self.text_display)
        
        self.table_display = QTableWidget()
        self.table_display.setColumnCount(0)
        self.table_display.setRowCount(0)
        self.table_display.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table_display)
        
    def _import_csv_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File","","CSV Files (**.csv);; All Files(*)")
        if file_name:
            df = self.data_importer.import_csv(file_name)
            if not df.empty:
                self._display_dataframe_in_table(df)
                self.text_display.clear()
            else:
                self.text_display.setText("Failed to import CSV or CSV is empty")
                self.table_display.clearContents()
                self.table_display.setRowCount(0)
                self.table_display.setColumnCount(0)
                
    def _import_pdf_text_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "" , "PDF Files (*.pdf);;All Files(*)")
        if file_name:
            text = self.data_importer.import_pdf_text(file_name)
            if text:
                self.text_display.setText(text)
                self.table_display.clearContents()
                self.table_display.setRowCount(0)
                self.table_display.setColumnCount(0)
            else:
                self.text_display.setText("Failed to extract text from PDF or PDF is empty")
                
    def _import_pdf_tables_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File","", "PDF Files(*.pdf);;All Files(*)")
        if file_name:
            tables = self.data_importer.import_pdf_tables(file_name)
            if tables:
                self._display_dataframe_in_table(tables[0])
                self.text_display.setText("PDF table extraction attempted. Displaying first table found")
            else:
                self.text_display.setText("No tables extracted from PDF or extraction failed")
                self.table_display.clearContents()
                self.table_display.setRowCount(0)
                self.table_display.setColumnCount(0)
                
    def _display_dataframe_in_table(self,df:pd.DataFrame):
        self.table_display.setRowCount(df.shape[0])
        self.table_display.setColumnCount(df.shape[1])
        self.table_display.setHorizontalHeaderLabels(df.column.astype(str))
        
        for row_idx, row_data in df.iterrows():
            for col_idx, cell_data in enumerate (row_data):
                self.table_display.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))