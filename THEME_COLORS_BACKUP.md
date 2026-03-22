# 单元主题色配置备份
# 更新于 2026-03-21

## 8大知识模块配色

| 主题 | 模块 | 主色 | 浅色 | 单元 |
|------|------|------|------|------|
| foundation | 基础/实验 | #475569 灰 | #64748b | ch01, P3, P5 |
| mechanics | 力学 | #1e40af 深蓝 | #3b82f6 | ch02, ch03, ch12, ch13 |
| matter | 能量与材料 | #0e7490 青绿 | #06b6d4 | ch04, ch05, ch06 |
| waves | 波 | #7c3aed 紫 | #a78bfa | ch07, ch08, ch17 |
| fields | 电磁学 | #059669 绿 | #10b981 | ch09, ch10, ch11, ch18, ch19, ch20, ch21 |
| thermo | 热力学 | #dc2626 红 | #ef4444 | ch14, ch15, ch16, ch24 |
| modern | 现代物理 | #be185d 粉紫 | #ec4899 | ch22, ch23, ch25 |

## CSS 变量

```css
:root {
    --theme-primary: #XXXXXX;  /* 主色 */
    --theme-light: #XXXXXX;     /* 浅色 */
}
```

## 使用方法

```html
<script src="../../assets/unit-themes.js"></script>
<script>
    document.body.style.cssText = getUnitCSSVariables('ch12');
</script>
```

## 开发须知

开发新单元前，必须先确认该单元的主题色，配置正确的 CSS 变量。
