# PhysicsHub 开发同步提示词

## 项目概述

PhysicsHub 是一个 A-Level Physics 学习平台网站，用于物理教学。

**技术栈**: HTML/CSS/JS (前端), Node.js (后端 API)

**工作目录**: `/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub` (Mac) 或对应的 Windows/Linux 路径

---

## 目录结构

```
PhysicsHub/
├── index.html              # 首页
├── profile.html            # 用户资料页
├── admin.html              # 管理后台
├── auth/
│   ├── auth.js             # 认证系统核心
│   └── auth.css            # 认证相关样式
├── api/                    # 后端 API (在服务器上 /opt/physicshub/api)
│   ├── server.js
│   ├── routes/auth.js
│   └── database.js
├── units/                  # 各单元页面
│   ├── ch12/ ... ch20/
│   └── index.json          # 单元配置
├── assets/
│   ├── images/             # 图片资源
│   ├── mathjax/            # 数学公式渲染
│   └── icons/
├── homework/               # 作业 PDF
└── scripts/
    └── deploy_physicshub.sh # 部署脚本
```

---

## 服务器信息

- **网站**: `ubuntu@123.207.75.145:/var/www/physicshub/`
- **API**: `ubuntu@123.207.75.145:/opt/physicshub/api/`
- **数据库**: `/opt/physicshub/api/database.db` (部署时不能覆盖!)

**部署命令**:
```bash
cd /System/Volumes/Data/Users/ethan/Desktop/PhysicsHub
bash scripts/deploy_physicshub.sh
```

---

## 已完成的工作

### Bug 修复
1. **ch12/ch15 content bar** - 添加了 `scrollToSection()` 函数实现导航高亮
2. **Profile 加载错误** - 改进了错误处理，网络错误不弹窗
3. **头像保存** - 修复了前端发送 avatar_color/avatar_icon 到 API 的问题，header 现在显示保存的头像
4. **Unit 19 MS box 样式** - 添加了 flex-wrap 和 word-break CSS
5. **Mobile header** - 添加了 CSS 约束防止溢出

### Unit 20 开发
- 创建了 `units/ch20/index.html` - 主内容页 (Magnetic Fields)
- 创建了 `units/ch20/structured-questions.html` - 14 道练习题
- 颜色主题使用蓝色 `#1e40af` 匹配 Units 18-19
- 激活了首页 Unit 20 卡片 (原来是 "Coming Soon")

### 国际化 (English Only)
- 进度按钮: `未开始/进行中/已完成` → `Start/Active/Done`
- 退出按钮: `退出` → `Logout`
- Profile 页面全部翻译为英文
- Memory tips 翻译为英文
- 黄色/红色警告色改为蓝色主题

### UI 优化
- 进度按钮防止换行: 添加 `min-width: 0`, `white-space: nowrap`, `font-size: 11px`
- MathJax 支持 `$...$` 内联公式语法

---

## 当前待办

1. **图片插入** - Unit 19/20 的图片需要手动匹配到占位符位置
2. **滚动导航高亮** - ch20/index.html 已添加 IntersectionObserver (其他单元可能也需要检查)
3. **其他单元的 Units 下拉菜单** - 检查并添加缺失的 Unit 20 链接

---

## 常用任务

### 1. 修复 Bug
1. 找到对应的 HTML/JS/CSS 文件
2. 使用 `read` 读取文件内容
3. 使用 `edit` 修改
4. 部署: `bash scripts/deploy_physicshub.sh`

### 2. 添加新内容
1. 参考现有单元的结构
2. 确保 Units 下拉菜单包含所有单元 (ch12-ch20)
3. 使用 MathJax 格式: `$...$` 内联, `$$...$$` 块级
4. 颜色主题: Units 12-16 各有主题色, Units 17-20 统一蓝色 `#1e40af`

### 3. 翻译/国际化
- 全站必须是英文 (除用户生成内容)
- 中文 → 英文翻译规则:
  - `未开始/进行中/已完成` → `Start/Active/Done`
  - `退出` → `Logout`
  - `个人资料` → `Profile`
  - `加载中...` → `Loading...`
  - Memory tips 翻译为简洁英文

### 4. 修改 Units 下拉菜单
Units 下拉菜单在各单元页面的 header 中，格式:
```html
<a href="../ch12/index.html">Unit 12 - Title</a>
```

当前 Units 顺序: ch12 → ch13 → ... → ch20

---

## 重要规则

1. **部署前确认** - 确认 database.db 不会被覆盖
2. **英文界面** - 界面文字必须英文，教学内容也要英文
3. **颜色规范** - 避免使用红色/黄色 (系统警告色)，使用蓝色主题
4. **MathJax** - 公式使用 `$...$` 或 `\(...\)`
5. **移动端** - 确保 CSS 有响应式设计

---

## 代码风格

- 使用双引号
- CSS 内联在 HTML 中 (部分通用样式在 auth/auth.css)
- JavaScript 在 `<script>` 标签中
- 使用 `../../` 相对路径引用父目录资源

---

## 内容来源

小龙虾 负责教学内容创作，提供 Markdown 文档，由 OpenCode 转换为 HTML/CSS/JS。

参考目录:
- `/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub_Content_By_Assistant/`
