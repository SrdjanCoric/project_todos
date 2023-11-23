from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists")
def get_lists():
    lists = [
        {"name": "Lunch Groceries", "todos": []},
        {"name": "Dinner Groceries", "todos": []}

    ]
    return render_template('lists.html', lists=lists)

if __name__ == "__main__":
    app.run(debug=True)