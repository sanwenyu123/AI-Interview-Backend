"""
答案管理API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.question import Question as QuestionModel
from app.models.answer import Answer as AnswerModel
from app.schemas.answer import Answer, AnswerCreate
from app.services.interview_service import get_interview_by_id


router = APIRouter()


@router.post("/", response_model=Answer, status_code=status.HTTP_201_CREATED)
async def submit_answer(
    answer_create: AnswerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    提交答案
    
    - **question_id**: 问题ID
    - **answer_text**: 回答内容
    - **answer_type**: 回答类型（text/voice）
    - **audio_url**: 音频URL（语音回答时）
    - **duration**: 回答时长（秒，语音回答时）
    """
    # 获取问题
    question = db.query(QuestionModel).filter(
        QuestionModel.id == answer_create.question_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    
    # 检查权限
    interview = get_interview_by_id(db, question.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权回答此问题"
        )
    
    # 检查是否已回答
    existing_answer = db.query(AnswerModel).filter(
        AnswerModel.question_id == answer_create.question_id
    ).first()
    
    if existing_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该问题已有回答"
        )
    
    # 创建答案
    db_answer = AnswerModel(
        question_id=answer_create.question_id,
        answer_text=answer_create.answer_text,
        answer_type=answer_create.answer_type,
        audio_url=answer_create.audio_url,
        duration=answer_create.duration
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    
    return db_answer


@router.get("/{answer_id}", response_model=Answer)
async def get_answer(
    answer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取答案详情
    
    - **answer_id**: 答案ID
    """
    answer = db.query(AnswerModel).filter(AnswerModel.id == answer_id).first()
    
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="答案不存在"
        )
    
    # 检查权限
    question = db.query(QuestionModel).filter(
        QuestionModel.id == answer.question_id
    ).first()
    
    if question:
        interview = get_interview_by_id(db, question.interview_id)
        if not interview or interview.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此答案"
            )
    
    return answer


@router.get("/question/{question_id}", response_model=Answer)
async def get_answer_by_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    根据问题ID获取答案
    
    - **question_id**: 问题ID
    """
    # 获取问题
    question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    
    # 检查权限
    interview = get_interview_by_id(db, question.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此问题的答案"
        )
    
    # 获取答案
    answer = db.query(AnswerModel).filter(
        AnswerModel.question_id == question_id
    ).first()
    
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该问题尚未回答"
        )
    
    return answer





