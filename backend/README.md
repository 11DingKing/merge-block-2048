# 2048 游戏后端

基于 Django 的 RESTful API 服务，为 2048 游戏提供游戏逻辑和数据持久化。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.11+ | 运行环境 |
| Django | 4.2+ | Web 框架 |
| django-cors-headers | 4.3+ | CORS 跨域支持 |
| mysqlclient | 2.2+ | MySQL 数据库驱动 |
| MySQL | 8.0 | 生产数据库 |

## 项目结构

```
backend/
├── game/                 # 游戏应用
│   ├── models.py         # GameSession 数据模型
│   ├── views.py          # API 视图（new_game, move）
│   ├── urls.py           # 应用路由
│   ├── admin.py          # 管理后台配置
│   └── tests.py          # 测试用例
├── settings.py           # Django 项目配置
├── urls.py               # 主路由
├── wsgi.py / asgi.py     # WSGI/ASGI 配置
├── manage.py             # Django 管理脚本
├── requirements.txt      # Python 依赖
├── Dockerfile            # Docker 镜像配置
└── docker-entrypoint.sh  # 容器启动脚本
```

## 快速开始

### 本地开发

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行数据库迁移：
```bash
python manage.py migrate
```

3. 启动开发服务器：
```bash
python manage.py runserver
```

服务运行在 http://127.0.0.1:8000

### Docker 运行

```bash
# 单独运行后端
docker-compose up backend

# 或构建镜像
docker build -t game2048-backend .
docker run -p 8000:8000 game2048-backend
```

## API 接口

### POST `/api/new-game/`

创建新游戏会话。

**响应：**
```json
{
  "id": 1,
  "board": [[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 4, 0], [0, 0, 0, 0]],
  "score": 0,
  "best_score": 0,
  "game_over": false,
  "won": false
}
```

### POST `/api/move/`

执行移动操作。

**请求体：**
```json
{
  "direction": "left",
  "game_id": 1
}
```

**direction 可选值：** `up`, `down`, `left`, `right`

**响应：**
```json
{
  "board": [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
  "score": 6,
  "best_score": 6,
  "game_over": false,
  "won": false,
  "moved": true
}
```

## 数据模型

### GameSession

| 字段 | 类型 | 说明 |
|------|------|------|
| id | AutoField | 主键 |
| board | JSONField | 4x4 游戏棋盘 |
| score | IntegerField | 当前分数 |
| best_score | IntegerField | 最高分 |
| game_over | BooleanField | 游戏是否结束 |
| won | BooleanField | 是否达成 2048 |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

## 核心逻辑

- `new_game`: 创建新游戏，初始化 4x4 棋盘，随机放置两个数字（90% 概率为 2，10% 为 4）
- `move`: 处理移动，合并相同数字，计算得分，检测游戏结束/获胜状态
- `add_random_tile`: 在空位随机添加新数字
- `can_move`: 检测是否还有可移动空间
- `has_won`: 检测是否达成 2048

## 测试

```bash
# 运行所有测试
python manage.py test

# 运行特定测试
python manage.py test game.tests
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| DEBUG | True | 调试模式 |
| DJANGO_SETTINGS_MODULE | backend.settings | 配置模块 |

## 数据库配置

开发环境默认连接 Docker MySQL：
- Host: `db`
- Database: `game2048`
- User: `game2048`
- Password: `game2048pass`

本地开发需修改 `settings.py` 中的 `HOST` 为 `localhost`。
