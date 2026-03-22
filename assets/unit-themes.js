/**
 * PhysicsHub 单元主题色配置
 * 
 * 知识模块 → 颜色变量映射（在 index.html 中定义）：
 * - foundation:   #475569 (灰蓝) - 基础/实验
 * - mechanics:    #1e40af (深蓝) - 力学
 * - matter:      #0e7490 (青绿) - 能量与材料
 * - waves:       #7c3aed (紫色) - 波
 * - fields:      #059669 (绿色) - 电磁学
 * - thermo:      #dc2626 (红色) - 热力学
 * - modern:      #be185d (粉紫) - 现代物理
 */

const UNIT_THEMES = {
    // ========== Foundation (基础/实验) ==========
    ch01: { theme: 'foundation', title: 'Physical Quantities & Units' },
    p03: { theme: 'foundation', title: 'Paper 3 - Practical' },
    p05: { theme: 'foundation', title: 'Paper 5 - Planning' },
    
    // ========== Mechanics (力学) ==========
    ch02: { theme: 'mechanics', title: 'Kinematics' },
    ch03: { theme: 'mechanics', title: 'Dynamics' },
    ch12: { theme: 'mechanics', title: 'Motion in a Circle' },
    ch13: { theme: 'mechanics', title: 'Gravitational Field' },
    
    // ========== Matter (能量与材料) ==========
    ch04: { theme: 'matter', title: 'Forces & Vectors' },
    ch05: { theme: 'matter', title: 'Work, Energy & Power' },
    ch06: { theme: 'matter', title: 'Solids, Liquids & Gases' },
    
    // ========== Waves (波) ==========
    ch07: { theme: 'waves', title: 'Deformation of Solids' },
    ch08: { theme: 'waves', title: 'Waves' },
    ch17: { theme: 'waves', title: 'Oscillations' },
    
    // ========== Fields (电磁学) ==========
    ch09: { theme: 'fields', title: 'Superposition' },
    ch10: { theme: 'fields', title: 'Electric Fields' },
    ch11: { theme: 'fields', title: 'Electric Current' },
    ch18: { theme: 'fields', title: 'Electric Fields' },
    ch19: { theme: 'fields', title: 'Capacitance' },
    ch20: { theme: 'fields', title: 'Magnetic Fields' },
    ch21: { theme: 'fields', title: 'Electromagnetic Induction' },
    
    // ========== Thermodynamics (热力学) ==========
    ch14: { theme: 'thermo', title: 'Gravitational Field' },
    ch15: { theme: 'thermo', title: 'Temperature' },
    ch16: { theme: 'thermo', title: 'Ideal Gases' },
    ch24: { theme: 'thermo', title: 'Thermodynamics' },
    
    // ========== Modern Physics (现代物理) ==========
    ch22: { theme: 'modern', title: 'D.C. Circuits' },
    ch23: { theme: 'modern', title: 'Alternating Currents' },
    ch25: { theme: 'modern', title: 'Quantum Physics' },
};

// 主题色变量（与 index.html 保持一致）
const THEME_COLORS = {
    foundation:  { primary: '#475569', light: '#64748b' },
    mechanics:   { primary: '#1e40af', light: '#3b82f6' },
    matter:      { primary: '#0e7490', light: '#06b6d4' },
    waves:       { primary: '#7c3aed', light: '#a78bfa' },
    fields:      { primary: '#059669', light: '#10b981' },
    thermo:      { primary: '#dc2626', light: '#ef4444' },
    modern:      { primary: '#be185d', light: '#ec4899' },
};

// 获取指定单元的主题色
function getUnitTheme(unitId) {
    return UNIT_THEMES[unitId] || null;
}

// 获取指定主题的颜色
function getThemeColor(theme) {
    return THEME_COLORS[theme] || THEME_COLORS.foundation;
}

// 导出给各单元页面使用的 CSS 变量字符串
function getUnitCSSVariables(unitId) {
    const unit = getUnitTheme(unitId);
    if (!unit) return '';
    const colors = getThemeColor(unit.theme);
    return `--theme-primary: ${colors.primary}; --theme-light: ${colors.light};`;
}
