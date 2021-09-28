from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_text = db.Column(db.Text,nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return 'Future Task' + str(self.id)

@app.route('/',methods=['Get','Post'])
def hello():
    if request.method == 'POST':
        post_todo = request.form['todo_text']
        new_todo = Todo(todo_text=post_todo)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    else:
        all_todo =Todo.query.order_by(Todo.date_posted).all()
        return render_template('index.html',todos=all_todo)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>',methods=['Get','Post'])
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method=='POST':
        todo.todo_text = request.form['todo_text']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html',todo=todo)



if __name__=="__main__":
    app.run(debug=True)