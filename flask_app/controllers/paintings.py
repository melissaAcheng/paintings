from flask_app import app 
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import user, painting



# GET - render new painting form
# localhost:5000/paintings/new
@app.route('/paintings/new')
def new_painting():
    if 'user_id' not in session:
        return redirect('/logout')

    return render_template('new_painting.html')


# POST - create new painting
# localhost:5000/paintings/create
@app.route('/paintings/create', methods=["POST"])
def create_painting():
    if 'user_id' not in session:
        return redirect('/logout')

    if not painting.Painting.validate_painting(request.form):
        return redirect('/paintings/new')

    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": float(request.form["price"]),
        "quantity": int(request.form["quantity"]),
        "user_id": request.form["user_id"],
    }

    new_painting_id = painting.Painting.create_painting(data)
    print("NEW PAINTING ID!!!!!", new_painting_id)

    return redirect('/dashboard')



# READ - display painting
@app.route('/paintings/<int:id>')
def show_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id": id
    }

    purchased_count = painting.Painting.count_paintings(data)

    return render_template('show_painting.html', painting = painting.Painting.get_one_painting(data), purchased_count = purchased_count)

# UPDATE
# GET - render edit form
# localhost:5000/paintings/edit/<int:id>
@app.route('/paintings/edit/<int:id>')
def edit_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'id': id
    }

    return render_template('edit_painting.html', painting = painting.Painting.get_one_painting(data))


# POST - update form
# localhost:5000/paintings/update
@app.route('/paintings/update', methods=["POST"])
def update_painting():
    if 'user_id' not in session:
        return redirect('/logout')

    id = request.form['id']

    if not painting.Painting.validate_painting(request.form):
        return redirect (url_for('edit_painting', id=id))

    painting.Painting.update_painting(request.form)

    return redirect('/dashboard')

# POST - buy painting
@app.route('/paintings/buy', methods=["POST"])
def buy_painting():
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'user_id': request.form['user_id'],
        'painting_id': request.form['painting_id'],
    }
    painting.Painting.buy_painting(data)
    return redirect('/dashboard')


# DELETE painting
# localhost:5000/paintings/delete/<int:id>
@app.route('/paintings/delete/<int:id>')
def delete_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'id': id
    }
    painting.Painting.delete_painting(data)
    return redirect('/dashboard')


