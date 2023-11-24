```python
@app.route("/lists", methods=["POST"])
def create_list():
    name = request.form["list_name"].strip()
    if not 1 <= len(name) <= 100:
        flash("The list name must be between 1 and 100 characters", "error")
        return render_template('new_list.html')
    elif any(lst['name'] == name for lst in session['lists']):
        print("I am here")
        flash("The list name must be unique.", "error")
        return render_template('new_list.html')
    else:
        session['lists'].append({'name': name, 'todos': []})
        flash("The list has been created.", "success")
        session.modified = True
        return redirect(url_for('get_lists'))
```

