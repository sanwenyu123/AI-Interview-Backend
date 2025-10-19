"""
数据库初始化脚本
"""
from app.core.database import init_db, engine
from app.models import User, Interview, Question, Answer, Evaluation, Setting
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """初始化数据库"""
    logger.info("开始初始化数据库...")
    
    try:
        # 创建所有表
        init_db()
        logger.info("✅ 数据库初始化成功！")
        logger.info("已创建以下表:")
        logger.info("  - users (用户表)")
        logger.info("  - interviews (面试记录表)")
        logger.info("  - questions (问题表)")
        logger.info("  - answers (回答表)")
        logger.info("  - evaluations (评价表)")
        logger.info("  - settings (设置表)")
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        raise


if __name__ == "__main__":
    main()





