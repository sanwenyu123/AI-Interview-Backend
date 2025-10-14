"""
AI服务
集成OpenAI API，提供问题生成和答案评价功能
"""
from typing import List, Dict
import json
import openai
from openai import OpenAI

from app.config import settings
from app.utils.ai_prompts import (
    get_question_generation_prompt,
    get_evaluation_prompt,
    get_answer_analysis_prompt
)


# 初始化OpenAI客户端
client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


def generate_interview_questions(
    position: str,
    description: str,
    skills: List[str],
    difficulty: str,
    language: str,
    num_questions: int = 5
) -> List[str]:
    """
    使用AI生成面试问题
    
    Args:
        position: 岗位名称
        description: 岗位描述
        skills: 技能列表
        difficulty: 难度等级
        language: 语言代码
        num_questions: 问题数量
        
    Returns:
        List[str]: 生成的问题列表
        
    Raises:
        Exception: AI服务调用失败时抛出异常
    """
    if not client:
        raise Exception("OpenAI API密钥未配置")
    
    # 生成提示词
    prompt = get_question_generation_prompt(
        position=position,
        description=description,
        skills=skills,
        difficulty=difficulty,
        language=language,
        num_questions=num_questions
    )
    
    try:
        # 调用OpenAI API
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一位专业的面试官。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=settings.OPENAI_TEMPERATURE
        )
        
        # 解析响应
        content = response.choices[0].message.content
        
        # 按行分割问题
        questions = [q.strip() for q in content.strip().split('\n') if q.strip()]
        
        # 清理问题（移除编号等）
        cleaned_questions = []
        for q in questions:
            # 移除开头的数字编号
            q = q.lstrip('0123456789.、）) ')
            if q:
                cleaned_questions.append(q)
        
        return cleaned_questions[:num_questions]
        
    except Exception as e:
        raise Exception(f"AI问题生成失败: {str(e)}")


def evaluate_interview_answers(
    position: str,
    questions: List[str],
    answers: List[str],
    language: str
) -> Dict:
    """
    使用AI评价面试回答
    
    Args:
        position: 岗位名称
        questions: 问题列表
        answers: 回答列表
        language: 语言代码
        
    Returns:
        Dict: 评价结果，包含分数、反馈、建议等
        
    Raises:
        Exception: AI服务调用失败时抛出异常
    """
    if not client:
        raise Exception("OpenAI API密钥未配置")
    
    # 生成提示词
    prompt = get_evaluation_prompt(
        position=position,
        questions=questions,
        answers=answers,
        language=language
    )
    
    try:
        # 调用OpenAI API
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一位资深的HR和技术专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=0.5  # 使用较低的temperature以获得更稳定的评分
        )
        
        # 解析响应
        content = response.choices[0].message.content
        
        # 尝试解析JSON
        try:
            evaluation = json.loads(content)
            
            # 验证必需字段
            required_fields = [
                'overall_score', 'technical_score', 'communication_score',
                'experience_score', 'learning_score', 'feedback'
            ]
            for field in required_fields:
                if field not in evaluation:
                    raise ValueError(f"缺少必需字段: {field}")
            
            # 确保可选字段存在
            evaluation.setdefault('suggestions', [])
            evaluation.setdefault('strengths', [])
            evaluation.setdefault('weaknesses', [])
            
            return evaluation
            
        except json.JSONDecodeError:
            # 如果无法解析JSON，返回默认评价
            raise Exception("AI返回的评价格式错误")
        
    except Exception as e:
        raise Exception(f"AI评价生成失败: {str(e)}")


def analyze_single_answer(
    question: str,
    answer: str,
    language: str
) -> str:
    """
    分析单个回答并给出反馈
    
    Args:
        question: 问题
        answer: 回答
        language: 语言代码
        
    Returns:
        str: 分析反馈
        
    Raises:
        Exception: AI服务调用失败时抛出异常
    """
    if not client:
        raise Exception("OpenAI API密钥未配置")
    
    # 生成提示词
    prompt = get_answer_analysis_prompt(
        question=question,
        answer=answer,
        language=language
    )
    
    try:
        # 调用OpenAI API
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一位面试评估专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        # 返回反馈
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        raise Exception(f"答案分析失败: {str(e)}")


def test_openai_connection() -> bool:
    """
    测试OpenAI API连接
    
    Returns:
        bool: 连接是否成功
    """
    if not client:
        return False
    
    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        return True
    except:
        return False

