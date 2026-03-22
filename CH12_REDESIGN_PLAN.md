# PhysicsHub Ch 12 教学结构重构方案

## 🎯 教学理念转变
**从**：直接给定义 → **到**：引导式发现学习

## 📚 递进式教学流程

### 1. 引入（从现象到问题）
**开场问题**：
- "你坐过过山车吗？为什么在最高点不会掉下来？"
- "卫星为什么不会掉回地球？"
- "汽车转弯时，你感觉被推向哪边？"

**真实案例展示**（配图）：
- 过山车照片
- 卫星轨道动画
- 赛车转弯

---

### 2. 概念建立（从具体到抽象）

#### 2.1 角速度 - 从日常经验开始
**引导问题**：
"唱片机在旋转，边缘的点移动快，中心的点移动慢，但它们有什么相同？"

**发现过程**：
- 相同时间内扫过相同角度
- 引入角速度概念
- 公式推导：v = rω

**配图**：旋转唱片示意图，标注v和ω

#### 2.2 向心加速度 - 从速度变化推导
**引导问题**：
"速度是矢量，方向变了，算不算加速？"

**矢量分析图**（必须配图）：
```
   v⃗_A (在A点，切线方向)
    ↘
     Δv⃗ → 指向圆心
    ↗
   v⃗_B (在B点，切线方向)
```

**关键发现**：
- Δv⃗ 指向圆心
- 这就是加速度方向！

#### 2.3 向心力 - 不是新力，而是效果
**核心认知转变**：
> "向心力不是一种新力，而是其他力的合力效果"

**案例分析表**（配图+表格）：
| 情境 | 什么力提供向心力 | 图示 |
|------|----------------|------|
| 绳子系小球 | 张力 T | [图] |
| 汽车转弯 | 摩擦力 f | [图] |
| 卫星轨道 | 万有引力 F_g | [图] |
| 过山车顶部 | 重力 mg + 支持力 N | [图] |

---

### 3. 公式推导（分步可视化）

#### 3.1 a = v²/r 推导
**步骤图**（配图）：
1. 画圆，标两点A、B
2. 画速度矢量 v⃗_A, v⃗_B
3. 构造相似三角形
4. 推导 Δv⃗/v = Δs/r
5. 取极限得 a = v²/r

**记忆技巧**：
> "速度平方除以r，双倍的速四倍的力"

#### 3.2 竖直圆环临界条件
**分情况讨论**（配图）：

**最高点**（配图）：
- 受力：mg ↓ + N ↓
- 方程：mg + N = mv²/r
- 临界：N = 0 时，v_min = √(gr)

**最低点**（配图）：
- 受力：N ↑ - mg ↓
- 方程：N - mg = mv²/r
- N最大，感觉最重

---

### 4. P4 背诵清单（Definition Checklist）

#### 必背定义
| 序号 | 概念 | 定义 | 公式 |
|------|------|------|------|
| 1 | Angular velocity (ω) | Rate of change of angular displacement | ω = Δθ/Δt = 2π/T |
| 2 | Centripetal acceleration | Acceleration directed towards centre of circular path | a = v²/r = rω² |
| 3 | Centripetal force | Resultant force towards centre causing circular motion | F = mv²/r |
| 4 | Period (T) | Time for one complete revolution | T = 2π/ω |
| 5 | Frequency (f) | Number of revolutions per unit time | f = 1/T |

#### 必背关系
- [ ] v = rω
- [ ] a ∝ v² (at constant r)
- [ ] F_c ∝ v² (at constant r and m)
- [ ] a = 0 at constant velocity (wrong! must emphasize direction change)

#### 常见简答题模板
**Q: Explain why an object moving in a circle at constant speed is accelerating.**
```
Answer structure (3 marks):
1. Velocity is a vector quantity (has magnitude and direction)
2. In circular motion, direction of velocity is constantly changing
3. Any change in velocity means acceleration exists
4. Acceleration is directed towards the centre of the circle
```

**Q: Derive a = v²/r for uniform circular motion.**
```
Answer structure (4 marks):
1. Consider velocity vectors at two nearby points
2. Change in velocity Δv points towards centre
3. For small Δθ: |Δv| ≈ vΔθ (arc length)
4. a = |Δv|/Δt = v(Δθ/Δt) = vω
5. Substitute v = rω: a = v²/r
```

---

### 5. 案例库（每种类型配例题+图）

#### 类型1：圆锥摆（Conical Pendulum）
**配图**：悬挂小球在水平面内做圆周运动
**关键方程**：
- 竖直：Tcosθ = mg
- 水平：Tsinθ = mv²/r
- tanθ = v²/(rg)

#### 类型2：银行弯道（Banked Curve）
**配图**：倾斜路面的汽车
**设计速度**：tanθ = v²/(rg)

#### 类型3：竖直圆环（Vertical Circle）
**配图**：过山车在轨道顶部
**临界速度**：v_min = √(gr)

---

### 6. 图像学习区

#### 必会图像1：a vs v（恒定r）
- 形状：抛物线
- 特征：a ∝ v²
- 标注：当v → 2v，a → 4a

#### 必会图像2：v vs r（恒定ω）
- 形状：过原点的直线
- 斜率：ω
- 意义：距离中心越远，线速度越大

#### 必会图像3：F_c vs v（恒定m,r）
- 形状：抛物线
- 应用：解释为什么高速转弯更危险

---

## 🔧 导航栏永久修复方案

### 问题分析
导航栏失效的原因：
1. 滚动监听没有正确绑定
2. section ID和导航链接不匹配
3. 动态加载内容后没有重新初始化

### 解决方案
```javascript
// 1. 使用Intersection Observer API（现代浏览器原生支持）
// 2. 添加防抖函数避免频繁触发
// 3. 点击导航时平滑滚动
// 4. 页面加载完成后自动初始化
```

### 代码实现
见下方重构的HTML文件

---

## 📝 执行清单

- [ ] 重写Ch 12 index.html（递进式教学）
- [ ] 添加所有配图占位符
- [ ] 添加P4背诵清单
- [ ] 永久修复导航栏
- [ ] 提取课件图像并嵌入
- [ ] 添加案例库页面
- [ ] 添加图像学习区

---

**现在开始执行！**
