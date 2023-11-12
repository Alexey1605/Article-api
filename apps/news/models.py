from sqlalchemy import func

from apps.core.extensions import db
from apps.news.enums import NewsStatusEnum


class News(db.Model):
    __tablename__ = 'news'

    news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_date = db.Column(db.DateTime, onupdate=func.now())
    edition = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String, nullable=False, default=NewsStatusEnum.DRAFT.value)
