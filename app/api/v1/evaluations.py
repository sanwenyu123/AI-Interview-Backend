"""
评价管理API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.evaluation import Evaluation as EvaluationModel
from app.models.question import Question as QuestionModel
from app.models.answer import Answer as AnswerModel
from app.schemas.evaluation import Evaluation, EvaluationCreate
from app.services.interview_service import get_interview_by_id, complete_interview
from app.services.ai_service import evaluate_interview_answers


router = APIRouter()


@router.post("/", response_model=Evaluation, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    evaluation_create: EvaluationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建评价（手动）
    
    - **interview_id**: 面试ID
    - 各项评分和反馈
    """
    # 获取面试记录
    interview = get_interview_by_id(db, evaluation_create.interview_id)
    
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
    
    # 检查是否已有评价
    existing_evaluation = db.query(EvaluationModel).filter(
        EvaluationModel.interview_id == evaluation_create.interview_id
    ).first()
    
    if existing_evaluation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该面试已有评价"
        )
    
    # 创建评价
    db_evaluation = EvaluationModel(
        interview_id=evaluation_create.interview_id,
        overall_score=evaluation_create.overall_score,
        technical_score=evaluation_create.technical_score,
        communication_score=evaluation_create.communication_score,
        experience_score=evaluation_create.experience_score,
        learning_score=evaluation_create.learning_score,
        feedback=evaluation_create.feedback,
        suggestions=evaluation_create.suggestions,
        strengths=evaluation_create.strengths,
        weaknesses=evaluation_create.weaknesses
    )
    db.add(db_evaluation)
    
    # 更新面试分数
    interview.score = evaluation_create.overall_score
    
    db.commit()
    db.refresh(db_evaluation)
    
    return db_evaluation


@router.post("/generate/{interview_id}", response_model=Evaluation, status_code=status.HTTP_201_CREATED)
async def generate_evaluation(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    使用AI自动生成评价
    
    - **interview_id**: 面试ID
    
    根据面试问题和回答，使用AI生成全面的评价
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
            detail="无权操作此面试记录"
        )
    
    # 检查是否已有评价
    existing_evaluation = db.query(EvaluationModel).filter(
        EvaluationModel.interview_id == interview_id
    ).first()
    
    if existing_evaluation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该面试已有评价"
        )
    
    # 获取所有问题和答案
    questions = db.query(QuestionModel).filter(
        QuestionModel.interview_id == interview_id
    ).order_by(QuestionModel.question_order).all()
    
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="面试没有问题"
        )
    
    # 获取对应的答案
    question_texts = []
    answer_texts = []
    
    for question in questions:
        answer = db.query(AnswerModel).filter(
            AnswerModel.question_id == question.id
        ).first()
        
        if answer:
            question_texts.append(question.question_text)
            answer_texts.append(answer.answer_text)
    
    if not answer_texts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="面试没有回答"
        )
    
    try:
        # 使用AI生成评价
        evaluation_data = evaluate_interview_answers(
            position=interview.position,
            questions=question_texts,
            answers=answer_texts,
            language=interview.language
        )
        
        # 创建评价
        db_evaluation = EvaluationModel(
            interview_id=interview_id,
            overall_score=evaluation_data['overall_score'],
            technical_score=evaluation_data['technical_score'],
            communication_score=evaluation_data['communication_score'],
            experience_score=evaluation_data['experience_score'],
            learning_score=evaluation_data['learning_score'],
            feedback=evaluation_data['feedback'],
            suggestions=evaluation_data.get('suggestions', []),
            strengths=evaluation_data.get('strengths', []),
            weaknesses=evaluation_data.get('weaknesses', [])
        )
        db.add(db_evaluation)
        
        # 更新面试分数并完成面试
        complete_interview(db, interview_id, evaluation_data['overall_score'])
        
        db.commit()
        db.refresh(db_evaluation)
        
        return db_evaluation
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"评价生成失败: {str(e)}"
        )


@router.get("/interview/{interview_id}", response_model=Evaluation)
async def get_interview_evaluation(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取面试的评价
    
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
    
    # 获取评价
    evaluation = db.query(EvaluationModel).filter(
        EvaluationModel.interview_id == interview_id
    ).first()
    
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该面试尚未评价"
        )
    
    return evaluation


@router.get("/{evaluation_id}", response_model=Evaluation)
async def get_evaluation(
    evaluation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取评价详情
    
    - **evaluation_id**: 评价ID
    """
    evaluation = db.query(EvaluationModel).filter(
        EvaluationModel.id == evaluation_id
    ).first()
    
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评价不存在"
        )
    
    # 检查权限
    interview = get_interview_by_id(db, evaluation.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此评价"
        )
    
    return evaluation





