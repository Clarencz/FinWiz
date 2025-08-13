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
        QTa