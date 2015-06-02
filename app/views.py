from app import app

@app.route('/')
def index():
    return "Hello, CTY 2015!"
