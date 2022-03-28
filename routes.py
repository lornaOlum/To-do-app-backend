
from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False




class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    complete = db.Column(db.Integer)
    
class TodoEncoder(json.JSONEncoder):
  def default(self, Todo):
     if isinstance(Todo, complex):
      return {'description':Todo.description, 'complete':Todo.complete}

    
   

@app.route("/todos", methods=['POST'])
def create_todo():
    todo = Todo(description=request.get_json('description'), complete=request.get_json())
    db.session.add(todo)
    db.session.commit()
    return request.get_json(todo)

@app.route("/todos/<id>", methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)
    todo = Todo(description=request.get_json('description'), complete=request.get_json())
    todo.insert([], todo)
    db.session.add(todo)
    db.session.commit()
    return json.dumps ({'description':Todo.description, 'complete':Todo.complete})


@app.route("/todos", methods=['GET'])
def get_todos():
    
    todos = Todo.query.all()
    
    output = []
    for todo in todos:
        todo_data  = {'description':Todo.description, 'complete':Todo.complete}
        output.append(todo_data)
    
    return json.dumps({'todos':output})

@app.route("/todos/<id>", methods=['GET'])
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    
    return json.dumps ({'description':Todo.description, 'complete':Todo.complete})
    


@app.route("/todos/<id>", methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit
    return json.dumps(Todo.query.all())


@app.route("/healthy")
def healthy():
    db.engine.execute('SELECT 1')
    return ' healthy!!'
    

def __repr__(self):
        return jsonify(f"{ {self.description}, - {self.complete}}")

if __name__ =='__main__':
    app.run(debug=True)
