# pip install flask_restful

# ================================================================================================================================
# API REST
# ================================================================================================================================

from flask_restful import Api, Resource, reqparse


# Flask REST Api code 
api = Api(app) 


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








