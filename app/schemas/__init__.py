"""
Pydantic模式
"""
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserInDB,
    User
)
from app.schemas.auth import (
    Token,
    TokenPayload,
    LoginRequest
)
from app.schemas.interview import (
    InterviewBase,
    InterviewCreate,
    InterviewUpdate,
    Interview,
    InterviewWithDetails
)
from app.schemas.question import (
    QuestionBase,
    QuestionCreate,
    Question
)
from app.schemas.answer import (
    AnswerBase,
    AnswerCreate,
    Answer
)
from app.schemas.evaluation import (
    EvaluationBase,
    EvaluationCreate,
    Evaluation
)
from app.schemas.setting import (
    SettingBase,
    SettingCreate,
    SettingUpdate,
    Setting
)

__all__ = [
    "UserBase", "UserCreate", "UserUpdate", "UserInDB", "User",
    "Token", "TokenPayload", "LoginRequest",
    "InterviewBase", "InterviewCreate", "InterviewUpdate", "Interview", "InterviewWithDetails",
    "QuestionBase", "QuestionCreate", "Question",
    "AnswerBase", "AnswerCreate", "Answer",
    "EvaluationBase", "EvaluationCreate", "Evaluation",
    "SettingBase", "SettingCreate", "SettingUpdate", "Setting"
]

