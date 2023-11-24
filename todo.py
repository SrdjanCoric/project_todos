from flask import Flask, session, render_template, url_for, redirect, request, flash
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
    if 1 <= len(name) <= 100:
        session['lists'].append({'name': name, 'todos': []})
        flash("The list has been created.", "success")
        session.modified = True
        return redirect(url_for('get_lists'))
    else:
        flash("The list name must be between 1 and 100 characters", "error")
        return render_template('new_list.html')

@app.route("/lists/new")
def add_todo():
    return render_template('new_list.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)