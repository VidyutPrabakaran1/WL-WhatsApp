'''
MIT License

Copyright (c) 2025 Vidyut Prabakaran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtGui import QIcon



# Optional: Silence QSocketNotifier warning
os.environ["QT_LOGGING_RULES"] = "*.debug=false"


class WhatsAppViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WhatsApp Web Viewer")
        self.setGeometry(100, 100, 1200, 800)

        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.png')))

        # Custom User-Agent to prevent "Update Chrome" warning
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        # Web Browser Widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://web.whatsapp.com/"))
        self.setCentralWidget(self.browser)

        # Force WhatsApp Web to use Dark Mode (via injected JS)
        self.browser.loadFinished.connect(self.inject_dark_mode)

        # Navigation Toolbar
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        self.back_btn = QAction("← Back", self)
        self.back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(self.back_btn)

        self.forward_btn = QAction("→ Forward", self)
        self.forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(self.forward_btn)

        reload_btn = QAction("⟳ Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        about_btn = QAction("ℹ About", self)
        about_btn.triggered.connect(self.show_about_dialog)
        nav_bar.addAction(about_btn)

        # Update nav buttons after each page load
        self.browser.loadFinished.connect(self.update_nav_buttons)

    def inject_dark_mode(self):
        """Inject JS to force WhatsApp Web into Dark Mode."""
        js_code = """
        if (!document.documentElement.classList.contains('dark')) {
            const darkModeToggle = document.querySelector('button[data-testid="menu-dark-mode"]');
            if (darkModeToggle) {
                darkModeToggle.click();
            }
        }
        """
        self.browser.page().runJavaScript(js_code)

    def update_nav_buttons(self):
        self.back_btn.setEnabled(self.browser.history().canGoBack())
        self.forward_btn.setEnabled(self.browser.history().canGoForward())

    def show_about_dialog(self):
        QMessageBox.information(
            self,
            "About WhatsApp Viewer",
            "WL-WhatsApp\nVersion: 1.0\nAuthor: Vidyut Prabakaran"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the application style to Fusion (force dark mode)
    app.setStyle("Fusion")

    # Set the dark palette
    dark_palette = QPalette()

    # Dark colors
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
    dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    # Apply the dark palette
    app.setPalette(dark_palette)

    viewer = WhatsAppViewer()
    viewer.show()
    sys.exit(app.exec_())
