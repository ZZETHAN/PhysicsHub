# PhysicsHub - A-Level Physics 学习网站

## 项目结构

```
~/Desktop/PhysicsHub/
├── index.html              # 首页（单元导航）
├── units/
│   ├── ch12/               # 单元 12: Circular Motion
│   ├── ch13/               # 单元 13: Gravitational Field
│   └── ...                 # 其他单元
├── assets/
│   └── unit-themes.js      # ⭐ 单元主题色配置
└── auth/                   # 认证系统
```

## ⭐ 单元主题色系统

**配置文件：** `assets/unit-themes.js`
**备份：** `THEME_COLORS_BACKUP.md`

**开发须知：** OpenCode 开发新单元前，必须先确认该单元的主题色，配置正确的 CSS 变量。

每个单元属于一个知识模块，有对应的主题色：

| 主题 | 模块 | 主色 | 单元 |
|------|------|------|------|
| foundation | 基础/实验 | #475569 灰 | ch01, P3, P5 |
| mechanics | 力学 | #1e40af 深蓝 | ch02, ch03, ch12, ch13 |
| matter | 能量与材料 | #0e7490 青绿 | ch04, ch05, ch06 |
| waves | 波 | #7c3aed 紫 | ch07, ch08, ch17 |
| fields | 电磁学 | #059669 绿 | ch09, ch10, ch11, ch18-21 |
| thermo | 热力学 | #dc2626 红 | ch14, ch15, ch16 |
| modern | 现代物理 | #be185d 粉紫 | ch22, ch23, ch24, ch25 |

**使用时引入配置：**
```html
<script src="../../assets/unit-themes.js"></script>
<script>
    document.body.style.cssText = getUnitCSSVariables('ch12');
</script>
```

## 开发规范

### 新单元创建流程
1. 从 `units/UNIT_TEMPLATE.html` 复制
2. 设置正确的 `data-theme` 属性（参考上表）
3. 运行 `python3 ~/.openclaw/workspace/sync_unit_nav.py` 同步导航

### CSS 变量使用
优先使用 CSS 变量而非硬编码颜色：
```css
color: var(--theme-primary);
background: var(--theme-light);
```

### 部署流程
1. 本地开发 → `~/Desktop/PhysicsHub/`
2. 询问用户确认后方可部署
3. 部署命令参考 MEMORY.md

---

## 页面开发规范（重要！）

**新建单元前必须先学习：**
`PAGE_SPECIFICATION.md` - 包含完整页面格式模板

包括：
- 8种页面类型及文件名规范
- CSS组件样式（公式框、概念框、清单等）
- Header/Navigation 结构
- JavaScript 功能（Units菜单、滚动高亮、进度条）
- 必须功能清单
- 主题色配置参考

**开发流程：**
1. 读取 PAGE_SPECIFICATION.md
2. 参考 Unit 12 模板
3. 按规范生成各页面
4. 同步导航：`python3 sync_unit_nav.py`
