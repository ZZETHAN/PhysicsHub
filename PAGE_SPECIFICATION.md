# PhysicsHub Unit Page Specification
# 物理Hub 单元页面规范
# 基于 Unit 12 格式制定 | 2026-03-21
# 更新 | 2026-03-22 添加 OpenCode 开发规则

---

## ⚠️ OpenCode 开发规则（必须遵守）

1. **三级标题不带序号**（如 "Essential Difference" 而不是 "1.2 Essential Difference"）
2. **主题色**：根据单元所属模块使用对应配色（见下方主题色表）
3. **所有页面必须包含十大必须功能**（见第十节）
4. **参考单元 ch12-ch14 的实际代码**，而非仅参考本文档

---



---

## 一、页面类型

| 页面类型 | 文件名 | 说明 |
|---------|--------|------|
| 教学首页 | `index.html` | 主内容页面（章节讲解） |
| 例题 | `examples.html` | 典型例题解析 |
| 公式 | `formulas.html` | 公式汇总 |
| 理论 | `theory.html` | 理论概念 |
| 测验 | `quiz.html` | 小测验 |
| 错题 | `mistakes.html` | 常见错误 |
| 习题 | `structured-questions.html` | 真题+答案 |
| 作业 | `homework/chXX/` | 作业页面目录 |

---

## 二、文件结构

### 2.1 标准头部
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unit XX: [标题] | PhysicsHub by Ethan</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../assets/css/main.css">
    <link rel="stylesheet" href="../../auth/auth.css">
```

### 2.2 主题色变量
```css
:root {
    --[theme]-primary: #XXXXXX;      /* 主色 */
    --[theme]-dark: #XXXXXX;         /* 深色 */
    --[theme]-light: #XXXXXX;       /* 浅色 */
}

/* 8大模块主题色 */
--mechanics-primary: #1e40af;     /* 力学 - 深蓝 */
--waves-primary: #7c3aed;         /* 波 - 紫 */
--fields-primary: #059669;         /* 电磁学 - 绿 */
--thermo-primary: #dc2626;         /* 热力学 - 红 */
--electricity-primary: #b45309;   /* 电路 - 橙 */
--modern-primary: #be185d;         /* 现代物理 - 粉紫 */
--matter-primary: #0e7490;        /* 能量与材料 - 青 */
--foundation-primary: #475569;     /* 基础/实验 - 灰 */
```

### 2.3 基础样式
```css
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #fafafa;
    color: #1a1a1a;
    line-height: 1.6;
    margin: 0;
    font-size: 16px;
}
```

---

## 三、Header 结构

### 3.1 顶部导航栏
```html
<header style="background: white; border-bottom: 1px solid #e2e8f0; padding: 12px 0; position: sticky; top: 0; z-index: 100;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 16px; display: flex; justify-content: space-between; align-items: center; gap: 12px;">
        <!-- Logo -->
        <a href="../../index.html" style="text-decoration: none; display: flex; align-items: center; color: #1e40af; font-weight: 500;">
            <span style="font-size: 16px; margin-right: 4px;">←</span>
            <span style="font-size: 15px; font-weight: 600;">PhysicsHub</span>
        </a>
        
        <!-- Units 下拉菜单 -->
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="position: relative;">
                <button onclick="toggleUnitNav()" id="unitNavBtn" style="background: linear-gradient(135deg, #1e40af22 0%, white 100%); border: 1px solid #1e40af; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 500; color: #1e40af; display: flex; align-items: center; gap: 6px;">
                    <span>Units</span>
                    <span style="font-size: 10px;">▼</span>
                </button>
                <!-- 下拉内容 -->
                <div id="unitNavDropdown" style="display: none; position: absolute; top: calc(100% + 8px); right: 50%; transform: translateX(50%); ...">
                    ...
                </div>
            </div>
        </div>
        
        <!-- 登录按钮 -->
        <div id="authBtn"></div>
    </div>
</header>
```

### 3.2 阅读进度条
```html
<div id="reading-progress" style="position: fixed; top: 0; left: 0; width: 0%; height: 3px; background: linear-gradient(90deg, #1e3a5f, #1e40af, #3b82f6); z-index: 1001; transition: width 0.1s;"></div>
```

### 3.3 回到顶部按钮
```html
<a href="#" class="back-to-top" id="backToTop" onclick="event.preventDefault(); document.documentElement.scrollTop = 0; return false;">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="18 15 12 9 6 15"></polyline>
    </svg>
</a>
```

---

## 四、页面主体布局

### 4.1 双栏布局
```css
.content-grid {
    display: grid;
    grid-template-columns: 240px 1fr;  /* 侧边栏240px + 内容区 */
    gap: 32px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}

.sidebar-nav {
    position: sticky;
    top: 80px;
    height: fit-content;
    max-height: calc(100vh - 120px);
    overflow-y: auto;
    background: #fff;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    padding: 8px 0;
}
```

### 4.2 内容卡片
```css
.section-card {
    background: white;
    border-radius: 12px;
    padding: 32px;
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
    scroll-margin-top: 140px;  /* 锚点滚动偏移 */
}
```

### 4.3 响应式
```css
@media (max-width: 968px) {
    .content-grid { grid-template-columns: 1fr; }
    .sidebar-nav { display: none; }
    .mobile-menu-btn { display: flex; align-items: center; justify-content: center; }
}
```

---

## 五、常用组件

### 5.1 概念框 (concept-box)
```css
.concept-box {
    background: #f9fafb;
    border-radius: 8px;
    padding: 18px 20px;
    margin: 20px 0;
}
.concept-box::before {
    content: 'Concept';
    display: block;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6b7280;
    margin-bottom: 8px;
}
```

### 5.2 定义框 (definition-box)
```css
.definition-box {
    background: #f3f4f6;
    border-radius: 8px;
    padding: 20px 24px;
    margin: 20px 0;
}
.definition-title {
    font-size: 13px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 8px;
}
```

### 5.3 公式框 (formula-box)
```css
.formula-box {
    background: var(--theme-light);
    border: 1px solid var(--theme-primary);
    border-radius: 8px;
    padding: 24px 32px;
    margin: 20px 0;
    text-align: center;
}
.formula-box strong {
    color: var(--theme-dark);
    font-size: 16px;
}
.formula-box p {
    color: var(--theme-dark);
    font-size: 14px;
    margin-top: 12px;
}
```

### 5.4 考试提示框 (exam-alert)
```css
.exam-alert {
    background: #fffbeb;
    border: 1px solid #fcd34d;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 20px 0;
}
.exam-alert::before {
    content: 'Exam Tip';
    display: block;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #b45309;
    margin-bottom: 8px;
}
```

### 5.5 清单框 (checklist-box)
```css
.checklist-box {
    background: var(--theme-light);
    border: 1px solid var(--theme-primary);
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}
.checklist-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 8px 0;
    padding: 10px 12px;
    background: white;
    border-radius: 6px;
}
.checklist-item input[type="checkbox"] {
    width: 16px;
    height: 16px;
    accent-color: var(--theme-primary);
}
```

### 5.6 图片占位符
```css
.image-placeholder {
    background: var(--theme-light);
    border: 2px dashed var(--theme-primary);
    border-radius: 8px;
    padding: 40px 24px;
    text-align: center;
    margin: 20px 0;
}
.image-placeholder::before {
    content: 'Figure';
    display: block;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--theme-primary);
    margin-bottom: 8px;
}
```

### 5.7 表格 (case-table)
```css
.case-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 13px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    overflow: hidden;
}
.case-table th, .case-table td {
    padding: 12px 14px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}
.case-table th {
    background: var(--theme-light);
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--theme-dark);
}
```

---

## 六、Structured Questions 页面

### 6.1 题目块 (question-block)
```css
.question-block {
    background: white;
    border-radius: 12px;
    padding: 32px;
    margin: 24px 0;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.question-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 2px solid #f1f5f9;
}
.question-number {
    background: #1d4ed8;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
}
.exam-board {
    background: #f1f5f9;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 600;
    color: #475569;
}
```

### 6.2 小题 (sub-question)
```css
.sub-question {
    margin: 16px 0 16px 24px;
    padding: 16px;
    background: #f8fafc;
    border-radius: 8px;
    border-left: 3px solid #1d4ed8;
}
.sub-question-label {
    font-weight: 600;
    color: #1d4ed8;
    margin-bottom: 8px;
}
```

### 6.3 答案区 (mark-scheme)
```css
.mark-scheme {
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 8px;
    margin-top: 24px;
    overflow: hidden;
}
.mark-scheme-header {
    background: #dcfce7;
    padding: 16px 20px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.mark-scheme-title {
    font-weight: 600;
    color: #166534;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.mark-scheme-content {
    padding: 20px;
}
.mark-subsection {
    margin: 16px 0;
    padding: 12px;
    background: white;
    border-radius: 6px;
    border-left: 3px solid #22c55e;
}
.mark-item {
    display: flex;
    gap: 12px;
    margin: 8px 0;
    font-size: 14px;
}
```

---

## 七、作业页面

### 7.1 作业卡片
```css
.homework-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    margin: 16px 0;
    border: 1px solid #e5e7eb;
    transition: box-shadow 0.2s;
}
.homework-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.homework-tag {
    display: inline-block;
    padding: 4px 12px;
    background: var(--theme-light);
    color: var(--theme-primary);
    border-radius: 16px;
    font-size: 12px;
    font-weight: 600;
}
```

---

## 八、侧边栏导航

### 8.1 导航项目
```css
.nav-section-title {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #9ca3af;
    padding: 16px 16px 6px;
}
.nav-section-header {
    display: block;
    font-size: 13px;
    font-weight: 500;
    color: #374151;
    padding: 8px 12px;
    margin-top: 4px;
    border-radius: 6px;
    cursor: pointer;
}
.nav-section-header:hover,
.nav-section-header.active {
    background: var(--theme-light);
    color: var(--theme-primary);
}
.nav-link {
    display: block;
    padding: 6px 12px;
    color: #6b7280;
    text-decoration: none;
    border-radius: 6px;
    font-size: 12px;
}
.nav-link:hover,
.nav-link.active {
    background: var(--theme-light);
    color: var(--theme-primary);
}
```

---

## 九、JavaScript 功能

### 9.1 Units 下拉菜单
```javascript
function toggleUnitNav() {
    const dropdown = document.getElementById('unitNavDropdown');
    const btn = document.getElementById('unitNavBtn');
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
}
document.addEventListener('click', function(e) {
    if (!e.target.closest('[onclick="toggleUnitNav()"]') && !e.target.closest('#unitNavDropdown')) {
        dropdown.style.display = 'none';
    }
});
```

### 9.2 滚动进度条
```javascript
window.addEventListener('scroll', function() {
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / scrollHeight) * 100;
    document.getElementById('reading-progress').style.width = progress + '%';
});
```

### 9.3 回到顶部
```javascript
window.addEventListener('scroll', function() {
    const backToTop = document.getElementById('backToTop');
    if (window.scrollY > 400) {
        backToTop.classList.add('show');
    } else {
        backToTop.classList.remove('show');
    }
});
```

### 9.4 滚动监听高亮
```javascript
const sections = document.querySelectorAll('h2[id], h3[id]');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + id) {
                    link.classList.add('active');
                }
            });
        }
    });
}, { rootMargin: '-20% 0px -70% 0px' });
sections.forEach(section => observer.observe(section));
```

---

## 十、必须功能清单

新建单元时必须包含：

- [ ] Units 下拉菜单（所有单元导航）
- [ ] 阅读进度条
- [ ] 回到顶部按钮
- [ ] 侧边栏导航 + Scroll Spy
- [ ] 响应式布局（移动端隐藏侧边栏）
- [ ] 登录/认证按钮
- [ ] 主题色变量（CSS Variables）
- [ ] MathJax 公式渲染
- [ ] 图片占位符
- [ ] Checklist 复选框

---

## 十一、文件命名

| 页面 | 文件名 |
|------|--------|
| 教学首页 | `index.html` |
| 例题 | `examples.html` |
| 公式 | `formulas.html` |
| 理论 | `theory.html` |
| 测验 | `quiz.html` |
| 错题 | `mistakes.html` |
| 习题 | `structured-questions.html` |
| 作业目录 | `homework/chXX/` |

---

## 十二、开发流程

1. **内容准备** → 根据 `UnitXX_XXX_Content.md` 内容
2. **格式学习** → 参考本文档和 Unit 12 模板
3. **生成 HTML** → 按本规范生成页面
4. **功能验证** → 检查所有必须功能
5. **主题色** → 使用对应模块配色
6. **同步导航** → 运行 `sync_unit_nav.py`

---

*本文档为 OpenCode 开发新单元时的格式参考*
*更新于 2026-03-21*
