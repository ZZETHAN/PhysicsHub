# PhysicsHub 开发指南 (快速同步)

## 项目路径
`/System/Volumes/Data/Users/ethan/Desktop/PhysicsHub`

## 服务器
- 网站: `ubuntu@123.207.75.145:/var/www/physicshub/`
- API: `ubuntu@123.207.75.145:/opt/physicshub/api/`
- **数据库不能覆盖**: `/opt/physicshub/api/database.db`

## 部署
```bash
cd /System/Volumes/Data/Users/ethan/Desktop/PhysicsHub
bash scripts/deploy_physicshub.sh
```

## 当前状态
- Unit 20 (Magnetic Fields) 已完成并上线
- 所有 Bug 已修复
- 全站英文界面
- Units 18-20 使用蓝色主题 `#1e40af`

## 重要规则
1. **英文界面** - 按钮、提示、导航全部英文
2. **颜色** - 避免红/黄色系，用蓝色 `#1e40af` 或灰色系
3. **MathJax** - 公式用 `$...$` 或 `\(...\)`
4. **Units 下拉** - 每个单元页都要有 ch12-ch20 的完整链接
5. **进度按钮** - 用 `Start | Active | Done`，防止换行

## 常见任务
- 修改样式: 直接编辑对应 HTML 文件的 `<style>` 或 `auth/auth.css`
- 添加单元: 参考现有单元结构，注意 Units 下拉链接
- 修复 Bug: edit 文件 → 部署
- 翻译: grep 找中文 `[\u4e00-\u9fff]`，替换为英文
