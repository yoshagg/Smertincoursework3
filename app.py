import logging

# logging.basicConfig(filename='api.log', level=logging.INFO,
#                     format='%(asctime)s [%(levelname)s] %(message)s', encoding='utf-8')

from flask import Flask, render_template, request, jsonify
from utils import get_posts_all, get_posts_by_user, get_comments_by_post_id, \
    search_for_posts, get_post_by_pk, get_post_by_post_id

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=['GET'])
def feed_page():
    posts = get_posts_all()
    return render_template('index.html', posts=posts)


@app.route("/posts/<int:post_id>", methods=['GET'])
def post_page(post_id):
    post = get_post_by_pk(post_id)
    comments = get_comments_by_post_id(post_id)
    comments_quantity = 0
    for comment in comments:
        if post_id == comment['post_id']:
            comments_quantity += 1
    return render_template('post.html', post=post, comments=comments, comments_quantity=comments_quantity)


@app.route("/search/", methods=["GET"])
def search_page():
    query = request.args.get('s', '')
    posts = search_for_posts(query)
    posts_quantity = 0
    for post in posts:
        posts_quantity += 1
    return render_template('search.html', query=query, posts=posts, posts_quantity=posts_quantity)


@app.route("/user/<username>")
def user_page(username):
    posts = get_posts_by_user(username)
    return render_template('user-feed.html', posts=posts, username=username)


@app.errorhandler(404)
def not_found_error(error):
    """Вьюшка для вывода ошибки 404"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Вьюшка для вывода ошибки 500"""
    return render_template('500.html'), 500


@app.route('/api/posts', methods=["GET"])
def get_posts():
    posts = get_posts_all()
    logging.info("Запрос /api/posts")
    return jsonify(posts)


@app.route('/api/posts/<int:post_id>', methods=["GET"])
def get_posts_by_id(post_id):
    post = get_post_by_post_id(post_id)
    logging.info(f"Запрос /api/posts/{post_id}")
    return jsonify(post)


if __name__ == '__main__':
    app.run()
