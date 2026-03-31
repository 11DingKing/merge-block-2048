# 2048 游戏

一款经典的数字合并益智游戏，采用现代化 UI 设计和流畅的拖拽交互体验。

## 🎮 游戏玩法

- **目标**：通过合并相同数字的方块，最终凑出 2048
- **合并**：相同数字的方块碰撞时会相加合并（2+2=4, 4+4=8...）
- **得分**：每次合并获得合并后数字的分数
- **结束**：当棋盘填满且无法合并时游戏结束

## 🕹️ 操作方式

| 设备 | 操作 |
|------|------|
| 💻 电脑 | 点击并拖拽任意方块，向想要的方向滑动后松开 |
| 📱 手机/平板 | 触摸任意方块，滑动手指后松开 |

> 拖拽任意一个方块，所有方块都会向该方向移动

## 🛠️ 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 前端 | Vue 3 + Vite | Vue 3.4+ / Vite 5.0+ |
| 后端 | Django | 4.2+ |
| 数据库 | MySQL | 8.0 |
| HTTP 客户端 | Axios | 1.6+ |
| 测试框架 | Vitest | 1.0+ |
| 部署 | Docker Compose | 3.8 |

## � 项目结构

```
├── backend/                 # Django 后端服务
│   ├── game/               # 游戏核心模块
│   │   ├── models.py       # GameSession 数据模型
│   │   ├── views.py        # API 视图（new_game, move）
│   │   └── urls.py         # 路由配置
│   ├── settings.py         # Django 配置
│   ├── Dockerfile          # 后端容器配置
│   ├── docker-entrypoint.sh
│   └── requirements.txt    # Python 依赖
├── frontend-user/          # Vue 3 前端应用
│   ├── src/
│   │   ├── components/
│   │   │   ├── Game2048.vue      # 游戏主组件
│   │   │   └── ToastContainer.vue # 提示组件
│   │   ├── composables/
│   │   │   └── useToast.js       # Toast 组合式函数
│   │   └── api/
│   │       └── gameApi.js        # API 封装
│   ├── tests/              # 测试文件
│   ├── Dockerfile          # 前端容器配置
│   └── nginx.conf          # Nginx 配置
├── mysql/
│   └── init.sql            # 数据库初始化脚本
└── docker-compose.yml      # 容器编排配置
```

## 🚀 快速启动（Docker）

一键启动所有服务：

```bash
docker-compose up --build
```

启动后访问：
- 🎮 游戏界面：http://localhost:8081
- 🔌 后端 API：http://localhost:8000

停止服务：

```bash
docker-compose down
```

清除数据重新开始：

```bash
docker-compose down -v
docker-compose up --build
```

## � 本地开发

### 1. 启动 MySQL

```bash
docker run -d --name mysql-dev \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=game2048 \
  -e MYSQL_USER=game2048 \
  -e MYSQL_PASSWORD=game2048pass \
  -p 3306:3306 \
  mysql:8.0
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

后端运行在 http://localhost:8000

### 3. 启动前端

```bash
cd frontend-user
npm install
npm run dev
```

前端运行在 http://localhost:5173

## 🔌 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/new-game/` | POST | 创建新游戏，返回初始棋盘 |
| `/api/move/` | POST | 移动方块（direction: up/down/left/right） |

### 响应示例

**新游戏响应：**
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

**移动响应：**
```json
{
  "board": [[2, 4, 0, 0], ...],
  "score": 8,
  "best_score": 8,
  "game_over": false,
  "won": false,
  "moved": true
}
```

## ✨ 功能特点

- � 现代化渐变 UI 设计
- 💫 流畅的拖拽交互和动画效果
- 📱 完全响应式，支持移动端
- 🔔 Toast 提示系统
- 📊 实时分数和最高分记录
- 🎯 方向指示器显示拖拽方向

## 🎯 游戏技巧

1. 尽量将大数字保持在角落
2. 选择一个方向作为主要移动方向
3. 避免让大数字被小数字包围
4. 保持棋盘整洁，留出合并空间

## 📝 开发命令

```bash
# 前端测试
cd frontend-user
npm test              # 运行测试
npm run test:ui       # 测试 UI
npm run test:coverage # 测试覆盖率

# 后端测试
cd backend
python manage.py test
```

---

Have fun! 🎉
