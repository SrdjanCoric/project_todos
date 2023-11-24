from flask import (
    Flask, session, render_template,
    url_for, redirect, request, flash
)

from utils import (
    error_for_list_name, error_for_todo, list_class, is_list_completed,
    todos_remaining_count, todos_count, sort_items, is_todo_completed
)
app = Flask(__name__)

app.secret_key='secret'


@app.context_processor
def utility_processor():
    return dict(is_list_completed=is_list_completed,
                list_class=list_class, todos_count=todos_count,
                todos_remaining_count=todos_remaining_count,
                sort_items=sort_items, is_todo_completed=is_todo_completed
            )

@app.before_request
def before_request():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('show_lists'))

@app.route("/lists", methods=["GET"])
def show_lists():
    lists = session['lists']
    return render_template('lists.html', lists=lists)

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
    return redirect(url_for('show_lists'))

@app.route("/lists/new")
def add_todo():
    return render_template('new_list.html')

@app.route("/lists/<int:id>", methods=["GET"])
def show_list(id):
    lst = session['lists'][id]
    return render_template('list.html', list=lst, list_id=id)

@app.route("/lists/<int:id>", methods=["POST"])
def update_list(id):
    name = request.form["list_name"].strip()
    list = session['lists'][id]
    error = error_for_list_name(name, session['lists'])
    if error:
        flash(error, "error")
        return render_template('edit_list.html', list=list)
    list['name'] = name
    flash("The list has been updated.", "success")
    session.modified = True
    return redirect(url_for('show_lists'))

@app.route("/lists/<int:id>/edit")
def edit_list(id):
    list = session['lists'][id]
    return render_template('edit_list.html', list=list)

@app.route("/lists/<int:id>/delete", methods=["POST"])
def delete_list(id):
    del session['lists'][id]
    flash("The list has been deleted.", "success")
    session.modified = True
    return redirect(url_for('show_lists'))

@app.route("/lists/<int:list_id>/todos", methods=["POST"])
def create_todo(list_id):
    todo_name = request.form["todo"].strip()
    list = session['lists'][list_id]

    error = error_for_todo(todo_name)
    if error:
        flash(error, "error")
        return render_template('list.html', list=list, list_id=list_id)

    list['todos'].append({'name': todo_name, 'completed': False})
    flash("The todo was added.", "success")
    session.modified = True
    return redirect(url_for('show_list', id=list_id))

@app.route("/lists/<int:list_id>/todos/<int:id>/delete", methods=["POST"])
def delete_todo(list_id, id):
    list = session['lists'][list_id]
    del list['todos'][id]
    flash("The todo has been deleted.", "success")
    session.modified = True
    return redirect(url_for('show_list', id=list_id))

@app.route("/lists/<int:list_id>/todos/<int:id>", methods=["POST"])
def update_todo_status(list_id, id):
    list = session['lists'][list_id]
    is_completed = request.form['completed'] == 'True'
    list['todos'][id]['completed'] = is_completed

    flash("The todo has been updated.", "success")
    session.modified = True
    return redirect(url_for('show_list', id=list_id))

@app.route("/lists/<int:id>/complete_all", methods=["POST"])
def mark_all_todos_completed(id):
    list = session['lists'][id]
    for todo in list['todos']:
        todo['completed'] = True

    flash("All todos have been updated.", "success")
    session.modified = True
    return redirect(url_for('show_list', id=id))

if __name__ == "__main__":
    app.run(debug=False)
