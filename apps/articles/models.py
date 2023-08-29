from sqlalchemy import func

from apps.articles.enums import ArticleStatusEnum
from apps.core.extensions import db


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_date = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(db.String, nullable=False, default=ArticleStatusEnum.DRAFT.value)

    def __repr__(self):
        return f'<User {self.title!r}>'

    # @classmethod
    # def get_all(cls):
    #     return cls.query.all()
    #
    # @classmethod
    # def get_by_id(cls, id):
    #     return cls.query.get_or_404(id)


