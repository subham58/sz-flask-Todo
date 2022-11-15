from datetime import datetime

from flask import Flask, render_template, request, redirect  # imported flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # for creating flask app
# Initiliazing SQLALCHAMY
# process for creating sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# basically used for signalling emitting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.app_context()
db = SQLAlchemy(app)

# Creating a Database class
# pip install flask-sqlalchemy -> It is actually a ORM mapper which facilitates changes
# databases through python

# creating a Todo class


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # whenever we want to print an object of Todo then what we want to see, title pr sno
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

    # Use pip install flask-sqlalchemy == 2.5.1, to avoid the error: Working Outside of Application Context, when you try db.create_all() in terminal.


@app.route('/', methods=['GET', 'POST'])  # Routing multiple pages
def hello_world():
    # HANDLING POST REQUEST
    if request.method == 'POST':
        print('post')
        title = request.form['title']  # printing in terminal
        # print("\n")
        desc = request.form['desc']

    # creating instance/object
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()  # commit -> no. of times user entries, it will be added in the list
    # importing index.html from templates folder
    allTodo = Todo.query.all()  # Fetching all rows
    # print(allTodo) # Jinja 2 is a templating engine and is very helpful when we are creating
    # flask apps, or python variable.
    # all Todo in red is the variable
    return render_template('index.html', allTodo=allTodo)
    # return 'Hello, World!'


@app.route('/products')
def products():
    allTodo = Todo.query.all()  # Fetching all rows
    print(allTodo)  # Basically it's executing the repr function.
    return 'This is football'


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']  # printing in terminal
        # print("\n")
        desc = request.form['desc']

    # creating instance/object
        todos = Todo.query.filter_by(sno=sno).first()
        todos.title = title
        todos.desc = desc
        db.session.add(todos)
        db.session.commit()

        return redirect("/")
    todos = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todos=todos)


# Delete function/route will take a serial number
@app.route('/delete/<int:sno>')
def delete(sno):
    todos = Todo.query.filter_by(sno=sno).first()  # Fetching all rows
    # print(allTodo)  # Basically it's executing the repr function.
    db.session.delete(todos)
    db.session.commit()
    # return 'This is football'
    return redirect("/")


if __name__ == "__main__":
    # Keep debug=true when you are developing a software
    app.run(debug=True, port=8000)
    # Not in production mode
