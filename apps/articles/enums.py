from enum import Enum


class ArticleStatusEnum(Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    DELETED = 'deleted'


class ArticleColumnEnum(Enum):
    ID = 'id'
    TITLE = 'title'
    TEXT = 'text'
    CREATED_DATE = 'created_date'
    UPDATED_DATE = 'updated_date'
    STATUS = 'status'
    CATEGORY_NAME = 'category_name'

    @classmethod
    def get_values(cls) -> list[str]:
        return [item.value for item in cls]
