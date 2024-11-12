from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QMessageBox, QMenuBar, QMenu, QAction, QFileDialog, QLabel, QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import QPrintDialog
import sys
import os

# remove all comments but keep this one

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About...")
        self.setFixedSize(700, 700)  # Made the about window bigger
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add image
        image_path = os.path.join(os.path.dirname(__file__), 'about.png')
        if os.path.exists(image_path):
            label = QLabel()
            pixmap = QPixmap(image_path)
            label.setPixmap(pixmap.scaled(750, 750, Qt.KeepAspectRatio))  # Scaled image bigger
            layout.addWidget(label)
        
        # Add OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

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
        self.setWindowTitle("NuggyNet Reloaded Early Beta 1")
        self.setGeometry(100, 100, 1024, 768)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create menu bar
        menubar = self.menuBar()
        
        # File menu
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
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # French action
        french_action = QAction('French', self)
        french_action.triggered.connect(lambda: self.add_new_tab("https://en.wikipedia.org/wiki/Baguette"))
        menubar.addAction(french_action)
        
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
        self.forward_btn = QPushButton("[Forward]-->")
        self.reload_btn = QPushButton("[Refresh]")
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL")
        self.new_tab_btn = QPushButton("+ [New Tab]")
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addWidget(self.new_tab_btn)
        nav_layout.addWidget(self.url_bar)
        
        layout.addWidget(self.tabs)
        layout.addWidget(nav_bar)
        
        self.add_new_tab()
        
        self.back_btn.clicked.connect(lambda: self.current_tab().web_view.back())
        self.forward_btn.clicked.connect(lambda: self.current_tab().web_view.forward())
        self.reload_btn.clicked.connect(lambda: self.current_tab().web_view.reload())
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
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
        if self.url_bar.hasFocus():
            return
        self.url_bar.clear()
        self.url_bar.setPlaceholderText(url.toString())
        
    def update_tab_title(self, tab, title):
        index = self.tabs.indexOf(tab)
        if index != -1:
            self.tabs.setTabText(index, title)

    def showEvent(self, event):
        super().showEvent(event)
        msg = QMessageBox()
        msg.setWindowTitle("Just a heads up")
        msg.setText("This is an early beta of one of my new projects.\nBugs will appear and everything is unfinished!\nThis is a very early glimpse into the future of NuggyNet")
        accept_button = msg.addButton("I know what to expect", QMessageBox.AcceptRole)
        reject_button = msg.addButton("No thanks", QMessageBox.RejectRole)
        msg.exec_()
        
        if msg.clickedButton() == reject_button:
            self.show_alright_then_dialog()
        elif msg.clickedButton() == accept_button:
            # Removed the call to self.show_browser()
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

