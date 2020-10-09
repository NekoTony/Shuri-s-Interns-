from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.secret_key = 'thisisakey9112'
    app.run(debug=True, port=9000, threaded=True)