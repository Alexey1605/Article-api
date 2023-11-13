from enum import Enum


class NewsStatusEnum(Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    DELETED = 'deleted'


class NewsColumnEnum(Enum):
    NEWS_ID = 'news_id'
    TITLE = 'title'
    DESCRIPTION = 'description'
    CREATED_DATE = 'created_date'
    UPDATED_DATE = 'updated_date'
    STATUS = 'status'

    @classmethod
    def get_values(cls) -> list[str]:
        return [item.value for item in cls]
