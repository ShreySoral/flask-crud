from flask import Flask
from flask_scss import Scss
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,redirect,request
from datetime import datetime
# from flask_assets import Environment, Bundle

app=Flask(__name__)
Scss(app, static_dir='static', asset_dir='assets')
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
class MyTask(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(100),nullable=False)
    complete=db.Column(db.Integer,default=0)
    created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

with app.app_context():
    db.create_all()
@app.route('/',methods=["POST","GET"])
def index():
    if request.method=="POST":
        current_task=request.form['content']
        new_task=MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as ex:
            print(f"Error:{ex}")
            return f"Error:{ex}"
    else:
        tasks=MyTask.query.order_by(MyTask.created.desc()).all()
        return render_template("index.html",tasks=tasks)
    
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"
    
@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id:int):
    task=MyTask.query.get_or_404(id)
    if request.method=="POST":
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return render_template('edit.html',task=task)

if __name__ == "__main__":
    app.run(debug=True)