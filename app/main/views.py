from flask import request, render_template, redirect, url_for, jsonify
from . import main
from .forms import PostForm
from ..models import Post, Tag
from .. import db
from collections import defaultdict
from flask_login import login_required

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    posts = pagination.items
    tags = Tag.query.all()
    return render_template('index.html', posts=posts, pagination=pagination, tags=tags)

@main.route('/edit-post', methods=['GET', 'POST'])
@login_required
def edit_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        tag_ids = form.tag.data
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag is not None:
                post.tags.append(tag)
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template('edit_post.html', form=form)

@main.route('/post/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@main.route('/tags/posts')
def get_all_tags_and_posts():
    tags = Tag.query.order_by(Tag.id).all()
    return render_template('tags.html', tags=tags)

@main.route('/archives')
def get_archives():
    posts = Post.query.order_by(Post.timestamp.desc()).all();
    archive_posts = defaultdict(list)
    for post in posts:
        archive_posts[post.timestamp.year].append(post)
    return render_template('archives.html', archive_posts=archive_posts)

