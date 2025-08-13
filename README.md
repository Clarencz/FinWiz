# Trade Analyzer

## Project Overview

This project aims to develop a comprehensive desktop application using PySide6 for analyzing trades, evaluating investment styles, and performing mathematical analyses. It will feature PDF and CSV import capabilities, and an integrated sandboxed Python terminal for interactive code execution.

## Architecture Outline

The application will follow a modular architecture to ensure separation of concerns, maintainability, and extensibility. Key modules and their responsibilities are outlined below:

### 1. Core Application (`core/`)
- **`main.py`**: Entry point of the application, initializes the QApplication and the main window.
- **`main_window.py`**: Defines the main application window, including the layout, menu bar, toolbars, and central widget.
- **`config.py`**: Handles application-wide configurations and settings.

### 2. Data Management (`data/`)
- **`data_models.py`**: Defines data structures for trades, investments, and other relevant financial data.
- **`pdf_parser.py`**: Module for parsing and extracting data from PDF documents.
- **`csv_importer.py`**: Module for importing and processing data from CSV files.

### 3. Analysis Modules (`analysis/`)
- **`trade_evaluator.py`**: Contains logic for evaluating individual trades and portfolios.
- **`investment_styles.py`**: Implements algorithms and methodologies for analyzing different investment styles.
- **`math_tools.py`**: Provides mathematical and statistical functions for financial analysis (e.g., risk metrics, performance indicators).

### 4. User Interface (`ui/`)
- **`widgets.py`**: Custom PySide6 widgets used throughout the application.
- **`styles.py`**: Manages application styling, themes (e.g., dark mode), and UI/UX elements.
- **`dialogs.py`**: Defines various dialogs for user interaction (e.g., file open dialogs, settings dialogs).

### 5. Terminal (`terminal/`)
- **`python_terminal.py`**: Implements the interactive Python terminal interface.
- **`sandbox_executor.py`**: Handles the sandboxed execution of Python code to ensure security and stability.

### 6. Utilities (`utils/`)
- **`helpers.py`**: General utility functions.
- **`logger.py`**: Centralized logging utility.

## Development Environment Setup

1. Create a virtual environment:
   `python3 -m venv venv`
2. Activate the virtual environment:
   `source venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`

## Running the Application

`python main.py`




## Running the Application (Important Notes)

Due to the nature of the sandbox environment, directly running the PySide6 application with a graphical user interface is not fully supported. To run this application, you will need a local environment with a display server (e.g., X11 on Linux, or a standard desktop environment on Windows/macOS).

**Steps to run the application locally:**

1.  **Clone the repository:** (If you were to download this project)
    ```bash
    git clone <repository_url>
    cd trade_analyzer
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python main.py
    ```

This will launch the PySide6 desktop application, allowing you to interact with its features, including trade analysis, investment tools, data import, and the integrated Python terminal.


