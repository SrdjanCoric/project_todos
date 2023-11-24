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

@app.route("/lists/<int:id>", methods=["GET"])
def show_list(id):
    list = session['lists'][id]
    return render_template('list.html', id=id, list=list)

@app.route("/lists/<int:id>", methods=["POST"])
def update_list(id):
    name = request.form["list_name"].strip()
    list = session['lists'][id]
    error = error_for_list_name(name, session['lists'])
    if error:
        flash(error, "error")
        return render_template('edit_list.html', list=list, id=id)
    list['name'] = name
    flash("The list has been updated.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route("/lists/<int:id>/edit")
def edit_list(id):
    list = session['lists'][id]
    return render_template('edit_list.html', list=list, id=id)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
