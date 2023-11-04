from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Mapped

from apps.articles.enums import ArticleStatusEnum
from apps.core.extensions import db


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    articles: Mapped[List["Article"]] = relationship(back_populates='category')


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_date = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(db.String, nullable=False, default=ArticleStatusEnum.DRAFT.value)
    category_id = db.Column(db.ForeignKey('category.id'), nullable=False)

    category: Mapped["Category"] = relationship(back_populates='articles')

    @hybrid_property
    def category_name(self):
        return self.category.name

    @category_name.expression
    def category_name(self):
        return select(Category.name).where(Category.id == self.category_id).label('category_name')

    def __repr__(self):
        return f'<User {self.title}>'
