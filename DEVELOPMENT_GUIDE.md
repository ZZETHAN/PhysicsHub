# PhysicsHub 单元开发规范

## 配色方案（必须使用）

| 单元 | 主题色 Primary | 辅色 Secondary | 浅色 Light | CSS 变量 |
|------|---------------|----------------|------------|----------|
| Ch1 Physical Quantities | #475569 | #64748b | #f1f5f9 | `--theme-primary` |
| Ch2 Kinematics | #1e40af | #3b82f6 | #dbeafe | `--theme-primary` |
| Ch3 Dynamics | #1e40af | #3b82f6 | #dbeafe | `--theme-primary` |
| Ch4 Work & Energy | #059669 | #10b981 | #d1fae5 | `--theme-primary` |
| Ch5 Motion | #059669 | #10b981 | #d1fae5 | `--theme-primary` |
| Ch12 Motion in Circle | #1e3a8a | #3b82f6 | #dbeafe | `--theme-primary` |
| Ch13 Gravitational Field | #7c3aed | #8b5cf6 | #ede9fe | `--theme-primary` |
| Ch14 Temperature | #c2410c | #ea580c | #ffedd5 | `--theme-primary` |
| Ch15 Ideal Gases | #c2410c | #ea580c | #ffedd5 | `--theme-primary` |
| Ch16 Thermodynamics | #c2410c | #ea580c | #fee2e2 | `--theme-primary` |
| Ch17 Oscillations | #0891b2 | #06b6d4 | #cffafe | `--theme-primary` |

## 字体规范

所有文字必须使用 **Inter** 字体，备用系统字体：
```css
font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
```

### 必须指定字体的元素

| 元素 | 内联样式写法 |
|------|-------------|
| 大标题 h1 | `style="color: white; font-family: Inter..."` |
| 副标题 .subtitle | `style="color: white; font-family: Inter..."` |
| 正文 h2 | `style="font-family: Inter..."` |
| 正文 h3 | `style="font-weight: 600; font-family: Inter..."` |
| 正文 h4 | `style="font-family: Inter..."` |
| 侧边栏 .nav-link | `style="font-family: Inter..."` |

## 标题命名规范

### 章节标题（h2）
- 格式：`1. Section Title`（数字 + 点 + 空格 + 标题）
- 不要重复编号：如 `1. 1. Newton's Law` ❌ → `1. Newton's Law` ✅

### 副标题（h3）
- 格式：简洁描述，如 `Vector Analysis`

## 单元模板使用

1. 复制 `units/UNIT_TEMPLATE.html` 为新单元，如 `units/ch18/index.html`
2. 修改 `:root` 中的颜色变量
3. 替换 `[UNIT TITLE]`、`[Subtitle]` 等占位符
4. 添加内容，保持标题样式内联（不要用CSS类）

## 快速复制模板（基于 Ch16）

```bash
cp ~/Desktop/PhysicsHub/units/ch16/index.html ~/Desktop/PhysicsHub/units/chXX/index.html
```

然后修改：
1. `:root` 颜色变量
2. 标题内容
3. 侧边栏链接
4. 内容

## 常见错误

### ❌ 错误做法
```html
<h2>Introduction: What is Thermodynamics?</h2>
```
（没有指定字体）

### ✅ 正确做法
```html
<h2 style="font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif; color: #1e293b;">
    Introduction: What is Thermodynamics?
</h2>
```

## 备份

每次完成开发后执行：
```bash
~/.openclaw/scripts/backup_physicshub.sh
```
