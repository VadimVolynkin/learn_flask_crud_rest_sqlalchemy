from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request
from datetime import datetime
from flask_restful import Api, Resource, reqparse

# создаем экземпляр приложения
app = Flask(__name__)

# Flask REST Api code 
api = Api(app) 

# константа определяет вид используемой СУБД (в данном случае SQLite). Другие варианты:
# postgresql://user:password@localhost/mydatabase
# mysql://user:password@localhost/mydatabase
# oracle://user:password@127.0.0.1:1521/mydatabase 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# создание экземпляра SQLAlchemy для работы с БД
db = SQLAlchemy(app)


# ================================================================================================================================
# СОЗДАНИЕ БАЗЫ ДАННЫХ И ТАБЛИЦ
# ================================================================================================================================

# класс Model - базовый класс, который превращает класс Users в модель таблицы для SQLAlchemy
# класс Column - указывает SQLAlchemy воспринимать переменные как поля таблицы
# имя таблицы = имя класса малыми буквами, имена полей таблицы = имена переменных в классе

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def json(self):
        return {"id": self.id, "title": self.title, "text": self.text}


# создаем базу
@app.before_first_request
def create_table():
    db.create_all()


# ================================================================================================================================
# CRUD
# ================================================================================================================================

# create new post
@app.route('/posts/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create_post.html')
 
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        new_post = Post(title=title, text=text)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')


# retrieve list of post
@app.route('/' , methods = ['GET'])
def list_posts():
    posts  = Post.query.all()
    return render_template('posts.html', posts=posts)


# retrieve 1 post
@app.route('/<int:id>')
def get_post(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        return render_template('post.html', post = post)
    return f"Post with id ={id} Doenst exist"   


# update post
@app.route('/<int:id>/update',methods = ['GET','POST'])
def update(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        if post:
            db.session.delete(post)
            db.session.commit()
            title = request.form['title']
            text = request.form['text']

            post = Post(id=id, title=title, text=text)
            db.session.add(post)
            db.session.commit()
            return redirect(f'/{id}')
        return f"Post with id = {id} Does not exist"
 
    return render_template('update_post.html', post = post)


# delete post
@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        if post:
            db.session.delete(post)
            db.session.commit()
            return redirect('/')
        abort(404)
 
    return render_template('delete_post.html')


# ================================================================================================================================
# API REST
# ================================================================================================================================

class PostListAPIView(Resource):

    # get list of posts
    def get(self):
        posts = Post.query.all()
        return {"posts": list(x.json() for x in posts)}

    # create new post
    def post(self):
        data = request.get_json()
        new_post = Post(title=data['title'], text=data['text'])

        db.session.add(new_post)
        db.session.commit()

        return new_post.json(), 201



class PostAPIView(Resource):

    # retrieve 1 post
    def get(self, id):
        post = Post.query.filter_by(id=id).first()

        if post:
            return post.json()
        return {"message": "Post not found"}, 404

    # update post
    def put(self, id):
        data = request.get_json()
        post = Post.query.filter_by(id=id).first()

        if post:
            post.title = data['title']
            post.text = data['text']
            db.session.add(post)
            db.session.commit()
            return post.json()

        return {"message": "Post not found"}, 404


    # delete post
    def delete(self, id):
        post = Post.query.filter_by(id=id).first()

        if post:
            db.session.delete(post)
            db.session.commit()
            return {"message": "Post was Deleted"}
        else:
            return {"message": "Post not found"}, 404


# ROUTES FOR API
api.add_resource(PostListAPIView, '/api/v1/post')
api.add_resource(PostAPIView,'/api/v1/post/<int:id>')


# ================================================================================================================================
# RUN
# ================================================================================================================================

if __name__ == "__main__":
    app.run(debug=True)














