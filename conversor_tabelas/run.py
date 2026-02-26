import os, sys, webbrowser
from threading import Timer
from app import app

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/' )

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        app.static_folder = os.path.join(sys._MEIPASS, 'static')
        app.template_folder = os.path.join(sys._MEIPASS, 'templates')
    Timer(1.5, open_browser).start()
    app.run(host='127.0.0.1', port=5000, debug=False)
