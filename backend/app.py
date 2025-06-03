from flask import Flask, jsonify

app = Flask(__name__)
@app.route('/')
def home():
    return "backend"

@app.route('/hi')
def hi():
    return jsonify(message="Hi WealthAI User")

if __name__ == '__main__':
    app.run(debug=True)