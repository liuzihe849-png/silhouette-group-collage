# 剪影群像风格 Skill

把单张群像照片转换成竖版双联画式手工纸艺拼贴：上半部分以不透明群像剪影遮挡照片，下半部分将同一轮廓反转为照片镂空窗口，同时用受保护的原图人物层保留脸部、身体、服装、人物关系与原始照片纹理。

作者与风格 Skill 署名：**理智画**

## 主要能力

- 同一张照片的正负形互补遮罩
- 内置 Human Cutout Engine：先生成源尺寸 Alpha、透明人物 PNG 与校验清单，再进入拼贴流程
- 紧密群像、分散群像、横向队列及陪伴物轮廓
- 锁定原照片人物像素，不让生图模型重绘脸、五官、头发、皮肤、身体、手、服装和持有物
- 保留景物、胶片颗粒与现场光线
- 以 Shepherd's Red、Hearth Smoke、Butter Yellow、Heirloom Linen 为四个参考锚点，扩展为 20 个低饱和复古印刷色 Token
- 按雪景、海天、草地花园、暖室内、城市、中夜派对、夕阳道路七类场景，比较 Echo / Counterpoint / Atmosphere 三套候选后再人工定色
- 自动校验纸色与中缝文字对比度，并确定性生成纸面；不再依赖生图模型模拟最终纹理
- 五套安静纸张材料：柔和短纤维、细密哑光颗粒、稀疏浅色纸屑、稀疏深色墨点、中等浅色纸屑；已删除旧版云雾、折痕、布纹和重度脏污资产
- 色彩与材料分开选择，同一纹理可安全染成场景色；纹理不含星星、文字或重复接缝
- 在大色块与照片拼贴交界使用可复现的不规则撕纸边缘；上下互补状态共享同一路径，且绝不侵蚀受保护人物 Alpha
- 五套来自首版优秀作品的字体风格资产：高挑干刷、随性干笔、圆润粗记号笔、动势宽刷、宽幅日记笔触
- 为群像匹配一条位于双联画中缝的简短手写文字，使用内置 OFL 字体独立排版；不再使用 AI 生成的最终文字
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
python3 silhouette-group-collage/scripts/test_color_system.py
python3 silhouette-group-collage/scripts/test_texture_system.py
python3 silhouette-group-collage/scripts/test_torn_paper_seam.py
python3 silhouette-group-collage/scripts/test_finishing.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py silhouette-group-collage
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py human-cutout-engine
```

第一个命令检查必要文件、调用名称和关键规则；第二个命令验证 20 个色彩 Token、七类场景路由与所有推荐文字配色；第三个命令验证五套安静纸张材料、路由规则与实际染色输出；第四个命令验证撕纸边缘可复现、幅度克制且具有细微纤维 Alpha；第五个命令实际生成红色纸纹与中缝文字并验证纹理强度、拼写、尺寸和对比度；后续命令使用 Codex 官方校验器检查目录规范。

需要单独查看某张照片的三套候选色时：

```bash
python3 silhouette-group-collage/scripts/select_scene_palette.py photo.jpg --scene sea-sky --output palette-manifest.json
```

场景参数可选 `snow-winter`、`sea-sky`、`grass-garden`、`warm-indoor`、`city-neutral`、`night-party` 或 `sunset-road`。脚本输出是审美预检，不会代替最终整版人工判断。

## 目录

```text
├── silhouette-group-collage/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/design-system/
│   │   ├── color-system.json
│   │   ├── color-system-preview.png
│   │   ├── paper-texture-profiles.json
│   │   ├── paper-texture-system-preview.png
│   │   ├── torn-seam-profile.json
│   │   ├── torn-paper-seam-mask-preview.png
│   │   ├── typography-families.json
│   │   ├── paper-textures/neutral-uncoated-paper.png
│   │   ├── paper-textures/system/*.png
│   │   └── typography-reference/*.png
│   ├── assets/fonts/（OFL 字体与许可证）
│   ├── references/
│   │   ├── color-system.md
│   │   ├── paper-texture-system.md
│   │   ├── torn-paper-seam.md
│   │   ├── typography-system.md
│   │   ├── deterministic-finishing.md
│   │   ├── human-cutout-handoff.md
│   │   ├── prompt-recipes.md
│   │   └── art-direction-qc.md
│   └── scripts/
│       ├── select_scene_palette.py
│       ├── test_color_system.py
│       ├── render_color_board.py
│       ├── build_paper_texture_library.py
│       ├── test_texture_system.py
│       ├── render_texture_system_preview.py
│       ├── build_torn_paper_seam.py
│       ├── test_torn_paper_seam.py
│       ├── apply_paper_texture.py
│       ├── render_seam_phrase.py
│       ├── test_finishing.py
│       ├── test_skill.py
│       └── validate_cutout_handoff.py
└── human-cutout-engine/
    ├── SKILL.md
    ├── references/backends.md
    └── scripts/
```

## 使用与署名

项目代码与文档采用 MIT License。转载、修改或发布衍生 skill 时，须保留许可证中的版权与署名信息。公开展示用本 skill 制作的图片时，推荐标注：

`silhouette-group-collage/assets/fonts/` 中的字体分别遵循各自目录内的 SIL Open Font License 1.1；根目录 MIT License 不替代字体许可证。

```text
风格 Skill：剪影群像风格 Skill｜理智画
```

完整说明见 [使用与署名说明](USAGE_AND_ATTRIBUTION.md)。
