from . import db
from datetime import datetime
from markdown import markdown
import bleach
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    summary = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquoted', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p', 'img']
        allowed_attrs = {'*': ['class', 'style'],
                        'a': ['href', 'rel'],
                        'img': ['src', 'alt', 'title']}
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True, attributes=allowed_attrs))
        target.summary = target.body_html[:200]

db.event.listen(Post.body, 'set', Post.on_body_changed)

post_tag = db.Table('post_tag', db.Column('post_id', db.Integer, db.ForeignKey('posts.id')), db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    posts = db.relationship('Post', secondary=post_tag, backref=db.backref('tags', lazy='dynamic'), lazy='dynamic')

    @staticmethod
    def init_tags():
        tags = ['Java', 'Python', 'Redis', 'MySQL', 'Spring', 'Netty', 'Nginx', 'Hadoop', 'Flask', 'Dubbo']
        for tag in tags:
            t = Tag(name=tag)
            db.session.add(t)
            db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


