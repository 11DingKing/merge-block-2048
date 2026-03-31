# 2048 游戏前端

基于 Vue 3 + Vite 的现代化游戏界面，提供流畅的拖拽交互体验。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.4+ | 前端框架（Composition API） |
| Vite | 5.0+ | 构建工具 |
| Axios | 1.6+ | HTTP 客户端 |
| Vitest | 1.0+ | 测试框架 |
| @vue/test-utils | 2.4+ | Vue 测试工具 |

## 项目结构

```
frontend-user/
├── src/
│   ├── components/
│   │   ├── Game2048.vue        # 游戏主组件
│   │   └── ToastContainer.vue  # Toast 提示组件
│   ├── composables/
│   │   └── useToast.js         # Toast 组合式函数
│   ├── api/
│   │   └── gameApi.js          # API 封装
│   ├── App.vue                 # 根组件
│   ├── main.js                 # 入口文件
│   └── style.css               # 全局样式
├── tests/
│   ├── Game2048.test.js        # 游戏组件测试
│   ├── gameApi.test.js         # API 测试
│   ├── useToast.test.js        # Toast 测试
│   └── setup.js                # 测试配置
├── index.html
├── package.json
├── vite.config.js
├── vitest.config.js
├── Dockerfile
└── nginx.conf                  # 生产环境 Nginx 配置
```

## 快速开始

### 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

应用运行在 http://localhost:5173

### Docker 运行

```bash
docker-compose up frontend-user
```

应用运行在 http://localhost:8081

## 功能特点

| 功能 | 说明 |
|------|------|
| 🎨 现代化 UI | 渐变背景、圆角卡片、精美配色 |
| 💫 流畅动画 | 方块移动、合并、弹出动画 |
| 🖱️ 拖拽交互 | 支持鼠标拖拽和触摸滑动 |
| 📱 响应式设计 | 自适应各种屏幕尺寸 |
| 🔔 Toast 提示 | 操作反馈提示系统 |
| 📊 分数显示 | 实时分数和最高分 |
| ➡️ 方向指示 | 拖拽时显示移动方向 |
| 🎯 得分动画 | 合并时显示得分弹窗 |

## 组件说明

### Game2048.vue

游戏主组件，包含：
- 游戏棋盘渲染（4x4 网格）
- 方块拖拽逻辑（鼠标/触摸）
- 分数显示和更新
- 游戏结束/获胜弹窗
- 动画效果（pop、merge、shake）

### ToastContainer.vue

全局提示组件，用于显示操作反馈。

### useToast.js

Toast 组合式函数，提供 `toast.error()` 等方法。

### gameApi.js

API 封装：
- `gameApi.newGame()` - 创建新游戏
- `gameApi.move(direction, gameId)` - 执行移动

## 开发命令

```bash
npm run dev          # 开发模式
npm run build        # 构建生产版本
npm run preview      # 预览构建结果
npm test             # 运行测试
npm run test:ui      # 测试 UI 界面
npm run test:coverage # 测试覆盖率
```

## 环境变量

创建 `.env` 文件：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 构建部署

```bash
# 构建
npm run build

# Docker 部署
docker build -t game2048-frontend .
docker run -p 8081:80 game2048-frontend
```

生产环境使用 Nginx 提供静态文件服务并代理 API 请求。

## 浏览器支持

- Chrome (最新版本)
- Firefox (最新版本)
- Safari (最新版本)
- Edge (最新版本)
