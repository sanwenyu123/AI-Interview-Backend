"""
问题管理API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.question import Question as QuestionModel
from app.schemas.question import Question, QuestionCreate
from app.services.interview_service import get_interview_by_id
from app.services.ai_service import generate_interview_questions


router = APIRouter()


class QuestionGenerateRequest(BaseModel):
    """问题生成请求"""
    interview_id: int
    num_questions: int = Field(5, ge=1, le=10)


class QuestionGenerateResponse(BaseModel):
    """问题生成响应"""
    interview_id: int
    questions: List[str]
    count: int


@router.post("/generate", response_model=QuestionGenerateResponse)
async def generate_questions(
    request: QuestionGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    为指定面试生成问题
    
    - **interview_id**: 面试ID
    - **num_questions**: 生成问题数量（1-10）
    
    使用AI根据面试配置生成专业问题，并保存到数据库
    """
    # 获取面试记录
    interview = get_interview_by_id(db, request.interview_id)
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试记录不存在"
        )
    
    # 检查权限
    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此面试记录"
        )
    
    try:
        # 使用AI生成问题
        questions = generate_interview_questions(
            position=interview.position,
            description=interview.description or "",
            skills=interview.skills or [],
            difficulty=interview.difficulty.value,
            language=interview.language,
            num_questions=request.num_questions
        )
        
        # 保存问题到数据库
        saved_questions = []
        for idx, question_text in enumerate(questions, 1):
            db_question = QuestionModel(
                interview_id=interview.id,
                question_text=question_text,
                question_order=idx,
                language=interview.language
            )
            db.add(db_question)
            saved_questions.append(question_text)
        
        db.commit()
        
        return QuestionGenerateResponse(
            interview_id=interview.id,
            questions=saved_questions,
            count=len(saved_questions)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"问题生成失败: {str(e)}"
        )


@router.get("/interview/{interview_id}", response_model=List[Question])
async def get_interview_questions(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取面试的所有问题
    
    - **interview_id**: 面试ID
    """
    # 获取面试记录
    interview = get_interview_by_id(db, interview_id)
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试记录不存在"
        )
    
    # 检查权限
    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此面试记录"
        )
    
    # 获取问题列表
    questions = db.query(QuestionModel).filter(
        QuestionModel.interview_id == interview_id
    ).order_by(QuestionModel.question_order).all()
    
    return questions


@router.get("/{question_id}", response_model=Question)
async def get_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取单个问题详情
    
    - **question_id**: 问题ID
    """
    question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    
    # 检查权限（通过面试记录）
    interview = get_interview_by_id(db, question.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此问题"
        )
    
    return question

