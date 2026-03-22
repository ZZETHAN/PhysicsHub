# PhysicsHub 项目架构

## 项目目标
建立一个模块化的A-Level物理学习平台，支持：
- 分单元学习
- 在线练习
- 团队协作开发

## 目录结构
```
PhysicsHub/
├── index.html              # 主页/导航中心
├── assets/                 # 公共资源
│   ├── css/
│   │   ├── main.css       # 主样式
│   │   └── unit.css       # 单元页面样式
│   ├── js/
│   │   ├── nav.js         # 导航组件
│   │   └── practice.js    # 练习系统
│   └── images/
├── shared/                 # 共享组件
│   ├── header.html        # 页头模板
│   ├── footer.html        # 页脚模板
│   └── sidebar.html       # 侧边栏模板
├── units/                  # 单元内容（模块化）
│   ├── index.json         # 单元索引
│   ├── ch12/              # 每个单元独立文件夹
│   │   ├── index.html     # 单元主页
│   │   ├── theory.html    # 理论内容
│   │   ├── formulas.html  # 公式汇总
│   │   ├── examples.html  # 例题
│   │   └── quiz.html      # 单元测试
│   ├── ch13/
│   └── ...
└── practice/              # 练习系统
    ├── index.html         # 练习主页
    ├── by-topic/          # 按主题分类
    └── by-year/           # 按年份分类
```

## 开发规范
1. 每个单元独立文件夹，可独立开发
2. 使用统一CSS类名规范
3. JSON配置驱动导航
4. 组件化设计，方便复用

## 内容编写规范
- 理论内容：concept → formula → example
- 例题：problem → step-by-step solution → key points
- 所有内容支持中英双语

## 团队分工建议
- 内容编写：2人
- 练习题整理：1人
- 前端开发：1人
- 审核校对：1人
