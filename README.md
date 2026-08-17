# 剪影群像风格 Skill

把单张群像照片转换成竖版双联画式手工纸艺拼贴：上半部分以不透明群像剪影遮挡照片，下半部分将同一轮廓反转为照片镂空窗口，同时用受保护的原图人物层保留脸部、身体、服装、人物关系与原始照片纹理。

作者与风格 Skill 署名：**理智画**

## 主要能力

- 同一张照片的正负形互补遮罩
- 内置 Human Cutout Engine：先生成源尺寸 Alpha、透明人物 PNG 与校验清单，再进入拼贴流程
- 紧密群像、分散群像、横向队列及陪伴物轮廓
- 锁定原照片人物像素，不让生图模型重绘脸、五官、头发、皮肤、身体、手、服装和持有物
- 保留景物、胶片颗粒与现场光线
- 自动选择场景对比色、手工纸张质感和少量星星装饰
- 五套来自首版优秀作品的字体风格资产：高挑干刷、随性干笔、圆润粗记号笔、动势宽刷、宽幅日记笔触
- 为群像匹配一条位于双联画中缝的简短手写文字，并按场景选择字体家族
- 默认保留原照片像素宽度，按双联画构图推导高度；只有用户明确提出手机壁纸时才使用 9:16
- 内置结构测试、Alpha 交接校验和十二项成品质量检查

## 安装

```bash
git clone https://github.com/liuzihe849-png/silhouette-group-collage.git
cp -R silhouette-group-collage/silhouette-group-collage ~/.codex/skills/
cp -R silhouette-group-collage/human-cutout-engine ~/.codex/skills/
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

未指定文字时，skill 会根据照片中的动作和环境生成一条简短文案。群像人数、顺序、姿态、服装、持有物和环境锚点属于硬性保留项。所有可见人物必须直接来自原始照片的受保护人物层；如果当前工具无法恢复原图人物像素，skill 会停止交付，而不是接受相似但被 AI 重绘的脸。

未指定尺寸时，输出宽度沿用原图像素宽度，不会自动变成 9:16。需要手机壁纸时请明确写出“9:16 手机壁纸”。

首次运行 Human Cutout Engine 会按所选后端下载模型权重；权重不会包含在本仓库中。建议先阅读 `human-cutout-engine/references/backends.md`，在独立 Python 环境安装所需依赖并完成 Alpha 边缘人工复核。

## 本地测试

```bash
python3 silhouette-group-collage/scripts/test_skill.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py silhouette-group-collage
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py human-cutout-engine
```

第一个命令检查本项目的必要文件、调用名称和关键规则；第二个命令使用 Codex 官方 skill 校验器检查元数据与目录规范。

## 目录

```text
├── silhouette-group-collage/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/design-system/
│   │   ├── typography-families.json
│   │   └── typography-reference/*.png
│   ├── references/
│   │   ├── typography-system.md
│   │   ├── human-cutout-handoff.md
│   │   ├── prompt-recipes.md
│   │   └── art-direction-qc.md
│   └── scripts/
│       ├── test_skill.py
│       └── validate_cutout_handoff.py
└── human-cutout-engine/
    ├── SKILL.md
    ├── references/backends.md
    └── scripts/
```

## 使用与署名

项目代码与文档采用 MIT License。转载、修改或发布衍生 skill 时，须保留许可证中的版权与署名信息。公开展示用本 skill 制作的图片时，推荐标注：

```text
风格 Skill：剪影群像风格 Skill｜理智画
```

完整说明见 [使用与署名说明](USAGE_AND_ATTRIBUTION.md)。
