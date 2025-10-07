from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/data-entry')
def data_entry():
    return render_template('data_entry.html')


if __name__ == '__main__':
    app.run(debug=True)
