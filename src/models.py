import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from eralchemy2 import render_er

Base = declarative_base()


followers = Table('followers', Base.metadata,
    Column('follower_id', Integer, ForeignKey('usuario.id')),
    Column('following_id', Integer, ForeignKey('usuario.id'))
)


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    profile_image = Column(String(250), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


    posts = relationship('Post', backref='usuario', lazy=True)
    comments = relationship('Comentario', backref='usuario', lazy=True)
    likes = relationship('Like', backref='usuario', lazy=True)
    followers = relationship('Usuario', 
                             secondary=followers, 
                             primaryjoin=id == followers.c.follower_id, 
                             secondaryjoin=id == followers.c.following_id, 
                             backref='seguidores')


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    image_url = Column(String(250), nullable=False)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

   
    comments = relationship('Comentario', backref='post', lazy=True)
    likes = relationship('Like', backref='post', lazy=True)


class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
