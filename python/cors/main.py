from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    url = "https://myapp.com/api/v1/users"
    return render_template('index.html', iframe=url)


if __name__ == "__main__":
    app.run(debug=True)
