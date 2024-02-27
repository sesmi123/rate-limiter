from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/limited', methods=['GET'])
def limited():
    return "Limited, don't over use me!"

@app.route('/unlimited', methods=['GET'])
def unlimited():
    return "Unlimited! Let's Go!"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
