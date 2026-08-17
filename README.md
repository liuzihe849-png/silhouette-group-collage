# 剪影群像风格 Skill v1

把单张群像照片转换成竖版双联画式手工纸艺拼贴：上半部分以不透明群像剪影遮挡照片，下半部分将同一轮廓反转为照片镂空窗口，同时保留人物数量、顺序、姿态、服装、环境关系与原始照片纹理。

当前 GitHub 发布版是从最初真实出图任务中冻结的 **v1 风格基线**。公开调用名继续使用 `$silhouette-group-collage`，确保此前在社交媒体发布的名称、链接和使用方式保持有效。

作者与风格 Skill 署名：**理智画**

English name: **Silhouette Group Collage v1**

## 主要能力

- 同一张照片的正负形互补遮罩
- 紧密群像、分散群像、横向队列及陪伴物轮廓
- 锁定原照片人物像素；所有可见人物从原图确定性恢复，禁止 AI 重绘脸、身体、手、服装和持有物
- 保留人物身份、景物、胶片颗粒与现场光线
- 自动选择场景对比色、手工纸张质感和少量星星装饰
- 为群像匹配一条位于双联画中缝的简短手写文字
- 内置结构测试和八项成品质量检查

## 安装

```bash
git clone https://github.com/liuzihe849-png/silhouette-group-collage.git
cp -R silhouette-group-collage/silhouette-group-collage ~/.codex/skills/
```

安装后重新打开 Codex，或开始一个新任务以刷新 skill 列表。

## 使用

上传一张群像照片，然后输入：

```text
使用 $silhouette-group-collage 处理这张群像照片
```

也可以补充主色、装饰形状、画幅或中缝文字：

```text
使用 $silhouette-group-collage 处理这张照片。主色用梅子紫，保留狗作为独立陪伴物轮廓，中间写“cold air, warm company”。
```

未指定文字时，skill 会根据照片中的动作和环境生成一条简短文案。群像人数、顺序、姿态、服装、持有物和环境锚点属于硬性保留项。所有可见人物必须直接来自原始照片的受保护源像素；如果当前工具无法恢复并验证原图人物像素，skill 会停止交付，而不是接受相似但被 AI 重绘的人物。

人物像素锁定不依赖 Human Cutout Engine：生成模型只负责纸面、遮罩和非人物内容；所有可见人物必须使用与整张原照片相同的裁切、位移和等比缩放，从原图重新合成并进行像素比对。

## 本地测试

```bash
python3 silhouette-group-collage/scripts/test_skill.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py silhouette-group-collage
```

第一个命令检查本项目的必要文件、调用名称和关键规则；第二个命令使用 Codex 官方 skill 校验器检查元数据与目录规范。

## 目录

```text
silhouette-group-collage/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── prompt-recipes.md
│   ├── reference-breakdown.md
│   ├── style-system.md
│   └── face-preservation.md
└── scripts/test_skill.py
```

## 使用与署名

项目代码与文档采用 MIT License。转载、修改或发布衍生 skill 时，须保留许可证中的版权与署名信息。公开展示用本 skill 制作的图片时，推荐标注：

```text
风格 Skill：剪影群像风格 Skill｜理智画
```

完整说明见 [使用与署名说明](USAGE_AND_ATTRIBUTION.md)。

v1 的冻结范围与后续版本差异见 [v1 基线说明](V1-BASELINE.md)。
