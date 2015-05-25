from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to CTY 2015!"

if __name__ == '__main__':
    app.run()

