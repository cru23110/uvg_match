from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pro_version')
def pro_version():
    return render_template('pro_version.html')


if __name__ == '__main__':
    app.run(debug=True)

