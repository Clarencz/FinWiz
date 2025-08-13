from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel,QPushButton, QLineEdit, QHBoxLayout
from PySide6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np

from analysis.math_tools import calculate_returns, calculate_volatility, calculate_sharpe_ratio, calculate_max_drawdown
from analysis.investment_styles import analyze_investment_style, generate_dummy_returns

class AnalysisViewer(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.create_math_tools_section()
        self.create_investment_style_section()
        
    def create_math_tools_section(self):
        math_group_layout = QVBoxLayout()
        math_group_layout.addWidget(QLabel("<h3>Mathematical Tools</h3>"))
        
        #Input for dummy prices
        price_input_layout = QHBoxLayout()
        price_input_layout.addWidget(QLabel("Dummy prices(comma seperated)"))
        self.price_input = QLineEdit("100,100,39,39,234,34,12,45,121,452")
        price_input_layout.addWidget(self.price_input)
        math_group_layout.addLayout(price_input_layout)
        
        calculate_button = QPushButton("Calculate Metrics")
        calculate_button.clicked.connect(self.calculate_and_display_metrics)
        math_group_layout.addWidget(calculate_button)
        
        self.metrics_label = QLabel("Metrics")
        math_group_layout.addWidget(self.metrics_label)
        
        self.layout.addLayout(math_group_layout)
        
    def calculate_and_display_metrics(self):
        try:
            prices_str = self.price_input.text()
            prices_list = [float(p.strip()) for p in prices_str.split(",")]
            prices = pd.Series(prices_list)
            
            returns = calculate_returns(prices)
            volatility = calculate_volatility(returns)
            sharpe_ratio = calculate_sharpe_ratio(returns)
            max_drawdowns = calculate_max_drawdown(prices)
            
            metrics_text = f"Volatilty: {volatility:.4f}\n"
            metrics_text += f"Sharpe Ratio: {sharpe_ratio:.4f}\n"
            metrics_text += f" Max Drawdown: {max_drawdowns:.4f}"
            self.metrics_label.setText(metrics_text)
        except Exception as e:
            self.metrics_label.setText(f"Error: {e}")
            
    def create_investment_style_section(self):
        style_group_layout = QVBoxLayout()
        style_group_layout.addWidget(QLabel("<h3>Investment Style Analysis</h3>"))
        
        analyze_style_button = QPushButton("Analyze Dummy Style")
        analyze_style_button.clicked.connect(self.analyze_and_display_style)
        style_group_layout.addWidget(analyze_style_button)
        
        self.style_analysis_label = QLabel("Style Analysis: ")
        style_group_layout.addWidget(self.style_analysis_label)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        style_group_layout.addWidget(self.canvas)
        
        self.layout.addLayout(style_group_layout)
        
    def analyze_and_display_style(self):
        try:
            portfolio_returns = generate_dummy_returns()
            benchmark_returns = generate_dummy_returns()
            
            analysis_results = analyze_investment_style(portfolio_returns,benchmark_returns)
            self.style_analysis_label.setText(f"Correlation to Benchmark: {analysis_results['correlation_to_benchmark']:.4f}\nBeta to Benchmark: {analysis_results['beta_to_benchmark']:.4f}\nNotes: {analysis_results['notes']} ")
            
            self.ax.clear()
            self.ax.plot(portfolio_returns.cumsum(),label = 'Portfolio Cumulative Returns')
            self.ax.plot(benchmark_returns.cumsum(),label = "Benchmark Cumulative Returns")
            self.ax.set_title('Cumulative Returns Comparison')
            self.ax.legend()
            self.canvas.draw()
        except Exception as e:
            self.style_analysis_label.setText(f"Error: {e}")



# ===========================new code=================================
