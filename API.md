# API接口文档

## 🌐 基础信息

- **Base URL**: `http://localhost:8000`
- **API Version**: v1
- **API Prefix**: `/api/v1`

## 🔐 认证方式

使用JWT Bearer Token认证。

在请求头中添加：
```
Authorization: Bearer <access_token>
```

---

## 📋 API端点概览

### 认证相关 `/api/v1/auth`
| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| POST | `/register` | 用户注册 | ❌ |
| POST | `/login` | 用户登录 | ❌ |
| POST | `/refresh` | 刷新令牌 | ❌ |
| GET | `/me` | 获取当前用户信息 | ✅ |
| POST | `/logout` | 登出 | ✅ |

### 面试管理 `/api/v1/interviews`
| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| POST | `/` | 创建面试 | ✅ |
| GET | `/` | 获取面试列表 | ✅ |
| GET | `/statistics` | 获取统计数据 | ✅ |
| GET | `/{interview_id}` | 获取面试详情 | ✅ |
| PUT | `/{interview_id}` | 更新面试 | ✅ |
| DELETE | `/{interview_id}` | 删除面试 | ✅ |
| POST | `/{interview_id}/start` | 开始面试 | ✅ |
| POST | `/{interview_id}/complete` | 完成面试 | ✅ |
| POST | `/{interview_id}/cancel` | 取消面试 | ✅ |

### 问题管理 `/api/v1/questions`
| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| POST | `/generate` | 生成问题 | ✅ |
| GET | `/interview/{interview_id}` | 获取面试的问题列表 | ✅ |
| GET | `/{question_id}` | 获取问题详情 | ✅ |

### 答案管理 `/api/v1/answers`
| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| POST | `/` | 提交答案 | ✅ |
| GET | `/{answer_id}` | 获取答案详情 | ✅ |
| GET | `/question/{question_id}` | 根据问题ID获取答案 | ✅ |

### 评价管理 `/api/v1/evaluations`
| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| POST | `/` | 创建评价(手动) | ✅ |
| POST | `/generate/{interview_id}` | 生成评价(AI) | ✅ |
| GET | `/interview/{interview_id}` | 获取面试评价 | ✅ |
| GET | `/{evaluation_id}` | 获取评价详情 | ✅ |

---

## 🔍 详细接口说明

### 1. 认证相关

#### 1.1 用户注册
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

**响应 201**:
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "avatar": null,
  "is_active": true,
  "created_at": "2025-10-11T10:00:00Z"
}
```

#### 1.2 用户登录
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**响应 200**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 1.3 刷新令牌
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 1.4 获取当前用户
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

---

### 2. 面试管理

#### 2.1 创建面试
```http
POST /api/v1/interviews
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "position": "前端工程师",
  "description": "负责Web应用开发",
  "skills": ["React", "JavaScript", "TypeScript"],
  "difficulty": "medium",
  "duration": 30,
  "language": "zh-CN",
  "type": "text"
}
```

**参数说明**:
- `difficulty`: easy | medium | hard | expert
- `type`: text | voice
- `duration`: 15-120 分钟

#### 2.2 获取面试列表
```http
GET /api/v1/interviews?skip=0&limit=10&status=completed
Authorization: Bearer <access_token>
```

**查询参数**:
- `skip`: 跳过记录数（默认0）
- `limit`: 返回记录数（默认100，最大100）
- `status`: pending | in_progress | completed | cancelled

#### 2.3 开始面试
```http
POST /api/v1/interviews/{interview_id}/start
Authorization: Bearer <access_token>
```

#### 2.4 完成面试
```http
POST /api/v1/interviews/{interview_id}/complete?score=85
Authorization: Bearer <access_token>
```

---

### 3. 问题管理

#### 3.1 生成问题
```http
POST /api/v1/questions/generate
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "interview_id": 1,
  "num_questions": 5
}
```

**响应**:
```json
{
  "interview_id": 1,
  "questions": [
    "请介绍一下React的虚拟DOM机制？",
    "如何优化React应用的性能？",
    "..."
  ],
  "count": 5
}
```

#### 3.2 获取面试问题列表
```http
GET /api/v1/questions/interview/{interview_id}
Authorization: Bearer <access_token>
```

---

### 4. 答案管理

#### 4.1 提交答案
```http
POST /api/v1/answers
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "question_id": 1,
  "answer_text": "React的虚拟DOM是...",
  "answer_type": "text",
  "audio_url": null,
  "duration": null
}
```

**参数说明**:
- `answer_type`: text | voice
- `audio_url`: 语音答案的音频URL（voice类型必填）
- `duration`: 回答时长（秒，voice类型必填）

---

### 5. 评价管理

#### 5.1 生成AI评价
```http
POST /api/v1/evaluations/generate/{interview_id}
Authorization: Bearer <access_token>
```

**响应**:
```json
{
  "id": 1,
  "interview_id": 1,
  "overall_score": 85,
  "technical_score": 88,
  "communication_score": 82,
  "experience_score": 85,
  "learning_score": 86,
  "feedback": "总体表现良好，技术基础扎实...",
  "suggestions": [
    "建议加强项目经验的积累",
    "可以更详细地阐述技术细节"
  ],
  "strengths": [
    "对React核心概念理解透彻",
    "表达清晰，逻辑性强"
  ],
  "weaknesses": [
    "项目经验略显不足",
    "对性能优化的实践经验较少"
  ],
  "created_at": "2025-10-11T11:00:00Z"
}
```

#### 5.2 获取面试评价
```http
GET /api/v1/evaluations/interview/{interview_id}
Authorization: Bearer <access_token>
```

---

## 🔄 完整面试流程

### 1. 用户注册/登录
```bash
# 注册
POST /api/v1/auth/register

# 登录获取token
POST /api/v1/auth/login
```

### 2. 创建面试
```bash
POST /api/v1/interviews
```

### 3. 生成问题
```bash
POST /api/v1/questions/generate
```

### 4. 开始面试
```bash
POST /api/v1/interviews/{id}/start
```

### 5. 获取问题列表
```bash
GET /api/v1/questions/interview/{interview_id}
```

### 6. 逐个回答问题
```bash
POST /api/v1/answers
```

### 7. 生成AI评价
```bash
POST /api/v1/evaluations/generate/{interview_id}
```

### 8. 查看评价结果
```bash
GET /api/v1/evaluations/interview/{interview_id}
```

---

## 🚨 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无内容） |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 无权访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

**错误响应格式**:
```json
{
  "detail": "错误描述信息"
}
```

---

## 📝 使用示例

### Python示例
```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 登录
response = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "testuser",
    "password": "password123"
})
token = response.json()["access_token"]

# 设置认证头
headers = {"Authorization": f"Bearer {token}"}

# 创建面试
interview = requests.post(f"{BASE_URL}/interviews", headers=headers, json={
    "position": "Python开发工程师",
    "skills": ["Python", "FastAPI", "MySQL"],
    "difficulty": "medium",
    "duration": 30,
    "language": "zh-CN",
    "type": "text"
}).json()

interview_id = interview["id"]

# 生成问题
questions_response = requests.post(
    f"{BASE_URL}/questions/generate",
    headers=headers,
    json={"interview_id": interview_id, "num_questions": 5}
).json()

print(f"生成了 {questions_response['count']} 个问题")
```

### JavaScript/Fetch示例
```javascript
const BASE_URL = "http://localhost:8000/api/v1";

// 登录
const loginResponse = await fetch(`${BASE_URL}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'testuser',
    password: 'password123'
  })
});
const { access_token } = await loginResponse.json();

// 创建面试
const interviewResponse = await fetch(`${BASE_URL}/interviews`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    position: 'JavaScript开发工程师',
    skills: ['JavaScript', 'React', 'Node.js'],
    difficulty: 'medium',
    duration: 30,
    language: 'zh-CN',
    type: 'text'
  })
});
const interview = await interviewResponse.json();
```

---

## 🔧 测试工具

### 使用Swagger UI
访问 http://localhost:8000/docs 可以在线测试所有API

### 使用curl
```bash
# 登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# 创建面试
curl -X POST http://localhost:8000/api/v1/interviews \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"position":"前端工程师","difficulty":"medium","duration":30,"language":"zh-CN","type":"text"}'
```

---

**更多详情请查看**: http://localhost:8000/docs





