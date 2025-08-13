from PySide6.QtWidgets import *
from PySide6.QtCore import Qt ,QThread, Signal
import sys
import io 


class PythonInterpreterThread(QThread):
    output_signal = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._code_to_execute = None
        
    def run(self):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        sys.stderr = redirected_output
        
        try:
            if self._code_to_execute:
                exec(self._code_to_execute. globals())
        except Exception as e:
            self.output_signal.emit(f"Error: {e}")
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            output = redirected_output.getvalue()
            if output:
                self.output_signal.emit(output)
                
    def execute_code(self,code):
        self._code_to_execute = code
        self.start()
        
class PythonTerminal(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout= QVBoxLayout()
        self.setLayout(self.layout)
        
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setPlaceholderText("Python Terminal Output")
        self.layout.addWidget(self.output_display)
        
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter your python code here..")
        self.input_line.returnPressed.connect(self._execute_command)
        self.layout.addWidget(self.input_line)
        
        self.interpreter_thread = PythonInterpreterThread()
        self.interpreter_thread.output_signal.connect(self._append_output)
        
    def _execute_command(self):
        command = self.input_line.text()
        self.output_display.append(f">>> {command}")
        self.interpreter_thread.execute_code(command)
        
    def _append_output(self,text):
        self.output_display.append(text)