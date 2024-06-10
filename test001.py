import sys
import urllib.request
import json
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from datetime import datetime
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.showMaximized()

    def parse_url(self, url):
        try:
            # Citirea conținutului HTML de la URL
            response = urllib.request.urlopen(url)
            html_content = response.read().decode("utf-8")
            return html_content
        except Exception as e:
            print(f"Error fetching HTML content: {e}")
            return None

    def extract_html_from_json(self, json_content):
        try:
            data = json.loads(json_content)
            html_content = data.get("resource", {}).get("html", "")
            return html_content
        except json.JSONDecodeError:
            print("Error decoding JSON content.")
            return None
    def generate_current_url(self):
        current_date = datetime.now().strftime("%d.%m.%Y")
        current_hour = datetime.now().strftime("%H")
        url_to_load = f"https://m.cinemagia.ro/index.php?_action=getMoreMoviesOnTV&from_date={current_date}&hour={current_hour}&controller=MovieOnTV2"
        return url_to_load

    def show_html_web(self, html_content):
        self.browser.setHtml(html_content)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # url_to_load = "https://m.cinemagia.ro/index.php?_action=getMoreMoviesOnTV&from_date=08.06.2024&hour=22&controller=MovieOnTV2"
    # create the URL-ul by date and hour
    url_to_load = window.generate_current_url()  
    # Load URL-ul and get JSON
    json_content = window.parse_url(url_to_load)  
    if json_content:
        extracted_html = window.extract_html_from_json(json_content)
        if extracted_html:
            window.show_html_web(extracted_html)
            window.show()
            sys.exit(app.exec())
        else:
            print("No HTML content found in the JSON.")
    else:
        print("Failed to fetch JSON content.")

if __name__ == "__main__":
    main()
