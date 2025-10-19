"""
AI提示词模板
用于生成面试问题和评价
"""
from typing import List


def get_question_generation_prompt(
    position: str,
    description: str,
    skills: List[str],
    difficulty: str,
    language: str,
    num_questions: int = 5
) -> str:
    """
    生成面试问题的提示词
    
    Args:
        position: 岗位名称
        description: 岗位描述
        skills: 技能列表
        difficulty: 难度等级 (easy/medium/hard/expert)
        language: 语言代码
        num_questions: 问题数量
        
    Returns:
        str: 格式化的提示词
    """
    
    # 难度描述映射
    difficulty_map = {
        "easy": {
            "zh-CN": "初级，适合应届生或1-2年经验",
            "en-US": "Entry level, suitable for fresh graduates or 1-2 years experience",
        },
        "medium": {
            "zh-CN": "中级，适合3-5年经验",
            "en-US": "Intermediate level, suitable for 3-5 years experience",
        },
        "hard": {
            "zh-CN": "高级，适合5年以上经验",
            "en-US": "Advanced level, suitable for 5+ years experience",
        },
        "expert": {
            "zh-CN": "专家级，适合资深专家",
            "en-US": "Expert level, suitable for senior experts",
        }
    }
    
    # 语言映射
    language_instruction = {
        "zh-CN": "请用中文回答",
        "zh-TW": "請用繁體中文回答",
        "en-US": "Please answer in English",
        "en-GB": "Please answer in English",
        "ja-JP": "日本語で答えてください",
        "ko-KR": "한국어로 답변해 주세요"
    }
    
    skills_str = "、".join(skills) if skills else "无特定技能要求"
    difficulty_desc = difficulty_map.get(difficulty, {}).get(language, difficulty_map["medium"]["zh-CN"])
    lang_instruction = language_instruction.get(language, language_instruction["zh-CN"])
    
    if language.startswith("zh"):
        prompt = f"""你是一位资深的{position}面试官，拥有多年的招聘和技术评估经验。

请根据以下信息生成{num_questions}个专业的面试问题：

【岗位信息】
- 岗位名称：{position}
- 岗位描述：{description if description else '常规岗位要求'}
- 技能要求：{skills_str}
- 面试难度：{difficulty_desc}

【问题要求】
1. 问题应该专业、有深度，能够有效评估候选人的能力
2. 涵盖以下几个方面：
   - 专业技术知识（40%）
   - 项目经验和实践（30%）
   - 问题解决能力（20%）
   - 团队协作和沟通（10%）
3. 问题难度应该递增，从基础到进阶
4. 问题应该是开放式的，鼓励候选人详细阐述
5. 避免是非题和过于简单的问题

请直接生成问题列表，每行一个问题，不需要编号和额外说明。
"""
    else:
        prompt = f"""You are a senior {position} interviewer with years of experience in recruitment and technical assessment.

Please generate {num_questions} professional interview questions based on the following information:

【Position Information】
- Position: {position}
- Description: {description if description else 'Standard requirements'}
- Required Skills: {skills_str}
- Difficulty Level: {difficulty_desc}

【Question Requirements】
1. Questions should be professional and in-depth, effectively assessing candidate abilities
2. Cover the following aspects:
   - Technical knowledge (40%)
   - Project experience and practice (30%)
   - Problem-solving skills (20%)
   - Teamwork and communication (10%)
3. Questions should increase in difficulty from basic to advanced
4. Questions should be open-ended, encouraging detailed responses
5. Avoid yes/no questions and overly simple questions

Please generate the question list directly, one question per line, without numbering or additional explanations.
"""
    
    return prompt


def get_evaluation_prompt(
    position: str,
    questions: List[str],
    answers: List[str],
    language: str
) -> str:
    """
    生成评价的提示词
    
    Args:
        position: 岗位名称
        questions: 问题列表
        answers: 回答列表
        language: 语言代码
        
    Returns:
        str: 格式化的提示词
    """
    
    # 构建问答对
    qa_pairs = []
    for i, (q, a) in enumerate(zip(questions, answers), 1):
        qa_pairs.append(f"问题{i}: {q}\n回答{i}: {a}")
    
    qa_text = "\n\n".join(qa_pairs)
    
    if language.startswith("zh"):
        prompt = f"""你是一位资深的HR和技术专家，负责评价{position}面试表现。

【面试记录】
{qa_text}

请对这次面试进行全面评价，按以下格式输出JSON：

{{
  "overall_score": 0-100的整数,
  "technical_score": 0-100的整数（专业知识掌握程度）,
  "communication_score": 0-100的整数（表达和沟通能力）,
  "experience_score": 0-100的整数（项目经验和实践能力）,
  "learning_score": 0-100的整数（学习能力和潜力）,
  "feedback": "整体评价，200字左右",
  "suggestions": ["改进建议1", "改进建议2", "改进建议3"],
  "strengths": ["优势1", "优势2", "优势3"],
  "weaknesses": ["不足1", "不足2", "不足3"]
}}

【评分标准】
- 90-100分：优秀，完全符合岗位要求，表现出色
- 75-89分：良好，基本符合岗位要求，有一定亮点
- 60-74分：中等，勉强符合岗位要求，需要改进
- 60分以下：较差，不符合岗位要求

请确保输出有效的JSON格式，不要包含其他文字。
"""
    else:
        prompt = f"""You are a senior HR and technical expert responsible for evaluating {position} interview performance.

【Interview Record】
{qa_text}

Please provide a comprehensive evaluation of this interview in the following JSON format:

{{
  "overall_score": integer from 0-100,
  "technical_score": integer from 0-100 (technical knowledge),
  "communication_score": integer from 0-100 (communication skills),
  "experience_score": integer from 0-100 (project experience),
  "learning_score": integer from 0-100 (learning ability and potential),
  "feedback": "Overall feedback, around 200 words",
  "suggestions": ["Suggestion 1", "Suggestion 2", "Suggestion 3"],
  "strengths": ["Strength 1", "Strength 2", "Strength 3"],
  "weaknesses": ["Weakness 1", "Weakness 2", "Weakness 3"]
}}

【Scoring Criteria】
- 90-100: Excellent, fully meets requirements, outstanding performance
- 75-89: Good, generally meets requirements, some highlights
- 60-74: Average, barely meets requirements, needs improvement
- Below 60: Poor, does not meet requirements

Please ensure valid JSON output without any additional text.
"""
    
    return prompt


def get_answer_analysis_prompt(
    question: str,
    answer: str,
    language: str
) -> str:
    """
    生成单个答案分析的提示词
    
    Args:
        question: 问题
        answer: 回答
        language: 语言代码
        
    Returns:
        str: 格式化的提示词
    """
    
    if language.startswith("zh"):
        prompt = f"""请分析以下面试问答，给出简短评价和建议。

问题：{question}
回答：{answer}

请用50字以内简要评价回答质量，并给出1-2条改进建议。
"""
    else:
        prompt = f"""Please analyze the following interview Q&A and provide brief feedback and suggestions.

Question: {question}
Answer: {answer}

Please provide a brief assessment of the answer quality in 50 words or less, and give 1-2 improvement suggestions.
"""
    
    return prompt





