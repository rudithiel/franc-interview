from flask import Flask, render_template, jsonify, Response, request
import json
import datetime

app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    with open('./users.json', 'r') as f:
        users = json.loads(f.read())
    if username in users.keys():
        userPosts = []
        following = users[username]
        with open('./posts.json', 'r') as f:
            allPosts = json.loads(f.read())
        for follower in following:
            posts = allPosts[follower]
            for post in posts:
                post['author'] = follower
                post['time'] = datetime.datetime.strptime(post['time'], "%Y-%m-%dT%H:%M:%SZ")
                post['time'] = post['time'].strftime('%Y/%m/%d %H:%M:%S')
                userPosts.append(post)
        userPosts = sorted(userPosts, key=lambda d: d['time'], reverse=True)
        return render_template('index.html', username = username, posts=userPosts)
    return render_template('index.html')

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='127.0.0.1')