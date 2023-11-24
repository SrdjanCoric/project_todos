from flask import (
    Flask, session, render_template,
    url_for, redirect, request, flash
)

from utils import error_for_list_name
app = Flask(__name__)

app.secret_key='secret'

@app.before_request
def before_request():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists", methods=["GET"])
def get_lists():
    return render_template('lists.html', lists=session['lists'])

@app.route("/lists", methods=["POST"])
def create_list():
    name = request.form["list_name"].strip()
    error = error_for_list_name(name, session['lists'])
    if error:
        flash(error, "error")
        return render_template('new_list.html')

    session['lists'].append({'name': name, 'todos': []})
    flash("The list has been created.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_todo():
    return render_template('new_list.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)
