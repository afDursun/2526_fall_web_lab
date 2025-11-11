from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')
    comments: so.WriteOnlyMapped['Comment'] = so.relationship(back_populates='post')

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Comment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    content: so.Mapped[str] = so.mapped_column(sa.String(300))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('post.id'), index=True)

    post: so.Mapped[Post] = so.relationship(back_populates='comments')

    def __repr__(self):
        return '<Comment {}>'.format(self.content)



"""
u1 = User(username='Ahmet', email='ahmet@mail.com')
u2 = User(username='Kagan', email='kagan@mail.com')
db.session.add(u1)
db.session.add(u2)
db.session.commit()


p1 = Post(body='Hello World!', author=u1)
p2 = Post(body='My first post', author=u2)
db.session.add_all([p1, p2])
db.session.commit()

c1 = Comment(content='Nice post!', post=p1)
c2 = Comment(content='Thanks for sharing', post=p2)
db.session.add_all([c1, c2])
db.session.commit()
"""
