from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == "admin" and password == "secret":
        return "Success"
    else:
        return "Failure"

if __name__ == '__main__':
    app.run(debug=True)
