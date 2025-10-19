"""
数据库模型
"""
from app.models.user import User
from app.models.interview import Interview
from app.models.question import Question
from app.models.answer import Answer
from app.models.evaluation import Evaluation
from app.models.setting import Setting

__all__ = [
    "User",
    "Interview",
    "Question",
    "Answer",
    "Evaluation",
    "Setting"
]





