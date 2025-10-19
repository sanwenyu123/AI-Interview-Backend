# 创建MySQL数据库

## 方法1：使用MySQL命令行

打开MySQL命令行或使用MySQL客户端工具：

```sql
-- 1. 登录MySQL
mysql -u root -p

-- 2. 创建数据库
CREATE DATABASE interview_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 3. 查看数据库（可选）
SHOW DATABASES;

-- 4. 退出
EXIT;
```

## 方法2：使用MySQL Workbench

1. 打开 MySQL Workbench
2. 连接到你的 MySQL 服务器
3. 点击工具栏的 "Create a new schema" 图标
4. 输入数据库名称：`interview_db`
5. 选择字符集：`utf8mb4`
6. 选择排序规则：`utf8mb4_unicode_ci`
7. 点击 Apply

## 方法3：使用Navicat

1. 打开 Navicat
2. 右键点击连接 → 新建数据库
3. 数据库名：`interview_db`
4. 字符集：`utf8mb4`
5. 排序规则：`utf8mb4_unicode_ci`
6. 确定

## 配置环境变量

创建数据库后，在 `.env` 文件中配置连接字符串：

```env
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/interview_db
```

例如：
```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/interview_db
```

## 然后初始化表结构

```bash
python init_db.py
```

如果成功，你会看到：
```
✅ 数据库初始化成功！
已创建以下表:
  - users (用户表)
  - interviews (面试记录表)
  - questions (问题表)
  - answers (回答表)
  - evaluations (评价表)
  - settings (设置表)
```




