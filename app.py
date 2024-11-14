from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QMessageBox, QMenuBar, QMenu, QAction, QFileDialog, QLabel, QDialog, QDockWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import QPrintDialog
import sys
import os

button_style = """
    QPushButton {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #404040;
        font-size: 12px;
        min-width: 80px;
        min-height: 20px;
        padding: 5px 0px;
    }
    QPushButton:hover {
        background-color: #404040;
    }
    QPushButton:pressed {
        background-color: #1a1a1a;
    }
    QPushButton:checked {
        background-color: #404040;
        border: 2px solid #606060;
    }
    QMessageBox QPushButton {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #404040;
        font-size: 12px;
        min-width: 80px;
        min-height: 20px;
        padding: 5px 0px;
    }
    QMessageBox QPushButton:hover {
        background-color: #404040;
    }
    QMessageBox QPushButton:pressed {
        background-color: #1a1a1a;
    }
"""

dark_theme = """
    QMainWindow, QDialog {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    QTabWidget::pane {
        border: 1px solid #404040;
        background-color: #1a1a1a;
    }
    QTabBar::tab {
        background-color: #2d2d2d;
        color: #ffffff;
        padding: 8px;
        border: 1px solid #404040;
        border-radius: 5px;
    }
    QTabBar::tab:selected {
        background-color: #404040;
        border: 2px solid #606060;
        border-radius: 10px;
    }
    QTabBar::tab:active {
        background-color: #404040;
        border: 2px solid #606060;
    }
    QLineEdit {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #404040;
        border-radius: 5px;
        padding: 5px;
        font-size: 12px;
    }
    QMenuBar {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
    }
    QMenuBar::item:selected {
        background-color: #404040;
        border-radius: 5px;
    }
    QMenu {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
    }
    QMenu::item:selected {
        background-color: #404040;
    }
    QMenu::drop-down {
        background-color: #404040;
        border-radius: 5px;
    }
    QLabel {
        color: #ffffff;
        border-radius: 5px;
    }
    QMessageBox {
        background-color: #1a1a1a;
        color: #ffffff;
        border-radius: 5px;
    }
"""

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About...")
        self.setFixedSize(700, 700)  
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter)
        
        image_path = os.path.join(os.path.dirname(__file__), 'about.png')
        if os.path.exists(image_path):
            label = QLabel()
            pixmap = QPixmap(image_path)
            scaled_size = pixmap.size() * 0.75
            label.setPixmap(pixmap.scaled(scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setAlignment(Qt.AlignCenter)
            center_layout.addWidget(label)
        
        layout.addWidget(center_widget)
        
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 10, 10)
        button_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        
        ok_button = QPushButton("OK")
        ok_button.setFixedSize(80, 20)
        ok_button.setStyleSheet(button_style)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        layout.addWidget(button_container)

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.web_view = QWebEngineView()
        self.web_view.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.web_view)
        nwin_path = os.path.join(os.path.dirname(__file__), 'nwin.html')
        self.web_view.setUrl(QUrl.fromLocalFile(nwin_path))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drift [Beta 0.1.1]")
        self.setGeometry(100, 100, 1024, 768)
        self.school_mode = False
        
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        menubar = self.menuBar()
        
        
        file_menu = menubar.addMenu('File')
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        print_action = QAction('Print', self)
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        special_menu = menubar.addMenu('Special')
        self.school_mode_action = QAction('School Mode', self)
        self.school_mode_action.setCheckable(True)
        self.school_mode_action.triggered.connect(self.toggle_school_mode)
        special_menu.addAction(self.school_mode_action)
        
        french_action = QAction('French', self)
        french_action.triggered.connect(lambda: self.add_new_tab("https://en.wikipedia.org/wiki/Baguette"))
        special_menu.addAction(french_action)
        
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)        # Add beta notice to menubar
        beta_notice = menubar.addAction("Drift is in very early beta! Expect things to not work how you expect, some things may have no code, and this app is gonna be a macOS exclusive at some point")
        beta_notice.setEnabled(False)

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.setDocumentMode(True)
        
        nav_bar = QWidget()
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(2, 2, 2, 2)
        nav_bar.setLayout(nav_layout)
        
        self.back_btn = QPushButton("<--[Go Back]")
        self.back_btn.setStyleSheet(button_style)
        self.forward_btn = QPushButton("[Forward]-->")
        self.forward_btn.setStyleSheet(button_style)
        self.reload_btn = QPushButton("[Refresh]")
        self.reload_btn.setStyleSheet(button_style)
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL (doesn't need HTTPS prefix)")
        self.new_tab_btn = QPushButton("+ [New Tab]")
        self.new_tab_btn.setStyleSheet(button_style)
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        
        self.ice_social_btn = QPushButton("[IceSocial]")
        self.ice_social_btn.setStyleSheet(button_style)
        self.ice_social_btn.setCheckable(True)
        self.ice_social_btn.clicked.connect(self.toggle_ice_social)
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addWidget(self.new_tab_btn)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.ice_social_btn)
        
        layout.addWidget(self.tabs)
        layout.addWidget(nav_bar)
        
        self.ice_social_dock = QDockWidget(self)
        self.ice_social_dock.setTitleBarWidget(QWidget())
        self.ice_social_dock.setFixedWidth(220)
        self.ice_social_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        ice_social_widget = QWidget()
        ice_social_layout = QVBoxLayout(ice_social_widget)
        ice_social_layout.setContentsMargins(0, 0, 0, 0)
        
        self.ice_social_view = QWebEngineView()
        self.ice_social_view.setUrl(QUrl("https://icesocial.net"))
        ice_social_layout.addWidget(self.ice_social_view)
        
        self.ice_social_dock.setWidget(ice_social_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.ice_social_dock)
        self.ice_social_dock.hide()
        
        self.add_new_tab()
        
        self.back_btn.clicked.connect(lambda: self.current_tab().web_view.back())
        self.forward_btn.clicked.connect(lambda: self.current_tab().web_view.forward())
        self.reload_btn.clicked.connect(lambda: self.current_tab().web_view.reload())
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        app = QApplication.instance()
        app.setStyleSheet(dark_theme + button_style)
        
    def toggle_school_mode(self):
        self.school_mode = self.school_mode_action.isChecked()
        if self.school_mode:
            self.setWindowTitle("Drift Education 0.1.1")
            self.ice_social_btn.hide()
            self.ice_social_dock.hide()
        else:
            self.setWindowTitle("Drift [Beta 0.1.1]")
            self.ice_social_btn.show()
            
    def toggle_ice_social(self):
        if self.ice_social_btn.isChecked():
            self.ice_social_dock.show()
        else:
            self.ice_social_dock.hide()
        
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()
        
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", 
            "HTML Files (*.html);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                html = f.read()
            new_tab = self.add_new_tab()
            new_tab.web_view.setHtml(html, QUrl.fromLocalFile(file_name))
            
    def print_page(self):
        printer = QPrintDialog()
        if printer.exec_() == QPrintDialog.Accepted:
            self.current_tab().web_view.page().print(printer.printer())
        
    def add_new_tab(self, url=None):
        new_tab = BrowserTab()
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)
        if url:
            new_tab.web_view.setUrl(QUrl(url))
        new_tab.web_view.urlChanged.connect(lambda url: self.update_url_bar(url))
        new_tab.web_view.titleChanged.connect(lambda title: self.update_tab_title(new_tab, title))
        return new_tab
        
    def current_tab(self):
        return self.tabs.currentWidget()
        
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            sys.exit(1)
        
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        self.current_tab().web_view.setUrl(QUrl(url))
        self.url_bar.clear()
        
    def update_url_bar(self, url):
        pass
        
    def update_tab_title(self, tab, title):
        index = self.tabs.indexOf(tab)
        if index != -1:
            self.tabs.setTabText(index, title)

    def showEvent(self, event):
        super().showEvent(event)
        msg = QMessageBox()
        msg.setWindowTitle("Just a heads up")
        msg.setText("This is an early beta of one of my new projects.\nBugs will appear and everything is unfinished!\nThis is a very early glimpse into the future of Drift")
        accept_button = msg.addButton("I know what to expect", QMessageBox.AcceptRole)
        reject_button = msg.addButton("I'd rather wait", QMessageBox.RejectRole)
        accept_button.setStyleSheet(button_style)
        reject_button.setStyleSheet(button_style)
        msg.exec_()
        
        if msg.clickedButton() == reject_button:
            self.show_alright_then_dialog()
        elif msg.clickedButton() == accept_button:
            pass
        else:
            sys.exit(0)
        
        if msg.clickedButton() == reject_button:
            self.show_alright_then_dialog()

    def show_alright_then_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Alright then")
        msg.setText("You understand the risks of beta testing.\nYou can run the app by clicking \"I know what to expect.\"")
        alright_button = msg.addButton("Alright", QMessageBox.AcceptRole)
        alright_button.setStyleSheet(button_style)
        msg.exec_()
        
        if msg.clickedButton() == alright_button:
            sys.exit(0)
        
        if msg.clickedButton() == alright_button:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('WindowsVista')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())
    sys.exit(app.exec_())
