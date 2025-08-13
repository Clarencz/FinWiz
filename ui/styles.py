class DarkTheme:
    @staticmethod
    def get_stylesheet():
        return'''
        QWidget{
            background-color:#2e2e2e;
            color:#f0f0f0;
            font-family:Arial,sans-serif;
            font-size:14px;
        }
        QMainWindow{
            background=color:#2e2e2e;
        }
        QMenuBar{
            background-color: #3a3a3a;
            color : f0f0f0;
        }
        QMenuBar::item:selected{
            background-color:#5a5a5a;
            
        }
        QMenu{
            background-color:#3a3a3a;
            color:#f0f0f0;
            border: 1px solid #5a5a5a;
            
        }
        QMenu::item:selected{
            background-color: #5a5a5a;
        }
        QToolBar{
            background-color :#3a3a3a;
            color:#f0f0f0;
            spacing:5px;
        }
        QToolButton{
            background-color:#3a3a3a;
            color:#f0f0f0;
            border:none;
            padding:5px;
        }
        QToolButton:hover{
            background-color:#5a5a5a;
        }
        QStatusBar{
            background-color:#3a3a3a;
            color:#f0f0f0;
        }
        QTabWidget{
            border: 1px solid #5a5a5a;
            background-color: #2e2e2e;
        }
        QTabBar::tab{
            background-color: #3a3a3a;
            color:#f0f0f0;
            padding:8px 20px;
            border:1px solid #5a5a5a;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius:4px;
        }
        QTabBar::tab_selected{
            background-color:#2e2e2e;
            border-bottom-color:#2e2e2e;
        }
        QTabBar::tab:hover{
            background-color: #5a5a5a;
        }
        QTextEdit, QLineEdit{
            background-color:#3a3a3a;
            color:#f0f0f0;
            border:1px solid #5a5a5a;
        }
        QTableWidget{
            background-color:#2e2e2e;
            color:#f0f0f0;
            gridline-color:#5a5a5a;
            border: 1px solid #5a5a5a;
        }
        QHeaderView::section{
            background-color:#3a3a3a;
            color:#f0f0f0;
            padding:5px;
            border:1px solid #5a5a5a
        }
        QPushButton{
            background-color:#5a5a5a;
            color:#f0f0f0;
            border:1px solid #7a7a7a;
            padding: 8px 15px;
            border-radius:4px;
        }
        QPushButton:hover{
            background-color:#7a7a7a;
        }
        QLabel{
            color:#f0f0f0;
        }
        '''